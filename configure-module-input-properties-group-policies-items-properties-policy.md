# Untitled string in configure-module input Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies/items/properties/policy
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## policy Type

`string`

## policy Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[A-Za-z0-9_.-]{1,128}$
```

[try pattern](https://regexr.com/?expression=%5E%5BA-Za-z0-9_.-%5D%7B1%2C128%7D%24 "try regular expression with regexr.com")
