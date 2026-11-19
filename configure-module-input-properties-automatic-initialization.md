# Automatic initialization Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/auto_initialize
```

Let OpenBao initialize itself with directory login already configured: no root token or recovery keys are generated. Requires unseal_mode 'auto', user_domain and ldap_admin_group. It has no effect once OpenBao is initialized

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## auto_initialize Type

`boolean` ([Automatic initialization](configure-module-input-properties-automatic-initialization.md))
