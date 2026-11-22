# request-client-access input Schema

```txt
http://schema.nethserver.org/openbao/request-client-access-input.json
```

Role secretsclient. Record an access request of the calling module, shown to the OpenBao administrator. It grants nothing

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                          |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [request-client-access-input.json](openbao/request-client-access-input.json "open original schema") |

## request-client-access input Type

`object` ([request-client-access input](request-client-access-input.md))

## request-client-access input Examples

```json
{}
```

```json
{
  "groups": [
    "kumomta-cluster"
  ]
}
```

# request-client-access input Properties

| Property                            | Type      | Required | Nullable       | Defined by                                                                                                                                                                                   |
| :---------------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [database_engine](#database_engine) | `boolean` | Optional | cannot be null | [request-client-access input](request-client-access-input-properties-database_engine.md "http://schema.nethserver.org/openbao/request-client-access-input.json#/properties/database_engine") |
| [groups](#groups)                   | `array`   | Optional | cannot be null | [request-client-access input](request-client-access-input-properties-groups.md "http://schema.nethserver.org/openbao/request-client-access-input.json#/properties/groups")                   |

## database_engine



`database_engine`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [request-client-access input](request-client-access-input-properties-database_engine.md "http://schema.nethserver.org/openbao/request-client-access-input.json#/properties/database_engine")

### database_engine Type

`boolean`

## groups

Groups the module asks to join; the administrator decides

`groups`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [request-client-access input](request-client-access-input-properties-groups.md "http://schema.nethserver.org/openbao/request-client-access-input.json#/properties/groups")

### groups Type

`string[]`

### groups Constraints

**maximum number of items**: the maximum number of items for this array is: `8`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
