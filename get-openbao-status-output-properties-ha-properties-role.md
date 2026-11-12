# Untitled string in get-openbao-status output Schema

```txt
http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/role
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                        |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [get-openbao-status-output.json\*](openbao/get-openbao-status-output.json "open original schema") |

## role Type

`string`

## role Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value          | Explanation |    |    |
| :------------- | :---------- | :- | :- |
| `"standalone"` |             |
| `"primary"`    |             |
| `"member"`     |             |
