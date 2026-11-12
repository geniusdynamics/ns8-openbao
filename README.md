# README

## Top-level Schemas

* [configure-module input](./configure-module-input.md "Configure the OpenBao instance") – `http://schema.nethserver.org/openbao/configure-module-input.json`

* [get-configuration output](./get-configuration-output.md "Get the OpenBao instance configuration") – `http://schema.nethserver.org/openbao/get-configuration-output.json`

* [get-openbao-status output](./get-openbao-status-output.md "Get the OpenBao server state: initialization and seal status") – `http://schema.nethserver.org/openbao/get-openbao-status-output.json`

* [list-snapshots output](./list-snapshots-output.md "Scheduled Raft snapshots kept on the node") – `http://schema.nethserver.org/openbao/list-snapshots-output.json`

* [send-test-email input](./send-test-email-input.md "Send a test email through the cluster SMTP smarthost, to verify the notification settings") – `http://schema.nethserver.org/openbao/send-test-email-input.json`

* [send-test-email output](./send-test-email-output.md "Recipients of the test email") – `http://schema.nethserver.org/openbao/send-test-email-output.json`

## Other Schemas

### Objects

* [Untitled object in configure-module input](./configure-module-input-properties-group-policies-items.md) – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies/items`

* [Untitled object in get-configuration output](./get-configuration-output-properties-user_domains-items.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items`

* [Untitled object in get-configuration output](./get-configuration-output-properties-ldap_group_policies-items.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies/items`

* [Untitled object in get-configuration output](./get-configuration-output-properties-ha_candidates-items.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items`

* [Untitled object in get-openbao-status output](./get-openbao-status-output-properties-ha.md "High availability state (experimental)") – `http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha`

* [Untitled object in get-openbao-status output](./get-openbao-status-output-properties-ha-properties-peers-items.md) – `http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items`

* [Untitled object in list-snapshots output](./list-snapshots-output-properties-snapshots-items.md) – `http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots/items`

### Arrays

* [Allowed networks](./configure-module-input-properties-allowed-networks.md "Client IP addresses or networks (CIDR) allowed to reach the OpenBao API and web UI through Traefik") – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ip_allowlist`

* [Group policies](./configure-module-input-properties-group-policies.md "Additional directory groups mapped to OpenBao policies, applied by self-initialization or by openbao-apply-config") – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies`

* [Notification recipients](./configure-module-input-properties-notification-recipients.md "Email addresses notified when OpenBao is down or sealed") – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/notify_recipients`

* [Starter kits](./configure-module-input-properties-starter-kits.md "Components prepared by self-initialization or by openbao-apply-config: 'kv' key/value v2 store at secret/, 'pki' internal certificate authority at pki/, 'approle' application login") – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/starter_kits`

* [Untitled array in get-configuration output](./get-configuration-output-properties-notify_recipients.md "Email addresses notified when OpenBao is down or sealed") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/notify_recipients`

* [Untitled array in get-configuration output](./get-configuration-output-properties-user_domains.md "User domains of the cluster") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains`

* [Untitled array in get-configuration output](./get-configuration-output-properties-ip_allowlist.md "Networks allowed through Traefik; empty: no restriction") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ip_allowlist`

* [Untitled array in get-configuration output](./get-configuration-output-properties-ldap_group_policies.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies`

* [Untitled array in get-configuration output](./get-configuration-output-properties-starter_kits.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/starter_kits`

* [Untitled array in get-configuration output](./get-configuration-output-properties-builtin_policies.md "Policies created by the module") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/builtin_policies`

* [Untitled array in get-configuration output](./get-configuration-output-properties-ha_candidates.md "Other OpenBao instances with high availability enabled, which a new instance can join") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates`

* [Untitled array in list-snapshots output](./list-snapshots-output-properties-snapshots.md) – `http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots`

* [Untitled array in send-test-email input](./send-test-email-input-properties-recipients.md "Recipients of the test email") – `http://schema.nethserver.org/openbao/send-test-email-input.json#/properties/recipients`

* [Untitled array in send-test-email output](./send-test-email-output-properties-recipients.md) – `http://schema.nethserver.org/openbao/send-test-email-output.json#/properties/recipients`

## Version Note

The schemas linked above follow the JSON Schema Spec version: `http://json-schema.org/draft-07/schema#`
