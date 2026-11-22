# Notification recipients Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/notify_recipients
```

Email addresses notified when OpenBao is down or sealed. The cluster SMTP smarthost is used. Empty list disables the notifications

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## notify_recipients Type

`string[]`

## notify_recipients Constraints

**maximum number of items**: the maximum number of items for this array is: `20`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
