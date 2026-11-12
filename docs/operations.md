# Operations

Part of the [ns8-openbao documentation](../README.md#documentation).

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
