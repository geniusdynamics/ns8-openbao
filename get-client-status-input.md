# get-client-status input Schema

```txt
http://schema.nethserver.org/openbao/get-client-status-input.json
```

Reader-safe status of a client module. A module caller may omit module_id to read its own status

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [get-client-status-input.json](openbao/get-client-status-input.json "open original schema") |

## get-client-status input Type

`object` ([get-client-status input](get-client-status-input.md))

## get-client-status input Examples

```json
{}
```

```json
{
  "module_id": "kumomta1"
}
```

# get-client-status input Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                           |
| :---------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [module_id](#module_id) | `string` | Optional | cannot be null | [get-client-status input](get-client-status-input-properties-module_id.md "http://schema.nethserver.org/openbao/get-client-status-input.json#/properties/module_id") |

## module_id



`module_id`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-client-status input](get-client-status-input-properties-module_id.md "http://schema.nethserver.org/openbao/get-client-status-input.json#/properties/module_id")

### module_id Type

`string`

### module_id Constraints

**maximum length**: the maximum number of characters for this string is: `64`

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[a-z][a-z0-9-]{0,62}[0-9]$
```

[try pattern](https://regexr.com/?expression=%5E%5Ba-z%5D%5Ba-z0-9-%5D%7B0%2C62%7D%5B0-9%5D%24 "try regular expression with regexr.com")
