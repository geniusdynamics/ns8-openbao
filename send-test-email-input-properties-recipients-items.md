# Untitled string in send-test-email input Schema

```txt
http://schema.nethserver.org/openbao/send-test-email-input.json#/properties/recipients/items
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [send-test-email-input.json\*](openbao/send-test-email-input.json "open original schema") |

## items Type

`string`

## items Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[^@\s,]+@[^@\s,]+$
```

[try pattern](https://regexr.com/?expression=%5E%5B%5E%40%5Cs%2C%5D%2B%40%5B%5E%40%5Cs%2C%5D%2B%24 "try regular expression with regexr.com")

**email**: the string must be an email address, according to [RFC 5322, section 3.4.1](https://tools.ietf.org/html/rfc5322 "check the specification")
