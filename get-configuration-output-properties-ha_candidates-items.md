# Untitled object in get-configuration output Schema

```txt
http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-configuration-output.json\*](openbao/get-configuration-output.json "open original schema") |

## items Type

`object` ([Details](get-configuration-output-properties-ha_candidates-items.md))

# items Properties

| Property                                            | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                                                        |
| :-------------------------------------------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [module_id](#module_id)                             | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-module_id.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/module_id")                             |
| [node](#node)                                       | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-node.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/node")                                       |
| [ui_name](#ui_name)                                 | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-ui_name.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/ui_name")                                 |
| [ha_cluster](#ha_cluster)                           | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-ha_cluster.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/ha_cluster")                           |
| [ha_role](#ha_role)                                 | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-ha_role.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/ha_role")                                 |
| [raft_node_id](#raft_node_id)                       | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-raft_node_id.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/raft_node_id")                       |
| [api_url](#api_url)                                 | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-api_url.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/api_url")                                 |
| [cluster_address](#cluster_address)                 | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-cluster_address.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/cluster_address")                 |
| [unseal_mode](#unseal_mode)                         | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-unseal_mode.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/unseal_mode")                         |
| [transit_address](#transit_address)                 | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-transit_address.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/transit_address")                 |
| [transit_mount](#transit_mount)                     | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-transit_mount.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/transit_mount")                     |
| [transit_key](#transit_key)                         | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-transit_key.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/transit_key")                         |
| [transit_tls_skip_verify](#transit_tls_skip_verify) | `boolean` | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-transit_tls_skip_verify.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/transit_tls_skip_verify") |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-module_id.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/module_id")

### module_id Type

`string`

## node



`node`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-node.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/node")

### node Type

`string`

## ui_name



`ui_name`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-ui_name.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/ui_name")

### ui_name Type

`string`

## ha_cluster



`ha_cluster`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-ha_cluster.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/ha_cluster")

### ha_cluster Type

`string`

## ha_role



`ha_role`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-ha_role.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/ha_role")

### ha_role Type

`string`

## raft_node_id



`raft_node_id`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-raft_node_id.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/raft_node_id")

### raft_node_id Type

`string`

## api_url



`api_url`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-api_url.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/api_url")

### api_url Type

`string`

## cluster_address



`cluster_address`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-cluster_address.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/cluster_address")

### cluster_address Type

`string`

## unseal_mode



`unseal_mode`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-unseal_mode.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/unseal_mode")

### unseal_mode Type

`string`

## transit_address



`transit_address`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-transit_address.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/transit_address")

### transit_address Type

`string`

## transit_mount



`transit_mount`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-transit_mount.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/transit_mount")

### transit_mount Type

`string`

## transit_key



`transit_key`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-transit_key.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/transit_key")

### transit_key Type

`string`

## transit_tls_skip_verify



`transit_tls_skip_verify`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ha_candidates-items-properties-transit_tls_skip_verify.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items/properties/transit_tls_skip_verify")

### transit_tls_skip_verify Type

`boolean`
