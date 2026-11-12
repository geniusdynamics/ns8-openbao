*** Settings ***
Library    SSHLibrary
Library    Collections
Resource    openbao.resource

*** Variables ***
${module_id}    ${EMPTY}
${ldap_id}    ${EMPTY}
${HOST}    openbao-dir.example.org
${DOMAIN}    openbaodir.test
${ADMUSER}    admin
${ADMPASS}    Nethesis,1234

*** Test Cases ***
Check if an OpenLDAP user domain can be created
    ${output}  ${rc} =    Execute Command    add-module ghcr.io/nethserver/openldap:latest 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${ldap_id}    ${output.module_id}
    ${rc} =    Execute Command    api-cli run module/${ldap_id}/configure-module --data '{"provision": "new-domain", "domain": "${DOMAIN}", "admuser": "${ADMUSER}", "admpass": "${ADMPASS}"}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Check if openbao is installed correctly
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${module_id}    ${output.module_id}

Check if a missing administrators group is rejected
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "unseal_mode": "auto", "user_domain": "${DOMAIN}", "ldap_admin_group": "no such group", "auto_initialize": true}'
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Check if openbao initializes itself with directory login
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "unseal_mode": "auto", "user_domain": "${DOMAIN}", "ldap_admin_group": "domain admins", "auto_initialize": true, "ldap_group_policies": [{"group": "domain admins", "policy": "ns8-secrets-ro"}], "starter_kits": ["kv", "pki", "approle"]}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${HOST}

Check if the LDAP auth plugin is installed from its image
    ${rc} =    Execute Command    runagent -m ${module_id} test -x openbao-plugins/openbao-plugin-auth-ldap
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Check if the break-glass token gives administrator access
    ${breakglass}  ${rc} =    Execute Command    runagent -m ${module_id} openbao-breakglass-token
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{auth} =    Bao Request    ${HOST}    GET    sys/auth    ${EMPTY}    ${breakglass}
    Dictionary Should Contain Key    ${auth.data}    ldap/

Check if self-initialization created the module token
    ${output}  ${rc} =    Execute Command    runagent -m ${module_id} openbao-module-token status
    ...    return_rc=True
    Should Be Equal    ${output}    valid
    ${output}  ${rc} =    Execute Command    api-cli run module/${module_id}/get-openbao-status
    ...    return_rc=True
    &{status} =    Evaluate    json.loads('''${output}''')    modules=json
    Should Be Equal    ${status.root_token_present}    ${False}

Check if the module is bound to the user domain
    ${output}  ${rc} =    Execute Command    redis-cli HGET cluster/module_domains ${module_id}
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    Should Contain    ${output}    ${DOMAIN}

Check if a domain administrator can log in
    &{login} =    Bao Request    ${HOST}    POST    auth/ldap/login/${ADMUSER}    {"password": "${ADMPASS}"}
    Should Contain    ${login.auth.policies}    ns8-admin
    Set Suite Variable    ${token}    ${login.auth.client_token}

Check if the group policies and starter kits were applied
    &{group} =    Bao Request    ${HOST}    GET    auth/ldap/groups/domain%20admins    ${EMPTY}    ${token}
    Should Contain    ${group.data.policies}    ns8-admin
    Should Contain    ${group.data.policies}    ns8-secrets-ro
    &{mounts} =    Bao Request    ${HOST}    GET    sys/mounts    ${EMPTY}    ${token}
    Dictionary Should Contain Key    ${mounts.data}    pki/
    Dictionary Should Contain Key    ${mounts.data}    secret/
    &{auth} =    Bao Request    ${HOST}    GET    sys/auth    ${EMPTY}    ${token}
    Dictionary Should Contain Key    ${auth.data}    approle/
    &{ca} =    Bao Request    ${HOST}    GET    pki/issuers?list=true    ${EMPTY}    ${token}
    Should Not Be Empty    ${ca.data['keys']}

Check if the domain administrator can manage secrets
    Bao Request    ${HOST}    POST    secret/data/robot    {"data": {"answer": "42"}}    ${token}
    &{secret} =    Bao Request    ${HOST}    GET    secret/data/robot    ${EMPTY}    ${token}
    Should Be Equal    ${secret.data['data']['answer']}    42

Check if the bind password is no longer passed after initialization
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    ${rc} =    Execute Command    runagent -m ${module_id} grep -q NS8_LDAP_BIND_PASSWORD openbao-container.env
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Check if openbao and the user domain are removed correctly
    ${rc} =    Execute Command    remove-module --no-preserve ${module_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    ${rc} =    Execute Command    remove-module --no-preserve ${ldap_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
