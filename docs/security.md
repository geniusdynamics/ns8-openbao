# Security

Part of the [ns8-openbao documentation](../README.md#documentation).

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
