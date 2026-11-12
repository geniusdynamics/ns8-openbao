# Untitled object in configure-module input Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## items Type

`object` ([Details](configure-module-input-properties-group-policies-items.md))

# items Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                       |
| :---------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [group](#group)   | `string` | Required | cannot be null | [configure-module input](configure-module-input-properties-group-policies-items-properties-group.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies/items/properties/group")   |
| [policy](#policy) | `string` | Required | cannot be null | [configure-module input](configure-module-input-properties-group-policies-items-properties-policy.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies/items/properties/policy") |

## group



`group`

* is required

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-group-policies-items-properties-group.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies/items/properties/group")

### group Type

`string`

### group Constraints

**maximum length**: the maximum number of characters for this string is: `256`

**minimum length**: the minimum number of characters for this string is: `1`

## policy



`policy`

* is required

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-group-policies-items-properties-policy.md "http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies/items/properties/policy")

### policy Type

`string`

### policy Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[A-Za-z0-9_.-]{1,128}$
```

[try pattern](https://regexr.com/?expression=%5E%5BA-Za-z0-9_.-%5D%7B1%2C128%7D%24 "try regular expression with regexr.com")
