#
# Copyright (C) 2026 Genius Dynamics
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Shared helpers for the ns8-openbao module.

The module home `.config/pypkg` directory is in PYTHONPATH, so actions,
helper commands and systemd ExecStart* scripts can `import openbao`.

Every function expects the current working directory to be the module
state directory (AGENT_STATE_DIR), which is the default for actions and
for commands started with `runagent`.
"""

import hashlib
import json
import os
import secrets
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

# Files in the state directory
ENVIRONMENT_FILE = "environment"
CONFIG_DIR = "openbao-config"  # mounted read-only on /openbao/config
CONFIG_FILE = CONFIG_DIR + "/openbao.hcl"
APPLIED_FILE = "openbao-applied.json"  # configuration loaded by the server
INIT_FILE = CONFIG_DIR + "/ns8-initialize.json"  # self-initialization requests
CONTAINER_ENV_FILE = "openbao-container.env"
SEAL_KEY_FILE = "openbao-seal.key"

DATA_VOLUME = "openbao-data"

LOG_LEVELS = ["trace", "debug", "info", "warn", "error"]
UNSEAL_MODES = ["manual", "auto"]
DEFAULTS = {
    "OPENBAO_LOG_LEVEL": "info",
    "OPENBAO_AUDIT_LOG": "False",
    "OPENBAO_UNSEAL_MODE": "manual",
    "TRAEFIK_HTTP2HTTPS": "True",
    "OPENBAO_USER_DOMAIN": "",
    "OPENBAO_LDAP_ADMIN_GROUP": "",
    "OPENBAO_AUTO_INITIALIZE": "False",
    "OPENBAO_NOTIFY_RECIPIENTS": "",
}

# Policy granted to the directory group of OpenBao administrators
ADMIN_POLICY_NAME = "ns8-admin"
ADMIN_POLICY = """# Full administrative access, granted to the NethServer 8 directory
# group selected in the application settings.
path "*" {
  capabilities = ["create", "read", "update", "patch", "delete", "list", "scan", "sudo"]
}
"""
LDAP_BIND_PASSWORD_VAR = "NS8_LDAP_BIND_PASSWORD"
# Podman translates this address to the node loopback interface, where
# the NS8 ldapproxy listens (slirp4netns allow_host_loopback=true)
HOST_LOOPBACK_ADDR = "10.0.2.2"

# The Raft node ID and cluster address must never change: they are stored
# inside the Raft data. Do not derive them from MODULE_ID, otherwise a
# restore or a clone to a different instance name would leave Raft without
# a leader.
RAFT_NODE_ID = "ns8-openbao"
CLUSTER_ADDR = "https://127.0.0.1:8201"

# OpenBao listens on plain HTTP inside the container; the port is published
# only on the host loopback interface and Traefik terminates TLS. Trust the
# X-Forwarded-For header coming from loopback/private sources, so audit logs
# record the real client address. Sources outside these ranges cannot reach
# the listener at all.
XFF_AUTHORIZED_ADDRS = [
    "127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",
    "169.254.0.0/16", "::1/128", "fc00::/7",
]


def log(message, level=""):
    print(level + message, file=sys.stderr)


def read_environment():
    """Return the module environment, merged with defaults.

    Read the file instead of os.environ: values set by agent.set_env() in a
    previous step of the same action are already there.
    """
    env = dict(DEFAULTS)
    try:
        with open(ENVIRONMENT_FILE, encoding="utf-8") as fenv:
            for line in fenv:
                line = line.rstrip("\n")
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                env[key] = value
    except FileNotFoundError:
        pass
    for key, value in DEFAULTS.items():
        if not env.get(key):
            env[key] = value
    return env


def is_true(value):
    return str(value).lower() in ("1", "true", "yes", "on")


def _write_file(path, payload, mode):
    """Atomically replace path with payload, with the given permissions."""
    directory, filename = os.path.split(path)
    tmp_path = os.path.join(directory, f".{filename}.tmp-{os.getpid()}")
    fd = os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as ofile:
            ofile.write(payload)
            ofile.flush()
            os.fsync(ofile.fileno())
        os.chmod(tmp_path, mode)
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def ensure_seal_key():
    """Return (key_id, key_hex) of the static auto-unseal key.

    The key is created once and NEVER regenerated: losing or replacing it
    makes the OpenBao data unrecoverable. It is never sent through Redis
    or task payloads.
    """
    if not os.path.exists(SEAL_KEY_FILE):
        key_hex = secrets.token_bytes(32).hex()
        # O_EXCL: never overwrite an existing key, even under races
        fd = os.open(SEAL_KEY_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as kfile:
            kfile.write(key_hex + "\n")
            kfile.flush()
            os.fsync(kfile.fileno())
        log(f"Generated a new OpenBao static seal key in {SEAL_KEY_FILE}")
    with open(SEAL_KEY_FILE, encoding="utf-8") as kfile:
        key_hex = kfile.read().strip()
    if len(key_hex) != 64:
        raise ValueError(f"{SEAL_KEY_FILE} does not contain a 32-byte hex key")
    bytes.fromhex(key_hex)  # raises ValueError if not hex
    key_id = "ns8-" + hashlib.sha256(key_hex.encode()).hexdigest()[:16]
    return key_id, key_hex


def _hcl_string(value):
    return json.dumps(str(value))


def discover_ldap(domain):
    """Return the LDAP connection parameters of an NS8 user domain, or None.

    The endpoint is the local ldapproxy port: it relays to the domain
    servers with TLS and fails over between them.
    """
    if not domain:
        return None
    try:
        from agent.ldapproxy import Ldapproxy
        params = Ldapproxy().get_domain(domain)
    except Exception as ex:
        log(f"Cannot read the settings of user domain {domain}: {ex}", "<4>")
        return None
    if not params or params.get("schema") not in ("ad", "rfc2307"):
        log(f"User domain {domain} is not available or has an unknown schema", "<4>")
        return None
    return params


def list_user_domains():
    """Return [{name, schema, location}] of the cluster user domains."""
    try:
        from agent.ldapproxy import Ldapproxy
        proxy = Ldapproxy()
        names = proxy.get_domains_list()
        domains = []
        for name in sorted(names):
            params = proxy.domains.get(name, {}) if proxy.domains else {}
            domains.append({
                "name": name,
                "schema": params.get("schema", ""),
                "location": params.get("location", ""),
            })
        return domains
    except Exception as ex:
        log(f"Cannot list the user domains: {ex}", "<4>")
        return []


def ldap_auth_config(params, bindpass, container=True):
    """Return the data of the auth/ldap/config request.

    The search settings mirror the NS8 core LDAP client (agent.ldapclient):
    Active Directory uses sAMAccountName and group "member" attributes,
    RFC2307 (OpenLDAP) uses uid and posixGroup "memberUid".
    """
    host = HOST_LOOPBACK_ADDR if container else params["host"]
    config = {
        "url": f"ldap://{host}:{params['port']}",
        "binddn": params["bind_dn"],
        "bindpass": bindpass,
        "userdn": params["base_dn"],
        "groupdn": params["base_dn"],
        "starttls": False,
        "deny_null_bind": True,
        "case_sensitive_names": False,
        "username_as_alias": True,
        "request_timeout": 30,
    }
    if params["schema"] == "ad":
        config.update({
            "userattr": "sAMAccountName",
            "userfilter": "(&(objectClass=user)(objectCategory=person)({{.UserAttr}}={{.Username}}))",
            "groupfilter": "(&(objectClass=group)(member={{.UserDN}}))",
            "groupattr": "sAMAccountName",
        })
    else:
        config.update({
            "userattr": "uid",
            "userfilter": "(&(objectClass=posixAccount)({{.UserAttr}}={{.Username}}))",
            "groupfilter": "(&(objectClass=posixGroup)(memberUid={{.Username}}))",
            "groupattr": "cn",
        })
    return config


def directory_login_requests(params, admin_group, bindpass, container=True):
    """Return the OpenBao API requests that set up directory login.

    Every request is idempotent, and none contacts the LDAP server: they
    are safe for self-initialization, where a failure would leave OpenBao
    initialized without any way to log in.
    """
    return [
        {
            "name": "ns8-admin-policy",
            "operation": "update",
            "path": f"sys/policies/acl/{ADMIN_POLICY_NAME}",
            "data": {"policy": ADMIN_POLICY},
        },
        {
            "name": "ns8-ldap-mount",
            "operation": "update",
            "path": "sys/auth/ldap",
            "data": {
                "type": "ldap",
                "description": "NethServer 8 user domain login",
            },
        },
        {
            "name": "ns8-ldap-config",
            "operation": "update",
            "path": "auth/ldap/config",
            "data": ldap_auth_config(params, bindpass, container=container),
        },
        {
            "name": "ns8-ldap-admin-group",
            "operation": "update",
            "path": "auth/ldap/groups/" + admin_group,
            "data": {"policies": [ADMIN_POLICY_NAME]},
        },
    ]


def render_initialize(params, admin_group):
    """Return the JSON text of the self-initialization configuration."""
    bindpass = {
        "eval_source": "env",
        "eval_type": "string",
        "env_var": LDAP_BIND_PASSWORD_VAR,
        "require_present": True,
    }
    requests = []
    for req in directory_login_requests(params, admin_group, bindpass):
        body = {"operation": req["operation"], "path": req["path"], "data": req["data"]}
        requests.append({req["name"]: body})
    # A ready-to-use key/value store; not essential, so it may fail
    requests.append({"ns8-kv-mount": {
        "operation": "update",
        "path": "sys/mounts/secret",
        "data": {"type": "kv", "description": "Key/value secrets", "options": {"version": "2"}},
        "allow_failure": True,
    }})
    return json.dumps({"initialize": [{"ns8-directory-login": {"request": requests}}]}, indent=2) + "\n"


def auto_initialize_wanted(env):
    return (
        env["OPENBAO_UNSEAL_MODE"] == "auto"
        and is_true(env["OPENBAO_AUTO_INITIALIZE"])
        and bool(env["OPENBAO_USER_DOMAIN"])
        and bool(env["OPENBAO_LDAP_ADMIN_GROUP"])
    )


def render_config(env):
    """Return a dict with the generated files and their change signatures.

    - restart_signature covers the settings that OpenBao cannot reload with
      SIGHUP. log_level and declarative audit devices are reloadable.
    - init_hash covers the self-initialization requests: they matter only
      while OpenBao is not initialized.
    """
    host = env.get("TRAEFIK_HOST", "")
    api_addr = f"https://{host}" if host else "http://127.0.0.1:8200"
    unseal_mode = env["OPENBAO_UNSEAL_MODE"]
    log_level = env["OPENBAO_LOG_LEVEL"]
    if log_level not in LOG_LEVELS:
        log_level = DEFAULTS["OPENBAO_LOG_LEVEL"]

    static_part = []
    static_part.append(f"api_addr = {_hcl_string(api_addr)}")
    static_part.append(f"cluster_addr = {_hcl_string(CLUSTER_ADDR)}")
    static_part.append("ui = true")
    # Raft integrated storage: mlock is not needed and it is not available
    # to rootless containers.
    static_part.append("disable_mlock = true")
    static_part.append("")
    static_part.append('storage "raft" {')
    static_part.append('  path    = "/openbao/file"')
    static_part.append(f"  node_id = {_hcl_string(RAFT_NODE_ID)}")
    static_part.append("}")
    static_part.append("")
    static_part.append('listener "tcp" {')
    static_part.append('  address         = "0.0.0.0:8200"')
    static_part.append('  cluster_address = "127.0.0.1:8201"')
    static_part.append("  tls_disable     = true")
    static_part.append(f"  x_forwarded_for_authorized_addrs      = {_hcl_string(','.join(XFF_AUTHORIZED_ADDRS))}")
    static_part.append('  x_forwarded_for_reject_not_authorized = "false"')
    static_part.append('  x_forwarded_for_reject_not_present    = "false"')
    static_part.append("}")

    container_env = []
    if unseal_mode == "auto":
        key_id, key_hex = ensure_seal_key()
        static_part.append("")
        static_part.append('seal "static" {')
        static_part.append(f"  current_key_id = {_hcl_string(key_id)}")
        static_part.append('  current_key    = "env://BAO_STATIC_SEAL_CURRENT_KEY"')
        static_part.append("}")
        container_env.append(f"BAO_STATIC_SEAL_CURRENT_KEY_ID={key_id}")
        container_env.append(f"BAO_STATIC_SEAL_CURRENT_KEY={key_hex}")

    static_text = "\n".join(static_part) + "\n"
    signature = hashlib.sha256(static_text.encode()).hexdigest()

    reloadable = []
    reloadable.append(f"log_level = {_hcl_string(log_level)}")
    if is_true(env["OPENBAO_AUDIT_LOG"]):
        reloadable.append("")
        reloadable.append('audit "file" "ns8-journal" {')
        reloadable.append('  description = "Audit log sent to the systemd journal by NethServer 8"')
        reloadable.append("  options {")
        reloadable.append('    file_path = "stdout"')
        reloadable.append("  }")
        reloadable.append("}")

    # Self-initialization is generated only when every input is available:
    # a failure after OpenBao initializes itself would lock everybody out.
    init_text = ""
    init_env = []
    if auto_initialize_wanted(env):
        params = discover_ldap(env["OPENBAO_USER_DOMAIN"])
        if params:
            init_text = render_initialize(params, env["OPENBAO_LDAP_ADMIN_GROUP"])
            init_env.append(f"{LDAP_BIND_PASSWORD_VAR}={params['bind_password']}")
        else:
            log("Self-initialization skipped: the user domain is not available", "<4>")

    config_text = (
        "# Generated by ns8-openbao: manual changes are overwritten.\n"
        f"# restart-signature: {signature}\n\n"
        + static_text + "\n"
        + "\n".join(reloadable) + "\n"
    )
    container_env_text = "".join(line + "\n" for line in container_env + init_env)
    return {
        "config_text": config_text,
        "container_env_text": container_env_text,
        "init_text": init_text,
        "restart_signature": hashlib.sha256(
            (static_text + "".join(line + "\n" for line in container_env)).encode()).hexdigest(),
        "config_hash": hashlib.sha256(config_text.encode()).hexdigest(),
        "init_hash": hashlib.sha256(
            (init_text + "".join(init_env)).encode()).hexdigest(),
    }


def write_config():
    """Write the OpenBao configuration files from the module environment.

    Return the applied-state record of the written configuration, to be
    compared with read_applied() and saved with mark_applied().
    """
    env = read_environment()
    rendered = render_config(env)

    os.makedirs(CONFIG_DIR, mode=0o755, exist_ok=True)
    os.chmod(CONFIG_DIR, 0o755)
    # The container env file holds the seal key and, until OpenBao is
    # initialized, the LDAP bind password: owner-only permissions.
    _write_file(CONTAINER_ENV_FILE, rendered["container_env_text"], 0o600)
    # The OpenBao process runs as an unprivileged user inside the container
    # and must be able to read the configuration files. They hold no
    # secrets. The whole directory is mounted, so an atomic replace is
    # visible to a running container on reload.
    _write_file(CONFIG_FILE, rendered["config_text"], 0o644)
    if rendered["init_text"]:
        _write_file(INIT_FILE, rendered["init_text"], 0o644)
    elif os.path.exists(INIT_FILE):
        os.unlink(INIT_FILE)

    return {key: rendered[key] for key in ("restart_signature", "config_hash", "init_hash")}


def read_applied():
    """Return the record of the configuration loaded by the server, or None."""
    try:
        with open(APPLIED_FILE, encoding="utf-8") as afile:
            return json.load(afile)
    except (FileNotFoundError, ValueError):
        return None


def mark_applied(record):
    _write_file(APPLIED_FILE, json.dumps(record) + "\n", 0o644)


def required_change(record, initialized=True):
    """Return "none", "reload" or "restart" to make a running server load record.

    initialized tells whether the running server is initialized: changed
    self-initialization requests need a restart only if it is not.
    """
    applied = read_applied()
    if not applied or applied.get("restart_signature") != record["restart_signature"]:
        return "restart"
    if not initialized and applied.get("init_hash") != record["init_hash"]:
        return "restart"
    if applied.get("config_hash") != record["config_hash"]:
        return "reload"
    return "none"


def notify_recipients(env):
    return [r for r in env.get("OPENBAO_NOTIFY_RECIPIENTS", "").split(",") if r]


def send_notification(env, subject, body, recipients=None):
    """Send an email with the core ns8-sendmail command.

    ns8-sendmail reads the cluster SMTP smarthost settings when it runs, so
    smarthost changes apply without any module action. Return (ok, error).
    """
    if recipients is None:
        recipients = notify_recipients(env)
    if not recipients:
        return False, "no recipients"
    module_id = os.environ.get("MODULE_ID", "openbao")
    host = env.get("TRAEFIK_HOST", "")
    footer = f"\n\n--\nOpenBao instance {module_id}"
    if host:
        footer += f" - https://{host}/ui/"
    footer += "\nSent by NethServer 8. Recipients are set in the application Settings page.\n"
    try:
        proc = subprocess.run(
            ["ns8-sendmail", "-s", f"[OpenBao {module_id}] {subject}", *recipients],
            input=body + footer, text=True, capture_output=True, timeout=60, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as ex:
        return False, str(ex)
    if proc.returncode != 0:
        return False, (proc.stderr or proc.stdout).strip()
    return True, ""


def server_condition(env):
    """Return the OpenBao condition used by notifications and metrics.

    One of "unconfigured", "down", "uninitialized", "sealed", "ok".
    """
    if not env.get("TRAEFIK_HOST"):
        return "unconfigured", None
    status = get_seal_status(timeout=5) if service_is_active() else None
    if status is None:
        return "down", None
    if not status.get("initialized"):
        return "uninitialized", status
    if status.get("sealed"):
        return "sealed", status
    return "ok", status


def _opener():
    # Never send loopback API requests through an HTTP proxy configured
    # in the node environment.
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


def api_request(path, method="GET", data=None, token=None, timeout=10):
    """Call the OpenBao API on the local listener. Return the decoded JSON.

    Raises urllib.error.HTTPError on API errors.
    """
    url = f"http://127.0.0.1:{os.environ['TCP_PORT']}/v1/" + \
        urllib.parse.quote(path.lstrip("/"), safe="/")
    headers = {"Accept": "application/json"}
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    if token:
        headers["X-Vault-Token"] = token
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with _opener().open(req, timeout=timeout) as resp:
        payload = resp.read()
    return json.loads(payload) if payload else {}


def api_get(path, timeout=5):
    """GET an unauthenticated OpenBao API path. Return the decoded JSON."""
    return api_request(path, timeout=timeout)


def get_seal_status(timeout=5):
    """Return the /sys/seal-status payload, or None if OpenBao is unreachable."""
    try:
        return api_get("sys/seal-status", timeout=timeout)
    except (urllib.error.URLError, OSError, ValueError):
        return None


def service_is_active():
    proc = subprocess.run(
        ["systemctl", "--user", "-q", "is-active", "openbao.service"],
        check=False,
    )
    return proc.returncode == 0


def storage_has_data():
    """Return True if the data volume contains OpenBao storage files."""
    proc = subprocess.run(
        ["podman", "volume", "inspect", "--format", "{{.Mountpoint}}", DATA_VOLUME],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        return False
    mountpoint = proc.stdout.strip()
    # Files are owned by the container user: test them in the user namespace
    proc = subprocess.run(
        ["podman", "unshare", "test", "-e", os.path.join(mountpoint, "vault.db")],
        check=False,
    )
    return proc.returncode == 0


def storage_state():
    """Return "uninitialized", "initialized" or "unknown"."""
    status = get_seal_status()
    if status is not None:
        return "initialized" if status.get("initialized") else "uninitialized"
    if not storage_has_data():
        return "uninitialized"
    return "unknown"
