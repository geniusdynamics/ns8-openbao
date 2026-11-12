# Untitled object in get-configuration output Schema

```txt
http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-configuration-output.json\*](openbao/get-configuration-output.json "open original schema") |

## items Type

`object` ([Details](get-configuration-output-properties-user_domains-items.md))

# items Properties

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                        |
| :-------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)         | `string` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-user_domains-items-properties-name.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items/properties/name")         |
| [schema](#schema)     | `string` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-user_domains-items-properties-schema.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items/properties/schema")     |
| [location](#location) | `string` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-user_domains-items-properties-location.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items/properties/location") |

## name



`name`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-user_domains-items-properties-name.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items/properties/name")

### name Type

`string`

## schema

'ad' or 'rfc2307'

`schema`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-user_domains-items-properties-schema.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items/properties/schema")

### schema Type

`string`

## location

'internal' or 'external'

`location`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-user_domains-items-properties-location.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items/properties/location")

### location Type

`string`
