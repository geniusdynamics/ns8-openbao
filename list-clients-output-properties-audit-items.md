# Untitled object in list-clients output Schema

```txt
http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-clients-output.json\*](openbao/list-clients-output.json "open original schema") |

## items Type

`object` ([Details](list-clients-output-properties-audit-items.md))

# items Properties

| Property                | Type      | Required | Nullable       | Defined by                                                                                                                                                                                             |
| :---------------------- | :-------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [time](#time)           | `integer` | Required | cannot be null | [list-clients output](list-clients-output-properties-audit-items-properties-time.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit/items/properties/time")           |
| [event](#event)         | `string`  | Required | cannot be null | [list-clients output](list-clients-output-properties-audit-items-properties-event.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit/items/properties/event")         |
| [module_id](#module_id) | `string`  | Required | cannot be null | [list-clients output](list-clients-output-properties-audit-items-properties-module_id.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit/items/properties/module_id") |

## time



`time`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-audit-items-properties-time.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit/items/properties/time")

### time Type

`integer`

## event



`event`

* is required

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-audit-items-properties-event.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit/items/properties/event")

### event Type

`string`

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-audit-items-properties-module_id.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit/items/properties/module_id")

### module_id Type

`string`
