# list-clients output Schema

```txt
http://schema.nethserver.org/openbao/list-clients-output.json
```

Client modules of the client provisioning feature: no tokens, no accessors

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                          |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-clients-output.json](openbao/list-clients-output.json "open original schema") |

## list-clients output Type

`object` ([list-clients output](list-clients-output.md))

## list-clients output Examples

```json
{
  "client_provisioning": true,
  "provisioner": "valid",
  "ha_role": "standalone",
  "kv_mount": "ns8-kv",
  "token_role": "ns8-client",
  "clients": [],
  "groups": [],
  "modules": [
    "postgresql19c1"
  ],
  "audit": []
}
```

# list-clients output Properties

| Property                                    | Type      | Required | Nullable       | Defined by                                                                                                                                                                   |
| :------------------------------------------ | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [client_provisioning](#client_provisioning) | `boolean` | Required | cannot be null | [list-clients output](list-clients-output-properties-client_provisioning.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/client_provisioning") |
| [provisioner](#provisioner)                 | `string`  | Required | cannot be null | [list-clients output](list-clients-output-properties-provisioner.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/provisioner")                 |
| [ha_role](#ha_role)                         | `string`  | Optional | cannot be null | [list-clients output](list-clients-output-properties-ha_role.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/ha_role")                         |
| [kv_mount](#kv_mount)                       | `string`  | Optional | cannot be null | [list-clients output](list-clients-output-properties-kv_mount.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/kv_mount")                       |
| [token_role](#token_role)                   | `string`  | Optional | cannot be null | [list-clients output](list-clients-output-properties-token_role.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/token_role")                   |
| [clients](#clients)                         | `array`   | Required | cannot be null | [list-clients output](list-clients-output-properties-clients.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients")                         |
| [groups](#groups)                           | `array`   | Required | cannot be null | [list-clients output](list-clients-output-properties-groups.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups")                           |
| [modules](#modules)                         | `array`   | Required | cannot be null | [list-clients output](list-clients-output-properties-modules.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/modules")                         |
| [audit](#audit)                             | `array`   | Required | cannot be null | [list-clients output](list-clients-output-properties-audit.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit")                             |

## client_provisioning



`client_provisioning`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-client_provisioning.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/client_provisioning")

### client_provisioning Type

`boolean`

## provisioner



`provisioner`

* is required

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-provisioner.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/provisioner")

### provisioner Type

`string`

### provisioner Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value              | Explanation |    |    |
| :----------------- | :---------- | :- | :- |
| `"missing"`        |             |
| `"valid"`          |             |
| `"invalid"`        |             |
| `"unknown"`        |             |
| `"revoke_pending"` |             |

## ha_role



`ha_role`

* is optional

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-ha_role.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/ha_role")

### ha_role Type

`string`

## kv_mount



`kv_mount`

* is optional

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-kv_mount.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/kv_mount")

### kv_mount Type

`string`

## token_role



`token_role`

* is optional

* Type: `string`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-token_role.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/token_role")

### token_role Type

`string`

## clients



`clients`

* is required

* Type: `object[]` ([Details](list-clients-output-properties-clients-items.md))

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-clients.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients")

### clients Type

`object[]` ([Details](list-clients-output-properties-clients-items.md))

## groups



`groups`

* is required

* Type: `object[]` ([Details](list-clients-output-properties-groups-items.md))

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-groups.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups")

### groups Type

`object[]` ([Details](list-clients-output-properties-groups-items.md))

## modules

Other modules of the cluster, candidates for approval

`modules`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-modules.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/modules")

### modules Type

`string[]`

## audit



`audit`

* is required

* Type: `object[]` ([Details](list-clients-output-properties-audit-items.md))

* cannot be null

* defined in: [list-clients output](list-clients-output-properties-audit.md "http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit")

### audit Type

`object[]` ([Details](list-clients-output-properties-audit-items.md))
