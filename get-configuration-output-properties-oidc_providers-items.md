# Untitled object in get-configuration output Schema

```txt
http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-configuration-output.json\*](openbao/get-configuration-output.json "open original schema") |

## items Type

`object` ([Details](get-configuration-output-properties-oidc_providers-items.md))

# items Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                          |
| :------------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](#id)           | `string` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-oidc_providers-items-properties-id.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers/items/properties/id")           |
| [label](#label)     | `string` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-oidc_providers-items-properties-label.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers/items/properties/label")     |
| [domains](#domains) | `array`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-oidc_providers-items-properties-domains.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers/items/properties/domains") |

## id



`id`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-oidc_providers-items-properties-id.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers/items/properties/id")

### id Type

`string`

## label



`label`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-oidc_providers-items-properties-label.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers/items/properties/label")

### label Type

`string`

## domains



`domains`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-oidc_providers-items-properties-domains.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers/items/properties/domains")

### domains Type

`string[]`
