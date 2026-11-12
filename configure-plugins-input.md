# configure-plugins input Schema

```txt
http://schema.nethserver.org/openbao/configure-plugins-input.json
```

Choose the optional OpenBao plugins. Enabled plugins are downloaded (images pinned by digest), installed and declared; OpenBao restarts if the set changes (with manual unseal it must be unsealed again). Disabled plugins are removed with their images. Enabling a plugin in OpenBao (bao auth enable / bao secrets enable) needs an administrator token and is not done by the module.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [configure-plugins-input.json](openbao/configure-plugins-input.json "open original schema") |

## configure-plugins input Type

`object` ([configure-plugins input](configure-plugins-input.md))

## configure-plugins input Examples

```json
{
  "plugins": [
    "auth-github",
    "secrets-aws"
  ]
}
```

```json
{
  "plugins": []
}
```

# configure-plugins input Properties

| Property            | Type    | Required | Nullable       | Defined by                                                                                                                                                       |
| :------------------ | :------ | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [plugins](#plugins) | `array` | Required | cannot be null | [configure-plugins input](configure-plugins-input-properties-plugins.md "http://schema.nethserver.org/openbao/configure-plugins-input.json#/properties/plugins") |

## plugins

Ids of the enabled optional plugins

`plugins`

* is required

* Type: `string[]`

* cannot be null

* defined in: [configure-plugins input](configure-plugins-input-properties-plugins.md "http://schema.nethserver.org/openbao/configure-plugins-input.json#/properties/plugins")

### plugins Type

`string[]`

### plugins Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.
