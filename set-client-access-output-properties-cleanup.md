# Untitled string in set-client-access output Schema

```txt
http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/cleanup
```

pending: OpenBao was not available; tokens are revoked by openbao-maintenance

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                      |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [set-client-access-output.json\*](openbao/set-client-access-output.json "open original schema") |

## cleanup Type

`string`

## cleanup Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value       | Explanation |    |    |
| :---------- | :---------- | :- | :- |
| `"none"`    |             |
| `"done"`    |             |
| `"pending"` |             |
