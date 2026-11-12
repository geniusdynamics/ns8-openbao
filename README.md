# ns8-openbao

[OpenBao](https://openbao.org/) for [NethServer 8](https://github.com/NethServer/ns8-core).
OpenBao is an open source, community-driven fork of HashiCorp Vault: it
stores and controls access to tokens, passwords, certificates and
encryption keys, and provides PKI, dynamic secrets and encryption as a
service.

The module runs OpenBao as a rootless container with:

- **Raft integrated storage** in the `openbao-data` volume
- the API and web UI published by Traefik on a dedicated host name, with
  optional Let's Encrypt certificate
- **manual (Shamir) or automatic (static key) unseal**
- optional **audit log** to the systemd journal
- **directory login** with a NethServer user domain (OpenLDAP or Active
  Directory), optionally configured automatically at initialization
- **email notifications** through the cluster SMTP smarthost, and
  **alerts** in the NethServer metrics and alert system
- backup, restore and clone support

## Table of contents

- [Install](#install)
- [Configure](#configure)
- [First-time setup](#first-time-setup)
- [Unseal modes](#unseal-modes)
- [Directory login (LDAP / Active Directory)](#directory-login-ldap--active-directory)
- [Starter kits](#starter-kits)
- [Applying settings that need a token](#applying-settings-that-need-a-token)
- [Notifications and alerts](#notifications-and-alerts)
- [Module token, snapshots and root tokens](#module-token-snapshots-and-root-tokens)
- [Cluster network API](#cluster-network-api)
- [Snapshots and restore](#snapshots-and-restore)
- [Prometheus metrics](#prometheus-metrics)
- [Not implemented on purpose](#not-implemented-on-purpose)
- [High availability](#high-availability)
- [Get the configuration and state](#get-the-configuration-and-state)
- [Backup and restore](#backup-and-restore)
- [Update](#update)
- [Uninstall](#uninstall)
- [Security notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Testing](#testing)
- [UI translation](#ui-translation)

## Install

Instantiate the module with:

```bash
add-module ghcr.io/geniusdynamics/openbao:latest 1
```

The output of the command returns the instance name. Output example:

```json
{"module_id": "openbao1", "image_name": "openbao", "image_url": "ghcr.io/geniusdynamics/openbao:latest"}
```

## Configure

Let's assume that the OpenBao instance is named `openbao1`. Configure it
from the *Settings* page of the application, or with `configure-module`:

```bash
api-cli run configure-module --agent module/openbao1 --data - <<EOF
{
  "host": "vault.example.org",
  "http2https": true,
  "lets_encrypt": true,
  "unseal_mode": "manual",
  "log_level": "info",
  "audit_log": true,
  "user_domain": "ad.example.org",
  "ldap_admin_group": "domain admins",
  "auto_initialize": false,
  "notify_recipients": ["security@example.org"],
  "ip_allowlist": ["192.168.1.0/24"],
  "ldap_group_policies": [{"group": "Developers", "policy": "ns8-secrets-rw"}],
  "starter_kits": ["kv", "pki"]
}
EOF
```

Parameters:

- `host` (required): fully qualified host name of the OpenBao API and web UI
- `http2https`: redirect HTTP to HTTPS. Default `true`
- `lets_encrypt`: request a Let's Encrypt certificate for `host`
- `unseal_mode`: `manual` or `auto`, see [Unseal modes](#unseal-modes).
  Default `manual`. It can be changed only before OpenBao is initialized
- `log_level`: `trace`, `debug`, `info`, `warn` or `error`. Default `info`
- `audit_log`: send the OpenBao audit log to the systemd journal. Default `false`
- `user_domain`: NethServer user domain for directory login; `""` disables
  it. See [Directory login](#directory-login-ldap--active-directory)
- `ldap_admin_group`: group of `user_domain` whose members get full access
  to OpenBao. Required with `user_domain`; it must exist in the domain
- `auto_initialize`: with `unseal_mode` `auto` and a `user_domain`, let
  OpenBao initialize itself with directory login already configured
- `notify_recipients`: email addresses notified when OpenBao is down or
  sealed. `[]` disables them. See [Notifications](#notifications-and-alerts)

- `ip_allowlist`: client IP addresses or networks (CIDR) allowed to reach
  the API and web UI through Traefik. `[]` (default) allows everybody.
  Applications that read secrets through the host name must be listed too
- `ldap_group_policies`: more directory groups mapped to OpenBao policies,
  see [Group policies](#group-policies)
- `starter_kits`: components prepared at initialization, any of `kv`
  (default), `pki`, `approle`; see [Starter kits](#starter-kits)
- `vpn_api`: also publish the API on the cluster VPN, see
  [Cluster network API](#cluster-network-api). Default `false`
- `public_access`: publish the API and web UI through Traefik on `host`.
  `false` makes OpenBao reachable only on the cluster network API (requires
  `vpn_api`). Default `true`
- `snapshot_keep`: daily Raft snapshots kept on the node, see
  [Snapshots and restore](#snapshots-and-restore). Default `0` (disabled)
- `transit_address`, `transit_mount` (default `transit`), `transit_key`,
  `transit_tls_skip_verify`: settings of the `transit` unseal mode, see
  [Unseal modes](#unseal-modes)

Omitted optional parameters keep their current value.

The command starts OpenBao and configures the Traefik route. Clients reach
the API at `https://vault.example.org` (for example
`export BAO_ADDR=https://vault.example.org`) and the web UI at
`https://vault.example.org/ui/`.

Changing `log_level` or `audit_log` reloads OpenBao in place. Changing
`host` or `unseal_mode` restarts it: with manual unseal it must be
unsealed again.

## First-time setup

A new instance starts **uninitialized**: OpenBao has no data, no keys and
no users yet. *Initializing* it creates the encryption keys and the first
credentials. Which credentials you get, and where they appear, depends on
two settings chosen in *Settings* **before** initializing: the unseal mode
and directory login.

### Words used below

- **Root token**: a token with unlimited power, like the root password of
  OpenBao. Use it for the first configuration only, then revoke it.
- **Unseal keys** (manual unseal only): the master key split into shares,
  for example 5 shares of which any 3 unlock OpenBao. They are needed
  after **every** restart, update or reboot.
- **Recovery keys** (automatic unseal only): shares that never unseal
  OpenBao, but authorize sensitive operations such as generating a new root
  token when no administrator can log in.

OpenBao shows the root token and keys **only once** and cannot recover
them. The module never sees or stores them: NethServer keeps action
inputs and outputs in Redis, readable by other modules, so they are
handled only by the OpenBao web UI or CLI, over HTTPS.

### Setup wizard

The easiest way: open the application. While OpenBao is not configured,
the *Status* page starts the **setup wizard**, which asks for the web
address, the unseal mode (explaining the trade-offs), directory login and
email notifications, shows a summary, applies everything at once, and
ends with the exact next steps for the setup you chose (one of A-D
below), with buttons to open OpenBao or its LDAP login. It can be run
again at any time with the *Setup wizard* button of the *Status* page.
Advanced users can cancel it and use the *Settings* page, which has every
option.

### Choose your setup

| Setup | Unseal mode | Directory login | First credentials |
|---|---|---|---|
| [A](#a-manual-unseal-without-directory-login) | manual | no | unseal keys + root token |
| [B](#b-automatic-unseal-without-directory-login) | automatic | no | recovery keys + root token |
| [C](#c-automatic-unseal-with-automatic-directory-login) | automatic | yes, `auto_initialize` | none: domain admins log in |
| [D](#d-adding-directory-login-later) | any | yes, after initialization | root token of A or B |

Start in every case from the setup wizard, or from the *Settings* page:
set the host name, choose the unseal mode and, for C, the user domain and
the administrators group. Then follow the steps below.

### A. Manual unseal, without directory login

1. On the *Status* page click **Open OpenBao**. The web UI shows the
   initialization page.
2. Choose the number of key shares and the threshold (for example 5 and
   3) and initialize.
3. **Download the keys** (JSON file) or copy the root token and every
   unseal key. Hand the key shares to different trusted people; do not
   keep them together with the root token.
4. Continue to unseal: enter key shares until the threshold is reached.
5. Sign in with the **Token** method, using the root token.
6. Create real administrator access, for example a `userpass` user with
   an admin policy, or set up [directory login](#d-adding-directory-login-later).
7. Revoke the root token: `bao token revoke -self`.

The same with the CLI, from any computer with the `bao` client:

```bash
export BAO_ADDR=https://vault.example.org
bao operator init -key-shares=5 -key-threshold=3   # prints 5 unseal keys and the root token
bao operator unseal                                # repeat 3 times, one key each time
bao login                                          # paste the root token
```

**After every restart** (update, reboot, settings change of host name)
OpenBao is sealed again. The *Status* page shows *Sealed* with the
progress, and notifications are sent if configured. Open the web UI and
enter the threshold number of unseal keys, or run `bao operator unseal`.

### B. Automatic unseal, without directory login

1. On the *Status* page click **Open OpenBao** and initialize. There is no
   unseal step: OpenBao unseals itself with the key stored on the node.
2. Save the **root token** and the **recovery keys**.
3. Sign in with the root token, create administrator access (as in step 6
   of A) and revoke the root token.

CLI: `bao operator init -recovery-shares=5 -recovery-threshold=3`, then
`bao login`.

### C. Automatic unseal with automatic directory login

In *Settings* choose **Automatic unseal**, a **user domain**, an
**administrators group** and check **Initialize OpenBao automatically
with directory login**. On save:

1. OpenBao initializes itself at once. It enables LDAP login on the user
   domain, grants the `ns8-admin` policy (full access) to the
   administrators group and creates a `secret/` key/value store.
2. No root token and no recovery keys exist. The *Status* page shows
   *Unsealed*.
3. Click **Log in with directory account** on the *Status* page: the web
   UI opens with the LDAP method selected. Log in with the user name and
   password of a member of the administrators group.
4. Generate recovery keys and store them safely: without them a new root
   token can never be generated if directory login breaks.

   ```bash
   export BAO_ADDR=https://vault.example.org
   bao login -method=ldap username=alice
   bao operator rotate-keys -init -key-shares=5 -key-threshold=3 -target=recovery
   ```

### D. Adding directory login later

For an instance initialized with A or B, or when the user domain or group
changes later:

1. In *Settings* choose the user domain and the administrators group, and
   save.
2. On the node, run the command shown in *Settings* and paste a token
   with administrator rights (the root token works):

   ```bash
   runagent -m openbao1 openbao-apply-config
   ```

3. Members of the administrators group can now use **Log in with
   directory account**. You can revoke the root token.

### Lost credentials

- **Root token lost**: generate a new one with the unseal keys (A) or the
  recovery keys (B, or C after step 4):

  ```bash
  bao operator generate-root -init            # prints a nonce and an OTP
  bao operator generate-root                  # repeat with each key share
  bao operator generate-root -decode=<encoded token> -otp=<OTP>
  ```

- **Unseal keys lost** (manual unseal): if fewer than the threshold remain,
  the data cannot be decrypted by anybody. Keep copies in separate safe
  places.
- **Directory login broken after automatic initialization** (C): the
  self-initialization also creates a **break-glass administrator token**
  (`ns8-admin` policy), so a failed or wrong directory setup can never lock
  everybody out. It never leaves the node and expires 32 days after the
  initialization. Use it to repair the configuration or to generate
  recovery keys, then revoke it:

  ```bash
  runagent -m openbao1 openbao-breakglass-token   # prints the token
  export BAO_ADDR=https://vault.example.org BAO_TOKEN=<token>
  bao operator rotate-keys -init -key-shares=5 -key-threshold=3 -target=recovery
  bao token revoke -self
  ```

  Only the administrator policy and this token are mandatory steps of the
  self-initialization; directory login and the key/value store are allowed
  to fail, and the failure is logged.

## Unseal modes

| | `manual` (default) | `auto` | `transit` |
|---|---|---|---|
| Seal | Shamir key shares | `static` seal with a 32-byte key | Transit engine of an external OpenBao or Vault |
| After restart, update or reboot | sealed: an operator enters the unseal keys | unseals itself | unseals itself while the external server is reachable |
| Key storage | keys held by operators only | key generated on the node, `state/openbao-seal.key` (mode 0600), included in backups | key held by the external server; its token in `state/openbao-transit.token` (mode 0600), included in backups |
| Backup consistency | live copy, or Raft snapshot with the module token | OpenBao stopped for a few seconds for a consistent copy | live copy, or Raft snapshot with the module token |
| Protection against disk or backup theft | yes | no: whoever holds the key file and the data can decrypt the secrets | yes, if the external server is protected: revoke the token to make stolen copies useless |

For `transit`, prepare the external server (a Transit key, and a token
allowed to `update` `<mount>/encrypt/<key>` and `<mount>/decrypt/<key>`),
store the token on the node, then select the mode in *Settings*:

```bash
runagent -m openbao1 openbao-transit-token
```

The token is never entered in the web UI, so it never passes through
Redis; OpenBao renews it automatically. Another OpenBao instance of the
cluster can be the Transit server, reached through its
[cluster network API](#cluster-network-api).

Choose `manual` when the stored secrets are sensitive enough to justify
an operator unsealing OpenBao after every restart. Choose `auto` when
availability matters more and the node disk and backup repository are
trusted.

The seal type is written into the storage at initialization time, so
`unseal_mode` is locked in *Settings* once OpenBao is initialized. To
change it afterwards, run a [seal migration](https://openbao.org/docs/concepts/seal/#seal-migration)
on the node. Take a backup first; the command also keeps a copy of the
storage (`state/openbao-premigration-*.tar`):

```bash
runagent -m openbao1 openbao-seal-migrate start auto     # or: manual, transit --transit-address URL --transit-key KEY
export BAO_ADDR=https://vault.example.org
bao operator unseal -migrate                             # once per key, until the threshold
runagent -m openbao1 openbao-seal-migrate finish
```

Provide the **unseal keys** when leaving manual unseal (they become the
recovery keys), or the **recovery keys** when leaving automatic or Transit
unseal (they become the unseal keys when moving to manual). The keys go
straight to OpenBao. `openbao-seal-migrate status` and `abort` are
available until OpenBao has applied the migration. OpenBao is unavailable
for the duration of the migration.

**Never delete or replace `state/openbao-seal.key`** of an instance using
automatic unseal: without it the data cannot be decrypted.

## Directory login (LDAP / Active Directory)

Choose a user domain of the cluster (internal OpenLDAP or Samba Active
Directory, or an external LDAP/AD domain) and an administrators group in
*Settings*. The module binds the domain, so it appears in the cluster
*Domains and users* page. OpenBao is then configured with:

- the `ldap` auth method, connected to the node ldapproxy: it relays to
  the domain servers with TLS and fails over between them. User and group
  searches mirror the NethServer core: `sAMAccountName`/`member` for Active
  Directory, `uid`/`posixGroup` `memberUid` for OpenLDAP
- the `ns8-admin` policy, with full access, mapped to the administrators
  group

### Default NethServer domain accounts

Both NethServer account providers create a builtin group named
**`domain admins`**, so it is the natural administrators group, and the
*Settings* page and the setup wizard propose it:

- **Internal OpenLDAP**: the *admuser* given when the domain is created
  (for example `admin`) is created as a member of `domain admins`.
- **Samba Active Directory**: with the user name `administrator`, the
  builtin Samba administrator is used; with any other name, that user is
  created, added to `domain admins`, and the builtin `administrator` is
  disabled.

There is no default password: it is the one typed when the domain was
created. An external LDAP/AD domain has its own groups (for example
`Domain Admins` in Active Directory). OpenBao matches group names without
regard to case.

Users log in with their domain account:

```bash
bao login -method=ldap username=alice
```

or with the **Log in with directory account** button of the *Status*
page, which opens the web UI with the LDAP method selected
(`https://<host>/ui/vault/auth?with=ldap%2F`). Create further policies and
map other groups with `auth/ldap/groups/<group>`.

Since OpenBao 2.7 the LDAP auth method is not built into OpenBao: it is
an external plugin from the [openbao-plugins](https://github.com/openbao/openbao-plugins)
project. The module lists its pinned image
(`ghcr.io/openbao/openbao-plugin-auth-ldap`) among the module images, so
the node pulls it at install and update time, and OpenBao never downloads
anything at startup. Before each start the binary is copied from the image
into `state/openbao-plugins/` and declared in the server configuration
with its version and SHA-256 checksum.

How OpenBao gets this configuration depends on its state, see
[First-time setup](#first-time-setup):

- **Automatic initialization** ([setup C](#c-automatic-unseal-with-automatic-directory-login)):
  requires automatic unseal and an uninitialized server. The module checks
  that the group exists before saving, because a wrong group would leave a
  self-initialized OpenBao without administrators.
- **`openbao-apply-config`** ([setup D](#d-adding-directory-login-later)):
  for an initialized server, or with manual unseal. The module cannot
  change OpenBao without an administrator token, and tokens must never
  pass through module actions: the command prompts for a token on the node
  (or reads `BAO_TOKEN`), applies the configuration and forgets the token.

### Group policies

Besides the administrators group (`ns8-admin`), map other directory
groups to policies in *Settings*, *Group policies*. The module creates
these built-in policies:

| Policy | Access |
|---|---|
| `ns8-admin` | everything |
| `ns8-secrets-rw` | read and write the `secret/` key/value store |
| `ns8-secrets-ro` | read the `secret/` key/value store |
| `ns8-pki-issuer` | issue certificates with the `pki/roles/ns8-server` role |

The name of a policy created in OpenBao can be typed too. A group may
appear in several rows to get several policies.

> **Note:** when several policies of a token match a path, OpenBao applies
> only the most specific path; it does not add their capabilities up
> (capabilities are merged only for identical paths). `ns8-admin` repeats
> the paths of the other built-in policies, so giving administrators a
> built-in policy too never narrows their access. A custom policy with a
> narrower path, mapped to a group the administrators belong to, does
> narrow it: an administrator would then, for example, only read under
> that path.

Mappings need an administrator token to be written, so they are applied
by the self-initialization or, on an initialized server, by
`openbao-apply-config`. Run it again after changing them: it also removes
the mappings it created before and that are no longer configured, and
leaves mappings created by hand untouched.

OpenBao keeps its own copy of the LDAP connection settings. If the domain
bind credentials or servers change, the module logs a warning, sends a
notification and asks to run `openbao-apply-config` again.

## Starter kits

Choose in *Settings* (or in the wizard, for automatic initialization)
what OpenBao should be prepared with:

| Kit | Prepares |
|---|---|
| `kv` (default) | key/value version 2 store at `secret/` |
| `pki` | internal root CA at `pki/` (EC P-384, 10 years), issuing and CRL URLs on the host name, and the `ns8-server` role (any name, server and client usage, 30 days, maximum 90) |
| `approle` | the AppRole auth method at `approle/`, for applications and scripts |

Kits are applied by the self-initialization, or on an initialized server
by `openbao-apply-config`, which skips what already exists: an enabled
mount or an existing PKI issuer is never changed. Unchecking a kit does
not remove anything.

## Applying settings that need a token

The module never holds an OpenBao administrator token. Directory login,
group policies and starter kits are written by the self-initialization
or, afterwards, by this node command, which reads a token from the
terminal (or from `BAO_TOKEN`), applies everything idempotently and
forgets the token:

```bash
runagent -m openbao1 openbao-apply-config
```

`openbao-setup-ldap`, the command name of release 1.0.0, still works.

## Notifications and alerts

OpenBao itself does not send email. The module adds two notification
paths, both through the cluster SMTP smarthost (configured in the cluster
*Settings*, SMTP smarthost page):

- **Application recipients** (`notify_recipients`): every 5 minutes
  `openbao-notify.timer` checks OpenBao and sends one email when it is
  down or sealed for two checks in a row, and one when it recovers. A short
  planned stop, like the backup copy with automatic unseal, does not
  notify. Use *Send test email* in *Settings*, or the `send-test-email`
  action, to verify delivery.
- **Cluster alerts**: the module exports `openbao_up`, `openbao_initialized`,
  `openbao_sealed`, `openbao_build_info` and `openbao_auto_unseal`
  metrics (core 3.24 or later) and publishes alert rules to the NethServer
  metrics module: `OpenbaoDown` and `OpenbaoSealed` (critical, after 10
  minutes) and `OpenbaoNotInitialized` (warning, after 24 hours). They
  appear in the cluster alert list and are mailed to the cluster alert
  recipients.

## Module token, snapshots and root tokens

The module can hold a **module token**: a periodic OpenBao token with the
narrow `ns8-module` policy, stored on the node (`state/openbao-module.token`,
mode 0600), never returned by any action. It can take Raft snapshots and
read token metadata (not tokens, not secrets); it cannot change the
configuration or revoke anything. It is renewed daily by
`openbao-maintenance.timer`. With it:

- every backup includes `openbao.snap`, a **consistent Raft snapshot**
  taken without stopping OpenBao (in all unseal modes)
- the *Status* page warns when a **root token** is still active

Self-initialization creates it automatically. For other instances, create
it once with an administrator token:

```bash
runagent -m openbao1 openbao-module-token create
runagent -m openbao1 openbao-module-token status     # valid / missing / invalid
runagent -m openbao1 openbao-module-token revoke
```

List and revoke root tokens once other administrator access works:

```bash
runagent -m openbao1 openbao-root-tokens            # list
runagent -m openbao1 openbao-root-tokens --revoke   # revoke, after confirmation
```

A snapshot can also be taken at any time with
`runagent -m openbao1 openbao-snapshot /path/file.snap`.

## Snapshots and restore

Besides backups, the module can keep **daily Raft snapshots** on the node
(`snapshot_keep`, *Settings*, *Snapshots*), to recover quickly from a
deleted secret or a wrong change. They need the module token, are taken
by `openbao-maintenance.timer`, are stored in `state/snapshots/` and are
not part of backups. *Settings* lists them.

Restoring replaces **all** OpenBao data and needs an administrator token,
so it runs on the node:

```bash
runagent -m openbao1 openbao-snapshot-restore openbao-20261112-031500.snap
```

A snapshot of another OpenBao, for example the `openbao.snap` of a backup
of a different instance, needs `--force`; OpenBao then seals itself and
needs the unseal or recovery keys of the OpenBao that produced it.

## Cluster network API

To make OpenBao reachable **only** from the cluster, disable
`public_access` (it requires `vpn_api`): the Traefik route is removed and
`api_addr` points to the cluster network address. Clients using the host
name stop working, so this is opt-in.


With `vpn_api` enabled, the OpenBao API is also published on the third
module TCP port, bound to the node cluster VPN address
(`http://10.5.4.x:<port>`), for NethServer modules and services on other
nodes. The traffic is encrypted by the cluster VPN (WireGuard). The
public route through Traefik keeps working.

The endpoint is published as an NS8 service provider, and the
`openbao-changed` event is sent when it changes:

```python
rdb = agent.redis_connect(use_replica=True)
providers = agent.list_service_providers(rdb, "openbao", "http")
url = providers[0]["url"]   # e.g. http://10.5.4.1:20003
```

Instances installed with fewer TCP ports allocate the extra port when the
option is first enabled (role `node:portsadm`).

## Prometheus metrics

OpenBao [telemetry](https://openbao.org/docs/configuration/telemetry/) is
published for the NethServer **Metrics** module (Prometheus and Grafana),
which can run on any node of the cluster:

- a second OpenBao listener serves only `/v1/sys/metrics`, without
  authentication. It is published on the second TCP port of the module,
  bound to the node cluster VPN address (for example `10.5.4.1`): it is
  reachable by the cluster nodes only, never through Traefik. The public
  listener refuses metrics requests
- `configure-module` publishes the scrape target in
  `module/<module_id>/metrics_targets`, with the `/v1/sys/metrics` path and
  the `format=prometheus` parameter, and emits `metrics-target-changed`.
  If the node VPN address changes, the target and the listener follow it
- metric names keep the OpenBao default `vault_` prefix, for example
  `vault_core_unsealed`, `vault_core_handle_request_count` or
  `vault_token_count`, so dashboards made for Vault work as they are. They
  carry the `module_id="openbao1"` label added by the Metrics module

Query them from Grafana (enable it in the Metrics module settings), or test
the endpoint from a cluster node:

```bash
curl "http://10.5.4.1:<second port>/v1/sys/metrics?format=prometheus"
```

The second port is in the module `TCP_PORTS` environment variable
(`runagent -m openbao1 printenv TCP_PORTS`). Metrics are served only while
OpenBao is initialized and unsealed; the module own `openbao_up`,
`openbao_sealed` and `openbao_initialized` metrics cover the other states.

## Not implemented on purpose

Some convenient features would require sending secrets through NethServer
actions. Action inputs and outputs are kept in Redis for hours and are
readable by other modules, so these are left out; use the safe
alternative:

| Not implemented | Why | Safe alternative |
|---|---|---|
| Unseal from the NethServer UI (pasting key shares) | key shares would be stored in Redis | *Status*, **Open OpenBao**: the OpenBao web UI unseals over HTTPS; or `bao operator unseal` |
| Initialize from the NethServer UI | unseal keys and the root token would be stored in Redis | the OpenBao web UI or `bao operator init` (setups A, B), or self-initialization (setup C) |
| Revoke root tokens from the NethServer UI | needs an administrator token in an action | `openbao-root-tokens --revoke` on the node, or `bao token revoke -self` |
| Enter the Transit token in the NethServer UI | the token would be stored in Redis | `openbao-transit-token` on the node |

## High availability

Each instance is a single-node Raft cluster. Joining instances into one
highly available cluster is designed but not implemented yet, because it
needs testing on a real multi-node cluster: see
[docs/high-availability.md](docs/high-availability.md).

## Get the configuration and state

```bash
api-cli run get-configuration --agent module/openbao1
api-cli run get-openbao-status --agent module/openbao1
```

`get-openbao-status` returns whether the service is running, and whether
OpenBao is initialized and sealed, with the unseal progress, the version
and the web UI URL.

## Backup and restore

Configure a backup of the instance from the cluster *Backup* page. The
backup contains:

- `volumes/openbao-data`: the Raft storage, encrypted by OpenBao
- `state/openbao-data.tar`: with automatic unseal only, a consistent copy
  of the storage. To take it, `module-dump-state` stops OpenBao for a few
  seconds and starts it again; it unseals itself
- `state/openbao-seal.key`: the static unseal key, with automatic unseal

With manual unseal OpenBao cannot be stopped during the backup (it would
stay sealed), so the storage is copied while running. For guaranteed
consistency, also schedule a Raft snapshot with a token allowed to read
`sys/storage/raft/snapshot`:

```bash
bao operator raft snapshot save openbao-$(date +%F).snap
```

On restore, the instance comes back with the same data and seal. With
manual unseal it must be unsealed with the **original** unseal keys. With
automatic unseal it unseals itself. Let's Encrypt is not requested during
restore or clone, because the host name may not point to the new node yet:
enable it again from *Settings*.

To recover from a snapshot instead, initialize a fresh instance and run
`bao operator raft snapshot restore -force <file>`: OpenBao then needs the
unseal keys of the cluster that produced the snapshot.

## Update

```bash
api-cli run update-module --data '{
  "module_url": "ghcr.io/geniusdynamics/openbao:latest",
  "instances": ["openbao1"],
  "force": true
}'
```

An update restarts OpenBao: with manual unseal it must be unsealed again.

### Updating from 1.0.0

Release 1.0.0 shipped with OpenBao 2.7, which no longer bundles the LDAP
auth method. The update adds the pinned LDAP plugin image, a third TCP
port (allocated when the cluster network API is enabled) and the new
settings, which all start disabled or with their previous behaviour.

- **Manual unseal** (A): the instance is updated in place. Unseal it again
  after the update. Nothing else changes.
- **Automatic unseal without automatic initialization** (B): updated in
  place, it unseals itself.
- **Automatic unseal with automatic initialization** (C): in 1.0.0 the
  self-initialization failed at its first step, enabling LDAP login, and
  OpenBao logs `self-initialization failed: refusing to unseal` at every
  start. The update cannot repair that storage. Such an instance never
  became usable (the root token was never shown and nobody could log
  in), so it holds no secrets: after the update, reset it and let it
  initialize itself again:

  ```bash
  runagent -m openbao1 openbao-reset-failed-init
  ```

  The command refuses to run unless OpenBao uses automatic unseal, is
  initialized but sealed, and its log shows the self-initialization
  failure. Removing the application and installing it again has the same
  effect.

## Uninstall

```bash
remove-module --no-preserve openbao1
```

All the stored secrets are deleted, unless a backup exists.

## Security notes

- The OpenBao listener is bound to `127.0.0.1` on the node; TLS is
  terminated by Traefik. Leave `http2https` enabled.
- Restrict the networks that can reach OpenBao with `ip_allowlist` when
  its clients are known.
- The container runs as the unprivileged `openbao` user, with all
  capabilities dropped and `no-new-privileges`.
- `disable_mlock = true`: memory locking is not available to rootless
  containers and is not required with Raft storage. Make sure the node
  swap, if any, is encrypted.
- The Prometheus metrics listener has no authentication and is bound to
  the cluster VPN address only. Metrics hold counters and timings, not
  secrets.
- The `X-Forwarded-For` header set by Traefik is trusted, so audit logs
  record the real client address.
- Enable the audit log in production. Audit entries are sent to the
  journal: view them from the *System logs* page of the application.
- Revoke the root token after the initial setup; generate a new one with
  `bao operator generate-root` when needed.

## Troubleshooting

Inspect the module environment and the generated configuration:

```bash
runagent -m openbao1 env | grep -E 'OPENBAO|TRAEFIK|TCP_PORT'
runagent -m openbao1 cat openbao-config/openbao.hcl
```

Check the service and its logs:

```bash
runagent -m openbao1 systemctl --user status openbao.service
runagent -m openbao1 podman logs --tail 100 openbao   # or the System logs page
```

Use the OpenBao CLI inside the container:

```bash
runagent -m openbao1 podman exec -ti openbao sh -c 'BAO_ADDR=http://127.0.0.1:8200 bao status'
```

The configuration in `openbao-config/openbao.hcl` is regenerated from the
module environment at every start: do not edit it by hand.

## Testing

The tests are written with [Robot Framework](https://robotframework.org/)
and run by the *Test module* GitHub workflow on a QEMU virtual machine.
To run them against an existing NethServer 8 leader node:

```bash
robot -v NODE_ADDR:<node address> -v IMAGE_URL:ghcr.io/geniusdynamics/openbao:<tag> -v SSH_KEYFILE:<private key> --exclude ui tests/
```

## UI translation

Only `ui/public/i18n/en/translation.json` is edited in this repository.
Other languages are translated with [Weblate](https://hosted.weblate.org/projects/ns8/).
