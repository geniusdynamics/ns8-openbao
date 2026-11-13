*** Settings ***
Documentation    High availability: two instances on the same node form a Raft
...              cluster through the node VPN address, as instances on
...              different nodes do.
Library    SSHLibrary
Library    Collections
Resource    openbao.resource

*** Variables ***
${HOST}    openbao.example.org
${primary}    ${EMPTY}
${member}    ${EMPTY}
${PRIMARY_HOST}    openbao-ha1.example.org
${MEMBER_HOST}    openbao-ha2.example.org

*** Keywords ***
Raft Servers
    &{conf} =    Bao Request    ${PRIMARY_HOST}    GET    sys/storage/raft/configuration    ${EMPTY}    ${root_token}
    RETURN    ${conf.data.config.servers}

Raft Should Have Servers
    [Arguments]    ${count}
    ${servers} =    Raft Servers
    Length Should Be    ${servers}    ${count}

Instance Should Be Unsealed
    [Arguments]    ${host}
    &{status} =    Seal Status    ${host}
    Should Be Equal    ${status.initialized}    ${True}
    Should Be Equal    ${status.sealed}    ${False}

Secret Should Be Readable
    [Arguments]    ${host}
    &{secret} =    Bao Request    ${host}    GET    secret/data/robot    ${EMPTY}    ${root_token}
    Should Be Equal    ${secret.data['data']['answer']}    42

Configure Should Fail
    [Arguments]    ${module_id}    ${data}
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host":"${HOST}","http2https":true,"lets_encrypt":false}'
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Configure Should Succeed
    [Arguments]    ${module_id}    ${data}
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host":"${HOST}","http2https":true,"lets_encrypt":false}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

*** Test Cases ***
Check if two openbao instances are installed
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${primary}    ${output.module_id}
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${member}    ${output.module_id}

Check if a standalone instance is initialized with a secret
    Configure OpenBao    ${primary}    ${PRIMARY_HOST}    manual
    &{init} =    Bao Request    ${PRIMARY_HOST}    PUT    sys/init    {"secret_shares": 1, "secret_threshold": 1}
    Set Suite Variable    ${root_token}    ${init.root_token}
    Set Suite Variable    ${unseal_key}    ${init['keys'][0]}
    Unseal OpenBao    ${PRIMARY_HOST}    ${unseal_key}
    Wait Until Keyword Succeeds    30s    2s    OpenBao Should Be Active    ${PRIMARY_HOST}
    Bao Request    ${PRIMARY_HOST}    POST    sys/mounts/secret    {"type": "kv", "options": {"version": "2"}}    ${root_token}
    Wait Until Keyword Succeeds    30s    2s
    ...    Bao Request    ${PRIMARY_HOST}    POST    secret/data/robot    {"data": {"answer": "42"}}    ${root_token}
    ${rc} =    Execute Command    runagent -m ${primary} env BAO_TOKEN=${root_token} openbao-module-token create
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Check if automatic unseal cannot accept members
    Configure Should Fail    ${member}
    ...    {"host": "${MEMBER_HOST}", "http2https": false, "unseal_mode": "auto", "ha_role": "primary"}

Check if joining needs an instance that accepts members
    Configure Should Fail    ${member}
    ...    {"host": "${MEMBER_HOST}", "http2https": false, "ha_role": "member", "ha_join": "${primary}"}

Check if the initialized instance accepts members
    Configure Should Succeed    ${primary}    {"host": "${PRIMARY_HOST}", "http2https": false, "ha_role": "primary"}
    Wait Until Keyword Succeeds    30s    2s    Unseal OpenBao    ${PRIMARY_HOST}    ${unseal_key}
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${PRIMARY_HOST}
    Secret Should Be Readable    ${PRIMARY_HOST}
    # The Raft address moved from loopback to the node VPN address
    ${servers} =    Raft Servers
    Length Should Be    ${servers}    1
    Should Be Equal    ${servers[0]['node_id']}    ns8-openbao
    Should Not Contain    ${servers[0]['address']}    127.0.0.1
    ${port}  ${rc} =    Execute Command    redis-cli HGET module/${primary}/srv/tcp/openbao-cluster port
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    Should Not Be Empty    ${port}

Check if a new instance discovers the instance that accepts members
    ${output}  ${rc} =    Execute Command    api-cli run module/${member}/get-configuration
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{config} =    Evaluate    json.loads($output)    modules=json
    ${ids} =    Evaluate    [c['module_id'] for c in $config['ha_candidates']]
    Should Contain    ${ids}    ${primary}
    Should Not Contain    ${ids}    ${member}

Check if a new instance joins the cluster
    Configure Should Succeed    ${member}
    ...    {"host": "${MEMBER_HOST}", "http2https": false, "ha_role": "member", "ha_join": "${primary}"}
    # With manual unseal the member completes the join when it is unsealed
    # with the unseal keys of the cluster
    Wait Until Keyword Succeeds    120s    3s    Unseal OpenBao    ${MEMBER_HOST}    ${unseal_key}
    Wait Until Keyword Succeeds    120s    3s    Instance Should Be Unsealed    ${MEMBER_HOST}
    Wait Until Keyword Succeeds    60s    3s    Raft Should Have Servers    2
    ${servers} =    Raft Servers
    ${ids} =    Evaluate    [s['node_id'] for s in $servers]
    Should Contain    ${ids}    ${member}

Check if the member serves the cluster data
    Wait Until Keyword Succeeds    60s    3s    Secret Should Be Readable    ${MEMBER_HOST}

Check if get-openbao-status reports the high availability state
    ${output}  ${rc} =    Execute Command    api-cli run module/${member}/get-openbao-status
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{status} =    Evaluate    json.loads($output)    modules=json
    Should Be Equal    ${status.ha['role']}    member
    Should Be Equal    ${status.ha['node_id']}    ${member}
    Should Be Equal    ${status.ha['is_self']}    ${False}
    ${output}  ${rc} =    Execute Command    api-cli run module/${primary}/get-openbao-status
    ...    return_rc=True
    &{status} =    Evaluate    json.loads($output)    modules=json
    Should Be Equal    ${status.ha['role']}    primary
    Should Be Equal    ${status.ha['is_self']}    ${True}
    Length Should Be    ${status.ha['peers']}    2

Check if an instance with members cannot become standalone
    Configure Should Fail    ${primary}    {"host": "${PRIMARY_HOST}", "http2https": false, "ha_role": "standalone"}

Check if a joined member cannot leave the cluster by configuration
    Configure Should Fail    ${member}    {"host": "${MEMBER_HOST}", "http2https": false, "ha_role": "standalone"}

Check if the member is removed from the cluster
    Bao Request    ${PRIMARY_HOST}    POST    sys/storage/raft/remove-peer    {"server_id": "${member}"}    ${root_token}
    Wait Until Keyword Succeeds    30s    2s    Raft Should Have Servers    1
    ${rc} =    Execute Command    remove-module --no-preserve ${member}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    Wait Until Keyword Succeeds    30s    2s    OpenBao Should Be Active    ${PRIMARY_HOST}
    Secret Should Be Readable    ${PRIMARY_HOST}

Check if the instance returns standalone
    Configure Should Succeed    ${primary}    {"host": "${PRIMARY_HOST}", "http2https": false, "ha_role": "standalone"}
    Wait Until Keyword Succeeds    30s    2s    Unseal OpenBao    ${PRIMARY_HOST}    ${unseal_key}
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${PRIMARY_HOST}
    Secret Should Be Readable    ${PRIMARY_HOST}
    ${servers} =    Raft Servers
    Length Should Be    ${servers}    1
    Should Be Equal    ${servers[0]['address']}    127.0.0.1:8201
    ${output} =    Execute Command    redis-cli EXISTS module/${primary}/srv/tcp/openbao-cluster
    Should Be Equal As Integers    ${output}    0

Check if the instance is removed correctly
    ${rc} =    Execute Command    remove-module --no-preserve ${primary}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
