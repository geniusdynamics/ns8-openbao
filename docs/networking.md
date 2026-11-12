# Cluster network and metrics

Part of the [ns8-openbao documentation](../README.md#documentation).

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
