# get-configuration output Schema

```txt
http://schema.nethserver.org/openbao/get-configuration-output.json
```

Get the OpenBao instance configuration

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                    |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-configuration-output.json](openbao/get-configuration-output.json "open original schema") |

## get-configuration output Type

`object` ([get-configuration output](get-configuration-output.md))

## get-configuration output Examples

```json
{
  "host": "vault.example.org",
  "http2https": true,
  "lets_encrypt": true,
  "log_level": "info",
  "audit_log": false,
  "unseal_mode": "manual",
  "user_domain": "ad.example.org",
  "ldap_admin_group": "Domain Admins",
  "auto_initialize": false,
  "notify_recipients": [
    "security@example.org"
  ],
  "user_domains": [
    {
      "name": "ad.example.org",
      "schema": "ad",
      "location": "internal"
    }
  ],
  "smarthost_enabled": true,
  "ip_allowlist": [
    "192.168.1.0/24"
  ],
  "ldap_group_policies": [
    {
      "group": "Developers",
      "policy": "ns8-secrets-rw"
    }
  ],
  "starter_kits": [
    "kv"
  ],
  "builtin_policies": [
    "ns8-admin",
    "ns8-pki-issuer",
    "ns8-secrets-ro",
    "ns8-secrets-rw"
  ],
  "vpn_api": false,
  "vpn_api_url": "",
  "transit_address": "",
  "transit_mount": "transit",
  "transit_key": "",
  "transit_tls_skip_verify": false,
  "transit_token_present": false,
  "public_access": true,
  "snapshot_keep": 0
}
```

# get-configuration output Properties

| Property                                            | Type      | Required | Nullable       | Defined by                                                                                                                                                                                          |
| :-------------------------------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [host](#host)                                       | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-host.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/host")                                       |
| [http2https](#http2https)                           | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-http2https.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/http2https")                           |
| [lets_encrypt](#lets_encrypt)                       | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-lets_encrypt.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/lets_encrypt")                       |
| [log_level](#log_level)                             | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-log_level.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/log_level")                             |
| [audit_log](#audit_log)                             | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-audit_log.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/audit_log")                             |
| [unseal_mode](#unseal_mode)                         | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-unseal_mode.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/unseal_mode")                         |
| [user_domain](#user_domain)                         | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-user_domain.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domain")                         |
| [ldap_admin_group](#ldap_admin_group)               | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ldap_admin_group.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_admin_group")               |
| [auto_initialize](#auto_initialize)                 | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-auto_initialize.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/auto_initialize")                 |
| [notify_recipients](#notify_recipients)             | `array`   | Required | cannot be null | [get-configuration output](get-configuration-output-properties-notify_recipients.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/notify_recipients")             |
| [user_domains](#user_domains)                       | `array`   | Required | cannot be null | [get-configuration output](get-configuration-output-properties-user_domains.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains")                       |
| [smarthost_enabled](#smarthost_enabled)             | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-smarthost_enabled.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/smarthost_enabled")             |
| [ip_allowlist](#ip_allowlist)                       | `array`   | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ip_allowlist.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ip_allowlist")                       |
| [ldap_group_policies](#ldap_group_policies)         | `array`   | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ldap_group_policies.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies")         |
| [starter_kits](#starter_kits)                       | `array`   | Required | cannot be null | [get-configuration output](get-configuration-output-properties-starter_kits.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/starter_kits")                       |
| [builtin_policies](#builtin_policies)               | `array`   | Required | cannot be null | [get-configuration output](get-configuration-output-properties-builtin_policies.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/builtin_policies")               |
| [vpn_api](#vpn_api)                                 | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-vpn_api.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/vpn_api")                                 |
| [vpn_api_url](#vpn_api_url)                         | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-vpn_api_url.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/vpn_api_url")                         |
| [transit_address](#transit_address)                 | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-transit_address.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_address")                 |
| [transit_mount](#transit_mount)                     | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-transit_mount.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_mount")                     |
| [transit_key](#transit_key)                         | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-transit_key.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_key")                         |
| [transit_tls_skip_verify](#transit_tls_skip_verify) | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-transit_tls_skip_verify.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_tls_skip_verify") |
| [transit_token_present](#transit_token_present)     | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-transit_token_present.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_token_present")     |
| [public_access](#public_access)                     | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-public_access.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/public_access")                     |
| [snapshot_keep](#snapshot_keep)                     | `integer` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-snapshot_keep.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/snapshot_keep")                     |

## host

Host name of the OpenBao API and web UI. Empty if not configured yet

`host`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-host.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/host")

### host Type

`string`

## http2https

HTTP requests are redirected to HTTPS

`http2https`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-http2https.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/http2https")

### http2https Type

`boolean`

## lets_encrypt

A Let's Encrypt certificate is requested for the host name

`lets_encrypt`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-lets_encrypt.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/lets_encrypt")

### lets_encrypt Type

`boolean`

## log_level



`log_level`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-log_level.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/log_level")

### log_level Type

`string`

### log_level Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |    |    |
| :-------- | :---------- | :- | :- |
| `"trace"` |             |
| `"debug"` |             |
| `"info"`  |             |
| `"warn"`  |             |
| `"error"` |             |

## audit_log

The audit log is sent to the systemd journal

`audit_log`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-audit_log.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/audit_log")

### audit_log Type

`boolean`

## unseal_mode



`unseal_mode`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-unseal_mode.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/unseal_mode")

### unseal_mode Type

`string`

### unseal_mode Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value       | Explanation |    |    |
| :---------- | :---------- | :- | :- |
| `"manual"`  |             |
| `"auto"`    |             |
| `"transit"` |             |

## user_domain

User domain used for directory login; empty if disabled

`user_domain`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-user_domain.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domain")

### user_domain Type

`string`

## ldap_admin_group

Directory group of OpenBao administrators

`ldap_admin_group`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ldap_admin_group.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_admin_group")

### ldap_admin_group Type

`string`

## auto_initialize

OpenBao initializes itself with directory login when it starts uninitialized

`auto_initialize`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-auto_initialize.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/auto_initialize")

### auto_initialize Type

`boolean`

## notify_recipients

Email addresses notified when OpenBao is down or sealed

`notify_recipients`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-notify_recipients.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/notify_recipients")

### notify_recipients Type

`string[]`

## user_domains

User domains of the cluster

`user_domains`

* is required

* Type: `object[]` ([Details](get-configuration-output-properties-user_domains-items.md))

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-user_domains.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains")

### user_domains Type

`object[]` ([Details](get-configuration-output-properties-user_domains-items.md))

## smarthost_enabled

The cluster SMTP smarthost is enabled, so email notifications can be sent

`smarthost_enabled`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-smarthost_enabled.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/smarthost_enabled")

### smarthost_enabled Type

`boolean`

## ip_allowlist

Networks allowed through Traefik; empty: no restriction

`ip_allowlist`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ip_allowlist.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ip_allowlist")

### ip_allowlist Type

`string[]`

## ldap_group_policies



`ldap_group_policies`

* is required

* Type: `object[]` ([Details](get-configuration-output-properties-ldap_group_policies-items.md))

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ldap_group_policies.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies")

### ldap_group_policies Type

`object[]` ([Details](get-configuration-output-properties-ldap_group_policies-items.md))

## starter_kits



`starter_kits`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-starter_kits.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/starter_kits")

### starter_kits Type

`string[]`

## builtin_policies

Policies created by the module

`builtin_policies`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-builtin_policies.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/builtin_policies")

### builtin_policies Type

`string[]`

## vpn_api



`vpn_api`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-vpn_api.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/vpn_api")

### vpn_api Type

`boolean`

## vpn_api_url

Cluster network API URL; empty if disabled

`vpn_api_url`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-vpn_api_url.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/vpn_api_url")

### vpn_api_url Type

`string`

## transit_address



`transit_address`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-transit_address.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_address")

### transit_address Type

`string`

## transit_mount



`transit_mount`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-transit_mount.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_mount")

### transit_mount Type

`string`

## transit_key



`transit_key`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-transit_key.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_key")

### transit_key Type

`string`

## transit_tls_skip_verify



`transit_tls_skip_verify`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-transit_tls_skip_verify.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_tls_skip_verify")

### transit_tls_skip_verify Type

`boolean`

## transit_token_present

The Transit seal token was stored with openbao-transit-token

`transit_token_present`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-transit_token_present.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/transit_token_present")

### transit_token_present Type

`boolean`

## public_access



`public_access`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-public_access.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/public_access")

### public_access Type

`boolean`

## snapshot_keep



`snapshot_keep`

* is required

* Type: `integer`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-snapshot_keep.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/snapshot_keep")

### snapshot_keep Type

`integer`

### snapshot_keep Constraints

**minimum**: the value of this number must greater than or equal to: `0`
