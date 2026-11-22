#!/usr/bin/env python3

#
# Copyright (C) 2026 Genius Dynamics
# SPDX-License-Identifier: GPL-3.0-or-later
#

#
# Test client of the client provisioning feature, run as a module:
#
#   runagent -m CLIENT python3 /tmp/openbao-client-probe.py OPENBAO action ACTION '{"json": "input"}'
#   runagent -m CLIENT python3 /tmp/openbao-client-probe.py OPENBAO provision '{}'
#   runagent -m CLIENT python3 /tmp/openbao-client-probe.py OPENBAO kv-write modules/CLIENT/x [group]
#   runagent -m CLIENT python3 /tmp/openbao-client-probe.py OPENBAO kv-read  modules/CLIENT/x [group]
#   runagent -m CLIENT python3 /tmp/openbao-client-probe.py OPENBAO lookup-self
#
# "action" calls any action of OPENBAO as this module (AGENT_TASK_USER
# module/CLIENT) and prints {exit_code, output}. "provision" follows the
# client contract: verify the wrapping token, unwrap it, save the tokens
# in 0600 files of the client state directory, and print a summary
# without secrets. The other commands use the saved token and print the
# HTTP status.
#

import json
import os
import sys
import urllib.error
import urllib.request

import agent
import agent.tasks

openbao_id, command = sys.argv[1], sys.argv[2]
STATE = "openbao-client.json"


def call(address, path, method="GET", token="", data=None):
    """Return (HTTP status, decoded JSON body)."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["X-Vault-Token"] = token
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(f"{address}/v1/{path}", data=body, headers=headers, method=method)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=15) as resp:
            payload = resp.read()
            return resp.status, (json.loads(payload) if payload else {})
    except urllib.error.HTTPError as ex:
        return ex.code, {}


def save_secret(name, value):
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as sfile:
        sfile.write(value)


def unwrap(address, wrapped, creation_path):
    status, info = call(address, "sys/wrapping/lookup", "POST", data={"token": wrapped})
    assert status == 200 and info["data"]["creation_path"] == creation_path, "unexpected wrapping token"
    status, response = call(address, "sys/wrapping/unwrap", "POST", token=wrapped)
    assert status == 200, f"unwrap failed: {status}"
    again, _ = call(address, "sys/wrapping/unwrap", "POST", token=wrapped)
    return response["auth"], again


if command == "action":
    data = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    result = agent.tasks.run(f"module/{openbao_id}", sys.argv[3], data=data)
    print(json.dumps({"exit_code": result["exit_code"], "output": result["output"]}))
    sys.exit(0)

if command == "provision":
    result = agent.tasks.run(f"module/{openbao_id}", "provision-client", data=json.loads(sys.argv[3]))
    if result["exit_code"] != 0:
        print(json.dumps({"exit_code": result["exit_code"], "output": result["output"]}))
        sys.exit(0)
    out = result["output"]
    auth, again = unwrap(out["address"], out["wrapped_token"], out["wrap_creation_path"])
    save_secret("openbao-client.token", auth["client_token"])
    groups = {}
    for group in out["groups"]:
        gauth, _ = unwrap(out["address"], group["wrapped_token"], out["wrap_creation_path"])
        save_secret(f"openbao-client-{group['group_id']}.token", gauth["client_token"])
        groups[group["group_id"]] = group["kv_prefix"]
    with open(STATE, "w") as sfile:
        json.dump({"address": out["address"], "kv_mount": out["kv_mount"]}, sfile)
    print(json.dumps({
        "exit_code": 0,
        "address": out["address"],
        "kv_prefix": out["kv_prefix"],
        "policies": sorted(auth["policies"]),
        "renewable": auth.get("renewable", False),
        "second_unwrap_status": again,
        "groups": groups,
        "database_mount": out["database_mount"],
    }))
    sys.exit(0)

with open(STATE) as sfile:
    saved = json.load(sfile)
args = sys.argv[3:]
group = args[1] if len(args) > 1 else ""
with open(f"openbao-client-{group}.token" if group else "openbao-client.token") as tfile:
    token = tfile.read().strip()
if command == "kv-write":
    status, _ = call(saved["address"], f"{saved['kv_mount']}/data/{args[0]}", "POST", token, {"data": {"robot": "1"}})
elif command == "kv-read":
    status, _ = call(saved["address"], f"{saved['kv_mount']}/data/{args[0]}", "GET", token)
elif command == "write":
    status, _ = call(saved["address"], args[0], "POST", token, {"data": {"robot": "1"}})
elif command == "lookup-self":
    status, _ = call(saved["address"], "auth/token/lookup-self", "GET", token)
elif command == "renew-self":
    status, _ = call(saved["address"], "auth/token/renew-self", "POST", token, {})
else:
    sys.exit(f"unknown command {command}")
print(json.dumps({"status": status}))
