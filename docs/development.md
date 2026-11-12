# Development

Part of the [ns8-openbao documentation](../README.md#documentation).

## Testing

The tests are written with [Robot Framework](https://robotframework.org/)
and run by the *Test module* GitHub workflow on a QEMU virtual machine.
To run them against an existing NethServer 8 leader node:

```bash
robot -v NODE_ADDR:<node address> -v IMAGE_URL:ghcr.io/geniusdynamics/openbao:<tag> -v SSH_KEYFILE:<private key> --exclude ui tests/
```

| Suite | Covers |
|---|---|
| `10_openbao.robot` | install, manual unseal, metrics, notifications, allow-list, starter kits, module token, snapshots, cluster network API, seal migration, VPN-only |
| `20_openbao_auto_unseal.robot` | automatic unseal, static key file, consistent backup dump |
| `30_openbao_directory_login.robot` | OpenLDAP domain, self-initialization, directory login, group policies |
| `40_openbao_transit.robot` | Transit unseal |
| `50_openbao_ha.robot` | high availability: two instances join one Raft cluster on the same node |
| `60_openbao_plugins.robot` | plugin catalog: install on demand, registration, removal |

## UI translation

Only `ui/public/i18n/en/translation.json` is edited in this repository.
Other languages are translated with [Weblate](https://hosted.weblate.org/projects/ns8/).
