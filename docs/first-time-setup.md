# First-time setup

Part of the [ns8-openbao documentation](../README.md#documentation).

## First-time setup

A new instance starts **uninitialized**: OpenBao has no data, no keys and
no users yet. *Initializing* it creates the encryption keys and the first
credentials. Which credentials you get, and where they appear, depends on
two settings chosen in *Settings* **before** initializing: the unseal mode
and directory login.

### Words used below

- **Root token**: a token with unlimited power, like the root password of
  OpenBao. Use it for the first configuration only, then revoke it.
- **Unseal keys** (manual unseal only): the master key split into shares,
  for example 5 shares of which any 3 unlock OpenBao. They are needed
  after **every** restart, update or reboot.
- **Recovery keys** (automatic unseal only): shares that never unseal
  OpenBao, but authorize sensitive operations such as generating a new root
  token when no administrator can log in.

OpenBao shows the root token and keys **only once** and cannot recover
them. The module never sees or stores them: NethServer keeps action
inputs and outputs in Redis, readable by other modules, so they are
handled only by the OpenBao web UI or CLI, over HTTPS.

### Setup wizard

The easiest way: open the application. While OpenBao is not configured,
the *Status* page starts the **setup wizard**, which asks for the web
address, the unseal mode (explaining the trade-offs), directory login and
email notifications, shows a summary, applies everything at once, and
ends with the exact next steps for the setup you chose (one of A-D
below), with buttons to open OpenBao or its LDAP login. It can be run
again at any time with the *Setup wizard* button of the *Status* page.
Advanced users can cancel it and use the *Settings* page, which has every
option.

### Choose your setup

| Setup | Unseal mode | Directory login | First credentials |
|---|---|---|---|
| [A](#a-manual-unseal-without-directory-login) | manual | no | unseal keys + root token |
| [B](#b-automatic-unseal-without-directory-login) | automatic | no | recovery keys + root token |
| [C](#c-automatic-unseal-with-automatic-directory-login) | automatic | yes, `auto_initialize` | none: domain admins log in |
| [D](#d-adding-directory-login-later) | any | yes, after initialization | root token of A or B |

Start in every case from the setup wizard, or from the *Settings* page:
set the host name, choose the unseal mode and, for C, the user domain and
the administrators group. Then follow the steps below.

### A. Manual unseal, without directory login

1. On the *Status* page click **Open OpenBao**. The web UI shows the
   initialization page.
2. Choose the number of key shares and the threshold (for example 5 and
   3) and initialize.
3. **Download the keys** (JSON file) or copy the root token and every
   unseal key. Hand the key shares to different trusted people; do not
   keep them together with the root token.
4. Continue to unseal: enter key shares until the threshold is reached.
5. Sign in with the **Token** method, using the root token.
6. Create real administrator access, for example a `userpass` user with
   an admin policy, or set up [directory login](#d-adding-directory-login-later).
7. Revoke the root token: `bao token revoke -self`.

The same with the CLI, from any computer with the `bao` client:

```bash
export BAO_ADDR=https://vault.example.org
bao operator init -key-shares=5 -key-threshold=3   # prints 5 unseal keys and the root token
bao operator unseal                                # repeat 3 times, one key each time
bao login                                          # paste the root token
```

**After every restart** (update, reboot, settings change of host name)
OpenBao is sealed again. The *Status* page shows *Sealed* with the
progress, and notifications are sent if configured. Open the web UI and
enter the threshold number of unseal keys, or run `bao operator unseal`.

### B. Automatic unseal, without directory login

1. On the *Status* page click **Open OpenBao** and initialize. There is no
   unseal step: OpenBao unseals itself with the key stored on the node.
2. Save the **root token** and the **recovery keys**.
3. Sign in with the root token, create administrator access (as in step 6
   of A) and revoke the root token.

CLI: `bao operator init -recovery-shares=5 -recovery-threshold=3`, then
`bao login`.

### C. Automatic unseal with automatic directory login

In *Settings* choose **Automatic unseal**, a **user domain**, an
**administrators group** and check **Initialize OpenBao automatically
with directory login**. On save:

1. OpenBao initializes itself at once. It enables LDAP login on the user
   domain, grants the `ns8-admin` policy (full access) to the
   administrators group and creates a `secret/` key/value store.
2. No root token and no recovery keys exist. The *Status* page shows
   *Unsealed*.
3. Click **Log in with directory account** on the *Status* page: the web
   UI opens with the LDAP method selected. Log in with the user name and
   password of a member of the administrators group.
4. Generate recovery keys and store them safely: without them a new root
   token can never be generated if directory login breaks.

   ```bash
   export BAO_ADDR=https://vault.example.org
   bao login -method=ldap username=alice
   bao operator rotate-keys -init -key-shares=5 -key-threshold=3 -target=recovery
   ```

### D. Adding directory login later

For an instance initialized with A or B, or when the user domain or group
changes later:

1. In *Settings* choose the user domain and the administrators group, and
   save.
2. On the node, run the command shown in *Settings* and paste a token
   with administrator rights (the root token works):

   ```bash
   runagent -m openbao1 openbao-apply-config
   ```

3. Members of the administrators group can now use **Log in with
   directory account**. You can revoke the root token.

### Lost credentials

- **Root token lost**: generate a new one with the unseal keys (A) or the
  recovery keys (B, or C after step 4):

  ```bash
  bao operator generate-root -init            # prints a nonce and an OTP
  bao operator generate-root                  # repeat with each key share
  bao operator generate-root -decode=<encoded token> -otp=<OTP>
  ```

- **Unseal keys lost** (manual unseal): if fewer than the threshold remain,
  the data cannot be decrypted by anybody. Keep copies in separate safe
  places.
- **Directory login broken after automatic initialization** (C): the
  self-initialization also creates a **break-glass administrator token**
  (`ns8-admin` policy), so a failed or wrong directory setup can never lock
  everybody out. It never leaves the node and expires 32 days after the
  initialization. Use it to repair the configuration or to generate
  recovery keys, then revoke it:

  ```bash
  runagent -m openbao1 openbao-breakglass-token   # prints the token
  export BAO_ADDR=https://vault.example.org BAO_TOKEN=<token>
  bao operator rotate-keys -init -key-shares=5 -key-threshold=3 -target=recovery
  bao token revoke -self
  ```

  Only the administrator policy and this token are mandatory steps of the
  self-initialization; directory login and the key/value store are allowed
  to fail, and the failure is logged.
