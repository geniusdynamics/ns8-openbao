# SPDX-License-Identifier: GPL-3.0-or-later
"""Manage NS8 OIDC and local recovery on an initialized OpenBao server."""

import hashlib
import re
from urllib.error import HTTPError

import openbao

OIDC_PREFIX = "ns8-oidc-"
OIDC_DESCRIPTION = "OpenBao module NS8 OIDC"
RECOVERY_MOUNT = "ns8-recovery"
RECOVERY_DESCRIPTION = "OpenBao module local recovery"
RECOVERY_USER = "breakglass"
OIDC_ROLE = "ns8"
OIDC_FIELDS = {
    "oidc_provider": "OPENBAO_OIDC_PROVIDER",
    "oidc_domain": "OPENBAO_OIDC_DOMAIN",
    "oidc_link_identities": "OPENBAO_OIDC_LINK_IDENTITIES",
}


class AuthError(Exception):
    pass


def settings(env):
    return {
        "oidc_provider": env["OPENBAO_OIDC_PROVIDER"],
        "oidc_domain": env["OPENBAO_OIDC_DOMAIN"],
        "oidc_link_identities": openbao.is_true(env["OPENBAO_OIDC_LINK_IDENTITIES"]),
    }


def providers():
    import agent

    domains = [domain["name"] for domain in openbao.list_user_domains()
               if domain["schema"] in ("ad", "rfc2307")]
    result = {}
    for record in agent.list_service_providers(agent.redis_connect(), "oidc", "http",
                                               sortby="module_seq_asc"):
        module = record.get("module_id", "")
        uuid = record.get("module_uuid")
        host = record.get("host", "")
        prefix = record.get("issuer_url_prefix", "")
        if not uuid or not re.fullmatch(r"(?:idp|keycloak|lemonldapng)[0-9]+", module):
            continue
        if not re.fullmatch(r"[a-zA-Z0-9.-]+", host):
            continue
        if not re.fullmatch(rf"https://{re.escape(host)}(?:/[a-zA-Z0-9_-]+)+/", prefix):
            continue
        fixed = record.get("domain", "")
        result[uuid] = {
            "id": uuid,
            "module": module,
            "label": f"{record['ui_name']} ({module})" if record.get("ui_name") else module,
            "prefix": prefix,
            "domains": [domain for domain in domains if not fixed or domain == fixed],
        }
    return result


def selection_errors(request, env):
    current = settings(env)
    selected = current | {field: request[field] for field in OIDC_FIELDS if field in request}
    provider = selected["oidc_provider"]
    domain = selected["oidc_domain"]
    ldap = request.get("user_domain", env["OPENBAO_USER_DOMAIN"])
    if selected["oidc_link_identities"] and (not provider or not domain or ldap != domain):
        yield "oidc_link_identities", "oidc_same_domain_required"
    if not provider:
        return
    if not request.get("public_access", openbao.public_access(env)):
        yield "oidc_provider", "oidc_requires_web_access"
    if (provider, domain) != (current["oidc_provider"], current["oidc_domain"]):
        endpoint = providers().get(provider)
        if not endpoint:
            yield "oidc_provider", "oidc_provider_unavailable"
        elif domain not in endpoint["domains"]:
            yield "oidc_domain", "oidc_domain_unavailable"


def managed_oidc(mounts):
    return [
        path.rstrip("/") for path, mount in mounts.items()
        if re.fullmatch(OIDC_PREFIX + r"[0-9a-f]{16}/", path)
        and mount.get("type") in ("oidc", "jwt")
        and mount.get("description") == OIDC_DESCRIPTION
    ]


def mount_name(provider, issuer):
    binding = f"{provider}\n{issuer}".encode()
    return OIDC_PREFIX + hashlib.sha256(binding).hexdigest()[:16]


def register_client(endpoint, domain, issuer, redirects):
    import os
    import agent.tasks

    client_id = os.environ["MODULE_ID"]
    result = agent.tasks.run(
        f"module/{endpoint['module']}", "register-client",
        data={"domain": domain, "redirect_uris": redirects, "post_logout_redirect_uris": []},
        extra={"isNotificationHidden": True},
    )
    response = result.get("output")
    if result.get("exit_code") != 0 or not isinstance(response, dict):
        raise AuthError("NS8 could not register the OpenBao OIDC client")
    if (
        response.get("issuer") != issuer or response.get("realm") != domain
        or response.get("client_id") != client_id
        or not isinstance(response.get("client_secret"), str) or not response["client_secret"]
    ):
        raise AuthError("NS8 returned an unexpected OpenBao OIDC client")
    return client_id, response["client_secret"]


def apply_oidc(call, env):
    if openbao.ha_role(env) == "member":
        raise AuthError("Apply OIDC from the OpenBao cluster's primary module")
    selected = settings(env)
    mounts = call("sys/auth")["data"]
    old = managed_oidc(mounts)
    provider, domain = selected["oidc_provider"], selected["oidc_domain"]
    if not provider:
        for path in old:
            call(f"sys/auth/{path}", method="DELETE")
        if old:
            print("Module-managed OIDC disabled")
        return

    endpoint = providers().get(provider)
    if not endpoint or domain not in endpoint["domains"]:
        raise AuthError("The selected OIDC provider or domain is unavailable")
    if not openbao.public_access(env) or not env.get("TRAEFIK_HOST"):
        raise AuthError("OIDC requires the OpenBao HTTPS route")
    issuer = endpoint["prefix"] + domain
    path = mount_name(provider, issuer)
    if path + "/" in mounts and path not in old:
        raise AuthError("The OIDC mount path is already used by another configuration")
    host = env["TRAEFIK_HOST"]
    redirects = [
        f"https://{host}/ui/vault/auth/{path}/oidc/callback",
        f"https://{host}/v1/auth/{path}/oidc/callback",
    ]
    client_id, secret = register_client(endpoint, domain, issuer, redirects)

    created = path not in old
    if created:
        call(f"sys/auth/{path}", method="POST", data={"type": "oidc", "description": OIDC_DESCRIPTION})
    try:
        call(f"auth/{path}/role/{OIDC_ROLE}", method="POST", data={
            "role_type": "oidc",
            "user_claim": "sub",
            "bound_audiences": [client_id],
            "allowed_redirect_uris": redirects,
            "token_ttl": "1h",
            "token_explicit_max_ttl": "8h",
        })
        call(f"auth/{path}/config", method="POST", data={
            "oidc_discovery_url": issuer,
            "oidc_client_id": client_id,
            "oidc_client_secret": secret,
            "default_role": OIDC_ROLE,
        })
        call(f"sys/auth/{path}/tune", method="POST", data={"listing_visibility": "unauth"})
    except HTTPError:
        if created:
            call(f"sys/auth/{path}", method="DELETE")
        raise
    for previous in old:
        if previous != path:
            call(f"sys/auth/{previous}", method="DELETE")
    print(f"OIDC enabled: bao login -method=oidc -path={path} callbackmode=direct")


def recovery(call, action, password=None):
    path = f"sys/auth/{RECOVERY_MOUNT}"
    existing = call("sys/auth")["data"].get(RECOVERY_MOUNT + "/")
    if existing is not None and (
        existing.get("type") != "userpass" or existing.get("description") != RECOVERY_DESCRIPTION
    ):
        raise AuthError("The recovery mount path is already used by another configuration")
    if action == "disable":
        if existing is not None:
            call(path, method="DELETE")
        return
    if password is None or len(password.encode()) < 24 or len(password.encode()) > 72:
        raise AuthError("Use a randomly generated recovery password of 24 to 72 bytes")
    for request in openbao.policy_requests():
        if request["path"] == f"sys/policies/acl/{openbao.ADMIN_POLICY_NAME}":
            call(request["path"], method="POST", data=request["data"])
    if existing is None:
        call(path, method="POST", data={"type": "userpass", "description": RECOVERY_DESCRIPTION})
    try:
        call(f"auth/{RECOVERY_MOUNT}/users/{RECOVERY_USER}", method="POST", data={
            "password": password,
            "token_policies": [openbao.ADMIN_POLICY_NAME],
            "token_ttl": "15m",
            "token_explicit_max_ttl": "1h",
        })
    except HTTPError:
        if existing is None:
            call(path, method="DELETE")
        raise
    if existing is not None:
        # Expire credentials issued with the old password.
        call(f"sys/leases/revoke-prefix/auth/{RECOVERY_MOUNT}/login/{RECOVERY_USER}",
             method="POST", data={"sync": True})


def lookup_alias(call, mount, name):
    response = call("identity/lookup/entity", method="POST", data={
        "alias_mount_accessor": mount["accessor"], "alias_name": name,
    })
    entity = response.get("data", {})
    matches = [alias for alias in entity.get("aliases", [])
               if alias["mount_accessor"] == mount["accessor"] and alias["name"] == name]
    if len(matches) != 1:
        raise AuthError("Both users must have signed in first and the alias names must match exactly")
    return entity, matches[0]


def aliases_to_link(call, env, ldap_name, oidc_subject):
    selected = settings(env)
    provider, domain = selected["oidc_provider"], selected["oidc_domain"]
    if not selected["oidc_link_identities"] or not domain or domain != env["OPENBAO_USER_DOMAIN"]:
        raise AuthError("Enable shared identities for the same LDAP and OIDC domain in Settings")
    endpoint = providers().get(provider)
    if not endpoint or domain not in endpoint["domains"]:
        raise AuthError("The shared OIDC domain could not be verified")
    issuer = endpoint["prefix"] + domain
    path = mount_name(provider, issuer)
    mounts = call("sys/auth")["data"]
    ldap = mounts.get("ldap/", {})
    if ldap.get("type") != "ldap" or path not in managed_oidc(mounts):
        raise AuthError("Apply both authentication methods before linking users")
    params = openbao.discover_ldap(domain)
    if not params:
        raise AuthError("The LDAP domain could not be verified")
    active = call("auth/ldap/config").get("data", {})
    expected = openbao.ldap_auth_config(params, "")
    if any(active.get(key) != expected[key] for key in ("url", "binddn", "userdn", "userattr")):
        raise AuthError("The LDAP mount does not match the selected domain")
    oidc = mounts[path + "/"]
    ldap_entity, _ = lookup_alias(call, ldap, ldap_name)
    oidc_entity, alias = lookup_alias(call, oidc, oidc_subject)
    if ldap_entity["id"] == oidc_entity["id"]:
        return None, ldap_entity["id"]
    if ldap_entity.get("disabled") or oidc_entity.get("disabled"):
        raise AuthError("Disabled identities cannot be linked")
    if any(item["mount_accessor"] == oidc["accessor"] for item in ldap_entity["aliases"]):
        raise AuthError("The LDAP entity already has a different alias on this OIDC mount")
    if oidc_entity.get("policies") or oidc_entity.get("group_ids") or len(oidc_entity["aliases"]) != 1:
        raise AuthError("The OIDC entity has independent permissions or aliases; review it in OpenBao")
    return alias["id"], ldap_entity["id"]
