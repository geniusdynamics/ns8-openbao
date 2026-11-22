# Server log level Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/log_level
```

OpenBao server log level. Defaults to the current value, initially 'info'

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## log_level Type

`string` ([Server log level](configure-module-input-properties-server-log-level.md))

## log_level Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |    |    |
| :-------- | :---------- | :- | :- |
| `"trace"` |             |
| `"debug"` |             |
| `"info"`  |             |
| `"warn"`  |             |
| `"error"` |             |
