*** Settings ***
Library    SSHLibrary
Resource    openbao.resource

*** Variables ***
${module_id}    ${EMPTY}
${HOST}    openbao.example.org

*** Test Cases ***
Check if openbao is installed correctly
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${module_id}    ${output.module_id}

Check if openbao can be configured with automatic unseal
    Configure OpenBao    ${module_id}    ${HOST}    auto
    &{status} =    Seal Status    ${HOST}
    Should Be Equal    ${status.initialized}    ${False}
    Should Be Equal    ${status.type}    static

Check if the static seal key is private
    ${output}  ${rc} =    Execute Command    runagent -m ${module_id} stat -c %a openbao-seal.key openbao-container.env
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    Should Be Equal    ${output}    600\n600

Check if openbao can be initialized
    &{init} =    Bao Request    ${HOST}    PUT    sys/init    {"recovery_shares": 1, "recovery_threshold": 1}
    Set Suite Variable    ${root_token}    ${init.root_token}
    Wait Until Keyword Succeeds    30s    2s    OpenBao Should Be Active    ${HOST}
    Bao Request    ${HOST}    POST    sys/mounts/secret    {"type": "kv", "options": {"version": "2"}}    ${root_token}
    Bao Request    ${HOST}    POST    secret/data/robot    {"data": {"answer": "42"}}    ${root_token}

Check if openbao unseals itself after a restart
    ${rc} =    Execute Command    runagent -m ${module_id} systemctl --user restart openbao.service
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${HOST}
    &{secret} =    Bao Request    ${HOST}    GET    secret/data/robot    ${EMPTY}    ${root_token}
    Should Be Equal    ${secret.data['data']['answer']}    42

Check if the backup dump takes a consistent copy and restarts openbao
    ${rc} =    Execute Command    runagent -m ${module_id} module-dump-state
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    ${rc} =    Execute Command    runagent -m ${module_id} test -s openbao-data.tar
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${HOST}
    ${rc} =    Execute Command    runagent -m ${module_id} module-cleanup-state
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Check if openbao is removed correctly
    ${rc} =    Execute Command    remove-module --no-preserve ${module_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
