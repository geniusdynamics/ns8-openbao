# Untitled object in provision-client output Schema

```txt
http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                    |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [provision-client-output.json\*](openbao/provision-client-output.json "open original schema") |

## items Type

`object` ([Details](provision-client-output-properties-groups-items.md))

# items Properties

| Property                          | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                     |
| :-------------------------------- | :-------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [group_id](#group_id)             | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-groups-items-properties-group_id.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/group_id")             |
| [kv_prefix](#kv_prefix)           | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-groups-items-properties-kv_prefix.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/kv_prefix")           |
| [wrapped_token](#wrapped_token)   | `string`  | Required | cannot be null | [provision-client output](provision-client-output-properties-groups-items-properties-wrapped_token.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/wrapped_token")   |
| [wrap_ttl](#wrap_ttl)             | `integer` | Required | cannot be null | [provision-client output](provision-client-output-properties-groups-items-properties-wrap_ttl.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/wrap_ttl")             |
| [token_policies](#token_policies) | `array`   | Required | cannot be null | [provision-client output](provision-client-output-properties-groups-items-properties-token_policies.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/token_policies") |

## group_id



`group_id`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-groups-items-properties-group_id.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/group_id")

### group_id Type

`string`

### group_id Constraints

**maximum length**: the maximum number of characters for this string is: `64`

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[a-z][a-z0-9-]{0,62}[a-z]$
```

[try pattern](https://regexr.com/?expression=%5E%5Ba-z%5D%5Ba-z0-9-%5D%7B0%2C62%7D%5Ba-z%5D%24 "try regular expression with regexr.com")

## kv_prefix



`kv_prefix`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-groups-items-properties-kv_prefix.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/kv_prefix")

### kv_prefix Type

`string`

## wrapped_token

Response-wrapping token of the group token: single use, unwrap at once

`wrapped_token`

* is required

* Type: `string`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-groups-items-properties-wrapped_token.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/wrapped_token")

### wrapped_token Type

`string`

## wrap_ttl



`wrap_ttl`

* is required

* Type: `integer`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-groups-items-properties-wrap_ttl.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/wrap_ttl")

### wrap_ttl Type

`integer`

## token_policies



`token_policies`

* is required

* Type: `string[]`

* cannot be null

* defined in: [provision-client output](provision-client-output-properties-groups-items-properties-token_policies.md "http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/token_policies")

### token_policies Type

`string[]`
