# Untitled object in get-openbao-status output Schema

```txt
http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha
```

High availability state (experimental)

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                        |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-openbao-status-output.json\*](openbao/get-openbao-status-output.json "open original schema") |

## ha Type

`object` ([Details](get-openbao-status-output-properties-ha.md))

# ha Properties

| Property                          | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                       |
| :-------------------------------- | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [role](#role)                     | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-role.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/role")                     |
| [cluster](#cluster)               | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-cluster.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/cluster")               |
| [node_id](#node_id)               | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-node_id.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/node_id")               |
| [raft_address](#raft_address)     | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-raft_address.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/raft_address")     |
| [is_self](#is_self)               | `boolean` | Required | can be null    | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-is_self.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/is_self")               |
| [leader_address](#leader_address) | `string`  | Required | cannot be null | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-leader_address.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/leader_address") |
| [peers](#peers)                   | `array`   | Required | can be null    | [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers")                   |

## role



`role`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-role.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/role")

### role Type

`string`

### role Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value          | Explanation |    |    |
| :------------- | :---------- | :- | :- |
| `"standalone"` |             |
| `"primary"`    |             |
| `"member"`     |             |

## cluster



`cluster`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-cluster.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/cluster")

### cluster Type

`string`

## node_id



`node_id`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-node_id.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/node_id")

### node_id Type

`string`

## raft_address



`raft_address`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-raft_address.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/raft_address")

### raft_address Type

`string`

## is_self

This instance is the active (leader) node; null when unknown

`is_self`

* is required

* Type: `boolean`

* can be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-is_self.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/is_self")

### is_self Type

`boolean`

## leader_address



`leader_address`

* is required

* Type: `string`

* cannot be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-leader_address.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/leader_address")

### leader_address Type

`string`

## peers

Raft peers, read with the module token; null when not readable

`peers`

* is required

* Type: `object[]` ([Details](get-openbao-status-output-properties-ha-properties-peers-items.md))

* can be null

* defined in: [get-openbao-status output](get-openbao-status-output-properties-ha-properties-peers.md "http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers")

### peers Type

`object[]` ([Details](get-openbao-status-output-properties-ha-properties-peers-items.md))
