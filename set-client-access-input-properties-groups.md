# Untitled array in set-client-access input Schema

```txt
http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/groups
```

Shared groups: KV prefix groups/<group id>/ of the ns8-kv mount. A group ID ends with a letter

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                    |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [set-client-access-input.json\*](openbao/set-client-access-input.json "open original schema") |

## groups Type

`string[]`

## groups Constraints

**maximum number of items**: the maximum number of items for this array is: `8`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
