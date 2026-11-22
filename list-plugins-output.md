# list-plugins output Schema

```txt
http://schema.nethserver.org/openbao/list-plugins-output.json
```

OpenBao plugins: the bundled LDAP auth plugin and the optional plugins of the openbao-plugins project, with their state

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                          |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-plugins-output.json](openbao/list-plugins-output.json "open original schema") |

## list-plugins output Type

`object` ([list-plugins output](list-plugins-output.md))

## list-plugins output Examples

```json
{
  "plugins": [
    {
      "id": "auth-github",
      "type": "auth",
      "name": "github",
      "bundled": false,
      "enabled": true,
      "installed": true,
      "version": "v0.0.2",
      "installed_version": "v0.0.2",
      "docs_url": "https://github.com/openbao/openbao-plugins/tree/main/auth/github",
      "enable_command": "bao auth enable github",
      "setup_commands": [
        "bao write auth/github/config organization=<organization>"
      ]
    }
  ]
}
```

# list-plugins output Properties

| Property            | Type    | Required | Nullable       | Defined by                                                                                                                                           |
| :------------------ | :------ | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| [plugins](#plugins) | `array` | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins") |

## plugins



`plugins`

* is required

* Type: `object[]` ([Details](list-plugins-output-properties-plugins-items.md))

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins")

### plugins Type

`object[]` ([Details](list-plugins-output-properties-plugins-items.md))
