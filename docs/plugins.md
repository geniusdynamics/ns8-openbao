# Plugins

Part of the [ns8-openbao documentation](../README.md#documentation).

OpenBao 2.7 ships a small core: most authentication methods and secrets
engines are external plugins of the official
[openbao-plugins](https://github.com/openbao/openbao-plugins) project.
This module gives them a catalog on the **Plugins** page.

- **LDAP authentication** is built in: it is always installed, because
  directory login and the self-initialization use it.
- **Every other plugin is optional and nothing is downloaded by default.**
  A plugin is downloaded only when you enable it, and removed with its
  image when you disable it.

## Install and remove plugins

From the **Plugins** page of the application: turn plugins on or off and
**Apply**. Or from the command line:

```bash
api-cli run module/openbao1/list-plugins
api-cli run module/openbao1/configure-plugins --data '{"plugins": ["auth-github", "secrets-aws"]}'
```

`configure-plugins` takes the complete list of optional plugins to keep;
`[]` removes them all. Applying a change **restarts OpenBao**: with
manual unseal, unseal it again.

**Before removing a plugin**, disable the auth method or secrets engine
that uses it (`bao auth disable <path>`, `bao secrets disable <path>`),
otherwise that mount stops working.

## How it works

1. The module pulls the plugin image, pinned by digest
   (`ghcr.io/openbao/openbao-plugin-<id>:<version>@sha256:...`), into the
   instance's own Podman image store. If the node cannot reach ghcr.io,
   the change is refused and nothing changes.
2. Before each start of OpenBao, the binary is copied out of the image,
   its SHA-256 is recorded, and it is declared in the server configuration
   with that checksum. OpenBao registers it when it is unsealed.
3. The plugin directory is mounted **read-only** in the OpenBao container
   and owned by the module, not by the OpenBao process.

Plugins are registered with their version: check one with
`bao plugin info -version=<version> auth github` (the version is shown on
the Plugins page). Enabling an auth method or secrets engine without a
version uses it.

OpenBao can also download plugins itself (`plugin_auto_download`), but
that needs a plugin directory writable by the OpenBao process, which
could then plant binaries that OpenBao executes, and a working registry
at every startup. The module never enables it.

Catalog images are not in the module's `org.nethserver.images` label, so
instances that do not use a plugin never download it. Enabled plugins are
pulled again when needed: after a module update that pins a new version,
after a restore (the list of plugins is restored with the settings) and
after a clone.

## Enable and configure a plugin in OpenBao

Installing a plugin makes it available; using it is an OpenBao
administrator task, done with an administrator token (`bao login`) in the
OpenBao web UI or CLI. The module never holds an administrator token, and
the credentials a plugin needs (cloud keys, keytabs, shared secrets,
database passwords) are entered in OpenBao only: they never pass through
NethServer tasks, whose data Redis keeps for hours and every module can
read.

The Plugins page shows, for each installed plugin, the command that
enables it, the first configuration steps and a link to its documentation.
The same steps are listed [below](#first-steps).

## Catalog

| Id | Plugin | OpenBao name | Version | Enable | Documentation |
|---|---|---|---|---|---|
| `auth-aws` | Authentication: AWS | `aws` | v0.1.2 | `bao auth enable aws` | [docs](https://github.com/openbao/openbao-plugins/tree/main/auth/aws) |
| `auth-azure` | Authentication: Azure | `azure` | v0.23.1 | `bao auth enable azure` | [docs](https://github.com/openbao/openbao-plugins/tree/main/auth/azure) |
| `auth-gcp` | Authentication: Google Cloud | `gcp` | v0.22.1 | `bao auth enable gcp` | [docs](https://github.com/openbao/openbao-plugins/tree/main/auth/gcp) |
| `auth-github` | Authentication: GitHub | `github` | v0.0.2 | `bao auth enable github` | [docs](https://github.com/openbao/openbao-plugins/tree/main/auth/github) |
| `auth-kerberos` | Authentication: Kerberos | `kerberos` | v0.1.0 | `bao auth enable kerberos` | [docs](https://github.com/openbao/openbao-plugins/tree/main/auth/kerberos) |
| `auth-radius` | Authentication: RADIUS | `radius` | v0.2.0 | `bao auth enable radius` | [docs](https://github.com/openbao/openbao-plugins/tree/main/auth/radius) |
| `secrets-aws` | Secrets engine: AWS | `aws` | v0.3.3 | `bao secrets enable aws` | [docs](https://github.com/openbao/openbao-plugins/tree/main/secrets/aws) |
| `secrets-azure` | Secrets engine: Azure | `azure` | v0.23.1 | `bao secrets enable azure` | [docs](https://github.com/openbao/openbao-plugins/tree/main/secrets/azure) |
| `secrets-gcp` | Secrets engine: Google Cloud | `gcp` | v0.23.2 | `bao secrets enable gcp` | [docs](https://github.com/openbao/openbao-plugins/tree/main/secrets/gcp) |
| `secrets-gcpkms` | Secrets engine: Google Cloud KMS | `gcpkms` | v0.21.1 | `bao secrets enable gcpkms` | [docs](https://github.com/openbao/openbao-plugins/tree/main/secrets/gcpkms) |
| `secrets-consul` | Secrets engine: Consul | `consul` | v0.1.2 | `bao secrets enable consul` | [docs](https://github.com/openbao/openbao-plugins/tree/main/secrets/consul) |
| `secrets-nomad` | Secrets engine: Nomad | `nomad` | v0.1.7 | `bao secrets enable nomad` | [docs](https://github.com/openbao/openbao-plugins/tree/main/secrets/nomad) |
| `secrets-ldap` | Secrets engine: LDAP | `ldap` | v0.1.1 | `bao secrets enable ldap` | [docs](https://github.com/openbao/openbao-plugins/tree/main/secrets/ldap) |
| `database-mongodb` | Database: MongoDB | `mongodb-database-plugin` | v0.0.2 | `bao secrets enable database` | [docs](https://github.com/openbao/openbao-plugins/tree/main/database/mongodb) |

The database plugin is used by the database secrets engine: enable
`database` and use `plugin_name=mongodb-database-plugin` in the
connection.

## First steps

Replace the values in `<angle brackets>`. These are the usual first
steps; see each plugin's documentation for all the options.

### Authentication: AWS (`auth-aws`)

```bash
bao auth enable aws
bao write auth/aws/config/client access_key=<access key> secret_key=<secret key>
bao write auth/aws/role/<role> auth_type=iam bound_iam_principal_arn=<IAM ARN> policies=ns8-secrets-ro
```

### Authentication: Azure (`auth-azure`)

```bash
bao auth enable azure
bao write auth/azure/config tenant_id=<tenant ID> resource=https://management.azure.com/
bao write auth/azure/role/<role> bound_subscription_ids=<subscription ID> policies=ns8-secrets-ro
```

### Authentication: Google Cloud (`auth-gcp`)

```bash
bao auth enable gcp
bao write auth/gcp/config credentials=@<service-account>.json
bao write auth/gcp/role/<role> type=iam bound_service_accounts=<service account e-mail> policies=ns8-secrets-ro
```

### Authentication: GitHub (`auth-github`)

```bash
bao auth enable github
bao write auth/github/config organization=<organization>
bao write auth/github/map/teams/<team> value=ns8-secrets-rw
```

### Authentication: Kerberos (`auth-kerberos`)

```bash
bao auth enable kerberos
bao write auth/kerberos/config keytab=@<keytab, base64> service_account=<service account>
bao write auth/kerberos/config/ldap url=ldaps://<directory server> userdn=<users DN> groupdn=<groups DN>
```

### Authentication: RADIUS (`auth-radius`)

```bash
bao auth enable radius
bao write auth/radius/config host=<RADIUS server> secret=<shared secret>
bao write auth/radius/users/<user> policies=ns8-secrets-ro
```

### Secrets engine: AWS (`secrets-aws`)

```bash
bao secrets enable aws
bao write aws/config/root access_key=<access key> secret_key=<secret key> region=<region>
bao write aws/roles/<role> credential_type=iam_user policy_arns=<policy ARN>
bao read aws/creds/<role>
```

### Secrets engine: Azure (`secrets-azure`)

```bash
bao secrets enable azure
bao write azure/config subscription_id=<subscription ID> tenant_id=<tenant ID> client_id=<client ID> client_secret=<client secret>
bao write azure/roles/<role> azure_roles=@<roles>.json ttl=1h
```

### Secrets engine: Google Cloud (`secrets-gcp`)

```bash
bao secrets enable gcp
bao write gcp/config credentials=@<service-account>.json
bao write gcp/roleset/<roleset> project=<project> secret_type=access_token token_scopes=https://www.googleapis.com/auth/cloud-platform bindings=@<bindings>.hcl
```

### Secrets engine: Google Cloud KMS (`secrets-gcpkms`)

```bash
bao secrets enable gcpkms
bao write gcpkms/config credentials=@<service-account>.json
bao write gcpkms/keys/<key> key_ring=projects/<project>/locations/<location>/keyRings/<key ring> rotation_period=72h
```

### Secrets engine: Consul (`secrets-consul`)

```bash
bao secrets enable consul
bao write consul/config/access address=<Consul host>:8500 token=<management token>
bao write consul/roles/<role> policies=<Consul policy>
```

### Secrets engine: Nomad (`secrets-nomad`)

```bash
bao secrets enable nomad
bao write nomad/config/access address=http://<Nomad host>:4646 token=<management token>
bao write nomad/role/<role> policies=<Nomad policy>
```

### Secrets engine: LDAP (`secrets-ldap`)

```bash
bao secrets enable ldap
bao write ldap/config binddn=<bind DN> bindpass=<bind password> url=ldaps://<directory server>
bao write ldap/static-role/<role> dn=<account DN> username=<account> rotation_period=24h
```

### Database: MongoDB (`database-mongodb`)

```bash
bao secrets enable database
bao secrets enable database
bao write database/config/<connection> plugin_name=mongodb-database-plugin allowed_roles=<role> connection_url="mongodb://{{username}}:{{password}}@<host>:27017/admin" username=<admin user> password=<admin password>
bao write database/roles/<role> db_name=<connection> creation_statements='{ "db": "admin", "roles": [{ "role": "readWrite", "db": "<database>" }] }' default_ttl=1h
```

## Not in the catalog

- **KMS plugins** (AliCloud KMS, AWS KMS, Azure Key Vault, Google Cloud
  KMS, OCI KMS, OVHcloud KMS, Securosys, T Cloud Public KMS) are seals:
  OpenBao loads them from its configuration file before it is unsealed,
  and each provider needs its own settings and credentials. They would be
  new unseal modes, next to manual, automatic and Transit, with the
  credentials stored on the node like the Transit token. Not implemented
  yet.
- **PKCS#11** (HSM) needs the vendor's PKCS#11 library and access to the
  device inside the container, which the official OpenBao image does not
  provide. Not supported.
- **External keys** (`/sys/external-keys`, PKI and Transit keys held in a
  KMS) depend on KMS plugins and are configured through the OpenBao API
  with an administrator token. Not supported until KMS plugins are.
- **Custom plugin images** are not accepted: a plugin runs inside the
  secrets store, so only the official images pinned by this module are
  offered.

## For developers: updating the pinned versions

The catalog is `PLUGIN_CATALOG` in `imageroot/pypkg/openbao.py`: each
entry pins an image by tag and digest. To update a plugin, change its
`image` to the new `tag@sha256:digest` (from
`https://github.com/orgs/openbao/packages?repo_name=openbao-plugins`),
check the first steps in `PLUGIN_GUIDES`, and run the plugin test suite
(`tests/60_openbao_plugins.robot`).
