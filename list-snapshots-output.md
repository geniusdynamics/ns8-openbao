# list-snapshots output Schema

```txt
http://schema.nethserver.org/openbao/list-snapshots-output.json
```

Scheduled Raft snapshots kept on the node

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                              |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-snapshots-output.json](openbao/list-snapshots-output.json "open original schema") |

## list-snapshots output Type

`object` ([list-snapshots output](list-snapshots-output.md))

## list-snapshots output Examples

```json
{
  "snapshot_keep": 7,
  "module_token": true,
  "snapshots": [
    {
      "name": "openbao-20261112-031500.snap",
      "size": 524288,
      "created": 1794460500
    }
  ]
}
```

# list-snapshots output Properties

| Property                        | Type      | Required | Nullable       | Defined by                                                                                                                                                             |
| :------------------------------ | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [snapshot_keep](#snapshot_keep) | `integer` | Required | cannot be null | [list-snapshots output](list-snapshots-output-properties-snapshot_keep.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshot_keep") |
| [module_token](#module_token)   | `boolean` | Required | cannot be null | [list-snapshots output](list-snapshots-output-properties-module_token.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/module_token")   |
| [snapshots](#snapshots)         | `array`   | Required | cannot be null | [list-snapshots output](list-snapshots-output-properties-snapshots.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots")         |

## snapshot_keep



`snapshot_keep`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-snapshots output](list-snapshots-output-properties-snapshot_keep.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshot_keep")

### snapshot_keep Type

`integer`

### snapshot_keep Constraints

**minimum**: the value of this number must greater than or equal to: `0`

## module_token

A module token exists: scheduled snapshots can be taken

`module_token`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-snapshots output](list-snapshots-output-properties-module_token.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/module_token")

### module_token Type

`boolean`

## snapshots



`snapshots`

* is required

* Type: `object[]` ([Details](list-snapshots-output-properties-snapshots-items.md))

* cannot be null

* defined in: [list-snapshots output](list-snapshots-output-properties-snapshots.md "http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots")

### snapshots Type

`object[]` ([Details](list-snapshots-output-properties-snapshots-items.md))
