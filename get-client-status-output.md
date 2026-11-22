# get-client-status output Schema

```txt
http://schema.nethserver.org/openbao/get-client-status-output.json
```

Client provisioning status of one module: no secrets

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                    |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-client-status-output.json](openbao/get-client-status-output.json "open original schema") |

## get-client-status output Type

`object` ([get-client-status output](get-client-status-output.md))

## get-client-status output Examples

```json
{
  "module_id": "kumomta1",
  "openbao_module_id": "openbao1",
  "client_provisioning": true,
  "ready": true,
  "status": "pending",
  "database_engine": false,
  "database_engine_requested": false,
  "groups": [],
  "groups_requested": [
    "kumomta-cluster"
  ],
  "address": "http://10.5.4.1:20003",
  "address_type": "vpn",
  "kv_mount": "ns8-kv",
  "kv_prefix": "modules/kumomta1"
}
```

# get-client-status output Properties

| Property                                                | Type      | Required | Nullable       | Defined by                                                                                                                                                                                              |
| :------------------------------------------------------ | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [module_id](#module_id)                                 | `string`  | Required | cannot be null | [get-client-status output](get-client-status-output-properties-module_id.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/module_id")                                 |
| [openbao_module_id](#openbao_module_id)                 | `string`  | Required | cannot be null | [get-client-status output](get-client-status-output-properties-openbao_module_id.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/openbao_module_id")                 |
| [client_provisioning](#client_provisioning)             | `boolean` | Required | cannot be null | [get-client-status output](get-client-status-output-properties-client_provisioning.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/client_provisioning")             |
| [ready](#ready)                                         | `boolean` | Required | cannot be null | [get-client-status output](get-client-status-output-properties-ready.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/ready")                                         |
| [status](#status)                                       | `string`  | Required | cannot be null | [get-client-status output](get-client-status-output-properties-status.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/status")                                       |
| [database_engine](#database_engine)                     | `boolean` | Required | cannot be null | [get-client-status output](get-client-status-output-properties-database_engine.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/database_engine")                     |
| [database_engine_requested](#database_engine_requested) | `boolean` | Required | cannot be null | [get-client-status output](get-client-status-output-properties-database_engine_requested.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/database_engine_requested") |
| [groups](#groups)                                       | `array`   | Required | cannot be null | [get-client-status output](get-client-status-output-properties-groups.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/groups")                                       |
| [groups_requested](#groups_requested)                   | `array`   | Required | cannot be null | [get-client-status output](get-client-status-output-properties-groups_requested.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/groups_requested")                   |
| [address](#address)                                     | `string`  | Required | cannot be null | [get-client-status output](get-client-status-output-properties-address.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/address")                                     |
| [address_type](#address_type)                           | `string`  | Required | cannot be null | [get-client-status output](get-client-status-output-properties-address_type.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/address_type")                           |
| [kv_mount](#kv_mount)                                   | `string`  | Required | cannot be null | [get-client-status output](get-client-status-output-properties-kv_mount.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/kv_mount")                                   |
| [kv_prefix](#kv_prefix)                                 | `string`  | Required | cannot be null | [get-client-status output](get-client-status-output-properties-kv_prefix.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/kv_prefix")                                 |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-module_id.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/module_id")

### module_id Type

`string`

## openbao_module_id



`openbao_module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-openbao_module_id.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/openbao_module_id")

### openbao_module_id Type

`string`

## client_provisioning



`client_provisioning`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-client_provisioning.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/client_provisioning")

### client_provisioning Type

`boolean`

## ready

Provisioning is enabled, the provisioner token is valid and an address is available

`ready`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-ready.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/ready")

### ready Type

`boolean`

## status

stale: approved for a previous installation with the same module ID

`status`

* is required

* Type: `string`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-status.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/status")

### status Type

`string`

### status Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value        | Explanation |    |    |
| :----------- | :---------- | :- | :- |
| `"none"`     |             |
| `"pending"`  |             |
| `"approved"` |             |
| `"stale"`    |             |

## database_engine



`database_engine`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-database_engine.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/database_engine")

### database_engine Type

`boolean`

## database_engine_requested



`database_engine_requested`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-database_engine_requested.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/database_engine_requested")

### database_engine_requested Type

`boolean`

## groups



`groups`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-groups.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/groups")

### groups Type

`string[]`

## groups_requested



`groups_requested`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-groups_requested.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/groups_requested")

### groups_requested Type

`string[]`

## address



`address`

* is required

* Type: `string`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-address.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/address")

### address Type

`string`

## address_type



`address_type`

* is required

* Type: `string`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-address_type.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/address_type")

### address_type Type

`string`

## kv_mount



`kv_mount`

* is required

* Type: `string`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-kv_mount.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/kv_mount")

### kv_mount Type

`string`

## kv_prefix



`kv_prefix`

* is required

* Type: `string`

* cannot be null

* defined in: [get-client-status output](get-client-status-output-properties-kv_prefix.md "http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/kv_prefix")

### kv_prefix Type

`string`
