# Untitled string in configure-module input Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_mount
```

Transit seal: mount path of the transit engine. Default 'transit'

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## transit_mount Type

`string`

## transit_mount Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^$|^[A-Za-z0-9_./-]{1,128}$
```

[try pattern](https://regexr.com/?expression=%5E%24%7C%5E%5BA-Za-z0-9_.%2F-%5D%7B1%2C128%7D%24 "try regular expression with regexr.com")
