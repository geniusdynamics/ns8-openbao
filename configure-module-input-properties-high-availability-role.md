# High availability role Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ha_role
```

Experimental. 'standalone' (default): a single-node OpenBao. 'primary': accept other OpenBao instances as members of its Raft cluster; it publishes the Raft cluster port and the cluster network API on the node VPN address and requires manual or Transit unseal. 'member': join the Raft cluster of the instance named by ha_join; allowed only before this instance is initialized, and it takes the seal of that cluster.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## ha_role Type

`string` ([High availability role](configure-module-input-properties-high-availability-role.md))

## ha_role Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value          | Explanation |    |    |
| :------------- | :---------- | :- | :- |
| `"standalone"` |             |
| `"primary"`    |             |
| `"member"`     |             |
