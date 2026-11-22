# ns8-openbao

[OpenBao](https://openbao.org/) for [NethServer 8](https://github.com/NethServer/ns8-core).
OpenBao is an open source, community-driven fork of HashiCorp Vault: it
stores and controls access to tokens, passwords, certificates and
encryption keys, and provides PKI, dynamic secrets and encryption as a
service.

The module runs OpenBao as a rootless container with:

- **Raft integrated storage**, consistent snapshots and NethServer backup,
  restore and clone
- the API and web UI published by Traefik on a dedicated host name, with
  optional Let's Encrypt certificate, IP allow-list or cluster-network-only
  access
- **manual (Shamir), automatic (static key) or Transit unseal**, with seal
  migration
- **optional OpenID Connect** with a published NS8 provider, alongside LDAP or on its own
- **local recovery login** with an opt-in administrator account independent of external providers
- **directory login** with a NethServer user domain (OpenLDAP or Active
  Directory), group policies and starter kits, optionally configured
  automatically at initialization
- **plugins** from the official openbao-plugins project, downloaded only
  when enabled
- **email notifications**, alerts and **Prometheus metrics** for the
  NethServer metrics module
- a **setup wizard** for simple setups, and **high availability**
  (experimental) across nodes
- optional **client provisioning**: approved NethServer modules get their
  own narrowly scoped OpenBao token, without pasting an admin token

## Install

```bash
add-module ghcr.io/geniusdynamics/openbao:latest 1
```

The output returns the instance name, for example `openbao1`. Requires
NethServer 8 core 3.13.0 or later.

## Quick start

Open the application in the NethServer cluster admin: the **setup
wizard** opens on a new instance and asks for the host name, the unseal
mode, the directory login and the notification recipients. Advanced
users can use the *Settings* page directly, or the command line:

```bash
api-cli run configure-module --agent module/openbao1 --data '{"host": "vault.example.org", "http2https": true, "lets_encrypt": true, "unseal_mode": "manual"}'
```

Then initialize OpenBao. How you get the first credentials depends on the
setup you choose:

| Setup | Unseal mode | Directory login | First credentials |
|---|---|---|---|
| [A](docs/first-time-setup.md#a-manual-unseal-without-directory-login) | manual | no | unseal keys + root token |
| [B](docs/first-time-setup.md#b-automatic-unseal-without-directory-login) | automatic | no | recovery keys + root token |
| [C](docs/first-time-setup.md#c-automatic-unseal-with-automatic-directory-login) | automatic | yes, `auto_initialize` | none: domain admins log in |
| [D](docs/first-time-setup.md#d-adding-directory-login-later) | any | yes, after initialization | root token of A or B |

The [first-time setup guide](docs/first-time-setup.md) explains each one
step by step, and what to do when credentials are lost.

## Documentation

| Topic | What it covers |
|---|---|
| [First-time setup](docs/first-time-setup.md) | the setup wizard, setups A–D, getting the first keys and tokens, lost credentials |
| [Configuration reference](docs/configuration.md) | every `configure-module` parameter, reading the configuration and state |
| [Unseal modes](docs/unseal.md) | manual, automatic and Transit unseal, seal migration |
| [Directory login](docs/directory-login.md) | LDAP / Active Directory, NS8 OIDC, shared identities, local recovery, policies and starter kits |
| [Plugins](docs/plugins.md) | the plugin catalog, how plugins are installed, enabling and configuring them in OpenBao |
| [Cluster network and metrics](docs/networking.md) | the cluster network API, VPN-only access, Prometheus metrics |
| [Operations](docs/operations.md) | notifications, module token, snapshots, backup and restore, updates (including from 1.0.0), uninstall, troubleshooting |
| [Client provisioning](docs/client-provisioning.md) | approved modules get their own scoped token: enabling, approvals, groups, the client contract, security model |
| [High availability](docs/high-availability.md) | joining instances into a Raft cluster (experimental), design decisions and limits |
| [Security](docs/security.md) | security notes, and what is deliberately not implemented |
| [Development](docs/development.md) | tests and UI translation |

## Client provisioning

Off by default. When enabled, a module that declares the authorization
`openbao@any:secretsclient` (for example PostgreSQL or KumoMTA) asks for
access; the OpenBao administrator approves it on the **Client modules**
page; the module then calls `provision-client` and receives a
**response-wrapped**, single-use token that it unwraps at once. The token
reaches only `ns8-kv/modules/<module id>/`, plus the shared groups and the
database secrets engine (`ns8-db-<module id>/`) the administrator grants.

```bash
api-cli run module/openbao1/configure-module --data '{"host": "vault.example.org", "client_provisioning": true}'
runagent -m openbao1 openbao-client-provisioner create   # once, with an administrator token
api-cli run module/openbao1/set-client-access --data '{"module_id": "postgresql1", "allowed": true}'
```

The client contract (actions, JSON, unwrap and renewal steps, errors) and
the threat model are in [Client provisioning](docs/client-provisioning.md).

## Update

```bash
api-cli run update-module --data '{"module_url": "ghcr.io/geniusdynamics/openbao:latest", "instances": ["openbao1"], "force": true}'
```

An update restarts OpenBao: with manual unseal it must be unsealed again.
Updating from 1.0.0: see [Updating from 1.0.0](docs/operations.md#updating-from-100).

## Uninstall

```bash
remove-module --no-preserve openbao1
```

All the stored secrets are deleted, unless a backup exists.

## Security in brief

- Unseal keys, tokens and credentials never pass through NethServer
  actions: their payloads are kept in Redis, readable by every module.
  Settings that need a token are applied on the node; plugin credentials
  are entered in OpenBao only.
- OpenBao listens on the node loopback interface; Traefik terminates TLS.
  The container is rootless, with all capabilities dropped.
- Revoke the root token after the initial setup, and enable the audit log
  in production.
- Client provisioning hands out only response-wrapped tokens, confined by
  static templated policies; the provisioner token cannot write policies.

More in [Security](docs/security.md).
