# README

## Top-level Schemas

* [configure-module input](./configure-module-input.md "Configure the OpenBao instance") – `http://schema.nethserver.org/openbao/configure-module-input.json`

* [get-configuration output](./get-configuration-output.md "Get the OpenBao instance configuration") – `http://schema.nethserver.org/openbao/get-configuration-output.json`

* [get-openbao-status output](./get-openbao-status-output.md "Get the OpenBao server state: initialization and seal status") – `http://schema.nethserver.org/openbao/get-openbao-status-output.json`

* [send-test-email input](./send-test-email-input.md "Send a test email through the cluster SMTP smarthost, to verify the notification settings") – `http://schema.nethserver.org/openbao/send-test-email-input.json`

* [send-test-email output](./send-test-email-output.md "Recipients of the test email") – `http://schema.nethserver.org/openbao/send-test-email-output.json`

## Other Schemas

### Objects

* [Untitled object in get-configuration output](./get-configuration-output-properties-user_domains-items.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items`

### Arrays

* [Notification recipients](./configure-module-input-properties-notification-recipients.md "Email addresses notified when OpenBao is down or sealed") – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/notify_recipients`

* [Untitled array in get-configuration output](./get-configuration-output-properties-notify_recipients.md "Email addresses notified when OpenBao is down or sealed") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/notify_recipients`

* [Untitled array in get-configuration output](./get-configuration-output-properties-user_domains.md "User domains of the cluster") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains`

* [Untitled array in send-test-email input](./send-test-email-input-properties-recipients.md "Recipients of the test email") – `http://schema.nethserver.org/openbao/send-test-email-input.json#/properties/recipients`

* [Untitled array in send-test-email output](./send-test-email-output-properties-recipients.md) – `http://schema.nethserver.org/openbao/send-test-email-output.json#/properties/recipients`

## Version Note

The schemas linked above follow the JSON Schema Spec version: `http://json-schema.org/draft-07/schema#`
