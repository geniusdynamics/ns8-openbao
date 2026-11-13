# Public access Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/public_access
```

Publish the API and web UI through Traefik on the host name. false: reachable only on the cluster network API (requires vpn_api). Default true

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## public_access Type

`boolean` ([Public access](configure-module-input-properties-public-access.md))
