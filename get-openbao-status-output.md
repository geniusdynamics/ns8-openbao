# get-openbao-status output Schema

```txt
http://schema.nethserver.org/openbao/get-openbao-status-output.json
```

Get the OpenBao server state: initialization and seal status

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-openbao-status-output.json](openbao/get-openbao-status-output.json "open original schema") |

## get-openbao-status output Type

`object` ([get-openbao-status output](get-openbao-status-output.md))

## get-openbao-status output Examples

```json
{
  "service_active": true,
  "reachable": true,
  "initialized": true,
  "sealed": false,
  "seal_type": "shamir",
  "version": "2.7.2",
  "threshold": 3,
  "shares": 5,
  "progress": 0,
  "unseal_mode": "manual",
  "ui_url": "https://vault.example.org/ui/",
  "user_domain": "ad.example.org",
  "module_token": "valid",
  "root_token_present": false
}
```

# get-openbao-status output Properties

| Property                                  | Type      | Required | Nullable       | Defined by                                                                                                                                                                                   |
| :---------------------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [service_active](#service_active)         | `boolean` | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-service_active.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/service_active")         |
| [reachable](#reachable)                   | `boolean` | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-reachable.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/reachable")                   |
| [initialized](#initialized)               | `boolean` | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-initialized.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/initialized")               |
| [sealed](#sealed)                         | `boolean` | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-sealed.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/sealed")                         |
| [seal_type](#seal_type)                   | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-seal_type.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/seal_type")                   |
| [version](#version)                       | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-version.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/version")                       |
| [threshold](#threshold)                   | `integer` | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-threshold.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/threshold")                   |
| [shares](#shares)                         | `integer` | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-shares.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/shares")                         |
| [progress](#progress)                     | `integer` | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-progress.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/progress")                     |
| [unseal_mode](#unseal_mode)               | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-unseal_mode.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/unseal_mode")               |
| [ui_url](#ui_url)                         | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ui_url.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ui_url")                         |
| [user_domain](#user_domain)               | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-user_domain.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/user_domain")               |
| [module_token](#module_token)             | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-module_token.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/module_token")             |
| [root_token_present](#root_token_present) | `boolean` | Required | can be null    | [get-openbao-status output](get-openbao-status-output-properties-root_token_present.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/root_token_present") |

## service_active

The openbao.service unit is active

`service_active`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-service_active.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/service_active")

### service_active Type

`boolean`

## reachable

The OpenBao API answered

`reachable`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-reachable.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/reachable")

### reachable Type

`boolean`

## initialized



`initialized`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-initialized.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/initialized")

### initialized Type

`boolean`

## sealed



`sealed`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-sealed.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/sealed")

### sealed Type

`boolean`

## seal_type

'shamir' or 'static'; empty if unknown

`seal_type`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-seal_type.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/seal_type")

### seal_type Type

`string`

## version



`version`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-version.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/version")

### version Type

`string`

## threshold

Number of key shares required to unseal

`threshold`

* is required

* Type: `integer`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-threshold.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/threshold")

### threshold Type

`integer`

### threshold Constraints

**minimum**: the value of this number must greater than or equal to: `0`

## shares

Total number of key shares

`shares`

* is required

* Type: `integer`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-shares.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/shares")

### shares Type

`integer`

### shares Constraints

**minimum**: the value of this number must greater than or equal to: `0`

## progress

Key shares provided so far for the current unseal

`progress`

* is required

* Type: `integer`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-progress.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/progress")

### progress Type

`integer`

### progress Constraints

**minimum**: the value of this number must greater than or equal to: `0`

## unseal_mode



`unseal_mode`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-unseal_mode.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/unseal_mode")

### unseal_mode Type

`string`

### unseal_mode Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value       | Explanation |    |    |
| :---------- | :---------- | :- | :- |
| `"manual"`  |             |
| `"auto"`    |             |
| `"transit"` |             |

## ui_url

OpenBao web UI URL; empty if the host name is not configured

`ui_url`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ui_url.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ui_url")

### ui_url Type

`string`

## user_domain

User domain used for directory login; empty if disabled

`user_domain`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-user_domain.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/user_domain")

### user_domain Type

`string`

## module_token

State of the module token used for snapshots and root token detection

`module_token`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-module_token.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/module_token")

### module_token Type

`string`

### module_token Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value       | Explanation |    |    |
| :---------- | :---------- | :- | :- |
| `"missing"` |             |
| `"valid"`   |             |
| `"invalid"` |             |
| `"unknown"` |             |

## root_token_present

A root token exists; null if unknown (no module token, sealed, or too many tokens)

`root_token_present`

* is required

* Type: `boolean`

* can be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-root_token_present.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/root_token_present")

### root_token_present Type

`boolean`
