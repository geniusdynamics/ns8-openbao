*** Settings ***
Documentation    Client provisioning: off by default; enabled with the toggle and an
...              administrator token given on the node; a second module (another
...              instance of this image, granted the secretsclient role) requests
...              access, is approved, unwraps its token and is confined to its own
...              key/value prefix and the group granted by the administrator;
...              revocation and disabling revoke the tokens.
Library    SSHLibrary
Library    Collections
Resource    openbao.resource

*** Variables ***
${module_id}    ${EMPTY}
${client}    ${EMPTY}
${HOST}    openbao-clients.example.org
${PROBE}    /tmp/openbao-client-probe.py
${GROUP}    robot-group

*** Keywords ***
Run Action
    [Arguments]    ${action}    ${data}={}
    ${output}  ${rc} =    Execute Command    api-cli run module/${module_id}/${action} --data '${data}'
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0    ${action} failed: ${output}
    ${result} =    Evaluate    json.loads($output)    modules=json
    RETURN    ${result}

As Client
    [Documentation]    Run the probe as the client module; it prints JSON without secrets
    [Arguments]    @{args}
    ${quoted} =    Evaluate    " ".join("'" + a + "'" for a in $args)
    ${output}  ${rc} =    Execute Command    runagent -m ${client} python3 ${PROBE} ${module_id} ${quoted}
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0    ${output}
    ${result} =    Evaluate    json.loads($output.strip().splitlines()[-1])    modules=json
    RETURN    ${result}

Client Status Should Be
    [Arguments]    ${path}    ${expected}    @{group}
    &{result} =    As Client    kv-write    ${path}    @{group}
    Should Be Equal As Integers    ${result.status}    ${expected}    write ${path}

*** Test Cases ***
Check if openbao is installed and initialized
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${module_id}    ${output.module_id}
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "unseal_mode": "auto", "vpn_api": true}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    &{init} =    Bao Request    ${HOST}    PUT    sys/init    {"recovery_shares": 1, "recovery_threshold": 1}
    Set Suite Variable    ${root_token}    ${init.root_token}
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${HOST}
    Bao Request    ${HOST}    POST    sys/mounts/secret    {"type": "kv", "options": {"version": "2"}}    ${root_token}

Check if client provisioning is off by default
    &{config} =    Run Action    get-configuration
    Should Be Equal    ${config.client_provisioning}    ${False}
    Should Be Equal    ${config.client_provisioner_set}    ${False}
    &{clients} =    Run Action    list-clients
    Should Be Equal    ${clients.provisioner}    missing
    ${rc} =    Execute Command    runagent -m ${module_id} env BAO_TOKEN='${root_token}' openbao-client-provisioner create
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Check if a client module can be installed
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${client}    ${output.module_id}
    # What NS8 does for a module image that declares openbao@any:secretsclient
    Execute Command And Expect Success    redis-cli HSET roles/module/${client} module/${module_id} secretsclient
    Put File    ${CURDIR}/openbao-client-probe.py    ${PROBE}    mode=0644

Check if the client is refused while provisioning is off
    &{result} =    As Client    provision    {}
    Should Not Be Equal As Integers    ${result.exit_code}    0
    Should Contain    ${result.output}[0][error]    client_provisioning_disabled

Check if client provisioning can be enabled
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "vpn_api": true, "client_provisioning": true}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    ${output}  ${rc} =    Execute Command    runagent -m ${module_id} env BAO_TOKEN='${root_token}' openbao-client-provisioner create
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0    ${output}
    Should Not Contain    ${output}    ${root_token}
    ${output} =    Execute Command    runagent -m ${module_id} openbao-client-provisioner status
    Should Be Equal    ${output}    valid
    ${output} =    Execute Command    runagent -m ${module_id} stat -c %a openbao-provisioner.token
    Should Be Equal    ${output}    600
    &{config} =    Run Action    get-configuration
    Should Be Equal    ${config.client_provisioner_set}    ${True}

Check if the provisioner token cannot write policies
    ${token} =    Execute Command    runagent -m ${module_id} cat openbao-provisioner.token
    ${output} =    Execute Command    curl -s -o /dev/null -w '\%{http_code}' -X POST -H 'Host: ${HOST}' -H 'X-Vault-Token: ${token}' --data '{"policy": "path \\"*\\" { capabilities = [\\"sudo\\"] }"}' http://127.0.0.1/v1/sys/policies/acl/ns8-client-evil
    Should Be Equal    ${output}    403
    ${output} =    Execute Command    curl -s -o /dev/null -w '\%{http_code}' -X POST -H 'Host: ${HOST}' -H 'X-Vault-Token: ${token}' --data '{"policies": ["ns8-admin"]}' http://127.0.0.1/v1/auth/token/create/ns8-client
    Should Be Equal    ${output}    400

Check if an unapproved client is recorded as pending
    &{result} =    As Client    provision    {}
    Should Contain    ${result.output}[0][error]    client_not_approved
    &{result} =    As Client    action    request-client-access    {"groups": ["${GROUP}"]}
    Should Be Equal As Integers    ${result.exit_code}    0
    Should Be Equal    ${result.output}[status]    pending
    Should Be Equal    ${result.output}[groups_requested]    ${{ ["${GROUP}"] }}
    &{result} =    As Client    action    get-client-status    {}
    Should Be Equal    ${result.output}[status]    pending
    Should Be Equal    ${result.output}[groups]    ${{ [] }}
    &{clients} =    Run Action    list-clients
    ${ids} =    Evaluate    [c['module_id'] for c in $clients['clients'] if c['status'] == 'pending']
    Should Contain    ${ids}    ${client}

Check if an approved client gets a wrapped token confined to its prefix
    &{grant} =    Run Action    set-client-access    {"module_id": "${client}", "allowed": true, "groups": ["${GROUP}"]}
    Should Be Equal    ${grant.allowed}    ${True}
    &{result} =    As Client    provision    {}
    Should Be Equal As Integers    ${result.exit_code}    0    ${result}
    Should Be Equal    ${result.kv_prefix}    modules/${client}
    Should Contain    ${result.policies}    ns8-client-kv
    Should Not Contain    ${result.policies}    ns8-client-db
    # The wrapping token is single use
    Should Be Equal As Integers    ${result.second_unwrap_status}    400
    Client Status Should Be    modules/${client}/robot    200
    Client Status Should Be    modules/${module_id}9/robot    403
    Client Status Should Be    groups/${GROUP}/robot    403
    Client Status Should Be    groups/${GROUP}/robot    200    ${GROUP}
    Client Status Should Be    groups/other-group/robot    403    ${GROUP}
    &{write} =    As Client    write    secret/data/robot
    Should Be Equal As Integers    ${write.status}    403
    &{write} =    As Client    write    sys/policies/acl/robot
    Should Be Equal As Integers    ${write.status}    403
    &{renew} =    As Client    renew-self
    Should Be Equal As Integers    ${renew.status}    200

Check if the task output holds no usable credential
    &{clients} =    Run Action    list-clients
    ${audit} =    Evaluate    [a['event'] for a in $clients['audit']]
    Should Contain    ${audit}    token_issued
    ${token} =    Execute Command    runagent -m ${client} cat openbao-client.token
    ${output} =    Execute Command    redis-cli --scan --pattern 'task/module/${module_id}/*' | xargs -r -n1 redis-cli HGETALL
    Should Not Contain    ${output}    ${token}

Check if revoking the client revokes its token
    &{result} =    Run Action    set-client-access    {"module_id": "${client}", "allowed": false}
    Should Be Equal    ${result.cleanup}    done
    &{lookup} =    As Client    lookup-self
    Should Be Equal As Integers    ${lookup.status}    403
    &{result} =    As Client    provision    {}
    Should Contain    ${result.output}[0][error]    client_not_approved

Check if disabling revokes the client and provisioner tokens
    Run Action    set-client-access    {"module_id": "${client}", "allowed": true}
    &{result} =    As Client    provision    {}
    Should Be Equal As Integers    ${result.exit_code}    0
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host": "${HOST}", "http2https": false, "vpn_api": true, "client_provisioning": false}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    &{lookup} =    As Client    lookup-self
    Should Be Equal As Integers    ${lookup.status}    403
    ${output} =    Execute Command    runagent -m ${module_id} openbao-client-provisioner status
    Should Be Equal    ${output}    missing

Check if the modules are removed correctly
    FOR    ${mid}    IN    ${client}    ${module_id}
        ${rc} =    Execute Command    remove-module --no-preserve ${mid}
        ...    return_rc=True  return_stdout=False
        Should Be Equal As Integers    ${rc}  0
    END
    Execute Command    rm -f ${PROBE}
