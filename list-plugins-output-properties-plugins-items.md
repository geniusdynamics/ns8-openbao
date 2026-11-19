# Untitled object in list-plugins output Schema

```txt
http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-plugins-output.json\*](openbao/list-plugins-output.json "open original schema") |

## items Type

`object` ([Details](list-plugins-output-properties-plugins-items.md))

# items Properties

| Property                                | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                 |
| :-------------------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](#id)                               | `string`  | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-id.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/id")                               |
| [type](#type)                           | `string`  | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-type.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/type")                           |
| [name](#name)                           | `string`  | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-name.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/name")                           |
| [bundled](#bundled)                     | `boolean` | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-bundled.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/bundled")                     |
| [enabled](#enabled)                     | `boolean` | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-enabled.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/enabled")                     |
| [installed](#installed)                 | `boolean` | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-installed.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/installed")                 |
| [version](#version)                     | `string`  | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-version.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/version")                     |
| [installed_version](#installed_version) | `string`  | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-installed_version.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/installed_version") |
| [docs_url](#docs_url)                   | `string`  | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-docs_url.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/docs_url")                   |
| [enable_command](#enable_command)       | `string`  | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-enable_command.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/enable_command")       |
| [setup_commands](#setup_commands)       | `array`   | Required | cannot be null | [list-plugins output](list-plugins-output-properties-plugins-items-properties-setup_commands.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/setup_commands")       |

## id



`id`

* is required

* Type: `string`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-id.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/id")

### id Type

`string`

## type



`type`

* is required

* Type: `string`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-type.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value        | Explanation |    |    |
| :----------- | :---------- | :- | :- |
| `"auth"`     |             |
| `"secret"`   |             |
| `"database"` |             |

## name

Name registered in OpenBao

`name`

* is required

* Type: `string`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-name.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/name")

### name Type

`string`

## bundled

Always installed with the module (LDAP)

`bundled`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-bundled.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/bundled")

### bundled Type

`boolean`

## enabled



`enabled`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-enabled.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/enabled")

### enabled Type

`boolean`

## installed

The binary is installed and declared in the server configuration

`installed`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-installed.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/installed")

### installed Type

`boolean`

## version

Version pinned by this module release

`version`

* is required

* Type: `string`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-version.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/version")

### version Type

`string`

## installed_version



`installed_version`

* is required

* Type: `string`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-installed_version.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/installed_version")

### installed_version Type

`string`

## docs_url



`docs_url`

* is required

* Type: `string`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-docs_url.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/docs_url")

### docs_url Type

`string`

## enable_command



`enable_command`

* is required

* Type: `string`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-enable_command.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/enable_command")

### enable_command Type

`string`

## setup_commands



`setup_commands`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-plugins output](list-plugins-output-properties-plugins-items-properties-setup_commands.md "http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/setup_commands")

### setup_commands Type

`string[]`
