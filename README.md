# README

## Top-level Schemas

* [configure-module input](./configure-module-input.md "Configure the OpenBao instance") – `http://schema.nethserver.org/openbao/configure-module-input.json`

* [configure-plugins input](./configure-plugins-input.md "Choose the optional OpenBao plugins") – `http://schema.nethserver.org/openbao/configure-plugins-input.json`

* [get-client-status input](./get-client-status-input.md "Reader-safe status of a client module") – `http://schema.nethserver.org/openbao/get-client-status-input.json`

* [get-client-status output](./get-client-status-output.md "Client provisioning status of one module: no secrets") – `http://schema.nethserver.org/openbao/get-client-status-output.json`

* [get-configuration output](./get-configuration-output.md "Get the OpenBao instance configuration") – `http://schema.nethserver.org/openbao/get-configuration-output.json`

* [get-openbao-status output](./get-openbao-status-output.md "Get the OpenBao server state: initialization and seal status") – `http://schema.nethserver.org/openbao/get-openbao-status-output.json`

* [list-clients output](./list-clients-output.md "Client modules of the client provisioning feature: no tokens, no accessors") – `http://schema.nethserver.org/openbao/list-clients-output.json`

* [list-plugins output](./list-plugins-output.md "OpenBao plugins: the bundled LDAP auth plugin and the optional plugins of the openbao-plugins project, with their state") – `http://schema.nethserver.org/openbao/list-plugins-output.json`

* [list-snapshots output](./list-snapshots-output.md "Scheduled Raft snapshots kept on the node") – `http://schema.nethserver.org/openbao/list-snapshots-output.json`

* [provision-client input](./provision-client-input.md "Role secretsclient (authorization openbao@any:secretsclient)") – `http://schema.nethserver.org/openbao/provision-client-input.json`

* [provision-client output](./provision-client-output.md "A wrapped OpenBao token and how to use it") – `http://schema.nethserver.org/openbao/provision-client-output.json`

* [request-client-access input](./request-client-access-input.md "Role secretsclient") – `http://schema.nethserver.org/openbao/request-client-access-input.json`

* [request-client-access output](./request-client-access-output.md "Status of the calling module after the request (same as get-client-status)") – `http://schema.nethserver.org/openbao/request-client-access-output.json`

* [send-test-email input](./send-test-email-input.md "Send a test email through the cluster SMTP smarthost, to verify the notification settings") – `http://schema.nethserver.org/openbao/send-test-email-input.json`

* [send-test-email output](./send-test-email-output.md "Recipients of the test email") – `http://schema.nethserver.org/openbao/send-test-email-output.json`

* [set-client-access input](./set-client-access-input.md "Approve or revoke a client module") – `http://schema.nethserver.org/openbao/set-client-access-input.json`

* [set-client-access output](./set-client-access-output.md "Effective access of the client module") – `http://schema.nethserver.org/openbao/set-client-access-output.json`

## Other Schemas

### Objects

* [Untitled object in configure-module input](./configure-module-input-properties-group-policies-items.md) – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies/items`

* [Untitled object in get-configuration output](./get-configuration-output-properties-oidc_providers-items.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers/items`

* [Untitled object in get-configuration output](./get-configuration-output-properties-user_domains-items.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains/items`

* [Untitled object in get-configuration output](./get-configuration-output-properties-ldap_group_policies-items.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies/items`

* [Untitled object in get-configuration output](./get-configuration-output-properties-ha_candidates-items.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates/items`

* [Untitled object in get-openbao-status output](./get-openbao-status-output-properties-ha.md "High availability state (experimental)") – `http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha`

* [Untitled object in get-openbao-status output](./get-openbao-status-output-properties-ha-properties-peers-items.md) – `http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/ha/properties/peers/items`

* [Untitled object in list-clients output](./list-clients-output-properties-clients-items.md) – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items`

* [Untitled object in list-clients output](./list-clients-output-properties-groups-items.md) – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups/items`

* [Untitled object in list-clients output](./list-clients-output-properties-audit-items.md) – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit/items`

* [Untitled object in list-plugins output](./list-plugins-output-properties-plugins-items.md) – `http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items`

* [Untitled object in list-snapshots output](./list-snapshots-output-properties-snapshots-items.md) – `http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots/items`

* [Untitled object in provision-client output](./provision-client-output-properties-groups-items.md) – `http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items`

### Arrays

* [Allowed networks](./configure-module-input-properties-allowed-networks.md "Client IP addresses or networks (CIDR) allowed to reach the OpenBao API and web UI through Traefik") – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ip_allowlist`

* [Group policies](./configure-module-input-properties-group-policies.md "Additional directory groups mapped to OpenBao policies, applied by self-initialization or by openbao-apply-config") – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/ldap_group_policies`

* [Notification recipients](./configure-module-input-properties-notification-recipients.md "Email addresses notified when OpenBao is down or sealed") – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/notify_recipients`

* [Starter kits](./configure-module-input-properties-starter-kits.md "Components prepared by self-initialization or by openbao-apply-config: 'kv' key/value v2 store at secret/, 'pki' internal certificate authority at pki/, 'approle' application login") – `http://schema.nethserver.org/openbao/configure-module-input.json#/properties/starter_kits`

* [Untitled array in configure-plugins input](./configure-plugins-input-properties-plugins.md "Ids of the enabled optional plugins") – `http://schema.nethserver.org/openbao/configure-plugins-input.json#/properties/plugins`

* [Untitled array in get-client-status output](./get-client-status-output-properties-groups.md) – `http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/groups`

* [Untitled array in get-client-status output](./get-client-status-output-properties-groups_requested.md) – `http://schema.nethserver.org/openbao/get-client-status-output.json#/properties/groups_requested`

* [Untitled array in get-configuration output](./get-configuration-output-properties-oidc_providers.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers`

* [Untitled array in get-configuration output](./get-configuration-output-properties-oidc_providers-items-properties-domains.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/oidc_providers/items/properties/domains`

* [Untitled array in get-configuration output](./get-configuration-output-properties-notify_recipients.md "Email addresses notified when OpenBao is down or sealed") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/notify_recipients`

* [Untitled array in get-configuration output](./get-configuration-output-properties-user_domains.md "User domains of the cluster") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/user_domains`

* [Untitled array in get-configuration output](./get-configuration-output-properties-ip_allowlist.md "Networks allowed through Traefik; empty: no restriction") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ip_allowlist`

* [Untitled array in get-configuration output](./get-configuration-output-properties-ldap_group_policies.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ldap_group_policies`

* [Untitled array in get-configuration output](./get-configuration-output-properties-starter_kits.md) – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/starter_kits`

* [Untitled array in get-configuration output](./get-configuration-output-properties-builtin_policies.md "Policies created by the module") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/builtin_policies`

* [Untitled array in get-configuration output](./get-configuration-output-properties-ha_candidates.md "Other OpenBao instances with high availability enabled, which a new instance can join") – `http://schema.nethserver.org/openbao/get-configuration-output.json#/properties/ha_candidates`

* [Untitled array in get-openbao-status output](./get-openbao-status-output-properties-plugins.md "Ids of the optional plugins installed from the catalog") – `http://schema.nethserver.org/openbao/get-openbao-status-output.json#/properties/plugins`

* [Untitled array in list-clients output](./list-clients-output-properties-clients.md) – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients`

* [Untitled array in list-clients output](./list-clients-output-properties-clients-items-properties-groups.md) – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/groups`

* [Untitled array in list-clients output](./list-clients-output-properties-clients-items-properties-groups_requested.md) – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/clients/items/properties/groups_requested`

* [Untitled array in list-clients output](./list-clients-output-properties-groups.md) – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups`

* [Untitled array in list-clients output](./list-clients-output-properties-groups-items-properties-members.md) – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/groups/items/properties/members`

* [Untitled array in list-clients output](./list-clients-output-properties-modules.md "Other modules of the cluster, candidates for approval") – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/modules`

* [Untitled array in list-clients output](./list-clients-output-properties-audit.md) – `http://schema.nethserver.org/openbao/list-clients-output.json#/properties/audit`

* [Untitled array in list-plugins output](./list-plugins-output-properties-plugins.md) – `http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins`

* [Untitled array in list-plugins output](./list-plugins-output-properties-plugins-items-properties-setup_commands.md) – `http://schema.nethserver.org/openbao/list-plugins-output.json#/properties/plugins/items/properties/setup_commands`

* [Untitled array in list-snapshots output](./list-snapshots-output-properties-snapshots.md) – `http://schema.nethserver.org/openbao/list-snapshots-output.json#/properties/snapshots`

* [Untitled array in provision-client output](./provision-client-output-properties-token_policies.md) – `http://schema.nethserver.org/openbao/provision-client-output.json#/properties/token_policies`

* [Untitled array in provision-client output](./provision-client-output-properties-groups.md) – `http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups`

* [Untitled array in provision-client output](./provision-client-output-properties-groups-items-properties-token_policies.md) – `http://schema.nethserver.org/openbao/provision-client-output.json#/properties/groups/items/properties/token_policies`

* [Untitled array in request-client-access input](./request-client-access-input-properties-groups.md "Groups the module asks to join; the administrator decides") – `http://schema.nethserver.org/openbao/request-client-access-input.json#/properties/groups`

* [Untitled array in request-client-access output](./request-client-access-output-properties-groups.md) – `http://schema.nethserver.org/openbao/request-client-access-output.json#/properties/groups`

* [Untitled array in request-client-access output](./request-client-access-output-properties-groups_requested.md) – `http://schema.nethserver.org/openbao/request-client-access-output.json#/properties/groups_requested`

* [Untitled array in send-test-email input](./send-test-email-input-properties-recipients.md "Recipients of the test email") – `http://schema.nethserver.org/openbao/send-test-email-input.json#/properties/recipients`

* [Untitled array in send-test-email output](./send-test-email-output-properties-recipients.md) – `http://schema.nethserver.org/openbao/send-test-email-output.json#/properties/recipients`

* [Untitled array in set-client-access input](./set-client-access-input-properties-groups.md "Shared groups: KV prefix groups/<group id>/ of the ns8-kv mount") – `http://schema.nethserver.org/openbao/set-client-access-input.json#/properties/groups`

* [Untitled array in set-client-access output](./set-client-access-output-properties-groups.md) – `http://schema.nethserver.org/openbao/set-client-access-output.json#/properties/groups`

## Version Note

The schemas linked above follow the JSON Schema Spec version: `http://json-schema.org/draft-07/schema#`
