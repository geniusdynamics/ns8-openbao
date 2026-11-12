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
RUNTIME_ENV_FILE = "openbao-runtime.env"  # podman arguments for openbao.service
SEAL_KEY_FILE = "openbao-seal.key"
PLUGIN_DIR = "openbao-plugins"  # mounted read-only on /openbao/plugins
PLUGIN_STATE_FILE = "openbao-plugins.json"
BREAKGLASS_TOKEN_FILE = "openbao-breakglass.token"
MODULE_TOKEN_FILE = "openbao-module.token"
TRANSIT_TOKEN_FILE = "openbao-transit.token"
SNAPSHOT_FILE = "openbao.snap"

DATA_VOLUME = "openbao-data"

LOG_LEVELS = ["trace", "debug", "info", "warn", "error"]
UNSEAL_MODES = ["manual", "auto", "transit"]
DEFAULTS = {
    "OPENBAO_LOG_LEVEL": "info",
    "OPENBAO_AUDIT_LOG": "False",
    "OPENBAO_UNSEAL_MODE": "manual",
    "TRAEFIK_HTTP2HTTPS": "True",
    "OPENBAO_USER_DOMAIN": "",
    "OPENBAO_LDAP_ADMIN_GROUP": "",
    "OPENBAO_AUTO_INITIALIZE": "False",
    "OPENBAO_NOTIFY_RECIPIENTS": "",
    "OPENBAO_IP_ALLOWLIST": "",
    "OPENBAO_LDAP_GROUP_POLICIES": "",
    "OPENBAO_STARTER_KITS": "kv",
    "OPENBAO_VPN_API": "False",
    "OPENBAO_TRANSIT_ADDRESS": "",
    "OPENBAO_TRANSIT_MOUNT": "transit",
    "OPENBAO_TRANSIT_KEY": "",
    "OPENBAO_TRANSIT_TLS_SKIP_VERIFY": "False",
    "OPENBAO_PUBLIC_ACCESS": "True",
    "OPENBAO_SNAPSHOT_KEEP": "0",
    "OPENBAO_SEAL_MIGRATION_FROM": "",
}

SNAPSHOT_DIR = "snapshots"  # scheduled local snapshots, not in backups

STARTER_KITS = ["kv", "pki", "approle"]
APPLIED_GROUPS_FILE = "openbao-ldap-groups-applied.json"

# Policy granted to the directory group of OpenBao administrators
ADMIN_POLICY_NAME = "ns8-admin"
ADMIN_POLICY = """# Full administrative access, granted to the NethServer 8 directory
# group selected in the application settings.
path "*" {
  capabilities = ["create", "read", "update", "patch", "delete", "list", "scan", "sudo"]
}
"""
# Policies created by the module, offered in the group mapping table
BUILTIN_POLICIES = {
    "ns8-admin": ADMIN_POLICY,
    "ns8-secrets-rw": """# Read and write the secret/ key/value (v2) store
path "secret/data/*" {
  capabilities = ["create", "read", "update", "patch", "delete", "list"]
}
path "secret/metadata/*" {
  capabilities = ["read", "list", "delete"]
}
""",
    "ns8-secrets-ro": """# Read the secret/ key/value (v2) store
path "secret/data/*" {
  capabilities = ["read", "list"]
}
path "secret/metadata/*" {
  capabilities = ["read", "list"]
}
""",
    "ns8-pki-issuer": """# Issue certificates with the role of the internal PKI starter kit
path "pki/issue/ns8-server" {
  capabilities = ["create", "update"]
}
path "pki/cert/ca" {
  capabilities = ["read"]
}
""",
}

# Narrow policy of the module token: consistent backups (Raft snapshots),
# root token detection and Raft status. It cannot read secrets, change the
# configuration or revoke tokens.
MODULE_POLICY_NAME = "ns8-module"
MODULE_POLICY = """# Token held by the NethServer 8 module, on the node only
path "sys/storage/raft/snapshot" {
  capabilities = ["read"]
}
path "sys/storage/raft/configuration" {
  capabilities = ["read"]
}
path "auth/token/accessors" {
  capabilities = ["list", "sudo"]
}
path "auth/token/lookup-accessor" {
  capabilities = ["update"]
}
"""
MODULE_TOKEN_VAR = "NS8_MODULE_TOKEN"
MODULE_TOKEN_PERIOD = "768h"

LDAP_BIND_PASSWORD_VAR = "NS8_LDAP_BIND_PASSWORD"
BREAKGLASS_TOKEN_VAR = "NS8_BREAKGLASS_TOKEN"
# The break-glass token expires by itself: the token store maximum TTL
BREAKGLASS_TOKEN_TTL = "768h"

# External plugins. Since OpenBao 2.7 the LDAP auth method is no longer
# built in: it is distributed as an OCI image by the openbao-plugins
# project. The image is listed in the org.nethserver.images label, so the
# node pulls it with the module (no download at OpenBao startup) and
# Renovate tracks its version. The binary is copied from the image into
# PLUGIN_DIR by install_plugins() and declared in the server configuration.
PLUGINS = [
    {
        "name": "ldap",
        "type": "auth",
        "image_var": "OPENBAO_PLUGIN_AUTH_LDAP_IMAGE",
        "command": "openbao-plugin-auth-ldap",
    },
]
PLUGIN_CONTAINER_DIR = "/openbao/plugins"
# Podman translates this address to the node loopback interface, where
# the NS8 ldapproxy listens (slirp4netns allow_host_loopback=true)
HOST_LOOPBACK_ADDR = "10.0.2.2"

# Prometheus metrics: a dedicated listener that serves only /v1/sys/metrics,
# published on the node cluster VPN address, where the NS8 metrics module
# (possibly running on another node) scrapes it. The API listener published
# through Traefik never serves metrics.
METRICS_CONTAINER_PORT = 8202
METRICS_PATH = "/v1/sys/metrics"

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


def _image_version(image):
    """Return the tag of an image URL, e.g. "v0.2.0", or ""."""
    name = image.split("@", 1)[0]
    last = name.rsplit("/", 1)[-1]
    return last.rsplit(":", 1)[1] if ":" in last else ""


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as bfile:
        for chunk in iter(lambda: bfile.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_plugin_state():
    try:
        with open(PLUGIN_STATE_FILE, encoding="utf-8") as sfile:
            return json.load(sfile)
    except (FileNotFoundError, ValueError):
        return {}


def install_plugins():
    """Copy the external plugin binaries from their images into PLUGIN_DIR.

    It runs before OpenBao starts. A binary is extracted again only when
    its image changes. Return the dict of installed plugins.
    """
    env = read_environment()
    os.makedirs(PLUGIN_DIR, mode=0o755, exist_ok=True)
    os.chmod(PLUGIN_DIR, 0o755)
    state = _read_plugin_state()
    installed = {}
    for plugin in PLUGINS:
        image = env.get(plugin["image_var"]) or os.environ.get(plugin["image_var"], "")
        version = _image_version(image)
        if not image or not version:
            log(f"Plugin {plugin['name']}: image not available", "<4>")
            continue
        proc = subprocess.run(["podman", "image", "inspect", "--format", "{{.Id}}", image],
                              capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            log(f"Plugin {plugin['name']}: image {image} is not present on this node", "<4>")
            continue
        image_id = proc.stdout.strip()
        target = os.path.join(PLUGIN_DIR, plugin["command"])
        record = state.get(plugin["name"], {})
        if record.get("image_id") == image_id and os.path.exists(target) \
                and _sha256_file(target) == record.get("sha256"):
            installed[plugin["name"]] = record
            continue
        container = f"openbao-plugin-{plugin['name']}-extract"
        tmp_target = os.path.join(PLUGIN_DIR, f".{plugin['command']}.tmp")
        try:
            subprocess.run(["podman", "create", "--replace", "--name", container, image],
                           check=True, capture_output=True, text=True)
            subprocess.run(["podman", "cp", f"{container}:/{plugin['command']}", tmp_target],
                           check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as ex:
            log(f"Plugin {plugin['name']}: cannot extract the binary: {ex.stderr.strip()}", "<3>")
            continue
        finally:
            subprocess.run(["podman", "rm", "--force", "--ignore", container],
                           check=False, capture_output=True)
        # The OpenBao user inside the container must be able to execute it
        os.chmod(tmp_target, 0o755)
        os.replace(tmp_target, target)
        record = {
            "type": plugin["type"],
            "command": plugin["command"],
            "version": version,
            "sha256": _sha256_file(target),
            "image_id": image_id,
        }
        installed[plugin["name"]] = record
        log(f"Plugin {plugin['name']} {version} installed")
    _write_file(PLUGIN_STATE_FILE, json.dumps(installed, indent=2) + "\n", 0o644)
    return installed


def declared_plugins():
    """Return {name: record} of the installed plugins with a valid binary."""
    plugins = {}
    for name, record in _read_plugin_state().items():
        path = os.path.join(PLUGIN_DIR, record.get("command", ""))
        try:
            if _sha256_file(path) == record.get("sha256"):
                plugins[name] = record
        except OSError:
            continue
    return plugins


def ldap_plugin_available():
    return "ldap" in declared_plugins()


def ensure_breakglass_token():
    """Return the break-glass token ID, creating it once.

    Self-initialization creates an administrator token with this ID, so a
    failure of the directory login setup can never lock everybody out. The
    token never leaves the node: read it with openbao-breakglass-token.
    """
    if not os.path.exists(BREAKGLASS_TOKEN_FILE):
        token = "ns8bg" + secrets.token_hex(24)  # no "." allowed in custom IDs
        fd = os.open(BREAKGLASS_TOKEN_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as tfile:
            tfile.write(token + "\n")
    with open(BREAKGLASS_TOKEN_FILE, encoding="utf-8") as tfile:
        return tfile.read().strip()


def ensure_module_token_id():
    """Return the ID of the module token created by self-initialization."""
    if not os.path.exists(MODULE_TOKEN_FILE):
        write_secret_file(MODULE_TOKEN_FILE, "ns8mod" + secrets.token_hex(24))
    return read_module_token()


def write_secret_file(path, value):
    """Atomically write an owner-only file with a single value."""
    _write_file(path, value.strip() + "\n", 0o600)


def read_module_token():
    try:
        with open(MODULE_TOKEN_FILE, encoding="utf-8") as tfile:
            return tfile.read().strip()
    except FileNotFoundError:
        return ""


def module_token_status():
    """Return "missing", "valid", "invalid" or "unknown" (server unreachable)."""
    token = read_module_token()
    if not token:
        return "missing"
    try:
        api_request("auth/token/lookup-self", token=token, timeout=5)
        return "valid"
    except urllib.error.HTTPError as ex:
        return "invalid" if ex.code in (400, 403) else "unknown"
    except (urllib.error.URLError, OSError, ValueError):
        return "unknown"


def root_token_present(limit=500):
    """Return True if a root token exists, False if not, None if unknown.

    Uses the module token: lists the token accessors (not the tokens) and
    looks them up until a root token is found.
    """
    token = read_module_token()
    if not token:
        return None
    try:
        listing = api_request("auth/token/accessors", method="LIST", token=token, timeout=10)
        accessors = listing.get("data", {}).get("keys", [])
        if len(accessors) > limit:
            return None
        for accessor in accessors:
            info = api_request("auth/token/lookup-accessor", method="POST",
                               data={"accessor": accessor}, token=token, timeout=5)
            if "root" in info.get("data", {}).get("policies", []):
                return True
        return False
    except (urllib.error.URLError, OSError, ValueError):
        return None


def save_snapshot(path=SNAPSHOT_FILE):
    """Save a Raft snapshot with the module token. Return True on success."""
    token = read_module_token()
    if not token:
        return False
    url = f"http://127.0.0.1:{os.environ['TCP_PORT']}/v1/sys/storage/raft/snapshot"
    req = urllib.request.Request(url, headers={"X-Vault-Token": token})
    tmp_path = path + ".tmp"
    try:
        with _opener().open(req, timeout=300) as resp, \
                open(os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "wb") as sfile:
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                sfile.write(chunk)
        os.replace(tmp_path, path)
        return True
    except (urllib.error.URLError, OSError) as ex:
        log(f"Raft snapshot failed: {ex}", "<4>")
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return False


def vpn_api_enabled(env):
    return is_true(env.get("OPENBAO_VPN_API", "False"))


def vpn_api_port(env):
    """Return the TCP port of the cluster network API listener, or None."""
    ports = os.environ.get("TCP_PORTS", "").split(",")
    if len(ports) >= 3 and ports[2].strip().isdigit():
        return int(ports[2])
    value = env.get("OPENBAO_VPN_API_PORT", "")
    return int(value) if value.isdigit() else None


def vpn_api_endpoint(env):
    """Return (address, port) of the cluster network API, or None."""
    if not vpn_api_enabled(env):
        return None
    port = vpn_api_port(env)
    address = node_vpn_address() if port else None
    if not port or not address:
        return None
    return address, port


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


def render_initialize(params, env):
    """Return the JSON text of the self-initialization configuration.

    If any request fails without allow_failure, OpenBao stays initialized
    but refuses to unseal: only the admin policy and the break-glass token
    are mandatory, and both are purely local operations. Everything else
    may fail; the break-glass token then lets an administrator fix it.
    """
    bindpass = {
        "eval_source": "env",
        "eval_type": "string",
        "env_var": LDAP_BIND_PASSWORD_VAR,
        "require_present": True,
    }
    requests = []

    def add(req, allow_failure):
        body = {"operation": req["operation"], "path": req["path"], "data": req["data"]}
        if allow_failure:
            body["allow_failure"] = True
        requests.append({req["name"]: body})

    login = directory_login_requests(params, env["OPENBAO_LDAP_ADMIN_GROUP"], bindpass)
    # 1. administrator policy (mandatory)
    add(login[0], False)
    # 2. break-glass administrator token (mandatory)
    add({
        "name": "ns8-breakglass-token",
        "operation": "update",
        "path": "auth/token/create-orphan",
        "data": {
            "id": {
                "eval_source": "env",
                "eval_type": "string",
                "env_var": BREAKGLASS_TOKEN_VAR,
                "require_present": True,
            },
            "policies": [ADMIN_POLICY_NAME],
            "display_name": "ns8-breakglass",
            "ttl": BREAKGLASS_TOKEN_TTL,
            "renewable": False,
        },
    }, False)
    # 3. module token for snapshots and root token detection (allowed to fail)
    add({
        "name": "ns8-module-policy",
        "operation": "update",
        "path": f"sys/policies/acl/{MODULE_POLICY_NAME}",
        "data": {"policy": MODULE_POLICY},
    }, True)
    add({
        "name": "ns8-module-token",
        "operation": "update",
        "path": "auth/token/create-orphan",
        "data": {
            "id": {
                "eval_source": "env",
                "eval_type": "string",
                "env_var": MODULE_TOKEN_VAR,
                "require_present": True,
            },
            "policies": [MODULE_POLICY_NAME],
            "display_name": "ns8-module",
            "period": MODULE_TOKEN_PERIOD,
            "renewable": True,
        },
    }, True)
    # 4. the other built-in policies, directory login, group mappings and
    #    starter kits (allowed to fail)
    for req in policy_requests():
        if req["path"] != login[0]["path"]:
            add(req, True)
    add(login[1], True)  # ldap auth mount
    add(login[2], True)  # ldap auth configuration
    for req in group_requests(group_policy_map(env)):
        add(req, True)
    for req in kit_requests(starter_kits(env), env.get("TRAEFIK_HOST", "")):
        add(req, True)
    return json.dumps({"initialize": [{"ns8-directory-login": {"request": requests}}]}, indent=2) + "\n"


def metrics_port():
    """Return the second TCP port allocated to the module, or None."""
    ports = os.environ.get("TCP_PORTS", "").split(",")
    if len(ports) >= 2 and ports[1].strip().isdigit():
        return int(ports[1])
    return None


def node_vpn_address():
    """Return the cluster VPN IP address of this node, or None."""
    try:
        import agent
        rdb = agent.redis_connect(use_replica=True)
        return rdb.hget(f"node/{os.environ['NODE_ID']}/vpn", "ip_address") or None
    except Exception as ex:
        log(f"Cannot read the node VPN address: {ex}", "<4>")
        return None


def metrics_endpoint():
    """Return (address, port) where Prometheus scrapes OpenBao, or None."""
    port = metrics_port()
    address = node_vpn_address() if port else None
    if not port or not address:
        return None
    return address, port


def seal_stanza(env, mode, container_env, disabled=False):
    """Return the HCL lines of an auto seal, adding its secrets to container_env."""
    lines = [""]
    if mode == "transit":
        lines.append('seal "transit" {')
        lines.append(f"  address         = {_hcl_string(env['OPENBAO_TRANSIT_ADDRESS'])}")
        lines.append(f"  mount_path      = {_hcl_string(env['OPENBAO_TRANSIT_MOUNT'] or 'transit')}")
        lines.append(f"  key_name        = {_hcl_string(env['OPENBAO_TRANSIT_KEY'])}")
        lines.append(f"  tls_skip_verify = {_hcl_string(str(is_true(env['OPENBAO_TRANSIT_TLS_SKIP_VERIFY'])).lower())}")
        try:
            with open(TRANSIT_TOKEN_FILE, encoding="utf-8") as tfile:
                # The seal renews this token by itself
                container_env.append(f"BAO_TOKEN={tfile.read().strip()}")
        except FileNotFoundError:
            log("Transit seal: no token, run openbao-transit-token", "<3>")
    else:
        key_id, key_hex = ensure_seal_key()
        lines.append('seal "static" {')
        lines.append(f"  current_key_id = {_hcl_string(key_id)}")
        lines.append('  current_key    = "env://BAO_STATIC_SEAL_CURRENT_KEY"')
        container_env.append(f"BAO_STATIC_SEAL_CURRENT_KEY_ID={key_id}")
        container_env.append(f"BAO_STATIC_SEAL_CURRENT_KEY={key_hex}")
    if disabled:
        lines.append('  disabled        = "true"')
    lines.append("}")
    return lines


def public_access(env):
    return is_true(env.get("OPENBAO_PUBLIC_ACCESS", "True"))


def snapshot_keep(env):
    value = env.get("OPENBAO_SNAPSHOT_KEEP", "0")
    return int(value) if value.isdigit() else 0


def list_snapshots():
    """Return [{name, size, created}] of the scheduled snapshots, newest first."""
    snapshots = []
    try:
        names = os.listdir(SNAPSHOT_DIR)
    except FileNotFoundError:
        return []
    for name in names:
        if not name.endswith(".snap"):
            continue
        path = os.path.join(SNAPSHOT_DIR, name)
        stat = os.stat(path)
        snapshots.append({"name": name, "size": stat.st_size, "created": int(stat.st_mtime)})
    return sorted(snapshots, key=lambda s: s["created"], reverse=True)


def auto_initialize_wanted(env):
    return (
        env["OPENBAO_UNSEAL_MODE"] in ("auto", "transit")
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
    if not public_access(env):
        vpn_api = vpn_api_endpoint(env)
        if vpn_api:
            api_addr = f"http://{vpn_api[0]}:{vpn_api[1]}"
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
    static_part.append("  telemetry {")
    static_part.append("    disallow_metrics = true")
    static_part.append("  }")
    static_part.append("}")
    static_part.append("")
    static_part.append('listener "tcp" {')
    static_part.append(f'  address         = "0.0.0.0:{METRICS_CONTAINER_PORT}"')
    static_part.append(f'  cluster_address = "127.0.0.1:{METRICS_CONTAINER_PORT + 1}"')
    static_part.append("  tls_disable     = true")
    static_part.append("  telemetry {")
    static_part.append("    metrics_only                   = true")
    static_part.append("    unauthenticated_metrics_access = true")
    static_part.append("  }")
    static_part.append("}")
    static_part.append("")
    static_part.append("telemetry {")
    static_part.append('  prometheus_retention_time = "24h"')
    static_part.append("  disable_hostname          = true")
    static_part.append("}")

    plugins = declared_plugins()
    if plugins:
        static_part.append("")
        static_part.append(f"plugin_directory = {_hcl_string(PLUGIN_CONTAINER_DIR)}")
        for name in sorted(plugins):
            record = plugins[name]
            static_part.append(f"plugin {_hcl_string(record['type'])} {_hcl_string(name)} {{")
            static_part.append(f"  command   = {_hcl_string(record['command'])}")
            static_part.append(f"  version   = {_hcl_string(record['version'])}")
            static_part.append(f"  sha256sum = {_hcl_string(record['sha256'])}")
            static_part.append("}")

    container_env = []
    # During a seal migration the previous auto seal stays configured with
    # disabled = "true", next to the new seal (none for Shamir/manual).
    migrate_from = env.get("OPENBAO_SEAL_MIGRATION_FROM", "")
    if migrate_from and migrate_from != unseal_mode and migrate_from in ("auto", "transit"):
        static_part.extend(seal_stanza(env, migrate_from, container_env, disabled=True))
    if unseal_mode in ("auto", "transit"):
        static_part.extend(seal_stanza(env, unseal_mode, container_env))

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
        if not params:
            log("Self-initialization skipped: the user domain is not available", "<4>")
        elif "ldap" not in plugins:
            log("Self-initialization skipped: the LDAP auth plugin is not installed", "<4>")
        else:
            init_text = render_initialize(params, env)
            init_env.append(f"{LDAP_BIND_PASSWORD_VAR}={params['bind_password']}")
            init_env.append(f"{BREAKGLASS_TOKEN_VAR}={ensure_breakglass_token()}")
            init_env.append(f"{MODULE_TOKEN_VAR}={ensure_module_token_id()}")

    config_text = (
        "# Generated by ns8-openbao: manual changes are overwritten.\n"
        f"# restart-signature: {signature}\n\n"
        + static_text + "\n"
        + "\n".join(reloadable) + "\n"
    )
    container_env_text = "".join(line + "\n" for line in container_env + init_env)

    # Systemd expands $OPENBAO_PUBLISH_METRICS to zero or more podman
    # arguments: without an endpoint the metrics port is not published.
    endpoint = metrics_endpoint()
    publish = f"--publish={endpoint[0]}:{endpoint[1]}:{METRICS_CONTAINER_PORT}" if endpoint else ""
    runtime_env_text = f"OPENBAO_PUBLISH_METRICS={publish}\n"
    vpn_api = vpn_api_endpoint(env)
    vpn_publish = f"--publish={vpn_api[0]}:{vpn_api[1]}:8200" if vpn_api else ""
    runtime_env_text += f"OPENBAO_PUBLISH_VPN_API={vpn_publish}\n"
    return {
        "runtime_env_text": runtime_env_text,
        "config_text": config_text,
        "container_env_text": container_env_text,
        "init_text": init_text,
        "restart_signature": hashlib.sha256(
            (static_text + "".join(line + "\n" for line in container_env) + runtime_env_text).encode()).hexdigest(),
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
    _write_file(RUNTIME_ENV_FILE, rendered["runtime_env_text"], 0o644)
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


def ip_allowlist(env):
    return [n for n in env.get("OPENBAO_IP_ALLOWLIST", "").split(",") if n]


def starter_kits(env):
    return [k for k in env.get("OPENBAO_STARTER_KITS", "").split(",") if k in STARTER_KITS]


def encode_group_policies(mappings):
    """Encode [{group, policy}] for the environment file (no quotes/spaces)."""
    return urllib.parse.quote(json.dumps(mappings, separators=(",", ":")), safe="")


def ldap_group_policies(env):
    """Return the [{group, policy}] mapping of directory groups to policies."""
    raw = env.get("OPENBAO_LDAP_GROUP_POLICIES", "")
    if not raw:
        return []
    try:
        mappings = json.loads(urllib.parse.unquote(raw))
        return [m for m in mappings if m.get("group") and m.get("policy")]
    except (ValueError, AttributeError):
        log("Invalid OPENBAO_LDAP_GROUP_POLICIES value: ignored", "<4>")
        return []


def group_policy_map(env):
    """Return {group: [policies]}: the administrators group plus the mapping table."""
    groups = {}
    admin_group = env.get("OPENBAO_LDAP_ADMIN_GROUP", "")
    if admin_group:
        groups[admin_group] = [ADMIN_POLICY_NAME]
    for mapping in ldap_group_policies(env):
        policies = groups.setdefault(mapping["group"], [])
        if mapping["policy"] not in policies:
            policies.append(mapping["policy"])
    return groups


def policy_requests():
    """Requests that create or update the built-in policies."""
    return [{
        "name": f"policy-{name}",
        "operation": "update",
        "path": f"sys/policies/acl/{name}",
        "data": {"policy": text},
    } for name, text in BUILTIN_POLICIES.items()]


def group_requests(groups):
    """Requests that map directory groups to policies."""
    return [{
        "name": "ldap-group-" + "".join(c if c.isalnum() else "-" for c in group.lower()),
        "operation": "update",
        "path": "auth/ldap/groups/" + group,
        "data": {"policies": policies},
    } for group, policies in groups.items()]


def kit_requests(kits, host):
    """Requests of the starter kits. Each is idempotent on a fresh server."""
    requests = []
    if "kv" in kits:
        requests.append({
            "name": "kit-kv-mount",
            "operation": "update",
            "path": "sys/mounts/secret",
            "data": {"type": "kv", "description": "Key/value secrets", "options": {"version": "2"}},
        })
    if "pki" in kits:
        base = f"https://{host}/v1/pki" if host else ""
        requests.append({
            "name": "kit-pki-mount",
            "operation": "update",
            "path": "sys/mounts/pki",
            "data": {"type": "pki", "description": "Internal certificate authority",
                     "config": {"max_lease_ttl": "87600h"}},
        })
        requests.append({
            "name": "kit-pki-root",
            "operation": "update",
            "path": "pki/root/generate/internal",
            "data": {"common_name": f"{host or 'OpenBao'} internal root CA",
                     "issuer_name": "ns8-root", "ttl": "87600h",
                     "key_type": "ec", "key_bits": 384},
        })
        if base:
            requests.append({
                "name": "kit-pki-urls",
                "operation": "update",
                "path": "pki/config/urls",
                "data": {"issuing_certificates": [f"{base}/ca"],
                         "crl_distribution_points": [f"{base}/crl"]},
            })
        requests.append({
            "name": "kit-pki-role",
            "operation": "update",
            "path": "pki/roles/ns8-server",
            "data": {"allow_any_name": True, "server_flag": True, "client_flag": True,
                     "key_type": "ec", "key_bits": 256, "ttl": "720h", "max_ttl": "2160h"},
        })
    if "approle" in kits:
        requests.append({
            "name": "kit-approle",
            "operation": "update",
            "path": "sys/auth/approle",
            "data": {"type": "approle", "description": "Application login"},
        })
    return requests


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
