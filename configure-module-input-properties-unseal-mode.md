# Unseal mode Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/unseal_mode
```

'manual': Shamir unseal keys must be provided after every restart. 'auto': a static key stored on the node unseals OpenBao automatically. It can be changed only before OpenBao is initialized. Defaults to the current value, initially 'manual'

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## unseal_mode Type

`string` ([Unseal mode](configure-module-input-properties-unseal-mode.md))

## unseal_mode Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |    |    |
| :--------- | :---------- | :- | :- |
| `"manual"` |             |
| `"auto"`   |             |
