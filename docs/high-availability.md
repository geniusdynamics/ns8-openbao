# High availability: design decisions

Status: **experimental**. Single-node tests run in CI, including a real
join of two instances on the same node through the node VPN address
(`tests/50_openbao_ha.robot`). Multi-node behaviour (node loss, leader
change, rejoin) is verified manually on real clusters.

## Goals

- **Nothing changes for a single instance.** Every 1.x install, and every
  new install that does not choose a role, is a standalone single-node
  Raft cluster exactly as before: same node ID, same loopback cluster
  address, no extra published port.
- **Opt-in, per instance.** High availability is a role chosen in
  *Settings* or in the setup wizard of a new instance.
- **No secret through NS8 actions or Redis.** Redis keeps task payloads
  for 8 hours, readable by all modules. Joining needs no token; the seal
  key or token never leaves its node.

## Roles

| Role | Raft node ID | Cluster address | Published |
|---|---|---|---|
| `standalone` (default) | `ns8-openbao` | `127.0.0.1:8201` | nothing new |
| `primary` (accepts members) | `ns8-openbao` | `<node VPN IP>:<4th TCP port>` | cluster port and cluster network API on the VPN address |
| `member` | its module ID | `<node VPN IP>:<4th TCP port>` | cluster port on the VPN address |

### Node IDs

The Raft node ID is stored in the Raft data and never changes.

- Standalone and primary instances keep the fixed `ns8-openbao`. The first
  instance of a cluster therefore needs no node ID migration, and restore
  and clone to another instance name keep working.
- Only an instance that joins gets its own ID: `OPENBAO_RAFT_NODE_ID` is
  set to its module ID once, at join time. Raft needs IDs to be unique only
  within one Raft cluster, and module IDs are unique in the NethServer
  cluster.
- Restore and clone copy `OPENBAO_RAFT_NODE_ID`, because it must match the
  data.

### Cluster address: the one risky step

A standalone instance's own Raft entry holds `127.0.0.1:8201`. Raft
identifies the local server by ID, so a single node keeps electing itself,
but members could not reach it. When an initialized standalone instance
becomes a primary, the module uses OpenBao's documented outage recovery:

1. `configure-module` sets `OPENBAO_RAFT_RECOVER`.
2. In `ExecStartPre`, with the server stopped, `openbao-write-config`
   copies the Raft files to `raft.bak-<timestamp>` in the data volume and
   writes `raft/peers.json` with the single entry
   `{"id": "ns8-openbao", "address": "<VPN IP>:<port>", "non_voter": false}`.
3. OpenBao applies and deletes `peers.json` at start.

No member can have joined yet, because the cluster port was not
published, so rewriting the configuration as a single node loses nothing.
The same mechanism moves a primary back to loopback when it returns
standalone. That is allowed only when the module token shows it is the
last Raft member. It also detaches a restored or cloned HA instance from
its old cluster.

## Discovery: NS8 service providers

As other modules do (for example Webtop discovering Mail), an HA instance
publishes a service provider record:

```
module/<id>/srv/tcp/openbao-cluster
  host, port         cluster listener on the node VPN address
  api_url            cluster network API, used by joining instances
  ha_cluster         module ID of the primary
  ha_role, raft_node_id
  unseal_mode, transit_address, transit_mount, transit_key,
  transit_tls_skip_verify   (no token)
```

and the event `openbao-cluster-changed`.

- `get-configuration` returns the other records as `ha_candidates`: the
  Settings page and the wizard list them.
- Consumers use `agent.list_service_providers(rdb, "openbao-cluster", "tcp")`.

## Joining

- A member is configured with `ha_role: member` and `ha_join: <module ID>`.
- `configure-module` stores the `api_url` of every instance of that
  cluster in `OPENBAO_HA_JOIN_ADDRS`. They are rendered as `retry_join`
  blocks of the Raft storage, used only until the instance has joined.
- Raft join is unauthenticated: the joining node answers a challenge
  encrypted with the cluster keyring, so it must use the same seal:
  - **Manual (Shamir)**: the member is unsealed with the unseal keys of
    the cluster, which completes the join.
  - **Transit**: the member takes the cluster's Transit settings from the
    discovery record. Its own Transit token is stored on its node with
    `openbao-transit-token`, and it unseals itself.
  - **Automatic (static key)**: not supported. Members would need a copy
    of the key file, and the only built-in channel between nodes is Redis.
- Joining is allowed only on an uninitialized instance: the join replaces
  its storage. A member never initializes itself.

## Ports

- The fourth module TCP port is the cluster listener; `tcp-ports-demand`
  is 4.
- Instances installed by earlier releases get the port from `node:portsadm`
  when they first choose a role (`OPENBAO_CLUSTER_PORT`); NS8 updates the
  allowed demand when the module is updated.
- The listener inside the container is `0.0.0.0:8201`, published only on
  the node VPN address, which the cluster VPN protects. Raft and request
  forwarding use mutual TLS managed by OpenBao.

## Lifecycle rules

| Change | Allowed when |
|---|---|
| standalone → primary | manual or Transit unseal; storage state known |
| primary → standalone | no other Raft member (read with the module token) |
| standalone → member | the instance is not initialized |
| member → standalone | the member never joined (not initialized) |
| joined member leaves | not by configuration: remove its peer (`bao operator raft remove-peer <module id>`, administrator token), then remove its application |

## Backups, restore, clone

- Backups of the primary contain a consistent Raft snapshot (module
  token). Members have no module token and back up their data volume.
- Restore and clone never restore a role: the instance comes back
  standalone, and `OPENBAO_RAFT_RECOVER` rewrites the Raft configuration as
  a single node with the original node ID. Clone also drops the ports
  allocated to the original instance.

## Known limits

- **Quorum**: 2 members tolerate no failure; use 3.
- **Removing a member** needs an administrator token on the cluster, which
  the module never holds: it cannot remove the peer by itself.
- **Node VPN address change** of an HA node: the Raft data keeps the old
  address. The module logs a warning; the peer must be updated in the
  cluster (remove and rejoin the member, or use `peers.json` recovery on
  every node).
- **Upgrade order**: update the standby instances first, the active one
  last.
- **Traefik**: each instance has its own host name. A standby forwards
  requests to the active node, so any member's host name works. A shared
  host name in front of all members (DNS or an external load balancer) is
  outside the module.
