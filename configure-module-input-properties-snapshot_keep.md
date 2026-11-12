# Untitled integer in configure-module input Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/snapshot_keep
```

Number of daily Raft snapshots kept on the node (requires the module token). 0 disables them

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## snapshot_keep Type

`integer`

## snapshot_keep Constraints

**maximum**: the value of this number must smaller than or equal to: `90`

**minimum**: the value of this number must greater than or equal to: `0`
