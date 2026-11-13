# Untitled string in get-configuration output Schema

```txt
http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_role
```

High availability role (experimental)

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                      |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [get-configuration-output.json\*](openbao/get-configuration-output.json "open original schema") |

## ha_role Type

`string`

## ha_role Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value          | Explanation |    |    |
| :------------- | :---------- | :- | :- |
| `"standalone"` |             |
| `"primary"`    |             |
| `"member"`     |             |
