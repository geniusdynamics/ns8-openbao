# Copyright (C) 2026 Genius Dynamics
# SPDX-License-Identifier: GPL-3.0-or-later

"""Unit tests of client provisioning, against a fake OpenBao HTTP API.

    python3 -m unittest discover -s tests/unit

The fake API implements the endpoints the module calls, response
wrapping, entity aliases and a simplified ACL check of the policies the
module writes (templated on the entity alias name).
"""

import contextlib
import fnmatch
import io
import json
import os
import re
from pathlib import Path
import secrets
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "imageroot/pypkg"))
AGENT = MagicMock()
sys.modules["agent"] = AGENT
import openbao  # noqa: E402
import openbao_clients as clients  # noqa: E402

TOKEN_ACCESSOR = "auth_token_0123abcd"
ROOT = "root-token"


class FakeOpenBao:
    """In-memory OpenBao with the behaviour the module relies on."""

    def __init__(self):
        self.sealed = False
        self.initialized = True
        self.policies = {}
        self.mounts = {"secret/": {"type": "kv", "options": {"version": "2"}}}
        self.roles = {}
        self.tokens = {ROOT: {"accessor": "root-accessor", "policies": ["root"], "alias": "", "meta": {}}}
        self.wraps = {}
        self.kv = {}
        self.requests = []
        self.fail_create = False

    # -- ACL ------------------------------------------------------------
    def rules(self, token):
        info = self.tokens.get(token)
        if not info:
            return None
        rules = []
        for name in info["policies"]:
            if name == "root":
                return [("*", {"create", "read", "update", "delete", "list", "sudo"})]
            text = self.policies.get(name, "")
            text = text.replace("{{identity.entity.aliases.%s.name}}" % TOKEN_ACCESSOR, info["alias"] or "\0")
            for path, caps in re.findall(r'^path "([^"]+)" \{\s*capabilities = (\[[^\]]*\])', text, re.M):
                rules.append((path, set(json.loads(caps))))
        # default policy
        rules += [("auth/token/lookup-self", {"read"}), ("auth/token/renew-self", {"update"}),
                  ("auth/token/revoke-self", {"update"}), ("sys/wrapping/unwrap", {"update"})]
        return rules

    def allowed(self, token, path, cap):
        rules = self.rules(token)
        if rules is None:
            return False
        for pattern, caps in rules:
            if "\0" in pattern:
                continue
            if pattern.endswith("*") and path.startswith(pattern[:-1]) or fnmatch.fnmatchcase(path, pattern):
                if cap in caps:
                    return True
        return False

    # -- requests -------------------------------------------------------
    def handle(self, method, path, headers, body):
        self.requests.append((method, path))
        token = headers.get("X-Vault-Token", "")
        if path == "sys/seal-status":
            return 200, {"initialized": self.initialized, "sealed": self.sealed}
        if self.sealed:
            return 503, {"errors": ["Vault is sealed"]}
        if path in ("sys/wrapping/lookup",):
            wrap = self.wraps.get(body.get("token"))
            return (200, {"data": {"creation_path": wrap["path"]}}) if wrap else (400, {"errors": ["invalid"]})
        if path == "sys/wrapping/unwrap":
            wrap = self.wraps.pop(token, None)
            return (200, wrap["response"]) if wrap else (400, {"errors": ["wrapping token is not valid"]})
        cap = {"GET": "read", "LIST": "list", "DELETE": "delete"}.get(method, "update")
        if method == "POST" and path.startswith("sys/mounts/") and path[11:] + "/" not in self.mounts:
            cap = "create"
        if not self.allowed(token, path, cap):
            return 403, {"errors": ["permission denied"]}
        if path == "sys/auth":
            return 200, {"data": {"token/": {"type": "token", "accessor": TOKEN_ACCESSOR}}}
        if path.startswith("sys/mounts/"):
            name = path[len("sys/mounts/"):] + "/"
            if method == "GET":
                return (200, {"data": self.mounts[name]}) if name in self.mounts else (400, {"errors": ["no mount"]})
            if method == "DELETE":
                self.mounts.pop(name, None)
                return 204, None
            if name in self.mounts:
                return 400, {"errors": ["path is already in use"]}
            self.mounts[name] = {"type": body["type"], "options": body.get("options") or {}}
            return 204, None
        if path.startswith("sys/policies/acl/"):
            self.policies[path.rsplit("/", 1)[1]] = body["policy"]
            return 204, None
        if path.startswith("auth/token/roles/"):
            self.roles[path.rsplit("/", 1)[1]] = body
            return 204, None
        if path == "auth/token/lookup-self":
            return 200, {"data": {"policies": self.tokens[token]["policies"]}}
        if path == "auth/token/renew-self":
            return 200, {"auth": {"client_token": token}}
        if path == "auth/token/revoke-self":
            del self.tokens[token]
            return 204, None
        if path == "auth/token/lookup-accessor":
            found = [t for t, i in self.tokens.items() if i["accessor"] == body["accessor"]]
            return (200, {"data": {"policies": self.tokens[found[0]]["policies"]}}) if found \
                else (400, {"errors": ["invalid accessor"]})
        if path == "auth/token/revoke-accessor":
            found = [t for t, i in self.tokens.items() if i["accessor"] == body["accessor"]]
            if not found:
                return 400, {"errors": ["invalid accessor"]}
            del self.tokens[found[0]]
            return 204, None
        if path in ("auth/token/create-orphan",) or path.startswith("auth/token/create/"):
            if self.fail_create:
                return 500, {"errors": ["internal error"]}
            alias = ""
            if path.startswith("auth/token/create/"):
                role = self.roles.get(path.rsplit("/", 1)[1])
                if not role or not set(body["policies"]) <= set(role["allowed_policies"]):
                    return 400, {"errors": ["invalid policies"]}
                alias = body.get("entity_alias", "")
            new = "s." + secrets.token_hex(8)
            accessor = secrets.token_hex(6)
            self.tokens[new] = {"accessor": accessor, "policies": body["policies"], "alias": alias,
                                "meta": body.get("meta", {})}
            response = {"auth": {"client_token": new, "accessor": accessor, "policies": body["policies"]}}
            if headers.get("X-Vault-Wrap-TTL"):
                wrap = "s.wrap" + secrets.token_hex(8)
                self.wraps[wrap] = {"response": response, "path": path}
                return 200, {"wrap_info": {"token": wrap, "ttl": 120, "creation_path": path,
                                           "wrapped_accessor": accessor}}
            return 200, response
        if path.startswith("ns8-kv/"):
            rest = path[len("ns8-kv/"):]
            kind, _, key = rest.partition("/")
            if kind == "data":
                if method == "GET":
                    return (200, {"data": {"data": self.kv[key]}}) if key in self.kv else (404, {"errors": []})
                self.kv[key] = body["data"]
                return 200, {"data": {"version": 1}}
            if kind == "metadata" and method == "LIST":
                prefix = key.rstrip("/") + "/"
                keys = sorted({k[len(prefix):].split("/", 1)[0] + ("/" if "/" in k[len(prefix):] else "")
                               for k in self.kv if k.startswith(prefix)})
                return (200, {"data": {"keys": keys}}) if keys else (404, {"errors": []})
            if kind == "metadata" and method == "DELETE":
                self.kv.pop(key, None)
                return 204, None
        return 404, {"errors": [f"unsupported {method} {path}"]}


class Handler(BaseHTTPRequestHandler):
    fake = None

    def log_message(self, *args):
        pass

    def _serve(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length)) if length else {}
        path = self.path.split("?", 1)[0][len("/v1/"):]
        code, payload = self.fake.handle(self.command, path, self.headers, body)
        data = json.dumps(payload).encode() if payload is not None else b""
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    do_GET = do_POST = do_PUT = do_DELETE = do_LIST = _serve


class FakeRedis:
    def __init__(self, registry):
        self.registry = registry

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def hmget(self, key, fields):
        return [self.registry.get(f) for f in fields]

    def hkeys(self, key):
        return list(self.registry)


class ClientProvisioningTest(unittest.TestCase):
    def setUp(self):
        self.fake = FakeOpenBao()
        Handler.fake = self.fake
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(temp.name)
        self.write_env(True)
        self.registry = {"openbao1": "uuid-self", "pg1": "uuid-pg1", "kumo1": "uuid-k1", "kumo2": "uuid-k2"}
        AGENT.redis_connect.side_effect = lambda *a, **k: FakeRedis(self.registry)
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(patch.dict(os.environ, {
            "TCP_PORT": str(self.server.server_address[1]), "MODULE_ID": "openbao1", "NODE_ID": "1"}))
        stack.enter_context(contextlib.redirect_stderr(io.StringIO()))

    def write_env(self, enabled):
        Path("environment").write_text(
            "TRAEFIK_HOST=vault.example.org\nOPENBAO_PUBLIC_ACCESS=True\n"
            f"OPENBAO_CLIENT_PROVISIONING={enabled}\n")

    # -- helpers ----------------------------------------------------------
    def setup_provisioner(self):
        clients.setup_provisioner(ROOT)

    def call(self, method, path, token, body=None):
        return self.fake.handle(method, path, {"X-Vault-Token": token}, body or {})

    def unwrap(self, output, expected_path=clients.WRAP_CREATION_PATH):
        code, info = self.fake.handle("POST", "sys/wrapping/lookup", {}, {"token": output["wrapped_token"]})
        self.assertEqual(code, 200)
        self.assertEqual(info["data"]["creation_path"], expected_path)
        code, response = self.fake.handle("POST", "sys/wrapping/unwrap",
                                          {"X-Vault-Token": output["wrapped_token"]}, {})
        self.assertEqual(code, 200)
        return response["auth"]["client_token"]

    def assert_client_error(self, error, func, *args, **kwargs):
        with self.assertRaises(clients.ClientError) as ctx:
            func(*args, **kwargs)
        self.assertEqual(ctx.exception.error, error)

    # -- tests ------------------------------------------------------------
    def test_setup_writes_narrow_provisioner(self):
        self.setup_provisioner()
        self.assertEqual(Path(clients.PROVISIONER_TOKEN_FILE).stat().st_mode & 0o777, 0o600)
        token = clients.read_provisioner_token()
        self.assertEqual(self.fake.tokens[token]["policies"], ["ns8-provisioner"])
        self.assertEqual(self.fake.mounts["ns8-kv/"]["options"]["version"], "2")
        role = self.fake.roles["ns8-client"]
        self.assertEqual(sorted(role["allowed_policies"]), ["ns8-client-db", "ns8-client-group", "ns8-client-kv"])
        self.assertTrue(role["orphan"])
        # The provisioner cannot escalate: no policy, role or auth writes
        for path in ("sys/policies/acl/ns8-client-kv", "sys/policies/acl/evil",
                     "auth/token/roles/ns8-client", "sys/auth/approle", "auth/token/create-orphan",
                     "sys/mounts/secret", "secret/data/robot"):
            self.assertEqual(self.call("POST", path, token, {"policy": "", "type": "kv"})[0], 403, path)
        self.assertIn(TOKEN_ACCESSOR, self.fake.policies["ns8-client-kv"])

    def test_setup_refused_when_disabled_or_sealed(self):
        self.write_env(False)
        self.assert_client_error("client_provisioning_disabled", clients.setup_provisioner, ROOT)
        self.write_env(True)
        self.fake.sealed = True
        self.assert_client_error("openbao_unavailable", clients.setup_provisioner, ROOT)
        self.assertFalse(Path(clients.PROVISIONER_TOKEN_FILE).exists())

    def test_identity_comes_from_the_platform(self):
        for user in ("", "admin", "node/1", "module/", "module/openbao1", "module/x/../y", "module/PG1"):
            with self.subTest(user=user), patch.dict(os.environ, {"AGENT_TASK_USER": user}):
                self.assert_client_error("client_not_authorized", clients.caller_module)
        with patch.dict(os.environ, {"AGENT_TASK_USER": "module/pg1"}):
            self.assertEqual(clients.caller_module(), "pg1")

    def test_unapproved_client_is_recorded_as_pending(self):
        self.setup_provisioner()
        self.assert_client_error("client_not_approved", clients.provision, "pg1", True)
        listing = clients.list_clients()
        entry = listing["clients"][0]
        self.assertEqual((entry["module_id"], entry["status"]), ("pg1", "pending"))
        self.assertTrue(entry["database_engine_requested"])
        self.assertEqual(listing["audit"][0]["event"], "access_requested")
        self.assertEqual(clients.client_status("pg1")["status"], "pending")

    def test_provision_unwrap_and_scope(self):
        self.setup_provisioner()
        clients.set_access("pg1", True)
        clients.set_access("kumo1", True)
        output = clients.provision("pg1")
        self.assertEqual(output["kv_prefix"], "modules/pg1")
        self.assertEqual(output["address"], "https://vault.example.org")
        self.assertEqual(output["database_mount"], "")
        token = self.unwrap(output)
        self.assertEqual(self.fake.tokens[token]["alias"], "pg1")
        self.assertEqual(self.fake.tokens[token]["meta"]["ns8_module_uuid"], "uuid-pg1")
        # Single use wrapping token
        code, _ = self.fake.handle("POST", "sys/wrapping/unwrap", {"X-Vault-Token": output["wrapped_token"]}, {})
        self.assertEqual(code, 400)
        # Own prefix: allowed. Others: denied
        self.assertEqual(self.call("POST", "ns8-kv/data/modules/pg1/replication", token, {"data": {"a": 1}})[0], 200)
        for path in ("ns8-kv/data/modules/kumo1/x", "ns8-kv/data/modules/pg10/x", "ns8-kv/data/groups/x/y",
                     "secret/data/robot", "sys/policies/acl/x", "ns8-db-pg1/config/x"):
            self.assertEqual(self.call("POST", path, token, {"data": {}})[0], 403, path)
        # The task output never holds the token itself
        self.assertNotIn(token, json.dumps(output))
        state = Path(clients.STATE_FILE).read_text()
        self.assertNotIn(token, state)
        self.assertNotIn(output["wrapped_token"], state)
        self.assertEqual(Path(clients.STATE_FILE).stat().st_mode & 0o777, 0o600)
        audit = Path(clients.AUDIT_FILE).read_text()
        self.assertIn("token_issued", audit)
        self.assertNotIn(token, audit)

    def test_reinstalled_module_needs_new_approval(self):
        self.setup_provisioner()
        clients.set_access("pg1", True)
        token = self.unwrap(clients.provision("pg1"))
        self.registry["pg1"] = "uuid-pg1-new"
        self.assert_client_error("client_not_approved", clients.provision, "pg1")
        self.assertEqual(clients.list_clients()["clients"][0]["status"], "stale")
        # Approving the new instance revokes the tokens of the old one
        clients.set_access("pg1", True)
        self.assertNotIn(token, self.fake.tokens)
        self.unwrap(clients.provision("pg1"))

    def test_database_engine_is_approved_separately(self):
        self.setup_provisioner()
        clients.set_access("pg1", True)
        output = clients.provision("pg1", database_engine=True)
        self.assertFalse(output["database_engine"])
        self.assertTrue(clients.client_status("pg1")["database_engine_requested"])
        self.assertNotIn("ns8-db-pg1/", self.fake.mounts)
        clients.set_access("pg1", True, database_engine=True)
        output = clients.provision("pg1", database_engine=True)
        self.assertEqual(output["database_mount"], "ns8-db-pg1")
        self.assertEqual(self.fake.mounts["ns8-db-pg1/"]["type"], "database")
        token = self.unwrap(output)
        self.assertEqual(self.call("POST", "ns8-db-pg1/config/main", token)[0], 404)  # allowed, fake has no engine
        self.assertEqual(self.call("POST", "ns8-db-kumo1/config/main", token)[0], 403)
        self.assertEqual(self.call("DELETE", "sys/mounts/ns8-db-pg1", token)[0], 403)
        # Narrowing revokes the tokens holding the database policy
        clients.set_access("pg1", True, database_engine=False)
        self.assertNotIn(token, self.fake.tokens)

    def test_groups_are_granted_by_the_administrator(self):
        self.setup_provisioner()
        self.assert_client_error("invalid_group_id", clients.set_access, "kumo1", True, groups=["kumo1"])
        clients.request_access("kumo1", groups=["kumomta-cluster"])
        self.assertEqual(clients.client_status("kumo1")["groups_requested"], ["kumomta-cluster"])
        clients.set_access("kumo1", True)
        out1 = clients.provision("kumo1")
        self.assertEqual(out1["groups"], [])  # requested, not granted
        clients.set_access("kumo1", True, groups=["kumomta-cluster"])
        clients.set_access("kumo2", True, groups=["kumomta-cluster"])
        out1 = clients.provision("kumo1")
        out2 = clients.provision("kumo2")
        g1 = self.unwrap(out1["groups"][0])
        g2 = self.unwrap(out2["groups"][0])
        self.assertEqual(out1["groups"][0]["kv_prefix"], "groups/kumomta-cluster")
        path = "ns8-kv/data/groups/kumomta-cluster/dkim/example.org"
        self.assertEqual(self.call("POST", path, g1, {"data": {"key": "k"}})[0], 200)
        self.assertEqual(self.call("GET", path, g2)[0], 200)
        self.assertEqual(self.call("GET", "ns8-kv/data/modules/kumo1/x", g1)[0], 403)
        self.assertEqual(self.call("GET", "ns8-kv/data/groups/other/x", g1)[0], 403)
        listing = clients.list_clients()
        self.assertEqual(listing["groups"][0]["members"], ["kumo1", "kumo2"])
        # Leaving the group revokes the group token only
        main1 = self.unwrap(out1)
        clients.set_access("kumo1", True, groups=[])
        self.assertNotIn(g1, self.fake.tokens)
        self.assertIn(main1, self.fake.tokens)
        self.assertIn(g2, self.fake.tokens)

    def test_revoke_and_delete_data(self):
        self.setup_provisioner()
        clients.set_access("pg1", True, database_engine=True)
        token = self.unwrap(clients.provision("pg1", database_engine=True))
        self.call("POST", "ns8-kv/data/modules/pg1/a/b", token, {"data": {"x": 1}})
        self.call("POST", "ns8-kv/data/modules/pg1/c", token, {"data": {"x": 1}})
        self.fake.kv["modules/pg10/keep"] = {"x": 1}
        result = clients.set_access("pg1", False, delete_data=True)
        self.assertEqual(result["cleanup"], "done")
        self.assertNotIn(token, self.fake.tokens)
        self.assertEqual(sorted(self.fake.kv), ["modules/pg10/keep"])
        self.assertNotIn("ns8-db-pg1/", self.fake.mounts)
        self.assert_client_error("client_not_approved", clients.provision, "pg1")

    def test_sealed_openbao_fails_clearly_and_revocation_is_retried(self):
        self.setup_provisioner()
        clients.set_access("pg1", True)
        token = self.unwrap(clients.provision("pg1"))
        self.fake.sealed = True
        before = dict(self.fake.tokens)
        self.assert_client_error("openbao_unavailable", clients.provision, "pg1")
        self.assertEqual(self.fake.tokens, before)
        result = clients.set_access("pg1", False)
        self.assertEqual(result["cleanup"], "pending")
        self.assertEqual(clients.list_clients()["clients"][0]["status"], "cleanup_pending")
        self.fake.sealed = False
        clients.maintenance()
        self.assertNotIn(token, self.fake.tokens)
        self.assertEqual(clients.list_clients()["clients"], [])

    def test_failed_issue_leaves_nothing_behind(self):
        self.setup_provisioner()
        clients.set_access("pg1", True, database_engine=True)
        self.fake.fail_create = True
        tokens = set(self.fake.tokens)
        self.assert_client_error("openbao_request_failed", clients.provision, "pg1", True)
        self.assertNotIn("ns8-db-pg1/", self.fake.mounts)
        self.assertEqual(set(self.fake.tokens), tokens)
        self.assertEqual(clients.list_clients()["clients"][0]["tokens"], 0)

    def test_module_removed_revokes_tokens_and_keeps_data(self):
        self.setup_provisioner()
        clients.set_access("pg1", True)
        token = self.unwrap(clients.provision("pg1"))
        self.call("POST", "ns8-kv/data/modules/pg1/x", token, {"data": {"x": 1}})
        del self.registry["pg1"]
        self.assertTrue(clients.module_removed("pg1"))
        self.assertNotIn(token, self.fake.tokens)
        self.assertIn("modules/pg1/x", self.fake.kv)
        self.assertEqual(clients.load_state()["grants"], {})
        self.assertFalse(clients.module_removed("pg1"))

    def test_disable_revokes_client_and_provisioner_tokens(self):
        self.setup_provisioner()
        provisioner = clients.read_provisioner_token()
        clients.set_access("pg1", True)
        token = self.unwrap(clients.provision("pg1"))
        self.write_env(False)
        self.assert_client_error("client_provisioning_disabled", clients.provision, "pg1")
        self.assertTrue(clients.disable())
        self.assertNotIn(token, self.fake.tokens)
        self.assertNotIn(provisioner, self.fake.tokens)
        self.assertFalse(Path(clients.PROVISIONER_TOKEN_FILE).exists())
        self.assertIn("pg1", clients.load_state()["grants"])  # approvals are kept

    def test_disable_while_sealed_is_retried_by_maintenance(self):
        self.setup_provisioner()
        provisioner = clients.read_provisioner_token()
        self.write_env(False)
        self.fake.sealed = True
        self.assertFalse(clients.disable())
        self.assertEqual(clients.list_clients()["provisioner"], "revoke_pending")
        self.fake.sealed = False
        clients.maintenance()
        self.assertNotIn(provisioner, self.fake.tokens)

    def test_token_limit_per_client(self):
        self.setup_provisioner()
        clients.set_access("pg1", True)
        tokens = [self.unwrap(clients.provision("pg1")) for _ in range(clients.MAX_TOKENS_PER_CLIENT + 2)]
        live = [t for t in tokens if t in self.fake.tokens]
        self.assertEqual(live, tokens[-clients.MAX_TOKENS_PER_CLIENT:])

    def test_listing_is_reader_safe(self):
        self.setup_provisioner()
        clients.set_access("pg1", True)
        output = clients.provision("pg1")
        listing = json.dumps(clients.list_clients())
        status = json.dumps(clients.client_status("pg1"))
        for secret in [output["wrapped_token"], clients.read_provisioner_token()] + \
                [i["accessor"] for i in self.fake.tokens.values()]:
            self.assertNotIn(secret, listing)
            self.assertNotIn(secret, status)

    def test_api_request_sends_extra_headers(self):
        self.setup_provisioner()
        response = openbao.api_request("auth/token/create/ns8-client", method="POST",
                                       token=clients.read_provisioner_token(),
                                       headers={"X-Vault-Wrap-TTL": "120s"},
                                       data={"policies": ["ns8-client-kv"], "entity_alias": "pg1"})
        self.assertIn("wrap_info", response)

    def run_action(self, action, step, data, user):
        """Run an action step as NS8 would: JSON on stdin, JSON on stdout."""
        import runpy
        script = Path(__file__).resolve().parents[2] / "imageroot/actions" / action / step
        stdout = io.StringIO()
        with patch.dict(os.environ, {"AGENT_TASK_USER": user}), \
                patch.object(sys, "stdin", io.StringIO(json.dumps(data))), \
                contextlib.redirect_stdout(stdout):
            try:
                runpy.run_path(str(script), run_name="__main__")
                code = 0
            except SystemExit as ex:
                code = ex.code
        return code, json.loads(stdout.getvalue())

    def validate(self, action, kind, document):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is not installed")
        path = Path(__file__).resolve().parents[2] / "imageroot/actions" / action / f"validate-{kind}.json"
        schema = json.loads(path.read_text())
        jsonschema.validate(document, schema)
        for example in schema.get("examples", []):
            jsonschema.validate(example, schema)

    def test_actions_and_schemas(self):
        self.setup_provisioner()
        code, out = self.run_action("provision-client", "20provision", {}, "admin")
        self.assertEqual((code, out[0]["error"]), (3, "client_not_authorized"))
        code, out = self.run_action("request-client-access", "20request", {"groups": ["kumomta-cluster"]},
                                    "module/kumo1")
        self.assertEqual((code, out["status"]), (0, "pending"))
        self.validate("request-client-access", "input", {"groups": ["kumomta-cluster"]})
        self.validate("request-client-access", "output", out)
        code, out = self.run_action("set-client-access", "20set",
                                    {"module_id": "kumo1", "allowed": True, "groups": ["kumomta-cluster"]}, "admin")
        self.assertEqual(code, 0)
        self.validate("set-client-access", "output", out)
        code, out = self.run_action("provision-client", "20provision", {"database_engine": True}, "module/kumo1")
        self.assertEqual(code, 0)
        self.validate("provision-client", "output", out)
        self.validate("provision-client", "input", {"database_engine": True})
        self.assertEqual(len(out["groups"]), 1)
        code, out = self.run_action("get-client-status", "20read", {}, "module/kumo1")
        self.assertEqual((code, out["status"], out["database_engine_requested"]), (0, "approved", True))
        self.validate("get-client-status", "output", out)
        code, out = self.run_action("list-clients", "20read", {}, "admin")
        self.validate("list-clients", "output", out)
        self.validate("set-client-access", "input", {"module_id": "kumo1", "allowed": False, "delete_data": True})
        with self.assertRaises(Exception):
            self.validate("set-client-access", "input", {"module_id": "kumo1", "allowed": True, "groups": ["kumo1"]})


if __name__ == "__main__":
    unittest.main()
