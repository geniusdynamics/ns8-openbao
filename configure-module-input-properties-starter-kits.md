# Starter kits Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/starter_kits
```

Components prepared by self-initialization or by openbao-apply-config: 'kv' key/value v2 store at secret/, 'pki' internal certificate authority at pki/, 'approle' application login

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## starter_kits Type

`string[]`

## starter_kits Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.
