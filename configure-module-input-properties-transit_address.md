# Untitled string in configure-module input Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/transit_address
```

Transit seal: URL of the external OpenBao or Vault, like <https://vault.example.org:8200>

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## transit_address Type

`string`

## transit_address Constraints

**maximum length**: the maximum number of characters for this string is: `512`

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^$|^https?://
```

[try pattern](https://regexr.com/?expression=%5E%24%7C%5Ehttps%3F%3A%2F%2F "try regular expression with regexr.com")
