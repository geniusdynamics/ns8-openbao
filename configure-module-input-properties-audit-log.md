# Audit log Schema

```txt
http://schema.nethserver.org/openbao/configure-module-input.json#/properties/audit_log
```

Send the OpenBao audit log to the systemd journal. Defaults to the current value, initially false

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [configure-module-input.json\*](openbao/configure-module-input.json "open original schema") |

## audit_log Type

`boolean` ([Audit log](configure-module-input-properties-audit-log.md))
