# Untitled string in request-client-access input Schema

```txt
http://schema.nethserver.org/openbao/request-client-access-input.json#/properties/groups/items
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                            |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [request-client-access-input.json\*](openbao/request-client-access-input.json "open original schema") |

## items Type

`string`

## items Constraints

**maximum length**: the maximum number of characters for this string is: `64`

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[a-z][a-z0-9-]{0,62}[a-z]$
```

[try pattern](https://regexr.com/?expression=%5E%5Ba-z%5D%5Ba-z0-9-%5D%7B0%2C62%7D%5Ba-z%5D%24 "try regular expression with regexr.com")
