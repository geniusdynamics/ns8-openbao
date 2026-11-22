# Client provisioning

Part of the [ns8-openbao documentation](../README.md#documentation).

Other NethServer 8 modules, for example PostgreSQL, KumoMTA or Warpgate,
can get **their own, narrowly scoped OpenBao token** without an
administrator pasting a root or admin token into each module. The feature
is **off by default**. When it is off, modules keep the manual path: the
administrator pastes a token in the module settings.

- [How it works](#how-it-works)
- [Enabling and disabling](#enabling-and-disabling)
- [Approving client modules](#approving-client-modules)
- [Client contract](#client-contract)
- [Security model](#security-model)
- [Limits and follow-ups](#limits-and-follow-ups)

## How it works

```
 client module (role secretsclient)        OpenBao module (openbao1)              OpenBao
 ----------------------------------        -------------------------              -------
 request-client-access / provision-client ─▶ caller = AGENT_TASK_USER
                                            approval bound to MODULE_UUID?
                                            ── no ─▶ pending request, error
                                            ── yes ▶ provisioner token ──────────▶ auth/token/create/ns8-client
                                                                                    entity_alias = <module id>
                                                     ◀───────── wrapping token ──── (X-Vault-Wrap-TTL: 120s)
 ◀─ output: address, wrapped_token, kv_prefix ...
 sys/wrapping/unwrap ───────────────────────────────────────────────────────────▶ token (ns8-client-kv ...)
 read/write ns8-kv/data/modules/<module id>/* with the token, renew it daily
```

| Object | Name | Written by |
|---|---|---|
| KV version 2 mount | `ns8-kv/` | `openbao-client-provisioner create` (administrator token) |
| Client policy, templated | `ns8-client-kv`: `ns8-kv/{data,metadata,delete,undelete,destroy,subkeys}/modules/<alias>/*` | same |
| Group policy, templated | `ns8-client-group`: the same paths under `groups/<alias>/` | same |
| Database policy, templated | `ns8-client-db`: `ns8-db-<alias>/*` | same |
| Token role | `ns8-client`: allowed policies are only the three above, orphan, periodic 24 h, explicit max TTL 30 days | same |
| Provisioner policy and token | `ns8-provisioner`, token in `state/openbao-provisioner.token` (0600) | same |
| Database secrets engine of a client | `ns8-db-<module id>/` | the provisioner, when approved |

`<alias>` is the name of the token's entity alias. The module sets it to
the client module ID (or the group ID for group tokens) when it creates
the token, so one static policy confines every client to its own prefix.

## Enabling and disabling

1. *Settings* → *Client modules* → enable **Client provisioning** and
   save (or `configure-module` with `"client_provisioning": true`).
2. On the node, with an OpenBao administrator token (OpenBao unsealed):

   ```bash
   runagent -m openbao1 openbao-client-provisioner create
   ```

   The token is read from `BAO_TOKEN` or prompted, and never stored. The
   command writes the objects of the table above and creates the
   provisioner token last: a failure leaves no usable credential. Run it
   again to rotate the provisioner token or to update the policies after a
   module update.

   ```bash
   runagent -m openbao1 openbao-client-provisioner status   # valid / missing / invalid / unknown
   ```

Disabling the toggle **revokes every token issued to client modules and
the provisioner token**; approvals are kept. If OpenBao is sealed at that
moment, the revocation is retried by the daily `openbao-maintenance`
timer (the Client modules page shows *Revocation pending*).

With high availability, enable it on the primary instance: members
refuse it. All Raft members share the policies and tokens; requests on a
standby are forwarded to the active node, so the instance answers even
when it is not the active one. Client modules call the instance where
they were approved.

## Approving client modules

Open the **Client modules** page:

- modules that asked for access are listed as *Pending*, with what they
  asked for (database engine, groups);
- **Approve** binds the module ID to its current `MODULE_UUID`. Options:
  - **Database secrets engine**: the module may manage
    `ns8-db-<module id>/` (connections, roles, credentials). The mount is
    enabled by OpenBao's module, never by the client;
  - **Shared groups**: members of a group share `ns8-kv/groups/<group>/`,
    for example the peers of a KumoMTA cluster (DKIM keys) or the members
    of a PostgreSQL cluster (replication secrets). A group ID has lowercase
    letters, digits and dashes and **ends with a letter**, so it can never
    be a module ID. Membership is decided here only: a client can ask, it
    never joins by itself;
- **Change access** narrows or widens the options. Narrowing revokes the
  tokens that hold the removed scope at once;
- **Revoke** removes the approval and revokes the module tokens at once.
  *Also delete the module data* deletes `ns8-kv/modules/<module id>/` and
  the `ns8-db-<module id>/` engine. Group data is kept;
- a module **reinstalled** with the same ID shows as *Reinstalled: approve
  again*: the old approval does not apply to the new installation, and
  approving it revokes the tokens of the old one first;
- when a module is **removed** from the cluster, its approval is dropped
  and its tokens are revoked (`module-removed` event); its data is kept.
  Delete it with *Revoke* and *Also delete the module data*.

Command line equivalents:

```bash
api-cli run module/openbao1/list-clients
api-cli run module/openbao1/set-client-access --data '{"module_id": "postgresql19c1", "allowed": true, "database_engine": true}'
api-cli run module/openbao1/set-client-access --data '{"module_id": "kumomta1", "allowed": true, "groups": ["kumomta-cluster"]}'
api-cli run module/openbao1/set-client-access --data '{"module_id": "kumomta1", "allowed": false, "delete_data": false}'
```

The page also shows the **audit trail** (`state/client-audit.jsonl`, also
in the journal): access requests, approvals, tokens issued, revocations.
It holds module IDs, UUIDs, scopes and times, never tokens or accessors.

## Client contract

### Authorization

The consumer module image declares, in `build-images.sh`:

```bash
--label="org.nethserver.authorizations=... openbao@any:secretsclient"
```

Role **`secretsclient`** grants the actions `provision-client`,
`request-client-access` and `get-client-status` on every OpenBao
instance. NS8 grants it when the consumer is installed, or, for OpenBao
instances updated to this release, at the next module installation or
core update. Do not declare a second `openbao@any:` role: NS8 keeps only
the last role per agent pattern.

Discover OpenBao instances, as ns8-kumomta's `list-openbao-servers` does,
with the module list or the `openbao` service record (cluster network
API):

```python
providers = agent.list_service_providers(agent.redis_connect(use_replica=True), "openbao", "http")
```

Every action identifies the caller by **`AGENT_TASK_USER`**, set by the
NS8 API server: call them from the consumer module with
`agent.tasks.run(agent_id="module/openbao1", action=..., data=...)` (the
default HTTP endpoint authenticates as the module). There is no
`module_id` input: a module cannot act for another one.

### `get-client-status` (reader-safe)

Input: `{}` (a module gets its own status) or `{"module_id": "kumomta1"}`.
Readers can run it too: it returns no secret.

```json
{
  "module_id": "kumomta1",
  "openbao_module_id": "openbao1",
  "client_provisioning": true,
  "ready": true,
  "status": "pending",
  "database_engine": false,
  "database_engine_requested": false,
  "groups": [],
  "groups_requested": ["kumomta-cluster"],
  "address": "http://10.5.4.1:20003",
  "address_type": "vpn",
  "kv_mount": "ns8-kv",
  "kv_prefix": "modules/kumomta1"
}
```

`status`: `none` (never asked, or rejected), `pending`, `approved`,
`stale` (approved for a previous installation with the same module ID).
`ready` is true when provisioning is enabled, the provisioner token is
valid and an address is available. Use it in the consumer UI: offer the
OpenBao option when `client_provisioning` is true; show *Request access*
for `none`, *Waiting for approval* for `pending`, *Approved* for
`approved`; otherwise keep the manual token field.

### `request-client-access`

Input (all optional):

```json
{"database_engine": true, "groups": ["kumomta-cluster"]}
```

Records a pending request shown to the OpenBao administrator, or, for an
approved module, a request for more. It grants nothing. Output: the same
object as `get-client-status`. Errors: `client_provisioning_disabled`,
`invalid_group_id`, `too_many_groups`, `module_not_found`.

### `provision-client`

Input: `{}` or `{"database_engine": true}`. An unapproved module gets the
error `client_not_approved` and its request is recorded as pending (so
calling it directly is also a way to ask). A database engine asked for
but not approved is recorded as requested; the token is issued without it.

Output:

```json
{
  "module_id": "postgresql19c1",
  "openbao_module_id": "openbao1",
  "address": "http://10.5.4.1:20003",
  "address_type": "vpn",
  "wrapped_token": "s.<wrapping token>",
  "wrap_ttl": 120,
  "wrap_creation_path": "auth/token/create/ns8-client",
  "token_role": "ns8-client",
  "token_policies": ["default", "ns8-client-kv", "ns8-client-db"],
  "token_period": 86400,
  "token_explicit_max_ttl": 2592000,
  "kv_mount": "ns8-kv",
  "kv_version": 2,
  "kv_prefix": "modules/postgresql19c1",
  "database_engine": true,
  "database_mount": "ns8-db-postgresql19c1",
  "groups": [
    {
      "group_id": "pg-cluster",
      "kv_prefix": "groups/pg-cluster",
      "wrapped_token": "s.<wrapping token>",
      "wrap_ttl": 120,
      "token_policies": ["default", "ns8-client-group"]
    }
  ]
}
```

- `address`: the cluster network API of this instance
  (`module/<openbao>/srv/http/openbao`, plain HTTP inside the WireGuard
  VPN) when `vpn_api` is enabled, otherwise `https://<host name>` through
  Traefik (`address_type` `public`). Enable `vpn_api` for clients on other
  nodes that should not use the public name.
- One wrapped token for the module prefix, plus one per approved group.

Errors (validation failures, `[{"field", "parameter", "value", "error"}]`):

| error | meaning | what the client does |
|---|---|---|
| `client_not_authorized` | the caller is not a module (administrator, direct Redis task) | call it as the module |
| `client_provisioning_disabled` | the toggle is off | keep the manual token path |
| `client_provisioner_missing` / `client_provisioner_invalid` | the administrator has not run `openbao-client-provisioner create` | show "OpenBao provisioning not ready" |
| `client_not_approved` | no approval for this installation; request recorded | show "waiting for approval", retry later |
| `openbao_unavailable` (value `sealed`, `down`, `uninitialized`) | OpenBao cannot answer; nothing changed | retry later |
| `openbao_request_failed` | OpenBao refused the request; whatever this call created was undone | retry later, report |
| `no_address` | neither the cluster network API nor a public route | ask the administrator |
| `cluster_unavailable` | the cluster Redis cannot be read | retry later |

### Client steps

Run them in the consumer's action, right after `provision-client`
returns, and keep the token in a **0600 file under the module state
directory**, never in `agent.set_env()` (Redis) or in an action output.

1. **Check the wrapping token** (unauthenticated), so a substituted token
   is detected:

   ```
   POST {address}/v1/sys/wrapping/lookup   {"token": "<wrapped_token>"}
   → data.creation_path must equal wrap_creation_path
   ```

2. **Unwrap** it at once (within `wrap_ttl` seconds; it works once):

   ```
   POST {address}/v1/sys/wrapping/unwrap   X-Vault-Token: <wrapped_token>
   → auth.client_token, auth.accessor, auth.policies, auth.lease_duration
   ```

   If the unwrap fails with 400 although the call is fresh, somebody else
   unwrapped it first: log an error, ask the administrator to revoke and
   re-approve the module, and provision again.

3. **Store** `auth.client_token` in a 0600 file (for example
   `state/secrets/openbao.token`). Do the same for each group token.

4. **Use** it with `X-Vault-Token` on the KV v2 API:

   ```
   POST {address}/v1/ns8-kv/data/modules/<module id>/<key>   {"data": {...}}
   GET  {address}/v1/ns8-kv/data/modules/<module id>/<key>
   LIST {address}/v1/ns8-kv/metadata/modules/<module id>/
   POST {address}/v1/ns8-kv/data/groups/<group>/<key>        (with the group token)
   ```

   Keys live **under** the prefix (`modules/<module id>/<key>`); the
   prefix itself is not writable. With the database engine approved,
   configure `ns8-db-<module id>/config/<name>`,
   `ns8-db-<module id>/roles/<role>` and read
   `ns8-db-<module id>/creds/<role>`.

5. **Renew** every token at least daily (period 24 h), for example every
   8–12 hours from a timer:

   ```
   POST {address}/v1/auth/token/renew-self   X-Vault-Token: <token>   {}
   ```

   A token not renewed for 24 hours expires.

6. **Provision again** before the explicit maximum TTL (30 days from
   issue), for example when `renew-self` returns a `lease_duration`
   shorter than the period, after ~25 days, or on any 403 from
   `lookup-self`. A new call issues new tokens and checks the approval
   again; switch to the new token, then stop using the old one, which
   expires within 24 hours (or call `auth/token/revoke-self` with it).
   Each call issues new tokens: do not call it in a loop; a module keeps
   at most 5 live tokens per scope and older ones are revoked.

7. **Fallback**: on `client_provisioning_disabled` or 403 after a
   revocation, drop the stored token and fall back to the manual token
   path of the consumer.

Python sketch (no external package):

```python
import json, os, urllib.request
import agent, agent.tasks

def bao(address, path, method="GET", token="", data=None):
    req = urllib.request.Request(f"{address}/v1/{path}", method=method,
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={"X-Vault-Token": token} if token else {})
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read()
        return json.loads(body) if body else {}

ret = agent.tasks.run(agent_id="module/openbao1", action="provision-client", data={})
if ret["exit_code"] != 0:
    raise SystemExit(ret["output"])     # e.g. client_not_approved
out = ret["output"]
info = bao(out["address"], "sys/wrapping/lookup", "POST", data={"token": out["wrapped_token"]})
assert info["data"]["creation_path"] == out["wrap_creation_path"]
token = bao(out["address"], "sys/wrapping/unwrap", "POST", token=out["wrapped_token"])["auth"]["client_token"]
os.makedirs("secrets", mode=0o700, exist_ok=True)
fd = os.open("secrets/openbao.token", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, "w") as f:
    f.write(token)
```

Back up the token file with the consumer's `state-include.conf` only if
losing it matters: a restored token may have expired; provisioning again
is always possible while the module is approved.

## Security model

**Identity from the platform.** The caller is `AGENT_TASK_USER`
(`module/<id>`), set by the NS8 API server from the authenticated module
credentials. Tasks queued directly in Redis, administrators and other
users are refused. Paths, mounts and aliases are derived from that ID
only (validated against the NS8 module ID format: no `*`, `+`, `/` or
`{` reaches a policy).

**Two gates.** Any module image can declare `openbao@any:secretsclient`,
so the role alone is not enough: every module must also be approved by
the OpenBao administrator, and the approval is bound to the module ID
**and** its `MODULE_UUID` (read from the cluster leader at every call). A
module removed and installed again with the same ID gets a new UUID and
is not trusted until approved again; approving it revokes the old
installation's tokens first.

**No privilege escalation through the provisioner.** The first design
idea was AppRole roles and per-client policies written by a provisioner
token. Anyone who can write policies, or AppRole roles (whose
`token_policies` accept any policy name), can grant themselves any
policy: such a provisioner would be root-equivalent. Here the
provisioner can only create tokens of the `ns8-client` token role, whose
`allowed_policies` are fixed to the three templated client policies.
The policies and the role are written once with the administrator
token, which is never stored. A leaked provisioner token can reach client
data (by naming another alias) and revoke tokens whose accessor it knows,
but cannot read other OpenBao secrets, write policies, enable auth
methods or create privileged tokens.

**Least privilege per client.** One templated policy confines each
client token to `ns8-kv/*/modules/<module id>/*`. The database engine
policy reaches only `ns8-db-<module id>/*`, granted separately, and only
inside a mount the module enabled. Group tokens reach only their group
prefix, and group membership is granted by the administrator only. Tokens
are orphans with the `default` policy (lookup, renew, revoke self).

**Why tokens rather than AppRole.** Besides the escalation issue above:
AppRole's long-lived `secret_id` would be a bearer credential on the
client node anyway, equivalent to a token; renewing through NS8 every 30
days re-checks the approval; and revocation is direct (by accessor) and
immediate. The client side is simpler: unwrap, renew, re-provision.

**Nothing usable in Redis.** NS8 keeps action outputs in Redis for hours,
readable by cluster administrators. The output holds only response
wrapping tokens: single use, valid for 120 seconds, and checked by the
client through `creation_path`. An old task result holds a used or
expired wrapper. If somebody reads Redis within those seconds and unwraps
first, the legitimate client's unwrap fails, which is detected and
reported; the token is still confined to the client's own prefix. The
token accessors are kept in `state/client-access.json` (0600) on the node,
never in an output.

**Node files.** `openbao-provisioner.token` and `client-access.json` are
0600 files in the module state, included in backups (the Restic
repository is encrypted) and copied by a clone. The provisioner token is
periodic (7 days), renewed daily by `openbao-maintenance`.

**Bound CIDRs not used.** The API listener is published by rootless
Podman (slirp4netns port forwarding), which does not preserve the client
source address, and Traefik requests come through the node: binding tokens
to the VPN network would reject legitimate clients or not restrict
anything. Use `public_access: false` with `vpn_api` to keep OpenBao off
the public network.

**Failures.** Every action checks that OpenBao is initialized and
unsealed before changing anything. A failed provisioning revokes the
tokens it issued and removes a database mount it created. A revocation
always removes the approval at once; if OpenBao is sealed, the token
revocation (and data deletion) is queued and retried by
`openbao-maintenance`, and the page shows it.

## Limits and follow-ups

- Group data is never deleted by the module: delete
  `ns8-kv/metadata/groups/<group>/...` with an administrator token.
- Entity aliases and entities created for client and group tokens are
  kept by OpenBao after a revocation; they carry no permission.
- Revoking a token also revokes the leases it created, such as dynamic
  database credentials read with it.
- The audit trail is local to the instance and keeps the last 500
  entries; enable the OpenBao audit log for a complete record.
