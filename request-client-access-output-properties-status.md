# Untitled string in request-client-access output Schema

```txt
http://schema.nethserver.org/openbao/request-client-access-output.json#/properties/status
```

stale: approved for a previous installation with the same module ID

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                              |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [request-client-access-output.json\*](openbao/request-client-access-output.json "open original schema") |

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
