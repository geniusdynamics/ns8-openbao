# Untitled string in get-openbao-status output Schema

```txt
http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/unseal_mode
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                        |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [get-openbao-status-output.json\*](openbao/get-openbao-status-output.json "open original schema") |

## unseal_mode Type

`string`

## unseal_mode Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value       | Explanation |    |    |
| :---------- | :---------- | :- | :- |
| `"manual"`  |             |
| `"auto"`    |             |
| `"transit"` |             |
