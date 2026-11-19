# send-test-email input Schema

```txt
http://schema.nethserver.org/openbao/send-test-email-input.json
```

Send a test email through the cluster SMTP smarthost, to verify the notification settings

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                              |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [send-test-email-input.json](openbao/send-test-email-input.json "open original schema") |

## send-test-email input Type

`object` ([send-test-email input](send-test-email-input.md))

## send-test-email input Examples

```json
{}
```

```json
{
  "recipients": [
    "security@example.org"
  ]
}
```

# send-test-email input Properties

| Property                  | Type    | Required | Nullable       | Defined by                                                                                                                                                       |
| :------------------------ | :------ | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [recipients](#recipients) | `array` | Optional | cannot be null | [send-test-email input](send-test-email-input-properties-recipients.md "http://schema.nethserver.org/openbao/send-test-email-input.json#/properties/recipients") |

## recipients

Recipients of the test email. Defaults to the configured notification recipients

`recipients`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [send-test-email input](send-test-email-input-properties-recipients.md "http://schema.nethserver.org/openbao/send-test-email-input.json#/properties/recipients")

### recipients Type

`string[]`

### recipients Constraints

**maximum number of items**: the maximum number of items for this array is: `20`

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
