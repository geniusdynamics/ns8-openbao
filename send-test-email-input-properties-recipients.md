# Untitled array in send-test-email input Schema

```txt
http://schema.nethserver.org/openbao/send-test-email-input.json#/properties/recipients
```

Recipients of the test email. Defaults to the configured notification recipients

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [send-test-email-input.json\*](openbao/send-test-email-input.json "open original schema") |

## recipients Type

`string[]`

## recipients Constraints

**maximum number of items**: the maximum number of items for this array is: `20`

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
