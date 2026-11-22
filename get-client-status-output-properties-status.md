# Untitled string in get-client-status output Schema

```txt
http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/status
```

stale: approved for a previous installation with the same module ID

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                      |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [get-client-status-output.json\*](openbao/get-client-status-output.json "open original schema") |

## status Type

`string`

## status Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value        | Explanation |    |    |
| :----------- | :---------- | :- | :- |
| `"none"`     |             |
| `"pending"`  |             |
| `"approved"` |             |
| `"stale"`    |             |
