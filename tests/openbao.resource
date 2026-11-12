*** Settings ***
Library    SSHLibrary

*** Keywords ***
Configure OpenBao
    [Arguments]    ${module_id}    ${host}    ${unseal_mode}
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${host}", "http2https": false, "lets_encrypt": false, "unseal_mode": "${unseal_mode}"}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Bao Request
    [Documentation]    Call the OpenBao API through Traefik and return the decoded JSON response
    [Arguments]    ${host}    ${method}    ${path}    ${data}=${EMPTY}    ${token}=${EMPTY}
    ${token_header} =    Set Variable If    '${token}' != ''    -H 'X-Vault-Token: ${token}'    ${EMPTY}
    ${data_arg} =    Set Variable If    '${data}' != ''    --data '${data}'    ${EMPTY}
    ${output}  ${rc} =    Execute Command    curl -sS -f -X ${method} -H 'Host: ${host}' ${token_header} ${data_arg} http://127.0.0.1/v1/${path}
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    IF    '''${output}''' == ''
        RETURN    &{EMPTY}
    END
    &{response} =    Evaluate    json.loads('''${output}''')    modules=json
    RETURN    &{response}

Seal Status
    [Arguments]    ${host}
    &{status} =    Bao Request    ${host}    GET    sys/seal-status
    RETURN    &{status}

Unseal OpenBao
    [Arguments]    ${host}    ${key}
    Bao Request    ${host}    PUT    sys/unseal    {"key": "${key}"}

OpenBao Should Be Active
    [Arguments]    ${host}
    ${rc} =    Execute Command    curl -sS -f -o /dev/null -H 'Host: ${host}' http://127.0.0.1/v1/sys/health
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Route Should Be Forbidden
    [Arguments]    ${host}
    ${output}  ${rc} =    Execute Command    curl -sS -o /dev/null -w '%{http_code}' -H 'Host: ${host}' http://127.0.0.1/v1/sys/seal-status
    ...    return_rc=True
    Should Be Equal    ${output}    403

Execute Command And Expect Success
    [Arguments]    ${command}
    ${rc} =    Execute Command    ${command}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
