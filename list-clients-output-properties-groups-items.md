# Untitled object in list-clients output Schema

```txt
http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-clients-output.json\*](openbao/list-clients-output.json "open original schema") |

## items Type

`object` ([Details](list-clients-output-properties-groups-items.md))

# items Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                                                               |
| :---------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [group_id](#group_id)   | `string` | Required | cannot be null | [list-clients output](list-clients-output-properties-groups-items-properties-group_id.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups/items/properties/group_id")   |
| [kv_prefix](#kv_prefix) | `string` | Required | cannot be null | [list-clients output](list-clients-output-properties-groups-items-properties-kv_prefix.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups/items/properties/kv_prefix") |
| [members](#members)     | `array`  | Required | cannot be null | [list-clients output](list-clients-output-properties-groups-items-properties-members.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups/items/properties/members")     |

## group_id



`group_id`

* is required

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-groups-items-properties-group_id.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups/items/properties/group_id")

### group_id Type

`string`

## kv_prefix



`kv_prefix`

* is required

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-groups-items-properties-kv_prefix.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups/items/properties/kv_prefix")

### kv_prefix Type

`string`

## members



`members`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-groups-items-properties-members.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups/items/properties/members")

### members Type

`string[]`
