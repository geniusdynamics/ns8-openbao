# Allowed networks Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ip_allowlist
```

Client IP addresses or networks (CIDR) allowed to reach the OpenBao API and web UI through Traefik. Empty list: no restriction

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## ip_allowlist Type

`string[]`

## ip_allowlist Constraints

**maximum number of items**: the maximum number of items for this array is: `100`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
