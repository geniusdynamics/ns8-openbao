# Untitled string in list-clients output Schema

```txt
http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/status
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [list-clients-output.json\*](openbao/list-clients-output.json "open original schema") |

## status Type

`string`

## status Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value               | Explanation |    |    |
| :------------------ | :---------- | :- | :- |
| `"approved"`        |             |
| `"pending"`         |             |
| `"stale"`           |             |
| `"cleanup_pending"` |             |
