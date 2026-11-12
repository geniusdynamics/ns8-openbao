# configure-module input Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json
```

Configure the OpenBao instance

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [configure-module-input.json](openbao/configure-module-input.json "open original schema") |

## configure-module input Type

`object` ([configure-module input](configure-module-input.md))

## configure-module input Examples

```json
{
  "host": "vault.example.org",
  "http2https": true,
  "lets_encrypt": true,
  "log_level": "info",
  "audit_log": true,
  "unseal_mode": "manual",
  "user_domain": "ad.example.org",
  "ldap_admin_group": "Domain Admins",
  "auto_initialize": false,
  "notify_recipients": [
    "security@example.org"
  ],
  "ip_allowlist": [
    "192.168.1.0/24",
    "10.0.0.5"
  ],
  "ldap_group_policies": [
    {
      "group": "Developers",
      "policy": "ns8-secrets-rw"
    }
  ],
  "starter_kits": [
    "kv",
    "pki"
  ],
  "vpn_api": false
}
```

```json
{
  "host": "vault.example.org"
}
```

```json
{
  "host": "vault.example.org",
  "unseal_mode": "transit",
  "transit_address": "https://kms.example.org:8200",
  "transit_mount": "transit",
  "transit_key": "ns8-openbao"
}
```

# configure-module input Properties

| Property                                            | Type      | Required | Nullable       | Defined by                                                                                                                                                                                    |
| :-------------------------------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [host](#host)                                       | `string`  | Required | cannot be null | [configure-module input](configure-module-input-properties-host.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/host")                                       |
| [http2https](#http2https)                           | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-http-to-https-redirection.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/http2https")            |
| [lets_encrypt](#lets_encrypt)                       | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-lets-encrypt-certificate.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/lets_encrypt")           |
| [log_level](#log_level)                             | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-server-log-level.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/log_level")                      |
| [audit_log](#audit_log)                             | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-audit-log.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/audit_log")                             |
| [unseal_mode](#unseal_mode)                         | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-unseal-mode.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/unseal_mode")                         |
| [user_domain](#user_domain)                         | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-user-domain.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/user_domain")                         |
| [ldap_admin_group](#ldap_admin_group)               | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-administrators-group.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_admin_group")           |
| [auto_initialize](#auto_initialize)                 | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-automatic-initialization.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/auto_initialize")        |
| [notify_recipients](#notify_recipients)             | `array`   | Optional | cannot be null | [configure-module input](configure-module-input-properties-notification-recipients.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/notify_recipients")       |
| [ip_allowlist](#ip_allowlist)                       | `array`   | Optional | cannot be null | [configure-module input](configure-module-input-properties-allowed-networks.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ip_allowlist")                   |
| [ldap_group_policies](#ldap_group_policies)         | `array`   | Optional | cannot be null | [configure-module input](configure-module-input-properties-group-policies.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies")              |
| [starter_kits](#starter_kits)                       | `array`   | Optional | cannot be null | [configure-module input](configure-module-input-properties-starter-kits.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/starter_kits")                       |
| [vpn_api](#vpn_api)                                 | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-cluster-network-api.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/vpn_api")                     |
| [transit_address](#transit_address)                 | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-transit_address.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_address")                 |
| [transit_mount](#transit_mount)                     | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-transit_mount.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_mount")                     |
| [transit_key](#transit_key)                         | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-transit_key.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_key")                         |
| [transit_tls_skip_verify](#transit_tls_skip_verify) | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-transit_tls_skip_verify.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_tls_skip_verify") |

## host

Fully qualified host name of the OpenBao API and web UI, like 'vault.example.org'

`host`

* is required

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-host.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/host")

### host Type

`string`

### host Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
\.
```

[try pattern](https://regexr.com/?expression=%5C. "try regular expression with regexr.com")

**hostname**: the string must be a hostname, according to [RFC 1123, section 2.1](https://tools.ietf.org/html/rfc1123 "check the specification")

## http2https

Redirect all HTTP requests to HTTPS. Defaults to true

`http2https`

* is optional

* Type: `boolean` ([HTTP to HTTPS redirection](configure-module-input-properties-http-to-https-redirection.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-http-to-https-redirection.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/http2https")

### http2https Type

`boolean` ([HTTP to HTTPS redirection](configure-module-input-properties-http-to-https-redirection.md))

### http2https Default Value

The default value is:

```json
true
```

## lets_encrypt

Request a valid Let's Encrypt certificate for the host name

`lets_encrypt`

* is optional

* Type: `boolean` ([Let's Encrypt certificate](configure-module-input-properties-lets-encrypt-certificate.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-lets-encrypt-certificate.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/lets_encrypt")

### lets_encrypt Type

`boolean` ([Let's Encrypt certificate](configure-module-input-properties-lets-encrypt-certificate.md))

## log_level

OpenBao server log level. Defaults to the current value, initially 'info'

`log_level`

* is optional

* Type: `string` ([Server log level](configure-module-input-properties-server-log-level.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-server-log-level.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/log_level")

### log_level Type

`string` ([Server log level](configure-module-input-properties-server-log-level.md))

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

Send the OpenBao audit log to the systemd journal. Defaults to the current value, initially false

`audit_log`

* is optional

* Type: `boolean` ([Audit log](configure-module-input-properties-audit-log.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-audit-log.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/audit_log")

### audit_log Type

`boolean` ([Audit log](configure-module-input-properties-audit-log.md))

## unseal_mode

'manual': Shamir unseal keys must be provided after every restart. 'auto': a static key stored on the node unseals OpenBao automatically. 'transit': an external OpenBao or Vault Transit engine unseals it (store its token first with openbao-transit-token). It can be changed only before OpenBao is initialized. Defaults to the current value, initially 'manual'

`unseal_mode`

* is optional

* Type: `string` ([Unseal mode](configure-module-input-properties-unseal-mode.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-unseal-mode.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/unseal_mode")

### unseal_mode Type

`string` ([Unseal mode](configure-module-input-properties-unseal-mode.md))

### unseal_mode Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value       | Explanation |    |    |
| :---------- | :---------- | :- | :- |
| `"manual"`  |             |
| `"auto"`    |             |
| `"transit"` |             |

## user_domain

NethServer 8 user domain (LDAP or Active Directory) used for OpenBao directory login. Empty string disables it. Defaults to the current value

`user_domain`

* is optional

* Type: `string` ([User domain](configure-module-input-properties-user-domain.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-user-domain.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/user_domain")

### user_domain Type

`string` ([User domain](configure-module-input-properties-user-domain.md))

## ldap_admin_group

Group of user_domain whose members get full administrative access to OpenBao. Required when user_domain is set

`ldap_admin_group`

* is optional

* Type: `string` ([Administrators group](configure-module-input-properties-administrators-group.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-administrators-group.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_admin_group")

### ldap_admin_group Type

`string` ([Administrators group](configure-module-input-properties-administrators-group.md))

## auto_initialize

Let OpenBao initialize itself with directory login already configured: no root token or recovery keys are generated. Requires unseal_mode 'auto', user_domain and ldap_admin_group. It has no effect once OpenBao is initialized

`auto_initialize`

* is optional

* Type: `boolean` ([Automatic initialization](configure-module-input-properties-automatic-initialization.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-automatic-initialization.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/auto_initialize")

### auto_initialize Type

`boolean` ([Automatic initialization](configure-module-input-properties-automatic-initialization.md))

## notify_recipients

Email addresses notified when OpenBao is down or sealed. The cluster SMTP smarthost is used. Empty list disables the notifications

`notify_recipients`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-notification-recipients.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/notify_recipients")

### notify_recipients Type

`string[]`

### notify_recipients Constraints

**maximum number of items**: the maximum number of items for this array is: `20`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## ip_allowlist

Client IP addresses or networks (CIDR) allowed to reach the OpenBao API and web UI through Traefik. Empty list: no restriction

`ip_allowlist`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-allowed-networks.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ip_allowlist")

### ip_allowlist Type

`string[]`

### ip_allowlist Constraints

**maximum number of items**: the maximum number of items for this array is: `100`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## ldap_group_policies

Additional directory groups mapped to OpenBao policies, applied by self-initialization or by openbao-apply-config

`ldap_group_policies`

* is optional

* Type: `object[]` ([Details](configure-module-input-properties-group-policies-items.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-group-policies.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies")

### ldap_group_policies Type

`object[]` ([Details](configure-module-input-properties-group-policies-items.md))

### ldap_group_policies Constraints

**maximum number of items**: the maximum number of items for this array is: `100`

## starter_kits

Components prepared by self-initialization or by openbao-apply-config: 'kv' key/value v2 store at secret/, 'pki' internal certificate authority at pki/, 'approle' application login

`starter_kits`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-starter-kits.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/starter_kits")

### starter_kits Type

`string[]`

### starter_kits Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## vpn_api

Also publish the OpenBao API on the node cluster VPN address (third module TCP port), for NethServer modules and services of the cluster

`vpn_api`

* is optional

* Type: `boolean` ([Cluster network API](configure-module-input-properties-cluster-network-api.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-cluster-network-api.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/vpn_api")

### vpn_api Type

`boolean` ([Cluster network API](configure-module-input-properties-cluster-network-api.md))

## transit_address

Transit seal: URL of the external OpenBao or Vault, like <https://vault.example.org:8200>

`transit_address`

* is optional

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-transit_address.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_address")

### transit_address Type

`string`

### transit_address Constraints

**maximum length**: the maximum number of characters for this string is: `512`

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^$|^https?://
```

[try pattern](https://regexr.com/?expression=%5E%24%7C%5Ehttps%3F%3A%2F%2F "try regular expression with regexr.com")

## transit_mount

Transit seal: mount path of the transit engine. Default 'transit'

`transit_mount`

* is optional

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-transit_mount.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_mount")

### transit_mount Type

`string`

### transit_mount Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^$|^[A-Za-z0-9_./-]{1,128}$
```

[try pattern](https://regexr.com/?expression=%5E%24%7C%5E%5BA-Za-z0-9_.%2F-%5D%7B1%2C128%7D%24 "try regular expression with regexr.com")

## transit_key

Transit seal: name of the transit key

`transit_key`

* is optional

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-transit_key.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_key")

### transit_key Type

`string`

### transit_key Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^$|^[A-Za-z0-9_.-]{1,128}$
```

[try pattern](https://regexr.com/?expression=%5E%24%7C%5E%5BA-Za-z0-9_.-%5D%7B1%2C128%7D%24 "try regular expression with regexr.com")

## transit_tls_skip_verify

Transit seal: do not verify the TLS certificate of the external server

`transit_tls_skip_verify`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-transit_tls_skip_verify.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_tls_skip_verify")

### transit_tls_skip_verify Type

`boolean`
