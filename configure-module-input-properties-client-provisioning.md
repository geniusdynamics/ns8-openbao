# Client provisioning Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/client_provisioning
```

Let approved NethServer modules get their own narrowly scoped OpenBao token (role openbao\@any:secretsclient). Enabling it also needs openbao-client-provisioner create on the node; disabling revokes the client and provisioner tokens

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## client_provisioning Type

`boolean` ([Client provisioning](configure-module-input-properties-client-provisioning.md))
