# Untitled array in request-client-access input Schema

```txt
http://schema.nethserver.org/openbao/request-client-access-input.json#/properties/groups
```

Groups the module asks to join; the administrator decides

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                            |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [request-client-access-input.json\*](openbao/request-client-access-input.json "open original schema") |

## groups Type

`string[]`

## groups Constraints

**maximum number of items**: the maximum number of items for this array is: `8`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
