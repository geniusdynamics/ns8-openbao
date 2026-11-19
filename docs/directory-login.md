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

## NS8 OpenID Connect

In **Settings → OpenID Connect**, choose a published NethServer IdP, Keycloak,
or LemonLDAP::NG provider and an NS8 user domain. To use OIDC only on a new
instance, leave **Directory login** unset. To offer both methods, configure the
LDAP domain alongside OIDC. The two domains may be different. Existing
instances start with the module's OIDC option disabled.

Save Settings and run the following command after OpenBao has been initialized
and unsealed. It prompts for an OpenBao administrator token (or reads
`BAO_TOKEN`). The command registers the HTTPS callbacks with the NS8 provider
and gives OpenBao the client credentials. OpenBao stores them in its encrypted
storage. The NS8 settings action stores the provider and domain selection.

```bash
runagent -m openbao1 openbao-auth apply
```

Use the OpenBao HTTPS route. The provider's issuer must also be reachable
over HTTPS with a certificate trusted by the OpenBao container. In a Raft
cluster, run `apply` from the primary NS8 module. The configuration is
replicated through OpenBao.

Use the OIDC method shown on OpenBao's login page. For CLI login, copy the
command printed by `openbao-auth apply`; it specifies the auth mount and
`callbackmode=direct`. Accounts signing in with the module's default OIDC
role receive OpenBao's standard `default` policy. They get no secret or
administrator privileges from the role. Grant access through OpenBao
identity policies, or define additional roles bound to authoritative
provider claims. The module does not reuse LDAP group names as OIDC
authorization claims.

To remove module-managed OIDC, select **Disabled** and run `openbao-auth apply`
again. Removing the mount revokes its issued tokens. If you are moving an
existing installation to OIDC only, verify local recovery and OIDC access
before disabling an existing LDAP mount with `bao auth disable ldap`. Clearing
the NS8 LDAP setting removes the NS8 domain binding when OIDC does not use the
same domain. OpenBao leaves the LDAP mount in place until you explicitly
disable it.

After changing the OpenBao hostname, moving or restoring the module under a
new instance ID, or changing the provider, run `openbao-auth apply` again to
refresh client registration. A provider or issuer change uses a different
mount accessor, so a subject from the new issuer cannot inherit the previous
issuer's identity by reusing the same identifier.

### Shared identities for one directory

When both methods use the same NS8 user domain, enable **Allow linking LDAP
and OIDC identities** in Settings. After someone has signed in with both
methods, verify that the exact LDAP alias and OIDC `sub` belong to the same
directory account. OpenBao shows the alias names and their auth mounts on
the Identity page. Run:

```bash
runagent -m openbao1 openbao-auth link <ldap-alias> <oidc-subject>
```

The command checks the active LDAP mount against the selected domain and
requires an explicit confirmation. It moves the OIDC alias to the existing
LDAP entity. Future logins use that entity's identity policies and audit ID,
while the two auth methods still issue their own tokens and method-specific
policies. Review outstanding tokens issued before the link and revoke them
as needed. The command asks you to review the entity in OpenBao if it already
has policies, groups, or other aliases. For unrelated domains, configure
their identities independently.

### Local recovery account

The existing bootstrap break-glass token for self-initialized instances
expires after 32 days. Before relying on directory login, you can opt in to
a dedicated local `breakglass` account. Create it while OpenBao is unsealed
and you still have administrator access:

```bash
runagent -m openbao1 openbao-auth recovery set
```

The command asks for the administrator token and a fresh randomly generated
password of 24 to 72 bytes. Store the password in an offline recovery vault.
The module never saves it in NS8 settings. OpenBao stores its hash within the
encrypted Raft data. Run the same command to rotate it and revoke tokens
issued by the old login. There is no default local password.

If LDAP and OIDC are both unavailable, sign in without them:

```bash
bao login -method=userpass -path=ns8-recovery username=breakglass
```

In the web UI, choose **Username** and enter `ns8-recovery` as the mount path,
or open `https://<host>/ui/vault/auth?with=ns8-recovery%2F`. The account has the
`ns8-admin` policy, with a 15-minute initial token lifetime and a one-hour
maximum. It requires OpenBao to be reachable and unsealed. Keep the unseal
or recovery material required by your initialization mode.

To remove the local account and revoke its issued tokens, run
`runagent -m openbao1 openbao-auth recovery disable` with an administrator
token.
