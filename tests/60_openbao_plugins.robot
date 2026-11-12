*** Settings ***
Documentation    Optional plugins of the catalog: nothing is downloaded until a
...              plugin is enabled; an enabled plugin is installed, declared
...              and registered; a disabled plugin is removed.
Library    SSHLibrary
Library    Collections
Resource    openbao.resource

*** Variables ***
${module_id}    ${EMPTY}
${HOST}    openbao-plugins.example.org

*** Keywords ***
Plugin State
    [Arguments]    ${plugin_id}
    ${output}  ${rc} =    Execute Command    api-cli run module/${module_id}/list-plugins
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{result} =    Evaluate    json.loads($output)    modules=json
    # Robot variables are not visible inside a comprehension, except in its
    # first iterable: index by id, then look the id up outside it
    &{by_id} =    Evaluate    {p['id']: p for p in $result['plugins']}
    Dictionary Should Contain Key    ${by_id}    ${plugin_id}
    RETURN    ${by_id}[${plugin_id}]

Plugin Image Should Be Absent
    ${output} =    Execute Command    runagent -m ${module_id} podman images --format '{{.Repository}}'
    Should Not Contain    ${output}    openbao-plugin-auth-github

*** Test Cases ***
Check if openbao is installed and initialized
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${module_id}    ${output.module_id}
    Configure OpenBao    ${module_id}    ${HOST}    manual
    &{init} =    Bao Request    ${HOST}    PUT    sys/init    {"secret_shares": 1, "secret_threshold": 1}
    Set Suite Variable    ${root_token}    ${init.root_token}
    Set Suite Variable    ${unseal_key}    ${init['keys'][0]}
    Unseal OpenBao    ${HOST}    ${unseal_key}
    Wait Until Keyword Succeeds    30s    2s    OpenBao Should Be Active    ${HOST}

Check if the catalog lists plugins without downloading them
    &{ldap} =    Plugin State    auth-ldap
    Should Be Equal    ${ldap.bundled}    ${True}
    Should Be Equal    ${ldap.installed}    ${True}
    &{github} =    Plugin State    auth-github
    Should Be Equal    ${github.enabled}    ${False}
    Should Be Equal    ${github.installed}    ${False}
    Should Be Equal    ${github.enable_command}    bao auth enable github
    Plugin Image Should Be Absent

Check if an unknown plugin is rejected
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-plugins --data '{"plugins": ["auth-nonexistent"]}'
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Check if an enabled plugin is downloaded, installed and registered
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-plugins --data '{"plugins": ["auth-github"]}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    &{github} =    Plugin State    auth-github
    Should Be Equal    ${github.installed}    ${True}
    Should Be Equal    ${github.installed_version}    ${github.version}
    Wait Until Keyword Succeeds    30s    2s    Unseal OpenBao    ${HOST}    ${unseal_key}
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${HOST}
    # The module declares plugins with their version: read that entry
    &{catalog} =    Bao Request    ${HOST}    GET    sys/plugins/catalog/auth/github?version=${github.version}    ${EMPTY}    ${root_token}
    Should Be Equal    ${catalog.data['name']}    github
    Should Be Equal    ${catalog.data['version']}    ${github.version}

Check if the plugin can be enabled in OpenBao
    Bao Request    ${HOST}    POST    sys/auth/github    {"type": "github"}    ${root_token}
    &{auth} =    Bao Request    ${HOST}    GET    sys/auth    ${EMPTY}    ${root_token}
    Dictionary Should Contain Key    ${auth.data}    github/
    Bao Request    ${HOST}    DELETE    sys/auth/github    ${EMPTY}    ${root_token}

Check if get-openbao-status lists the installed plugins
    ${output}  ${rc} =    Execute Command    api-cli run module/${module_id}/get-openbao-status
    ...    return_rc=True
    &{status} =    Evaluate    json.loads($output)    modules=json
    Should Contain    ${status.plugins}    auth-github

Check if a disabled plugin is removed with its image
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-plugins --data '{"plugins": []}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
    &{github} =    Plugin State    auth-github
    Should Be Equal    ${github.installed}    ${False}
    ${rc} =    Execute Command    runagent -m ${module_id} test -e openbao-plugins/openbao-plugin-auth-github
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0
    Plugin Image Should Be Absent
    Wait Until Keyword Succeeds    30s    2s    Unseal OpenBao    ${HOST}    ${unseal_key}
    Wait Until Keyword Succeeds    60s    2s    OpenBao Should Be Active    ${HOST}
    &{ldap} =    Plugin State    auth-ldap
    Should Be Equal    ${ldap.installed}    ${True}

Check if openbao is removed correctly
    ${rc} =    Execute Command    remove-module --no-preserve ${module_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
