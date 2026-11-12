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
  ]
}
```

```json
{
  "host": "vault.example.org"
}
```

# configure-module input Properties

| Property                                | Type      | Required | Nullable       | Defined by                                                                                                                                                                              |
| :-------------------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [host](#host)                           | `string`  | Required | cannot be null | [configure-module input](configure-module-input-properties-host.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/host")                                 |
| [http2https](#http2https)               | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-http-to-https-redirection.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/http2https")      |
| [lets_encrypt](#lets_encrypt)           | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-lets-encrypt-certificate.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/lets_encrypt")     |
| [log_level](#log_level)                 | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-server-log-level.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/log_level")                |
| [audit_log](#audit_log)                 | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-audit-log.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/audit_log")                       |
| [unseal_mode](#unseal_mode)             | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-unseal-mode.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/unseal_mode")                   |
| [user_domain](#user_domain)             | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-user-domain.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/user_domain")                   |
| [ldap_admin_group](#ldap_admin_group)   | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-administrators-group.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_admin_group")     |
| [auto_initialize](#auto_initialize)     | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-automatic-initialization.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/auto_initialize")  |
| [notify_recipients](#notify_recipients) | `array`   | Optional | cannot be null | [configure-module input](configure-module-input-properties-notification-recipients.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/notify_recipients") |

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

'manual': Shamir unseal keys must be provided after every restart. 'auto': a static key stored on the node unseals OpenBao automatically. It can be changed only before OpenBao is initialized. Defaults to the current value, initially 'manual'

`unseal_mode`

* is optional

* Type: `string` ([Unseal mode](configure-module-input-properties-unseal-mode.md))

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-unseal-mode.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/unseal_mode")

### unseal_mode Type

`string` ([Unseal mode](configure-module-input-properties-unseal-mode.md))

### unseal_mode Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |    |    |
| :--------- | :---------- | :- | :- |
| `"manual"` |             |
| `"auto"`   |             |

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
