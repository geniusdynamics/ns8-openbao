# Group policies Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies
```

Additional directory groups mapped to OpenBao policies, applied by self-initialization or by openbao-apply-config

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## ldap_group_policies Type

`object[]` ([Details](configure-module-input-properties-group-policies-items.md))

## ldap_group_policies Constraints

**maximum number of items**: the maximum number of items for this array is: `100`
