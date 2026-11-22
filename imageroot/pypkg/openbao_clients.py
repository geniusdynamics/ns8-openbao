#
# Copyright (C) 2026 Genius Dynamics
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""Client provisioning: other NS8 modules get their own OpenBao token.

Optional and off by default (OPENBAO_CLIENT_PROVISIONING). See
docs/client-provisioning.md for the client contract and the security
model. In short:

- a module that declares the authorization openbao@any:secretsclient may
  run the provision-client action. Its identity is AGENT_TASK_USER,
  set by the NS8 API server: it never comes from the action input;
- the OpenBao administrator approves each client module in the UI. The
  approval binds the module ID to its MODULE_UUID: a module reinstalled
  with the same ID must be approved again;
- the client receives an OpenBao token of the "ns8-client" token role,
  wrapped (single use, WRAP_TTL seconds): the task output, which NS8
  keeps in Redis, never holds a usable credential;
- the token policies are static, written with an administrator token
  when the feature is enabled. They are templated on the entity alias of
  the token, which is the client module ID: every client reaches only
  ns8-kv/data/modules/<module id>/* and, when approved separately, the
  database secrets engine mounted at ns8-db-<module id>/;
- the module creates tokens with the narrow "ns8-provisioner" token. It
  can create tokens of the ns8-client role only (no policy, auth method
  or role writes), so even if it leaks it never grants more than client
  access.

Every function expects the module state directory as working directory.
"""

import contextlib
import fcntl
import json
import os
import re
import sys
import time
import urllib.error

import openbao

ENV_VAR = "OPENBAO_CLIENT_PROVISIONING"

# Files in the state directory
STATE_FILE = "client-access.json"   # approvals, pending requests, token accessors
LOCK_FILE = ".client-access.lock"
PROVISIONER_TOKEN_FILE = "openbao-provisioner.token"

# OpenBao objects. The policies and the token role are written by
# "openbao-client-provisioner create" with an administrator token.
PROVISIONER_POLICY_NAME = "ns8-provisioner"
PROVISIONER_TOKEN_PERIOD = "168h"   # renewed daily by openbao-maintenance
KV_POLICY_NAME = "ns8-client-kv"
DB_POLICY_NAME = "ns8-client-db"
GROUP_POLICY_NAME = "ns8-client-group"
TOKEN_ROLE = "ns8-client"
KV_MOUNT = "ns8-kv"
KV_PREFIX = "modules"
GROUP_PREFIX = "groups"
DB_MOUNT_PREFIX = "ns8-db-"

# Client tokens: periodic (renew at least once a day), capped at 30 days,
# then the client provisions a new one through NS8, which checks the
# approval again.
TOKEN_PERIOD = 24 * 3600
TOKEN_EXPLICIT_MAX_TTL = 30 * 24 * 3600
WRAP_TTL = 120
WRAP_CREATION_PATH = f"auth/token/create/{TOKEN_ROLE}"
MAX_TOKENS_PER_CLIENT = 5
MAX_PENDING = 32
MAX_GROUPS = 8
AUDIT_FILE = "client-audit.jsonl"   # no secrets: who got what, and when
AUDIT_KEEP = 500

# NS8 module IDs: no "*", "+", "/" or "{": safe in policy paths and mounts
MODULE_ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,62}[0-9]$")
# Shared groups: the last character is a letter, so a group ID is never a
# module ID and their entity aliases never collide
GROUP_ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,62}[a-z]$")


class ClientError(Exception):
    """A failure reported to the caller as a validation error."""

    def __init__(self, error, field="module_id", value=""):
        super().__init__(error)
        self.error = error
        self.field = field
        self.value = value

    def payload(self):
        return [{"field": self.field, "parameter": self.field, "value": self.value, "error": self.error}]


def report(ex):
    """Print a ClientError as an NS8 validation failure and exit."""
    import agent
    agent.set_status("validation-failed")
    json.dump(ex.payload(), fp=sys.stdout)
    sys.exit(3)


def log(message, level=""):
    print(level + message, file=sys.stderr)


def enabled(env=None):
    env = env if env is not None else openbao.read_environment()
    return openbao.is_true(env.get(ENV_VAR, "False"))


def valid_module_id(module_id):
    return isinstance(module_id, str) and bool(MODULE_ID_RE.fullmatch(module_id))


def valid_group_id(group_id):
    return isinstance(group_id, str) and bool(GROUP_ID_RE.fullmatch(group_id))


def kv_prefix(module_id):
    return f"{KV_PREFIX}/{module_id}"


def group_prefix(group_id):
    return f"{GROUP_PREFIX}/{group_id}"


def db_mount(module_id):
    return DB_MOUNT_PREFIX + module_id


# --------------------------------------------------------------------------
# Policies and token role (written with an administrator token)
# --------------------------------------------------------------------------

def _alias(accessor):
    return "{{identity.entity.aliases.%s.name}}" % accessor


def kv_policy(accessor):
    """Templated policy: CRUD on the KV v2 prefix of the token's module."""
    name = _alias(accessor)
    return f"""# NethServer 8 client modules: own key/value prefix only. The path is
# templated on the entity alias of the token (the client module ID),
# set by the ns8-client token role when the module provisions a token.
path "{KV_MOUNT}/data/{KV_PREFIX}/{name}/*" {{
  capabilities = ["create", "read", "update", "patch", "delete", "list"]
}}
path "{KV_MOUNT}/metadata/{KV_PREFIX}/{name}/*" {{
  capabilities = ["read", "update", "patch", "delete", "list"]
}}
path "{KV_MOUNT}/delete/{KV_PREFIX}/{name}/*" {{
  capabilities = ["update"]
}}
path "{KV_MOUNT}/undelete/{KV_PREFIX}/{name}/*" {{
  capabilities = ["update"]
}}
path "{KV_MOUNT}/destroy/{KV_PREFIX}/{name}/*" {{
  capabilities = ["update"]
}}
path "{KV_MOUNT}/subkeys/{KV_PREFIX}/{name}/*" {{
  capabilities = ["read"]
}}
"""


def group_policy(accessor):
    """Templated policy of group tokens: CRUD on the shared group prefix.
    A group token has the group ID as entity alias; the module issues it
    only to the members the administrator approved for that group."""
    name = _alias(accessor)
    return kv_policy(accessor).replace(
        f"{KV_PREFIX}/{name}/", f"{GROUP_PREFIX}/{name}/").replace(
        "# NethServer 8 client modules: own key/value prefix only.",
        "# NethServer 8 client module groups: shared key/value prefix only.").replace(
        "(the client module ID)", "(the group ID)")


def db_policy(accessor):
    """Templated policy: manage the database secrets engine of the module."""
    name = _alias(accessor)
    return f"""# NethServer 8 client modules approved for a database secrets engine:
# everything inside the mount named after the client module. The mount
# itself is enabled by the module, never by the client.
path "{DB_MOUNT_PREFIX}{name}/*" {{
  capabilities = ["create", "read", "update", "patch", "delete", "list"]
}}
"""


PROVISIONER_POLICY = f"""# Token of the NethServer 8 module for client provisioning, on the node
# only. It creates tokens of the {TOKEN_ROLE} token role, whose allowed
# policies are fixed: it cannot write policies, roles or auth methods.
path "auth/token/create/{TOKEN_ROLE}" {{
  capabilities = ["update"]
}}
# Revoke and prune the tokens issued to clients (by accessor)
path "auth/token/lookup-accessor" {{
  capabilities = ["update"]
}}
path "auth/token/revoke-accessor" {{
  capabilities = ["update"]
}}
# Delete the data of a revoked client, when the administrator chooses so
path "{KV_MOUNT}/metadata/{KV_PREFIX}/*" {{
  capabilities = ["list", "delete"]
}}
# Database secrets engines dedicated to approved clients
path "sys/mounts/{DB_MOUNT_PREFIX}*" {{
  capabilities = ["create", "read", "update", "delete", "sudo"]
}}
"""


def token_role_data():
    return {
        "allowed_policies": [KV_POLICY_NAME, DB_POLICY_NAME, GROUP_POLICY_NAME],
        "orphan": True,
        "renewable": True,
        "token_period": TOKEN_PERIOD,
        "token_explicit_max_ttl": TOKEN_EXPLICIT_MAX_TTL,
        "token_type": "service",
        # The provisioner names the alias after the client module ID or
        # the group ID, validated before every request
        "allowed_entity_aliases": ["*"],
        "token_no_default_policy": False,
    }


# --------------------------------------------------------------------------
# Provisioner token
# --------------------------------------------------------------------------

def read_provisioner_token():
    try:
        with open(PROVISIONER_TOKEN_FILE, encoding="utf-8") as tfile:
            return tfile.read().strip()
    except FileNotFoundError:
        return ""


def provisioner_status():
    """Return "missing", "valid", "invalid" or "unknown" (server unreachable)."""
    return _token_status(read_provisioner_token())


def _token_status(token):
    if not token:
        return "missing"
    try:
        openbao.api_request("auth/token/lookup-self", token=token, timeout=5)
        return "valid"
    except urllib.error.HTTPError as ex:
        return "invalid" if ex.code in (400, 403) else "unknown"
    except (urllib.error.URLError, OSError, ValueError):
        return "unknown"


def _mount_info(path, token):
    try:
        info = openbao.api_request(f"sys/mounts/{path}", token=token, timeout=10)
    except urllib.error.HTTPError as ex:
        if ex.code in (400, 404):
            return None
        raise
    return info.get("data", info)


def setup_provisioner(admin_token):
    """Write the policies, mount and token role, then create the
    provisioner token. Every step is idempotent; the token is created last,
    so a failure leaves no usable credential. The administrator token is
    never stored. Return a message for the administrator."""
    env = openbao.read_environment()
    if not enabled(env):
        raise ClientError("client_provisioning_disabled", "client_provisioning", False)
    if openbao.ha_role(env) == "member":
        raise ClientError("client_provisioning_ha_member", "client_provisioning", True)
    require_ready()

    def call(path, method="GET", data=None):
        return openbao.api_request(path, method=method, data=data, token=admin_token, timeout=30)

    auth = call("sys/auth")
    mounts = auth.get("data") or auth
    accessor = (mounts.get("token/") or {}).get("accessor", "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", accessor or ""):
        raise RuntimeError("cannot read the accessor of the token auth method")

    kv = _mount_info(KV_MOUNT, admin_token)
    if kv is None:
        call(f"sys/mounts/{KV_MOUNT}", "POST", {
            "type": "kv",
            "options": {"version": "2"},
            "description": "NethServer 8 client modules (modules/<module id>/)",
        })
    elif kv.get("type") not in ("kv", "kv-v2") or str((kv.get("options") or {}).get("version", "2")) != "2":
        raise RuntimeError(f"the {KV_MOUNT}/ mount exists and is not a KV version 2 store")

    call(f"sys/policies/acl/{KV_POLICY_NAME}", "POST", {"policy": kv_policy(accessor)})
    call(f"sys/policies/acl/{DB_POLICY_NAME}", "POST", {"policy": db_policy(accessor)})
    call(f"sys/policies/acl/{GROUP_POLICY_NAME}", "POST", {"policy": group_policy(accessor)})
    call(f"sys/policies/acl/{PROVISIONER_POLICY_NAME}", "POST", {"policy": PROVISIONER_POLICY})
    call(f"auth/token/roles/{TOKEN_ROLE}", "POST", token_role_data())
    response = call("auth/token/create-orphan", "POST", {
        "policies": [PROVISIONER_POLICY_NAME],
        "display_name": "ns8-provisioner",
        "period": PROVISIONER_TOKEN_PERIOD,
        "renewable": True,
        "meta": {"ns8_module_id": os.environ.get("MODULE_ID", "")},
    })
    old_token = read_provisioner_token()
    openbao.write_secret_file(PROVISIONER_TOKEN_FILE, response["auth"]["client_token"])
    if old_token:
        _revoke_self(old_token)
    return "Client provisioning enabled: approve client modules on the Clients page"


def _revoke_self(token):
    try:
        openbao.api_request("auth/token/revoke-self", method="POST", data={}, token=token)
        return True
    except urllib.error.HTTPError as ex:
        # 403: the token is already invalid
        return ex.code in (400, 403)
    except (urllib.error.URLError, OSError, ValueError):
        return False


def renew_provisioner():
    token = read_provisioner_token()
    if not token or not enabled():
        return False
    openbao.api_request("auth/token/renew-self", method="POST", data={}, token=token)
    return True


# --------------------------------------------------------------------------
# Approvals and token records
# --------------------------------------------------------------------------

def _empty_state():
    return {"grants": {}, "pending": {}, "tokens": {}, "cleanup": {}}


def load_state():
    state = _empty_state()
    try:
        with open(STATE_FILE, encoding="utf-8") as sfile:
            stored = json.load(sfile)
        for key in state:
            if isinstance(stored.get(key), dict):
                state[key] = stored[key]
    except (FileNotFoundError, ValueError):
        pass
    return state


def save_state(state):
    openbao._write_file(STATE_FILE, json.dumps(state, indent=2, sort_keys=True) + "\n", 0o600)


@contextlib.contextmanager
def locked_state():
    """Yield the state under an exclusive lock; the caller saves it."""
    fd = os.open(LOCK_FILE, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, "r+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield load_state()


def registered_uuids(module_ids):
    """Return {module id: MODULE_UUID or None}, read from the leader: the
    cluster owns module_uuid, which changes when a module is reinstalled."""
    module_ids = [m for m in module_ids if valid_module_id(m)]
    if not module_ids:
        return {}
    try:
        import agent
        with agent.redis_connect(socket_timeout=5, socket_connect_timeout=5) as rdb:
            values = rdb.hmget("cluster/module_uuid", module_ids)
    except Exception as ex:
        log(f"Cannot read the module UUIDs: {type(ex).__name__}", "<3>")
        raise ClientError("cluster_unavailable", "module_id", ",".join(module_ids)) from None
    return {m: (v or None) for m, v in zip(module_ids, values)}


def registered_uuid(module_id):
    if module_id == os.environ.get("MODULE_ID"):
        return None
    return registered_uuids([module_id]).get(module_id)


def installed_modules():
    """Return the sorted IDs of the other modules of the cluster."""
    try:
        import agent
        with agent.redis_connect(use_replica=True, socket_timeout=5, socket_connect_timeout=5) as rdb:
            ids = rdb.hkeys("cluster/module_uuid")
    except Exception as ex:
        log(f"Cannot list the cluster modules: {type(ex).__name__}", "<4>")
        return []
    return sorted(m for m in ids if valid_module_id(m) and m != os.environ.get("MODULE_ID"))


def caller_module():
    """Return the module ID of the caller, or raise ClientError.

    The NS8 API server puts the authenticated identity in AGENT_TASK_USER;
    a task written directly to Redis, an administrator and a missing
    identity are refused.
    """
    user = os.environ.get("AGENT_TASK_USER", "")
    prefix, _, module_id = user.partition("/")
    if prefix != "module" or not valid_module_id(module_id) or module_id == os.environ.get("MODULE_ID"):
        raise ClientError("client_not_authorized", "module_id", user)
    return module_id


# --------------------------------------------------------------------------
# OpenBao helpers
# --------------------------------------------------------------------------

def require_ready():
    """Raise ClientError unless OpenBao is running, initialized and unsealed."""
    status = openbao.get_seal_status(timeout=5)
    if not status:
        raise ClientError("openbao_unavailable", "openbao", "down")
    if not status.get("initialized"):
        raise ClientError("openbao_unavailable", "openbao", "uninitialized")
    if status.get("sealed"):
        raise ClientError("openbao_unavailable", "openbao", "sealed")


def _token_exists(token, accessor):
    """Return True/False, or None if unknown."""
    try:
        openbao.api_request("auth/token/lookup-accessor", method="POST",
                            data={"accessor": accessor}, token=token, timeout=10)
        return True
    except urllib.error.HTTPError as ex:
        # 400 "invalid accessor": revoked or expired
        return False if ex.code == 400 else None
    except (urllib.error.URLError, OSError, ValueError):
        return None


def _revoke_accessor(token, accessor):
    """Return True if the token is revoked or no longer exists."""
    try:
        openbao.api_request("auth/token/revoke-accessor", method="POST",
                            data={"accessor": accessor}, token=token, timeout=10)
        return True
    except urllib.error.HTTPError as ex:
        return ex.code == 400
    except (urllib.error.URLError, OSError, ValueError):
        return False


def _kv_delete_tree(token, path):
    """Delete every key (all versions and metadata) under path."""
    try:
        listing = openbao.api_request(f"{KV_MOUNT}/metadata/{path}/", method="LIST", token=token, timeout=30)
    except urllib.error.HTTPError as ex:
        if ex.code == 404:
            return
        raise
    for key in (listing.get("data") or {}).get("keys", []):
        if key.endswith("/"):
            _kv_delete_tree(token, f"{path}/{key.rstrip('/')}")
        else:
            openbao.api_request(f"{KV_MOUNT}/metadata/{path}/{key}", method="DELETE", token=token, timeout=30)


def _disable_db_mount(token, module_id):
    try:
        openbao.api_request(f"sys/mounts/{db_mount(module_id)}", method="DELETE", token=token, timeout=60)
    except urllib.error.HTTPError as ex:
        if ex.code not in (400, 404):
            raise


def _ensure_db_mount(token, module_id):
    """Enable the database secrets engine of a client. Return True if
    it was created by this call."""
    info = _mount_info(db_mount(module_id), token)
    if info is not None:
        if info.get("type") != "database":
            raise ClientError("database_mount_conflict", "database_engine", db_mount(module_id))
        return False
    openbao.api_request(f"sys/mounts/{db_mount(module_id)}", method="POST", token=token, timeout=30, data={
        "type": "database",
        "description": f"NethServer 8 module {module_id}",
    })
    return True


def _queue_cleanup(state, module_id, delete_data=False):
    """Move the token records of a client to the cleanup queue."""
    entry = state["cleanup"].setdefault(module_id, {"accessors": [], "delete_data": False})
    for record in state["tokens"].pop(module_id, []):
        if record.get("accessor") and record["accessor"] not in entry["accessors"]:
            entry["accessors"].append(record["accessor"])
    entry["delete_data"] = bool(entry.get("delete_data") or delete_data)
    if not entry["accessors"] and not entry["delete_data"]:
        state["cleanup"].pop(module_id, None)


def run_cleanup(state, token=None):
    """Revoke the queued tokens and delete the queued data. Return the IDs
    still pending. Needs the provisioner token and an unsealed OpenBao."""
    token = token if token is not None else read_provisioner_token()
    if not state["cleanup"]:
        return []
    if not token:
        return sorted(state["cleanup"])
    try:
        require_ready()
    except ClientError:
        return sorted(state["cleanup"])
    if _token_status(token) != "valid":
        return sorted(state["cleanup"])
    for module_id in sorted(state["cleanup"]):
        entry = state["cleanup"][module_id]
        entry["accessors"] = [a for a in entry.get("accessors", []) if not _revoke_accessor(token, a)]
        if entry.get("delete_data") and not entry["accessors"]:
            try:
                if valid_module_id(module_id):
                    _kv_delete_tree(token, kv_prefix(module_id))
                    _disable_db_mount(token, module_id)
                entry["delete_data"] = False
                log(f"Data of client module {module_id} deleted")
            except (urllib.error.URLError, OSError, ValueError) as ex:
                log(f"Cannot delete the data of client module {module_id}: {type(ex).__name__}", "<4>")
        if not entry["accessors"] and not entry.get("delete_data"):
            del state["cleanup"][module_id]
            log(f"Tokens of client module {module_id} revoked")
    return sorted(state["cleanup"])


def _prune_tokens(state, module_id, token):
    """Forget the records of tokens that expired or were revoked."""
    kept = []
    for record in state["tokens"].get(module_id, []):
        if _token_exists(token, record.get("accessor", "")) is not False:
            kept.append(record)
    if kept:
        state["tokens"][module_id] = kept
    else:
        state["tokens"].pop(module_id, None)


def client_address(env):
    """Return (address, kind) clients use to reach OpenBao: the cluster
    network API if enabled, otherwise the public host name."""
    endpoint = openbao.vpn_api_endpoint(env)
    if endpoint:
        return "http://{}:{}".format(*endpoint), "vpn"
    if env.get("TRAEFIK_HOST") and openbao.public_access(env):
        return f"https://{env['TRAEFIK_HOST']}", "public"
    raise ClientError("no_address", "vpn_api", False)


# --------------------------------------------------------------------------
# Actions
# --------------------------------------------------------------------------

def clean_groups(groups, field="groups"):
    """Validate a list of group IDs; return it sorted and without duplicates."""
    groups = sorted(set(groups or []))
    for group_id in groups:
        if not valid_group_id(group_id):
            raise ClientError("invalid_group_id", field, group_id)
    if len(groups) > MAX_GROUPS:
        raise ClientError("too_many_groups", field, len(groups))
    return groups


def audit(event, module_id, **fields):
    """Append an audit record, without secrets, and log it to the journal."""
    record = {"time": int(time.time()), "event": event, "module_id": module_id}
    record.update(fields)
    line = json.dumps(record, sort_keys=True)
    log(f"Client provisioning audit: {line}")
    try:
        try:
            with open(AUDIT_FILE, encoding="utf-8") as afile:
                lines = afile.read().splitlines()[-(AUDIT_KEEP - 1):]
        except FileNotFoundError:
            lines = []
        openbao._write_file(AUDIT_FILE, "\n".join(lines + [line]) + "\n", 0o600)
    except OSError as ex:
        log(f"Cannot write the client audit file: {ex}", "<4>")


def read_audit(limit=50):
    try:
        with open(AUDIT_FILE, encoding="utf-8") as afile:
            lines = afile.read().splitlines()
    except FileNotFoundError:
        return []
    records = []
    for line in lines[-limit:]:
        try:
            records.append(json.loads(line))
        except ValueError:
            continue
    return list(reversed(records))


def _record_pending(state, module_id, module_uuid, database_engine, groups=()):
    if not module_uuid:
        return False
    pending = state["pending"]
    if module_id not in pending and len(pending) >= MAX_PENDING:
        oldest = min(pending, key=lambda m: pending[m].get("requested_at", 0))
        del pending[oldest]
    previous = pending.get(module_id, {})
    pending[module_id] = {
        "module_uuid": module_uuid,
        "database_engine": bool(database_engine),
        # Requested by the client: shown to the administrator, who decides.
        # Never granted by the request itself.
        "groups": list(groups),
        "requested_at": int(time.time()),
    }
    return previous.get("module_uuid") != module_uuid


def _effective_grant(state, module_id, module_uuid):
    grant = state["grants"].get(module_id)
    if module_uuid and grant and grant.get("module_uuid") == module_uuid:
        return grant
    return None


def _wrapped_token(token, policies, alias, meta):
    response = openbao.api_request(
        WRAP_CREATION_PATH, method="POST", token=token, timeout=30,
        headers={"X-Vault-Wrap-TTL": f"{WRAP_TTL}s"},
        data={
            "policies": policies,
            "entity_alias": alias,
            "display_name": alias,
            "meta": meta,
        })
    wrap = response.get("wrap_info") or {}
    if not wrap.get("token"):
        raise ValueError("the response is not wrapped")
    return wrap


def request_access(module_id, database_engine=False, groups=()):
    """Record a pending access request of a module (or a change request of
    an approved one). Return the client status."""
    env = openbao.read_environment()
    if not enabled(env):
        raise ClientError("client_provisioning_disabled", "client_provisioning", False)
    groups = clean_groups(groups)
    with locked_state() as state:
        module_uuid = registered_uuid(module_id)
        if not module_uuid:
            raise ClientError("module_not_found", "module_id", module_id)
        grant = _effective_grant(state, module_id, module_uuid)
        if grant:
            wanted_db = database_engine and not grant.get("database_engine")
            wanted_groups = sorted(set(groups) - set(grant.get("groups", [])))
            if wanted_db:
                grant["database_engine_requested"] = True
            if wanted_groups:
                grant["groups_requested"] = sorted(set(grant.get("groups_requested", [])) | set(wanted_groups))
            if wanted_db or wanted_groups:
                audit("change_requested", module_id, module_uuid=module_uuid,
                      database_engine=bool(wanted_db), groups=wanted_groups)
        elif _record_pending(state, module_id, module_uuid, database_engine, groups):
            audit("access_requested", module_id, module_uuid=module_uuid,
                  database_engine=bool(database_engine), groups=groups)
        save_state(state)
    return client_status(module_id)


def provision(module_id, database_engine=False):
    """Issue wrapped client tokens to an approved module. Return the
    output of the provision-client action."""
    env = openbao.read_environment()
    if not enabled(env):
        raise ClientError("client_provisioning_disabled", "client_provisioning", False)
    token = read_provisioner_token()
    if not token:
        raise ClientError("client_provisioner_missing", "client_provisioning", True)
    address, address_kind = client_address(env)
    with locked_state() as state:
        module_uuid = registered_uuid(module_id)
        grant = _effective_grant(state, module_id, module_uuid)
        if not grant:
            if _record_pending(state, module_id, module_uuid, database_engine):
                audit("access_requested", module_id, module_uuid=module_uuid,
                      database_engine=bool(database_engine), groups=[])
            save_state(state)
            log(f"Client module {module_id} is not approved: request recorded")
            raise ClientError("client_not_approved", "module_id", module_id)
        if database_engine and not grant.get("database_engine") and not grant.get("database_engine_requested"):
            grant["database_engine_requested"] = True
            save_state(state)
        require_ready()
        if provisioner_status() == "invalid":
            raise ClientError("client_provisioner_invalid", "client_provisioning", True)
        run_cleanup(state, token)
        _prune_tokens(state, module_id, token)

        with_db = bool(grant.get("database_engine"))
        groups = [g for g in grant.get("groups", []) if valid_group_id(g)]
        policies = [KV_POLICY_NAME] + ([DB_POLICY_NAME] if with_db else [])
        meta = {"ns8_module_id": module_id, "ns8_module_uuid": module_uuid}
        created_mount = False
        issued = []   # (group or "", wrap_info)
        try:
            if with_db:
                created_mount = _ensure_db_mount(token, module_id)
            issued.append(("", _wrapped_token(token, policies, module_id, meta)))
            for group_id in groups:
                issued.append((group_id, _wrapped_token(
                    token, [GROUP_POLICY_NAME], group_id, dict(meta, ns8_group=group_id))))
        except (urllib.error.URLError, OSError, ValueError) as ex:
            # Nothing partial: revoke what this call issued, remove the new mount
            for _, wrap in issued:
                if wrap.get("wrapped_accessor"):
                    _revoke_accessor(token, wrap["wrapped_accessor"])
            if created_mount:
                try:
                    _disable_db_mount(token, module_id)
                except (urllib.error.URLError, OSError, ValueError):
                    log(f"Cannot remove the new mount {db_mount(module_id)}", "<4>")
            # Never log a response body: it may hold a token
            code = getattr(ex, "code", type(ex).__name__)
            log(f"Cannot create a token for client module {module_id}: {code}", "<3>")
            save_state(state)
            raise ClientError("openbao_request_failed", "module_id", module_id) from None

        now = int(time.time())
        records = state["tokens"].setdefault(module_id, [])
        for group_id, wrap in issued:
            records.append({
                "accessor": wrap.get("wrapped_accessor", ""),
                "module_uuid": module_uuid,
                "database_engine": with_db and not group_id,
                "group": group_id,
                "issued_at": now,
                "expires_at": now + TOKEN_EXPLICIT_MAX_TTL,
            })
        # A client normally holds one or two tokens per scope (while it
        # switches): revoke the oldest beyond the limit
        for scope in {r.get("group", "") for r in records}:
            scoped = [r for r in records if r.get("group", "") == scope]
            for old in scoped[:-MAX_TOKENS_PER_CLIENT]:
                records.remove(old)
                if old.get("accessor") and not _revoke_accessor(token, old["accessor"]):
                    state["cleanup"].setdefault(module_id, {"accessors": [], "delete_data": False})[
                        "accessors"].append(old["accessor"])
        state["pending"].pop(module_id, None)
        save_state(state)

    audit("token_issued", module_id, module_uuid=module_uuid, database_engine=with_db,
          groups=groups, address_type=address_kind)
    main_wrap = issued[0][1]
    return {
        "module_id": module_id,
        "openbao_module_id": os.environ.get("MODULE_ID", ""),
        "address": address,
        "address_type": address_kind,
        "wrapped_token": main_wrap["token"],
        "wrap_ttl": int(main_wrap.get("ttl") or WRAP_TTL),
        "wrap_creation_path": WRAP_CREATION_PATH,
        "token_role": TOKEN_ROLE,
        "token_policies": ["default"] + policies,
        "token_period": TOKEN_PERIOD,
        "token_explicit_max_ttl": TOKEN_EXPLICIT_MAX_TTL,
        "kv_mount": KV_MOUNT,
        "kv_version": 2,
        "kv_prefix": kv_prefix(module_id),
        "database_engine": with_db,
        "database_mount": db_mount(module_id) if with_db else "",
        "groups": [{
            "group_id": group_id,
            "kv_prefix": group_prefix(group_id),
            "wrapped_token": wrap["token"],
            "wrap_ttl": int(wrap.get("ttl") or WRAP_TTL),
            "token_policies": ["default", GROUP_POLICY_NAME],
        } for group_id, wrap in issued[1:]],
    }


def set_access(module_id, allowed, database_engine=False, delete_data=False, groups=()):
    """Approve or revoke a client module. Return the action output."""
    if not valid_module_id(module_id) or module_id == os.environ.get("MODULE_ID"):
        raise ClientError("invalid_module_id", "module_id", module_id)
    groups = clean_groups(groups) if allowed else []
    env = openbao.read_environment()
    token = read_provisioner_token()
    with locked_state() as state:
        if allowed:
            if not enabled(env):
                raise ClientError("client_provisioning_disabled", "client_provisioning", False)
            module_uuid = registered_uuid(module_id)
            if not module_uuid:
                raise ClientError("module_not_found", "module_id", module_id)
            records = state["tokens"].get(module_id, [])
            previous = state["grants"].get(module_id, {})
            # Tokens of a previous instance with the same ID, and tokens
            # whose scope (database engine, group) is no longer approved,
            # are revoked first: an approval never revives them.
            stale = [r for r in records if r.get("module_uuid") != module_uuid
                     or (r.get("database_engine") and not database_engine)
                     or (r.get("group") and r["group"] not in groups)]
            keep = [r for r in records if r not in stale]
            if stale:
                state["tokens"][module_id] = stale
                _queue_cleanup(state, module_id)
                if keep:
                    state["tokens"][module_id] = keep
            if module_id in state["cleanup"] and module_id in run_cleanup(state, token):
                save_state(state)
                raise ClientError("openbao_unavailable", "module_id", module_id)
            same = previous.get("module_uuid") == module_uuid
            state["grants"][module_id] = {
                "module_uuid": module_uuid,
                "database_engine": bool(database_engine),
                "database_engine_requested": False,
                "groups": groups,
                "groups_requested": [],
                "approved_at": int(previous.get("approved_at") or 0) if same else 0,
            }
            if not state["grants"][module_id]["approved_at"]:
                state["grants"][module_id]["approved_at"] = int(time.time())
            state["pending"].pop(module_id, None)
            save_state(state)
            audit("approved", module_id, module_uuid=module_uuid,
                  database_engine=bool(database_engine), groups=groups)
            return {"module_id": module_id, "allowed": True, "database_engine": bool(database_engine),
                    "groups": groups, "cleanup": "none"}

        # Revoke: the approval is removed first, then the tokens (and the
        # data, if chosen) are deleted in OpenBao. If OpenBao is sealed the
        # cleanup is queued and retried by openbao-maintenance.
        state["grants"].pop(module_id, None)
        state["pending"].pop(module_id, None)
        _queue_cleanup(state, module_id, delete_data)
        pending = module_id in run_cleanup(state, token)
        save_state(state)
    audit("revoked", module_id, delete_data=bool(delete_data), cleanup="pending" if pending else "done")
    return {"module_id": module_id, "allowed": False, "database_engine": False, "groups": [],
            "cleanup": "pending" if pending else "done"}


def module_removed(module_id):
    """A module was removed from the cluster: forget its approval and
    revoke its tokens. Its data is kept."""
    if not valid_module_id(module_id) or not os.path.exists(STATE_FILE):
        return False
    with locked_state() as state:
        if not any(module_id in state[key] for key in state):
            return False
        state["grants"].pop(module_id, None)
        state["pending"].pop(module_id, None)
        _queue_cleanup(state, module_id)
        pending = run_cleanup(state)
        save_state(state)
    audit("module_removed", module_id, cleanup="pending" if module_id in pending else "done")
    return True


def disable():
    """Client provisioning was turned off: revoke every client token, then
    the provisioner token. Approvals are kept. Return True when done; if
    OpenBao is sealed the revocation is retried by openbao-maintenance."""
    token = read_provisioner_token()
    if not token:
        return True
    if provisioner_status() == "invalid":
        # Nothing can be revoked with it (for example data restored from
        # before it existed). The queue is kept for a future token; client
        # tokens expire by themselves.
        os.unlink(PROVISIONER_TOKEN_FILE)
        log("The provisioner token is no longer valid: removed", "<4>")
        return True
    with locked_state() as state:
        for module_id in list(state["tokens"]):
            _queue_cleanup(state, module_id)
        pending = run_cleanup(state, token)
        save_state(state)
    if pending:
        log("Client tokens not revoked yet: retried by openbao-maintenance", "<4>")
        return False
    if not _revoke_self(token):
        log("Cannot revoke the provisioner token: retried by openbao-maintenance", "<4>")
        return False
    os.unlink(PROVISIONER_TOKEN_FILE)
    audit("disabled", "", cleanup="done")
    return True


def maintenance():
    """Daily: renew the provisioner token, retry queued cleanups and a
    pending disable."""
    if not read_provisioner_token():
        return
    if not enabled():
        disable()
        return
    try:
        renew_provisioner()
        log("Provisioner token renewed")
    except urllib.error.HTTPError as ex:
        log(f"Cannot renew the provisioner token: HTTP {ex.code}", "<4>")
    except (urllib.error.URLError, OSError) as ex:
        log(f"Cannot renew the provisioner token: {type(ex).__name__}", "<4>")
    if os.path.exists(STATE_FILE):
        with locked_state() as state:
            if state["cleanup"]:
                run_cleanup(state)
                save_state(state)


def _client_entry(state, module_id, current, now):
    """Return the reader-safe record of a client, or None."""
    grant = state["grants"].get(module_id)
    pending = state["pending"].get(module_id)
    if grant and current and grant.get("module_uuid") == current:
        status = "approved"
    elif grant:
        status = "stale"  # reinstalled with the same ID: approve again
    elif pending and current and pending.get("module_uuid") == current:
        status = "pending"
    elif module_id in state["cleanup"]:
        status = "cleanup_pending"
    else:
        return None  # pending request of a module that no longer exists
    records = state["tokens"].get(module_id, [])
    return {
        "module_id": module_id,
        "module_uuid": current or "",
        "installed": bool(current),
        "status": status,
        "database_engine": bool(grant and grant.get("database_engine")),
        "database_engine_requested": bool(
            (grant and grant.get("database_engine_requested"))
            or (status == "pending" and pending.get("database_engine"))),
        "groups": list((grant or {}).get("groups", [])),
        "groups_requested": list((grant or {}).get("groups_requested", []) if grant
                                 else (pending or {}).get("groups", [])),
        "approved_at": int((grant or {}).get("approved_at") or 0),
        "requested_at": int((pending or {}).get("requested_at") or 0),
        "tokens": len([r for r in records if r.get("expires_at", 0) > now]),
        "last_issued_at": max([int(r.get("issued_at", 0)) for r in records] or [0]),
        "cleanup_pending": module_id in state["cleanup"],
    }


def _provisioner_state(env):
    if enabled(env):
        return provisioner_status()
    return "revoke_pending" if read_provisioner_token() else "missing"


def list_clients():
    """Return the reader-safe list of approved and pending clients."""
    env = openbao.read_environment()
    state = load_state()
    ids = sorted(set(state["grants"]) | set(state["pending"]) | set(state["cleanup"]))
    try:
        uuids = registered_uuids(ids)
    except ClientError:
        uuids = {}
    now = int(time.time())
    clients = [c for c in (_client_entry(state, m, uuids.get(m), now) for m in ids) if c]
    groups = sorted({g for c in clients for g in c["groups"]})
    return {
        "client_provisioning": enabled(env),
        "provisioner": _provisioner_state(env),
        "ha_role": openbao.ha_role(env),
        "kv_mount": KV_MOUNT,
        "token_role": TOKEN_ROLE,
        "clients": clients,
        "groups": [{"group_id": g, "kv_prefix": group_prefix(g),
                    "members": [c["module_id"] for c in clients if g in c["groups"]]} for g in groups],
        "modules": installed_modules(),
        "audit": read_audit(),
    }


def client_status(module_id):
    """Reader-safe status of one client, for consumer UIs."""
    env = openbao.read_environment()
    state = load_state()
    current = registered_uuid(module_id) if valid_module_id(module_id) else None
    entry = _client_entry(state, module_id, current, int(time.time())) if current else None
    try:
        address, address_kind = client_address(env)
    except ClientError:
        address, address_kind = "", ""
    status = entry["status"] if entry and entry["status"] in ("approved", "pending", "stale") else "none"
    provisioner = _provisioner_state(env)
    return {
        "module_id": module_id,
        "openbao_module_id": os.environ.get("MODULE_ID", ""),
        "client_provisioning": enabled(env),
        "ready": enabled(env) and provisioner == "valid" and bool(address),
        "status": status,
        "database_engine": bool(entry and entry["database_engine"]),
        "database_engine_requested": bool(entry and entry["database_engine_requested"]),
        "groups": entry["groups"] if entry else [],
        "groups_requested": entry["groups_requested"] if entry else [],
        "address": address,
        "address_type": address_kind,
        "kv_mount": KV_MOUNT,
        "kv_prefix": kv_prefix(module_id) if valid_module_id(module_id) else "",
    }
