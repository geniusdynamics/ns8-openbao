# provision-client output Schema

```txt
http://schema.nethserver.org/openbao/provision-client-output.json
```

A wrapped OpenBao token and how to use it. The wrapping tokens are single use and expire after wrap_ttl seconds

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [provision-client-output.json](openbao/provision-client-output.json "open original schema") |

## provision-client output Type

`object` ([provision-client output](provision-client-output.md))

## provision-client output Examples

```json
{
  "module_id": "postgresql19c1",
  "openbao_module_id": "openbao1",
  "address": "http://10.5.4.1:20003",
  "address_type": "vpn",
  "wrapped_token": "s.WRAPPINGTOKEN",
  "wrap_ttl": 120,
  "wrap_creation_path": "auth/token/create/ns8-client",
  "token_role": "ns8-client",
  "token_policies": [
    "default",
    "ns8-client-kv"
  ],
  "token_period": 86400,
  "token_explicit_max_ttl": 2592000,
  "kv_mount": "ns8-kv",
  "kv_version": 2,
  "kv_prefix": "modules/postgresql19c1",
  "database_engine": false,
  "database_mount": "",
  "groups": []
}
```

# provision-client output Properties

| Property                                          | Type      | Required | Nullable       | Defined by                                                                                                                                                                                     |
| :------------------------------------------------ | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [module_id](#module_id)                           | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-module_id.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/module_id")                           |
| [openbao_module_id](#openbao_module_id)           | `string`  | Optional | cannot be null | [provision-client output](provision-client-output-properties-openbao_module_id.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/openbao_module_id")           |
| [address](#address)                               | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-address.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/address")                               |
| [address_type](#address_type)                     | `string`  | Optional | cannot be null | [provision-client output](provision-client-output-properties-address_type.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/address_type")                     |
| [wrapped_token](#wrapped_token)                   | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-wrapped_token.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/wrapped_token")                   |
| [wrap_ttl](#wrap_ttl)                             | `integer` | Required | cannot be null | [provision-client output](provision-client-output-properties-wrap_ttl.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/wrap_ttl")                             |
| [wrap_creation_path](#wrap_creation_path)         | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-wrap_creation_path.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/wrap_creation_path")         |
| [token_role](#token_role)                         | `string`  | Optional | cannot be null | [provision-client output](provision-client-output-properties-token_role.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/token_role")                         |
| [token_policies](#token_policies)                 | `array`   | Optional | cannot be null | [provision-client output](provision-client-output-properties-token_policies.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/token_policies")                 |
| [token_period](#token_period)                     | `integer` | Optional | cannot be null | [provision-client output](provision-client-output-properties-token_period.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/token_period")                     |
| [token_explicit_max_ttl](#token_explicit_max_ttl) | `integer` | Optional | cannot be null | [provision-client output](provision-client-output-properties-token_explicit_max_ttl.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/token_explicit_max_ttl") |
| [kv_mount](#kv_mount)                             | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-kv_mount.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/kv_mount")                             |
| [kv_version](#kv_version)                         | `integer` | Optional | cannot be null | [provision-client output](provision-client-output-properties-kv_version.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/kv_version")                         |
| [kv_prefix](#kv_prefix)                           | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-kv_prefix.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/kv_prefix")                           |
| [database_engine](#database_engine)               | `boolean` | Required | cannot be null | [provision-client output](provision-client-output-properties-database_engine.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/database_engine")               |
| [database_mount](#database_mount)                 | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-database_mount.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/database_mount")                 |
| [groups](#groups)                                 | `array`   | Required | cannot be null | [provision-client output](provision-client-output-properties-groups.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups")                                 |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-module_id.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/module_id")

### module_id Type

`string`

## openbao_module_id



`openbao_module_id`

* is optional

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-openbao_module_id.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/openbao_module_id")

### openbao_module_id Type

`string`

## address

OpenBao API base URL for the client

`address`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-address.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/address")

### address Type

`string`

## address_type



`address_type`

* is optional

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-address_type.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/address_type")

### address_type Type

`string`

### address_type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |    |    |
| :--------- | :---------- | :- | :- |
| `"vpn"`    |             |
| `"public"` |             |

## wrapped_token

Response-wrapping token: POST it to sys/wrapping/unwrap within wrap_ttl seconds

`wrapped_token`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-wrapped_token.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/wrapped_token")

### wrapped_token Type

`string`

## wrap_ttl



`wrap_ttl`

* is required

* Type: `integer`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-wrap_ttl.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/wrap_ttl")

### wrap_ttl Type

`integer`

## wrap_creation_path

Expected creation_path of the wrapping token (check it with sys/wrapping/lookup)

`wrap_creation_path`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-wrap_creation_path.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/wrap_creation_path")

### wrap_creation_path Type

`string`

## token_role



`token_role`

* is optional

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-token_role.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/token_role")

### token_role Type

`string`

## token_policies



`token_policies`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-token_policies.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/token_policies")

### token_policies Type

`string[]`

## token_period

Seconds: renew the token (auth/token/renew-self) before it elapses

`token_period`

* is optional

* Type: `integer`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-token_period.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/token_period")

### token_period Type

`integer`

## token_explicit_max_ttl

Seconds: the token cannot live longer; provision again before

`token_explicit_max_ttl`

* is optional

* Type: `integer`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-token_explicit_max_ttl.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/token_explicit_max_ttl")

### token_explicit_max_ttl Type

`integer`

## kv_mount



`kv_mount`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-kv_mount.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/kv_mount")

### kv_mount Type

`string`

## kv_version



`kv_version`

* is optional

* Type: `integer`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-kv_version.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/kv_version")

### kv_version Type

`integer`

## kv_prefix



`kv_prefix`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-kv_prefix.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/kv_prefix")

### kv_prefix Type

`string`

## database_engine



`database_engine`

* is required

* Type: `boolean`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-database_engine.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/database_engine")

### database_engine Type

`boolean`

## database_mount



`database_mount`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-database_mount.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/database_mount")

### database_mount Type

`string`

## groups



`groups`

* is required

* Type: `object[]` ([Details](provision-client-output-properties-groups-items.md))

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-groups.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups")

### groups Type

`object[]` ([Details](provision-client-output-properties-groups-items.md))
