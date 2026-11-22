# set-client-access input Schema

```txt
http://schema.nethserver.org/openbao/set-client-access-input.json
```

Approve or revoke a client module. An approval binds the module ID to its current MODULE_UUID

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [set-client-access-input.json](openbao/set-client-access-input.json "open original schema") |

## set-client-access input Type

`object` ([set-client-access input](set-client-access-input.md))

## set-client-access input Examples

```json
{
  "module_id": "postgresql19c1",
  "allowed": true,
  "database_engine": true
}
```

```json
{
  "module_id": "kumomta1",
  "allowed": true,
  "groups": [
    "kumomta-cluster"
  ]
}
```

```json
{
  "module_id": "kumomta1",
  "allowed": false,
  "delete_data": false
}
```

# set-client-access input Properties

| Property                            | Type      | Required | Nullable       | Defined by                                                                                                                                                                       |
| :---------------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [module_id](#module_id)             | `string`  | Required | cannot be null | [set-client-access input](set-client-access-input-properties-module_id.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/module_id")             |
| [allowed](#allowed)                 | `boolean` | Required | cannot be null | [set-client-access input](set-client-access-input-properties-allowed.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/allowed")                 |
| [database_engine](#database_engine) | `boolean` | Optional | cannot be null | [set-client-access input](set-client-access-input-properties-database_engine.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/database_engine") |
| [groups](#groups)                   | `array`   | Optional | cannot be null | [set-client-access input](set-client-access-input-properties-groups.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/groups")                   |
| [delete_data](#delete_data)         | `boolean` | Optional | cannot be null | [set-client-access input](set-client-access-input-properties-delete_data.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/delete_data")         |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [set-client-access input](set-client-access-input-properties-module_id.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/module_id")

### module_id Type

`string`

### module_id Constraints

**maximum length**: the maximum number of characters for this string is: `64`

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[a-z][a-z0-9-]{0,62}[0-9]$
```

[try pattern](https://regexr.com/?expression=%5E%5Ba-z%5D%5Ba-z0-9-%5D%7B0%2C62%7D%5B0-9%5D%24 "try regular expression with regexr.com")

## allowed



`allowed`

* is required

* Type: `boolean`

* cannot be null

* defined in: [set-client-access input](set-client-access-input-properties-allowed.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/allowed")

### allowed Type

`boolean`

## database_engine

Approve the database secrets engine mounted at ns8-db-<module id>/

`database_engine`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [set-client-access input](set-client-access-input-properties-database_engine.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/database_engine")

### database_engine Type

`boolean`

## groups

Shared groups: KV prefix groups/<group id>/ of the ns8-kv mount. A group ID ends with a letter

`groups`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [set-client-access input](set-client-access-input-properties-groups.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/groups")

### groups Type

`string[]`

### groups Constraints

**maximum number of items**: the maximum number of items for this array is: `8`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## delete_data

On revoke: also delete the module KV prefix and its database secrets engine

`delete_data`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [set-client-access input](set-client-access-input-properties-delete_data.md "http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/delete_data")

### delete_data Type

`boolean`
