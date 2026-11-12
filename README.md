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
- [Initialize and unseal](#initialize-and-unseal)
- [Unseal modes](#unseal-modes)
- [Directory login (LDAP / Active Directory)](#directory-login-ldap--active-directory)
- [Notifications and alerts](#notifications-and-alerts)
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
  "ldap_admin_group": "Domain Admins",
  "auto_initialize": false,
  "notify_recipients": ["security@example.org"]
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

Omitted optional parameters keep their current value.

The command starts OpenBao and configures the Traefik route. Clients reach
the API at `https://vault.example.org` (for example
`export BAO_ADDR=https://vault.example.org`) and the web UI at
`https://vault.example.org/ui/`.

Changing `log_level` or `audit_log` reloads OpenBao in place. Changing
`host` or `unseal_mode` restarts it: with manual unseal it must be
unsealed again.

## Initialize and unseal

A new instance starts **uninitialized**. Open the web UI at
`https://<host>/ui/` (the *Open OpenBao* button on the *Status* page) and
initialize it, or use the CLI:

```bash
export BAO_ADDR=https://vault.example.org
bao operator init                    # manual unseal: 5 key shares, threshold 3
bao operator init -recovery-shares=5 -recovery-threshold=3   # automatic unseal
```

The root token and the unseal (or recovery) keys are shown **only once**.
Store them in a safe place, separately. Then revoke the root token once
you have configured an auth method and an administrative policy.

On purpose, the module never handles root tokens, unseal keys or recovery
keys: NethServer 8 keeps action inputs and outputs in Redis, readable by
other modules, so secrets must not travel through module actions. The
*Status* page only reads the unauthenticated seal status.

## Unseal modes

| | `manual` (default) | `auto` |
|---|---|---|
| Seal | Shamir key shares | `static` seal with a 32-byte key |
| After restart, update or reboot | sealed: an operator enters the unseal keys | unseals itself |
| Key storage | keys held by operators only | key generated on the node, `state/openbao-seal.key` (mode 0600), included in backups |
| Backup consistency | live copy of the Raft storage | OpenBao stopped for a few seconds for a consistent copy |
| Protection against disk or backup theft | yes | no: whoever holds the key file and the data can decrypt the secrets |

Choose `manual` when the stored secrets are sensitive enough to justify
an operator unsealing OpenBao after every restart. Choose `auto` when
availability matters more and the node disk and backup repository are
trusted.

The seal type is written into the storage at initialization time, so
`unseal_mode` is locked once OpenBao is initialized. Switching later
requires an OpenBao [seal migration](https://openbao.org/docs/concepts/seal/#seal-migration),
which is not automated by the module.

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

Users log in with their domain account:

```bash
bao login -method=ldap username=alice
```

or from the web UI, choosing the *LDAP* method. Create further policies
and map other groups with `auth/ldap/groups/<group>`.

How OpenBao is configured depends on its state:

- **Automatic initialization** (`auto_initialize`, requires automatic
  unseal and an uninitialized server): OpenBao initializes itself at the
  next start with directory login, the `ns8-admin` policy and a `secret/`
  key/value (v2) store. No root token and no recovery keys are created:
  members of the administrators group log in at once. After the first
  login, generate recovery keys and store them safely:

  ```bash
  bao operator rotate-keys -init -key-shares=5 -key-threshold=3 -target=recovery
  ```

  The module checks that the group exists before saving, because a wrong
  group would leave OpenBao without administrators.

- **Already initialized, or manual unseal**: the module cannot change
  OpenBao without an administrator token, and tokens must never pass
  through module actions. After saving the settings, run on the node:

  ```bash
  runagent -m openbao1 openbao-setup-ldap
  ```

  It prompts for an OpenBao token (or reads `BAO_TOKEN`), applies the same
  configuration and forgets the token.

OpenBao keeps its own copy of the LDAP connection settings. If the domain
bind credentials or servers change, the module logs a warning, sends a
notification and asks to run `openbao-setup-ldap` again.

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

Releases before 1.0.0 ran OpenBao in **development mode**, which keeps
everything in memory: no data was ever persisted. The update removes the
old pod and starts a new, uninitialized server. Configure the unseal mode,
then initialize it.

## Uninstall

```bash
remove-module --no-preserve openbao1
```

All the stored secrets are deleted, unless a backup exists.

## Security notes

- The OpenBao listener is bound to `127.0.0.1` on the node; TLS is
  terminated by Traefik. Leave `http2https` enabled.
- The container runs as the unprivileged `openbao` user, with all
  capabilities dropped and `no-new-privileges`.
- `disable_mlock = true`: memory locking is not available to rootless
  containers and is not required with Raft storage. Make sure the node
  swap, if any, is encrypted.
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
