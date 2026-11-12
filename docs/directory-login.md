# Directory login, group policies and starter kits

Part of the [ns8-openbao documentation](../README.md#documentation).

## Directory login (LDAP / Active Directory)

Choose a user domain of the cluster (internal OpenLDAP or Samba Active
Directory, or an external LDAP/AD domain) and an administrators group in
*Settings*. The module binds the domain, so it appears in the cluster
*Domains and users* page. OpenBao is then configured with:

- the `ldap` auth method, connected to the node ldapproxy: it relays to
  the domain servers with TLS and fails over between them. User and group
  searches mirror the NethServer core: `sAMAccountName`/`member` for Active
  Directory, `uid`/`posixGroup` `memberUid` for OpenLDAP
- the `ns8-admin` policy, with full access, mapped to the administrators
  group

### Default NethServer domain accounts

Both NethServer account providers create a builtin group named
**`domain admins`**, so it is the natural administrators group, and the
*Settings* page and the setup wizard propose it:

- **Internal OpenLDAP**: the *admuser* given when the domain is created
  (for example `admin`) is created as a member of `domain admins`.
- **Samba Active Directory**: with the user name `administrator`, the
  builtin Samba administrator is used; with any other name, that user is
  created, added to `domain admins`, and the builtin `administrator` is
  disabled.

There is no default password: it is the one typed when the domain was
created. An external LDAP/AD domain has its own groups (for example
`Domain Admins` in Active Directory). OpenBao matches group names without
regard to case.

Users log in with their domain account:

```bash
bao login -method=ldap username=alice
```

or with the **Log in with directory account** button of the *Status*
page, which opens the web UI with the LDAP method selected
(`https://<host>/ui/vault/auth?with=ldap%2F`). Create further policies and
map other groups with `auth/ldap/groups/<group>`.

Since OpenBao 2.7 the LDAP auth method is not built into OpenBao: it is
an external plugin from the [openbao-plugins](https://github.com/openbao/openbao-plugins)
project. The module lists its pinned image
(`ghcr.io/openbao/openbao-plugin-auth-ldap`) among the module images, so
the node pulls it at install and update time, and OpenBao never downloads
anything at startup. Before each start the binary is copied from the image
into `state/openbao-plugins/` and declared in the server configuration
with its version and SHA-256 checksum.

How OpenBao gets this configuration depends on its state, see
[First-time setup](first-time-setup.md#first-time-setup):

- **Automatic initialization** ([setup C](first-time-setup.md#c-automatic-unseal-with-automatic-directory-login)):
  requires automatic unseal and an uninitialized server. The module checks
  that the group exists before saving, because a wrong group would leave a
  self-initialized OpenBao without administrators.
- **`openbao-apply-config`** ([setup D](first-time-setup.md#d-adding-directory-login-later)):
  for an initialized server, or with manual unseal. The module cannot
  change OpenBao without an administrator token, and tokens must never
  pass through module actions: the command prompts for a token on the node
  (or reads `BAO_TOKEN`), applies the configuration and forgets the token.

### Group policies

Besides the administrators group (`ns8-admin`), map other directory
groups to policies in *Settings*, *Group policies*. The module creates
these built-in policies:

| Policy | Access |
|---|---|
| `ns8-admin` | everything |
| `ns8-secrets-rw` | read and write the `secret/` key/value store |
| `ns8-secrets-ro` | read the `secret/` key/value store |
| `ns8-pki-issuer` | issue certificates with the `pki/roles/ns8-server` role |

The name of a policy created in OpenBao can be typed too. A group may
appear in several rows to get several policies.

> **Note:** when several policies of a token match a path, OpenBao applies
> only the most specific path; it does not add their capabilities up
> (capabilities are merged only for identical paths). `ns8-admin` repeats
> the paths of the other built-in policies, so giving administrators a
> built-in policy too never narrows their access. A custom policy with a
> narrower path, mapped to a group the administrators belong to, does
> narrow it: an administrator would then, for example, only read under
> that path.

Mappings need an administrator token to be written, so they are applied
by the self-initialization or, on an initialized server, by
`openbao-apply-config`. Run it again after changing them: it also removes
the mappings it created before and that are no longer configured, and
leaves mappings created by hand untouched.

OpenBao keeps its own copy of the LDAP connection settings. If the domain
bind credentials or servers change, the module logs a warning, sends a
notification and asks to run `openbao-apply-config` again.

## Starter kits

Choose in *Settings* (or in the wizard, for automatic initialization)
what OpenBao should be prepared with:

| Kit | Prepares |
|---|---|
| `kv` (default) | key/value version 2 store at `secret/` |
| `pki` | internal root CA at `pki/` (EC P-384, 10 years), issuing and CRL URLs on the host name, and the `ns8-server` role (any name, server and client usage, 30 days, maximum 90) |
| `approle` | the AppRole auth method at `approle/`, for applications and scripts |

Kits are applied by the self-initialization, or on an initialized server
by `openbao-apply-config`, which skips what already exists: an enabled
mount or an existing PKI issuer is never changed. Unchecking a kit does
not remove anything.

## Applying settings that need a token

The module never holds an OpenBao administrator token. Directory login,
group policies and starter kits are written by the self-initialization
or, afterwards, by this node command, which reads a token from the
terminal (or from `BAO_TOKEN`), applies everything idempotently and
forgets the token:

```bash
runagent -m openbao1 openbao-apply-config
```

`openbao-setup-ldap`, the command name of release 1.0.0, still works.
