*** Settings ***
Library    SSHLibrary
Library    Collections
Resource    openbao.resource

*** Variables ***
${provider_id}    ${EMPTY}
${module_id}    ${EMPTY}
${PROVIDER_HOST}    openbao-kms.example.org
${HOST}    openbao-transit.example.org

*** Test Cases ***
Check if a Transit provider instance can be prepared
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${provider_id}    ${output.module_id}
    ${rc} =    Execute Command    api-cli run module/${provider_id}/configure-module --data '{"host": "${PROVIDER_HOST}", "http2https": false, "unseal_mode": "auto", "vpn_api": true}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    &{init} =    Bao Request    ${PROVIDER_HOST}    PUT    sys/init    {"recovery_shares": 1, "recovery_threshold": 1}
    Set Suite Variable    ${provider_token}    ${init.root_token}
    Wait Until Keyword Succeeds    30s    2s    OpenBao Should Be Active    ${PROVIDER_HOST}
    Bao Request    ${PROVIDER_HOST}    POST    sys/mounts/transit    {"type": "transit"}    ${provider_token}
    Bao Request    ${PROVIDER_HOST}    POST    transit/keys/ns8-unseal    {}    ${provider_token}
    Bao Request    ${PROVIDER_HOST}    POST    sys/policies/acl/ns8-unseal    {"policy": "path \\"transit/encrypt/ns8-unseal\\" { capabilities = [\\"update\\"] }\\npath \\"transit/decrypt/ns8-unseal\\" { capabilities = [\\"update\\"] }"}    ${provider_token}
    &{token} =    Bao Request    ${PROVIDER_HOST}    POST    auth/token/create-orphan    {"policies": ["ns8-unseal"], "period": "768h"}    ${provider_token}
    Set Suite Variable    ${transit_token}    ${token.auth.client_token}
    ${url}  ${rc} =    Execute Command    redis-cli HGET module/${provider_id}/srv/http/openbao url
    ...    return_rc=True
    Should Start With    ${url}    http://
    Set Suite Variable    ${transit_url}    ${url}

Check if Transit unseal is rejected without a token
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${module_id}    ${output.module_id}
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "unseal_mode": "transit", "transit_address": "${transit_url}", "transit_key": "ns8-unseal"}'
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Check if OpenBao unseals itself with the Transit provider
    ${rc} =    Execute Command    runagent -m ${module_id} env TRANSIT_TOKEN=${transit_token} openbao-transit-token
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "unseal_mode": "transit", "transit_address": "${transit_url}", "transit_key": "ns8-unseal"}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    &{status} =    Seal Status    ${HOST}
    Should Be Equal    ${status.type}    transit
    &{init} =    Bao Request    ${HOST}    PUT    sys/init    {"recovery_shares": 1, "recovery_threshold": 1}
    Wait Until Keyword Succeeds    30s    2s    OpenBao Should Be Active    ${HOST}
    ${rc} =    Execute Command    runagent -m ${module_id} systemctl --user restart openbao.service
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${HOST}

Check if the instances are removed correctly
    ${rc} =    Execute Command    remove-module --no-preserve ${module_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    ${rc} =    Execute Command    remove-module --no-preserve ${provider_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
