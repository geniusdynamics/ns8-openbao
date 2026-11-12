*** Settings ***
Library    SSHLibrary
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
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "unseal_mode": "auto", "user_domain": "${DOMAIN}", "ldap_admin_group": "domain admins", "auto_initialize": true}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${HOST}

Check if the module is bound to the user domain
    ${output}  ${rc} =    Execute Command    redis-cli HGET cluster/module_domains ${module_id}
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    Should Contain    ${output}    ${DOMAIN}

Check if a domain administrator can log in
    &{login} =    Bao Request    ${HOST}    POST    auth/ldap/login/${ADMUSER}    {"password": "${ADMPASS}"}
    Should Contain    ${login.auth.policies}    ns8-admin
    Set Suite Variable    ${token}    ${login.auth.client_token}

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
