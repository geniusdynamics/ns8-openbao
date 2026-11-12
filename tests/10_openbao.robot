*** Settings ***
Library    SSHLibrary
Library    String
Resource    openbao.resource

*** Variables ***
${ADMIN_USER}    admin
${ADMIN_PASSWORD}    Nethesis,1234
${module_id}    ${EMPTY}
${HOST}    openbao-test.example.org

*** Keywords ***
Login to cluster-admin
    New Page    https://${NODE_ADDR}/cluster-admin/
    Fill Text    text="Username"    ${ADMIN_USER}
    Click    button >> text="Continue"
    Fill Text    text="Password"    ${ADMIN_PASSWORD}
    Click    button >> text="Log in"
    Wait For Elements State    css=#main-content    visible    timeout=10s

*** Test Cases ***
Check if openbao is installed correctly
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Global Variable    ${module_id}    ${output.module_id}

Take screenshots
    [Tags]    ui
    Import Library    Browser
    New Browser    chromium    headless=True
    New Context    ignoreHTTPSErrors=True
    Login to cluster-admin
    Go To    https://${NODE_ADDR}/cluster-admin/#/apps/${module_id}
    Wait For Elements State    iframe >>> h2 >> text="Status"    visible    timeout=10s
    Sleep    5s
    Take Screenshot    filename=${OUTPUT DIR}/browser/screenshot/1._Status.png
    Go To    https://${NODE_ADDR}/cluster-admin/#/apps/${module_id}?page=settings
    Wait For Elements State    iframe >>> h2 >> text="Settings"    visible    timeout=10s
    Sleep    5s
    Take Screenshot    filename=${OUTPUT DIR}/browser/screenshot/2._Settings.png
    Close Browser

Check if openbao can be configured
    Configure OpenBao    ${module_id}    ${HOST}    manual

Check if the service is running
    ${rc} =    Execute Command    runagent -m ${module_id} systemctl --user -q is-active openbao.service
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Check if openbao is published by Traefik and not initialized
    &{status} =    Seal Status    ${HOST}
    Should Be Equal    ${status.initialized}    ${False}
    Should Be Equal    ${status.type}    shamir

Check if get-openbao-status reports the server state
    ${output}  ${rc} =    Execute Command    api-cli run module/${module_id}/get-openbao-status
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{status} =    Evaluate    json.loads('''${output}''')    modules=json
    Should Be Equal    ${status.service_active}    ${True}
    Should Be Equal    ${status.initialized}    ${False}
    Should Be Equal    ${status.ui_url}    https://${HOST}/ui/

Check if metrics are exported
    ${output}  ${rc} =    Execute Command    runagent -m ${module_id} export-metrics
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    Should Contain    ${output}    openbao_up 1
    Should Contain    ${output}    openbao_initialized 0

Check if the alert rules are published
    FOR    ${rule}    IN    openbao-down    openbao-sealed    openbao-uninitialized
        ${output}  ${rc} =    Execute Command    redis-cli HEXISTS module/${module_id}/metrics_alert_rules ${rule}
        ...    return_rc=True
        Should Be Equal As Integers    ${rc}  0
        Should Be Equal As Integers    ${output}  1
    END

Check if notification recipients are validated
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "notify_recipients": ["not-an-address"]}'
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Check if notifications enable the check timer
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "notify_recipients": ["security@example.org"]}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    ${rc} =    Execute Command    runagent -m ${module_id} systemctl --user -q is-active openbao-notify.timer
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Check if openbao can be initialized and unsealed
    &{init} =    Bao Request    ${HOST}    PUT    sys/init    {"secret_shares": 1, "secret_threshold": 1}
    Set Suite Variable    ${root_token}    ${init.root_token}
    Set Suite Variable    ${unseal_key}    ${init['keys'][0]}
    Unseal OpenBao    ${HOST}    ${unseal_key}
    Wait Until Keyword Succeeds    30s    2s    OpenBao Should Be Active    ${HOST}

Check if a secret can be stored
    Bao Request    ${HOST}    POST    sys/mounts/secret    {"type": "kv", "options": {"version": "2"}}    ${root_token}
    Bao Request    ${HOST}    POST    secret/data/robot    {"data": {"answer": "42"}}    ${root_token}

Check if the Prometheus target is published
    ${output}  ${rc} =    Execute Command    redis-cli HGET module/${module_id}/metrics_targets openbao
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    Should Contain    ${output}    /v1/sys/metrics
    ${target} =    Evaluate    json.loads('''${output}''')[0]['targets'][0]    modules=json
    Set Suite Variable    ${metrics_target}    ${target}

Check if Prometheus metrics can be scraped from the cluster VPN address
    ${output}  ${rc} =    Execute Command    curl -sS -f 'http://${metrics_target}/v1/sys/metrics?format=prometheus'
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    Should Contain    ${output}    vault_core_unsealed

Check if metrics are not served by the public listener
    ${rc} =    Execute Command    curl -sS -f -o /dev/null -H 'Host: ${HOST}' 'http://127.0.0.1/v1/sys/metrics?format=prometheus'
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Check if the unseal mode is locked after initialization
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "unseal_mode": "auto"}'
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Check if a settings change is applied without sealing openbao
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "log_level": "debug", "audit_log": true}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    &{status} =    Seal Status    ${HOST}
    Should Be Equal    ${status.sealed}    ${False}

Check if secrets survive a restart with manual unseal
    ${rc} =    Execute Command    runagent -m ${module_id} systemctl --user restart openbao.service
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    &{status} =    Seal Status    ${HOST}
    Should Be Equal    ${status.initialized}    ${True}
    Should Be Equal    ${status.sealed}    ${True}
    Unseal OpenBao    ${HOST}    ${unseal_key}
    Wait Until Keyword Succeeds    30s    2s    OpenBao Should Be Active    ${HOST}
    &{secret} =    Bao Request    ${HOST}    GET    secret/data/robot    ${EMPTY}    ${root_token}
    Should Be Equal    ${secret.data['data']['answer']}    42

Check if openbao is removed correctly
    ${rc} =    Execute Command    remove-module --no-preserve ${module_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
