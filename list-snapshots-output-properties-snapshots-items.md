# Untitled object in list-snapshots output Schema

```txt
http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-snapshots-output.json\*](openbao/list-snapshots-output.json "open original schema") |

## items Type

`object` ([Details](list-snapshots-output-properties-snapshots-items.md))

# items Properties

| Property            | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                       |
| :------------------ | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)       | `string`  | Required | cannot be null | [list-snapshots output](list-snapshots-output-properties-snapshots-items-properties-name.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots/items/properties/name")       |
| [size](#size)       | `integer` | Required | cannot be null | [list-snapshots output](list-snapshots-output-properties-snapshots-items-properties-size.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots/items/properties/size")       |
| [created](#created) | `integer` | Required | cannot be null | [list-snapshots output](list-snapshots-output-properties-snapshots-items-properties-created.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots/items/properties/created") |

## name



`name`

* is required

* Type: `string`

* cannot be null

* defined in: [list-snapshots output](list-snapshots-output-properties-snapshots-items-properties-name.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots/items/properties/name")

### name Type

`string`

## size



`size`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-snapshots output](list-snapshots-output-properties-snapshots-items-properties-size.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots/items/properties/size")

### size Type

`integer`

## created

Unix time

`created`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-snapshots output](list-snapshots-output-properties-snapshots-items-properties-created.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots/items/properties/created")

### created Type

`integer`
