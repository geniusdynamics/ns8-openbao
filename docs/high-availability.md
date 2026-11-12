# High availability: design notes

Status: **not implemented**. This document records the design and why it
is not shipped yet. Today each OpenBao instance is a single-node Raft
cluster.

## Why it is not shipped yet

Joining instances into one Raft cluster changes how storage, unseal,
backup and restore behave, and a mistake in Raft membership loses data.
It needs testing on a real multi-node NethServer cluster (node loss,
leader change, rejoin, restore) before it can be offered. The CI runs on a
single VM.

## Constraints of the current design

- **Fixed Raft node ID `ns8-openbao`** and cluster address
  `https://127.0.0.1:8201`. They are stored in the Raft data; the fixed
  values let restore and clone to another instance name work. HA needs a
  unique node ID per member and a cluster address reachable from the other
  nodes.
- **Cluster port is local**: 8201 is not published. Members must reach
  each other's cluster port (mutual TLS, managed by OpenBao) on the node
  VPN addresses.
- **Seal**: every member must use the same seal. Static auto-unseal would
  need the key file copied to each member over a secure channel (never
  through Redis); Transit is the natural choice for HA.
- **Backup/restore**: Raft snapshots of the leader are the backup; the
  volume copy of a follower is not a valid restore source.

## Proposed design

1. A member instance is installed with a `ha_leader` setting naming an
   existing instance (`module_id`). It discovers the leader's cluster
   network API through the `openbao` service provider record.
2. New members use `node_id = MODULE_ID`; the first (existing) instance
   keeps `ns8-openbao`, so it needs no migration of its own node ID.
3. The cluster port is published on a fourth TCP port, bound to the node
   VPN address; `cluster_addr` becomes `https://<vpn address>:<port>`. The
   first instance's own Raft address must be updated to that value with
   `bao operator raft` while it is the only voter (the risky step).
4. Members start with `retry_join { leader_api_addr = "<leader cluster
   network API>" }`, and are unsealed with the same seal (Transit
   recommended).
5. Traefik routes on each node point to the local member; standby members
   forward requests to the active one (request forwarding is on by
   default), so any member's host name works.
6. Backups run `module-dump-state` only on the active member (snapshot
   through the module token); restore rebuilds a single-node cluster and
   members rejoin.
7. The Status page shows the Raft peers (`sys/storage/raft/configuration`,
   readable with the module token) and the leader.

## Open questions

- Removing a member (`bao operator raft remove-peer`) when its module is
  removed: the departing instance needs a token to call the leader.
- Quorum: 2 members tolerate no failure; the UI should recommend 3.
- Upgrade order: OpenBao requires followers to be updated before the
  leader.
