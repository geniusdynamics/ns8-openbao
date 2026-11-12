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
- backup, restore and clone support

## Table of contents

- [Install](#install)
- [Configure](#configure)
- [Initialize and unseal](#initialize-and-unseal)
- [Unseal modes](#unseal-modes)
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
  "audit_log": true
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
