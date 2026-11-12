# Unseal modes

Part of the [ns8-openbao documentation](../README.md#documentation).

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
[cluster network API](networking.md#cluster-network-api).

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
