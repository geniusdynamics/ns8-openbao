# Untitled object in get-configuration output Schema

```txt
http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-configuration-output.json\*](openbao/get-configuration-output.json "open original schema") |

## items Type

`object` ([Details](get-configuration-output-properties-ldap_group_policies-items.md))

# items Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                                  |
| :---------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [group](#group)   | `string` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ldap_group_policies-items-properties-group.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies/items/properties/group")   |
| [policy](#policy) | `string` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ldap_group_policies-items-properties-policy.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies/items/properties/policy") |

## group



`group`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ldap_group_policies-items-properties-group.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies/items/properties/group")

### group Type

`string`

## policy



`policy`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ldap_group_policies-items-properties-policy.md "http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies/items/properties/policy")

### policy Type

`string`
