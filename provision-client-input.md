# provision-client input Schema

```txt
http://schema.nethserver.org/openbao/provision-client-input.json
```

Role secretsclient (authorization openbao\@any:secretsclient). Issue a wrapped OpenBao token to the calling module, identified by NS8 (never by input). See docs/client-provisioning.md

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [provision-client-input.json](openbao/provision-client-input.json "open original schema") |

## provision-client input Type

`object` ([provision-client input](provision-client-input.md))

## provision-client input Examples

```json
{}
```

```json
{
  "database_engine": true
}
```

# provision-client input Properties

| Property                            | Type      | Required | Nullable       | Defined by                                                                                                                                                                    |
| :---------------------------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [database_engine](#database_engine) | `boolean` | Optional | cannot be null | [provision-client input](provision-client-input-properties-database_engine.md "http://schema.nethserver.org/openbao/provision-client-input.json#/properties/database_engine") |

## database_engine

Ask for the database secrets engine mounted at ns8-db-<module id>/. Granted only if the administrator approved it; otherwise recorded as a request

`database_engine`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [provision-client input](provision-client-input-properties-database_engine.md "http://schema.nethserver.org/openbao/provision-client-input.json#/properties/database_engine")

### database_engine Type

`boolean`
