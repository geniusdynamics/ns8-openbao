# Instance to join Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ha_join
```

Module ID of an OpenBao instance that accepts members (see ha_candidates of get-configuration). Required with ha_role 'member'.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## ha_join Type

`string` ([Instance to join](configure-module-input-properties-instance-to-join.md))

## ha_join Constraints

**maximum length**: the maximum number of characters for this string is: `64`
