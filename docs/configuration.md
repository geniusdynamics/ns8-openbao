# Configuration reference

Part of the [ns8-openbao documentation](../README.md#documentation).

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
- `unseal_mode`: `manual`, `auto` or `transit`, see [Unseal modes](unseal.md#unseal-modes).
  Default `manual`. It can be changed only before OpenBao is initialized
- `log_level`: `trace`, `debug`, `info`, `warn` or `error`. Default `info`
- `audit_log`: send the OpenBao audit log to the systemd journal. Default `false`
- `user_domain`: NethServer user domain for directory login; `""` disables
  it. See [Directory login](directory-login.md#directory-login-ldap--active-directory)
- `ldap_admin_group`: group of `user_domain` whose members get full access
  to OpenBao. Required with `user_domain`; it must exist in the domain
- `auto_initialize`: with `unseal_mode` `auto` and a `user_domain`, let
  OpenBao initialize itself with directory login already configured
- `notify_recipients`: email addresses notified when OpenBao is down or
  sealed. `[]` disables them. See [Notifications](operations.md#notifications-and-alerts)
- `ip_allowlist`: client IP addresses or networks (CIDR) allowed to reach
  the API and web UI through Traefik. `[]` (default) allows everybody.
  Applications that read secrets through the host name must be listed too
- `ldap_group_policies`: more directory groups mapped to OpenBao policies,
  see [Group policies](directory-login.md#group-policies)
- `starter_kits`: components prepared at initialization, any of `kv`
  (default), `pki`, `approle`; see [Starter kits](directory-login.md#starter-kits)
- `vpn_api`: also publish the API on the cluster VPN, see
  [Cluster network API](networking.md#cluster-network-api). Default `false`
- `public_access`: publish the API and web UI through Traefik on `host`.
  `false` makes OpenBao reachable only on the cluster network API (requires
  `vpn_api`). Default `true`
- `snapshot_keep`: daily Raft snapshots kept on the node, see
  [Snapshots and restore](operations.md#snapshots-and-restore). Default `0` (disabled)
- `transit_address`, `transit_mount` (default `transit`), `transit_key`,
  `transit_tls_skip_verify`: settings of the `transit` unseal mode, see
  [Unseal modes](unseal.md#unseal-modes)
- `ha_role`: `standalone` (default), `primary` (accept other instances as
  members) or `member` (join `ha_join`); experimental, see
  [High availability](high-availability.md)
- `ha_join`: module ID of the instance to join, with `ha_role` `member`

Omitted optional parameters keep their current value.

Plugins are configured with their own actions, `list-plugins` and
`configure-plugins`: see [Plugins](plugins.md).

The command starts OpenBao and configures the Traefik route. Clients reach
the API at `https://vault.example.org` (for example
`export BAO_ADDR=https://vault.example.org`) and the web UI at
`https://vault.example.org/ui/`.

Changing `log_level` or `audit_log` reloads OpenBao in place. Changing
`host` or `unseal_mode` restarts it: with manual unseal it must be
unsealed again.

## Get the configuration and state

```bash
api-cli run get-configuration --agent module/openbao1
api-cli run get-openbao-status --agent module/openbao1
```

`get-openbao-status` returns whether the service is running, and whether
OpenBao is initialized and sealed, with the unseal progress, the version
and the web UI URL; the module token and root token checks; the high
availability state; and the installed optional plugins.

`get-configuration` also returns `ha_candidates`, the other instances
that accept members.

The JSON schemas of all the actions are in `imageroot/actions/*/validate-*.json`.
