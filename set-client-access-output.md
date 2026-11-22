# set-client-access output Schema

```txt
http://schema.nethserver.org/openbao/set-client-access-output.json
```

Effective access of the client module

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                    |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [set-client-access-output.json](openbao/set-client-access-output.json "open original schema") |

## set-client-access output Type

`object` ([set-client-access output](set-client-access-output.md))

## set-client-access output Examples

```json
{
  "module_id": "kumomta1",
  "allowed": false,
  "database_engine": false,
  "groups": [],
  "cleanup": "done"
}
```

# set-client-access output Properties

| Property                            | Type      | Required | Nullable       | Defined by                                                                                                                                                                          |
| :---------------------------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [module_id](#module_id)             | `string`  | Required | cannot be null | [set-client-access output](set-client-access-output-properties-module_id.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/module_id")             |
| [allowed](#allowed)                 | `boolean` | Required | cannot be null | [set-client-access output](set-client-access-output-properties-allowed.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/allowed")                 |
| [database_engine](#database_engine) | `boolean` | Required | cannot be null | [set-client-access output](set-client-access-output-properties-database_engine.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/database_engine") |
| [groups](#groups)                   | `array`   | Required | cannot be null | [set-client-access output](set-client-access-output-properties-groups.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/groups")                   |
| [cleanup](#cleanup)                 | `string`  | Required | cannot be null | [set-client-access output](set-client-access-output-properties-cleanup.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/cleanup")                 |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [set-client-access output](set-client-access-output-properties-module_id.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/module_id")

### module_id Type

`string`

## allowed



`allowed`

* is required

* Type: `boolean`

* cannot be null

* defined in: [set-client-access output](set-client-access-output-properties-allowed.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/allowed")

### allowed Type

`boolean`

## database_engine



`database_engine`

* is required

* Type: `boolean`

* cannot be null

* defined in: [set-client-access output](set-client-access-output-properties-database_engine.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/database_engine")

### database_engine Type

`boolean`

## groups



`groups`

* is required

* Type: `string[]`

* cannot be null

* defined in: [set-client-access output](set-client-access-output-properties-groups.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/groups")

### groups Type

`string[]`

## cleanup

pending: OpenBao was not available; tokens are revoked by openbao-maintenance

`cleanup`

* is required

* Type: `string`

* cannot be null

* defined in: [set-client-access output](set-client-access-output-properties-cleanup.md "http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/cleanup")

### cleanup Type

`string`

### cleanup Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value       | Explanation |    |    |
| :---------- | :---------- | :- | :- |
| `"none"`    |             |
| `"done"`    |             |
| `"pending"` |             |
