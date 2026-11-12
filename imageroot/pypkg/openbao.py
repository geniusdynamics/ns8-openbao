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
import urllib.request

# Files in the state directory
ENVIRONMENT_FILE = "environment"
CONFIG_DIR = "openbao-config"  # mounted read-only on /openbao/config
CONFIG_FILE = CONFIG_DIR + "/openbao.hcl"
APPLIED_FILE = "openbao-applied.json"  # configuration loaded by the server
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
}

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


def render_config(env):
    """Return (config_text, container_env_text, restart_signature).

    restart_signature covers the settings that OpenBao cannot reload with
    SIGHUP. log_level and declarative audit devices are reloadable.
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

    config_text = (
        "# Generated by ns8-openbao: manual changes are overwritten.\n"
        f"# restart-signature: {signature}\n\n"
        + static_text + "\n"
        + "\n".join(reloadable) + "\n"
    )
    container_env_text = "\n".join(container_env) + ("\n" if container_env else "")
    return config_text, container_env_text, signature


def write_config():
    """Write the OpenBao configuration files from the module environment.

    Return the applied-state record of the written configuration, to be
    compared with read_applied() and saved with mark_applied().
    """
    env = read_environment()
    config_text, container_env_text, signature = render_config(env)

    os.makedirs(CONFIG_DIR, mode=0o755, exist_ok=True)
    os.chmod(CONFIG_DIR, 0o755)
    # The container env file holds the seal key: owner-only permissions.
    _write_file(CONTAINER_ENV_FILE, container_env_text, 0o600)
    # The OpenBao process runs as an unprivileged user inside the container
    # and must be able to read the configuration file. It holds no secrets.
    # The whole directory is mounted, so an atomic replace is visible to a
    # running container on reload.
    _write_file(CONFIG_FILE, config_text, 0o644)

    return {
        "restart_signature": signature,
        "config_hash": hashlib.sha256(
            (config_text + container_env_text).encode()).hexdigest(),
    }


def read_applied():
    """Return the record of the configuration loaded by the server, or None."""
    try:
        with open(APPLIED_FILE, encoding="utf-8") as afile:
            return json.load(afile)
    except (FileNotFoundError, ValueError):
        return None


def mark_applied(record):
    _write_file(APPLIED_FILE, json.dumps(record) + "\n", 0o644)


def required_change(record):
    """Return "none", "reload" or "restart" to make a running server load record."""
    applied = read_applied()
    if not applied or applied.get("restart_signature") != record["restart_signature"]:
        return "restart"
    if applied.get("config_hash") != record["config_hash"]:
        return "reload"
    return "none"


def _opener():
    # Never send loopback API requests through an HTTP proxy configured
    # in the node environment.
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


def api_get(path, timeout=5):
    """GET an unauthenticated OpenBao API path. Return the decoded JSON."""
    url = f"http://127.0.0.1:{os.environ['TCP_PORT']}/v1/{path.lstrip('/')}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with _opener().open(req, timeout=timeout) as resp:
        return json.load(resp)


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
