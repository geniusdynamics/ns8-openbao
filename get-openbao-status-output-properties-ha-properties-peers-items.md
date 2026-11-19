# Untitled object in get-openbao-status output Schema

```txt
http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                        |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-openbao-status-output.json\*](openbao/get-openbao-status-output.json "open original schema") |

## items Type

`object` ([Details](get-openbao-status-output-properties-ha-properties-peers-items.md))

# items Properties

| Property            | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                                       |
| :------------------ | :-------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [node_id](#node_id) | `string`  | Optional | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers-items-properties-node_id.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items/properties/node_id") |
| [address](#address) | `string`  | Optional | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers-items-properties-address.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items/properties/address") |
| [leader](#leader)   | `boolean` | Optional | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers-items-properties-leader.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items/properties/leader")   |
| [voter](#voter)     | `boolean` | Optional | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers-items-properties-voter.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items/properties/voter")     |

## node_id



`node_id`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers-items-properties-node_id.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items/properties/node_id")

### node_id Type

`string`

## address



`address`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers-items-properties-address.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items/properties/address")

### address Type

`string`

## leader



`leader`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers-items-properties-leader.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items/properties/leader")

### leader Type

`boolean`

## voter



`voter`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers-items-properties-voter.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items/properties/voter")

### voter Type

`boolean`
