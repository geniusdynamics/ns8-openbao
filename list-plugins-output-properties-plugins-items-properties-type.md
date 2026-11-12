# Untitled string in list-plugins output Schema

```txt
http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/type
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [list-plugins-output.json\*](openbao/list-plugins-output.json "open original schema") |

## type Type

`string`

## type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value        | Explanation |    |    |
| :----------- | :---------- | :- | :- |
| `"auth"`     |             |
| `"secret"`   |             |
| `"database"` |             |
