# Untitled string in configure-plugins input Schema

```txt
http://schema.nethserver.org/openbao/configure-plugins-input.json#/properties/plugins/items
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                    |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-plugins-input.json\*](openbao/configure-plugins-input.json "open original schema") |

## items Type

`string`

## items Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value                | Explanation |    |    |
| :------------------- | :---------- | :- | :- |
| `"auth-aws"`         |             |
| `"auth-azure"`       |             |
| `"auth-gcp"`         |             |
| `"auth-github"`      |             |
| `"auth-kerberos"`    |             |
| `"auth-radius"`      |             |
| `"secrets-aws"`      |             |
| `"secrets-azure"`    |             |
| `"secrets-gcp"`      |             |
| `"secrets-gcpkms"`   |             |
| `"secrets-consul"`   |             |
| `"secrets-nomad"`    |             |
| `"secrets-ldap"`     |             |
| `"database-mongodb"` |             |
