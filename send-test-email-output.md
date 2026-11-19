# send-test-email output Schema

```txt
http://schema.nethserver.org/openbao/send-test-email-output.json
```

Recipients of the test email

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [send-test-email-output.json](openbao/send-test-email-output.json "open original schema") |

## send-test-email output Type

`object` ([send-test-email output](send-test-email-output.md))

## send-test-email output Examples

```json
{
  "recipients": [
    "security@example.org"
  ]
}
```

# send-test-email output Properties

| Property                  | Type    | Required | Nullable       | Defined by                                                                                                                                                          |
| :------------------------ | :------ | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [recipients](#recipients) | `array` | Required | cannot be null | [send-test-email output](send-test-email-output-properties-recipients.md "http://schema.nethserver.org/openbao/send-test-email-output.json#/properties/recipients") |

## recipients



`recipients`

* is required

* Type: `string[]`

* cannot be null

* defined in: [send-test-email output](send-test-email-output-properties-recipients.md "http://schema.nethserver.org/openbao/send-test-email-output.json#/properties/recipients")

### recipients Type

`string[]`
