# Untitled object in list-clients output Schema

```txt
http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-clients-output.json\*](openbao/list-clients-output.json "open original schema") |

## items Type

`object` ([Details](list-clients-output-properties-clients-items.md))

# items Properties

| Property                                                | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                                 |
| :------------------------------------------------------ | :-------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [module_id](#module_id)                                 | `string`  | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-module_id.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/module_id")                                 |
| [module_uuid](#module_uuid)                             | `string`  | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-module_uuid.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/module_uuid")                             |
| [installed](#installed)                                 | `boolean` | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-installed.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/installed")                                 |
| [status](#status)                                       | `string`  | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-status.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/status")                                       |
| [database_engine](#database_engine)                     | `boolean` | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-database_engine.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/database_engine")                     |
| [database_engine_requested](#database_engine_requested) | `boolean` | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-database_engine_requested.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/database_engine_requested") |
| [groups](#groups)                                       | `array`   | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-groups.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/groups")                                       |
| [groups_requested](#groups_requested)                   | `array`   | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-groups_requested.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/groups_requested")                   |
| [approved_at](#approved_at)                             | `integer` | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-approved_at.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/approved_at")                             |
| [requested_at](#requested_at)                           | `integer` | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-requested_at.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/requested_at")                           |
| [tokens](#tokens)                                       | `integer` | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-tokens.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/tokens")                                       |
| [last_issued_at](#last_issued_at)                       | `integer` | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-last_issued_at.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/last_issued_at")                       |
| [cleanup_pending](#cleanup_pending)                     | `boolean` | Required | cannot be null | [list-clients output](list-clients-output-properties-clients-items-properties-cleanup_pending.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/cleanup_pending")                     |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-module_id.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/module_id")

### module_id Type

`string`

## module_uuid



`module_uuid`

* is required

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-module_uuid.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/module_uuid")

### module_uuid Type

`string`

## installed



`installed`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-installed.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/installed")

### installed Type

`boolean`

## status



`status`

* is required

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-status.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/status")

### status Type

`string`

### status Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value               | Explanation |    |    |
| :------------------ | :---------- | :- | :- |
| `"approved"`        |             |
| `"pending"`         |             |
| `"stale"`           |             |
| `"cleanup_pending"` |             |

## database_engine



`database_engine`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-database_engine.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/database_engine")

### database_engine Type

`boolean`

## database_engine_requested



`database_engine_requested`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-database_engine_requested.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/database_engine_requested")

### database_engine_requested Type

`boolean`

## groups



`groups`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-groups.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/groups")

### groups Type

`string[]`

## groups_requested



`groups_requested`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-groups_requested.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/groups_requested")

### groups_requested Type

`string[]`

## approved_at



`approved_at`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-approved_at.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/approved_at")

### approved_at Type

`integer`

## requested_at



`requested_at`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-requested_at.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/requested_at")

### requested_at Type

`integer`

## tokens

Tokens issued and not past their maximum TTL

`tokens`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-tokens.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/tokens")

### tokens Type

`integer`

## last_issued_at



`last_issued_at`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-last_issued_at.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/last_issued_at")

### last_issued_at Type

`integer`

## cleanup_pending



`cleanup_pending`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients-items-properties-cleanup_pending.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/cleanup_pending")

### cleanup_pending Type

`boolean`
