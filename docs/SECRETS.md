# SECRETS.md: how to store and load your API keys

**Short version:** your API keys do **not** go in `.env` (or any file in these
repos). Store them in your operating system's keychain and inject them into a
single command with the `secrun` wrapper below. `.env` holds only non-secret
config (`PROVIDER`, `MODEL`, base URLs).

This is itself an AI-engineering lesson; see [Why not `.env`?](#why-not-env)
below. If you just want it working, jump to your platform:
[macOS](#macos) · [Linux](#linux) · [Windows](#windows) ·
[any OS with 1Password/Doppler](#any-os-1password-doppler-vault).

---

## How the lessons read a key

Every repo loads config with `load_dotenv()` and then reads keys from the
**process environment**:

```python
from dotenv import load_dotenv
load_dotenv()                       # loads .env, but NOT your keys anymore
key = os.getenv("OPENAI_API_KEY")   # comes from the environment
```

`load_dotenv()` uses `override=False`, so **anything already in the environment
wins** over `.env`. That's the whole trick: `secrun` puts the key in the
environment for one command, the lesson reads it from there, and nothing is ever
written to disk. Because the lessons only read from the environment, *any* method
that exports the variable works; Keychain + `secrun` is just the one we
recommend.

---

## Why not `.env`?

A `.env` file is plaintext on disk, sitting in the project directory. Three
concrete problems:

1. **It gets committed by accident.** The single most common way keys leak. A
   `.gitignore` helps until someone runs `git add -f` or copies the file.
2. **Every tool in the repo can read it.** Most sharply: an AI coding agent with
   file access reads `.env` trivially; it's right there in the working tree.
   Moving keys out of the tree removes that easy target.
3. **It's plaintext.** No encryption at rest. Anything that can read your files
   (backup, sync client, malware, a shared screen) can read the key.

A keychain fixes 1–3: the key is encrypted at rest, unlocked by your login, and
lives outside the repo entirely.

> **Honest limit.** `secrun` narrows *when* a key is live (only during the one
> command you wrap); it does **not** hide keys from code you choose to run. Any
> process you launch in your session can itself call `security find-generic-password`
> or read its own environment. A coding agent with shell access is such a process.
> This defeats *accidental* and *passive* exposure (commits, file scans, `env`
> dumps, screen-shares), which is the realistic threat for a laptop dev setup. It
> is not a substitute for a hardware boundary (a secrets broker with per-request
> approval, hardware tokens, a separate machine) when you need one.

---

## macOS

The whole setup is about 2 minutes. Uses the built-in login Keychain.

### 1. Store each key in the login Keychain

Run the line for each provider you use. `-U` updates the item if it already
exists; omitting `-w` makes `security` prompt for the value so the key never
lands in your shell history:

```bash
security add-generic-password -U -a "$USER" -s deepdives:OPENAI_API_KEY    -w
security add-generic-password -U -a "$USER" -s deepdives:ANTHROPIC_API_KEY -w
security add-generic-password -U -a "$USER" -s deepdives:VOYAGE_API_KEY    -w

# Optional: only if a project uses LangSmith tracing. (LangSmith is
# region-sharded; the matching LANGSMITH_ENDPOINT is not a secret and goes in
# that project's .env, not here.)
security add-generic-password -U -a "$USER" -s deepdives:LANGSMITH_API_KEY -w
```

Verify (prints the length, not the key):

```bash
security find-generic-password -a "$USER" -s deepdives:OPENAI_API_KEY -w | tr -d '\n' | wc -c
```

### 2. Add `secrun` to your shell profile

Paste this into `~/.zshrc` (or `~/.bashrc`; the body is POSIX-ish; adjust the
first line), then open a new terminal:

```zsh
# Fetch DeepDives API keys from the macOS Keychain and inject them into ONE
# command's environment. They never touch your interactive shell or any file.
#   secrun python examples/01_foo.py
secrun() {
  emulate -L zsh
  if (( $# == 0 )); then
    print -u2 "usage: secrun <command> [args...]   (runs cmd with DeepDives API keys)"
    return 2
  fi
  local -a keys=(ANTHROPIC_API_KEY OPENAI_API_KEY VOYAGE_API_KEY)
  # Optional keys: injected when the Keychain item exists, skipped silently
  # when it doesn't (only some projects need them).
  local -a opt_keys=(LANGSMITH_API_KEY)
  (  # subshell: exported keys never leak back into the interactive shell
    local k v
    for k in $keys; do
      if ! v=$(security find-generic-password -a "$USER" -s "deepdives:$k" -w 2>/dev/null); then
        print -u2 "secrun: missing Keychain item 'deepdives:$k'; see SECRETS.md"
        exit 1
      fi
      export $k="$v"
    done
    for k in $opt_keys; do
      if v=$(security find-generic-password -a "$USER" -s "deepdives:$k" -w 2>/dev/null); then
        export $k="$v"
      fi
    done
    exec "$@"
  )
}
```

> Only stored a subset of the keys? `secrun` errors on the first missing one.
> Either store all three (a not-yet-used key costs nothing to hold) or trim the
> `keys=(...)` list to what you actually have.

### 3. Run lessons with `secrun`

```bash
secrun python check_setup.py          # confirms the key is reachable
secrun python examples/01_foo.py      # any script that hits a real API
python examples/02_offline.py         # offline examples need no wrapper
```

That's it. Your shell stays key-free (`echo $OPENAI_API_KEY` prints nothing); the
key exists only inside the wrapped process, for its lifetime.

---

## Linux

Uses `secret-tool` (libsecret: the GNOME Keyring or KDE Wallet). The keyring is
unlocked automatically when you log into a desktop session.

### 1. Install secret-tool

```bash
sudo apt install libsecret-tools     # Debian / Ubuntu
sudo dnf install libsecret           # Fedora
sudo pacman -S libsecret             # Arch
```

### 2. Store each key

`secret-tool store` reads the value from a hidden prompt (never your shell
history). The `service` and `key` attributes are how you look it up again:

```bash
secret-tool store --label='DeepDives OPENAI_API_KEY'    service deepdives key OPENAI_API_KEY
secret-tool store --label='DeepDives ANTHROPIC_API_KEY' service deepdives key ANTHROPIC_API_KEY
secret-tool store --label='DeepDives VOYAGE_API_KEY'    service deepdives key VOYAGE_API_KEY
```

Verify (prints the length, not the key):

```bash
secret-tool lookup service deepdives key OPENAI_API_KEY | tr -d '\n' | wc -c
```

### 3. Add `secrun` to your shell profile

Paste into `~/.bashrc` (or `~/.zshrc`), then open a new terminal:

```bash
# Fetch DeepDives API keys from the keyring and inject them into ONE command's
# environment. They never touch your interactive shell or any file.
#   secrun python examples/01_foo.py
secrun() {
  if [ "$#" -eq 0 ]; then
    echo "usage: secrun <command> [args...]   (runs cmd with DeepDives API keys)" >&2
    return 2
  fi
  (  # subshell: exported keys never leak back into the interactive shell
    for k in ANTHROPIC_API_KEY OPENAI_API_KEY VOYAGE_API_KEY; do
      if ! v=$(secret-tool lookup service deepdives key "$k" 2>/dev/null); then
        echo "secrun: missing keyring item '$k'; see SECRETS.md" >&2
        exit 1
      fi
      export "$k=$v"
    done
    # Optional keys: injected when stored, skipped silently when not.
    for k in LANGSMITH_API_KEY; do
      if v=$(secret-tool lookup service deepdives key "$k" 2>/dev/null); then
        export "$k=$v"
      fi
    done
    exec "$@"
  )
}
```

### 4. Run lessons with `secrun`

```bash
secrun python check_setup.py          # confirms the key is reachable
secrun python examples/01_foo.py      # any script that hits a real API
python examples/02_offline.py         # offline examples need no wrapper
```

> **Headless server, or `secret-tool` errors with "Cannot autolaunch D-Bus"?**
> There's no desktop keyring to talk to. Use [`pass`](https://www.passwordstore.org/)
> instead (GPG-backed, works over SSH): `pass init <your-gpg-id>`, then
> `pass insert deepdives/OPENAI_API_KEY` for each key. In `secrun`, swap the lookup
> line for `v=$(pass show "deepdives/$k")`.

---

## Windows

Uses PowerShell's SecretManagement with the built-in encrypted **SecretStore**
vault (protected by your Windows account, encrypted at rest). Run these in
**PowerShell 7+** (`pwsh`).

> **Prefer the Linux tooling?** If you have **WSL**, open your WSL shell and follow
> the [Linux](#linux) section there instead; it's the smoother path, and it's
> where you'll run the lessons anyway.

### 1. Install the modules and register a vault

```powershell
Install-Module Microsoft.PowerShell.SecretManagement, Microsoft.PowerShell.SecretStore -Scope CurrentUser
Register-SecretVault -Name deepdives -ModuleName Microsoft.PowerShell.SecretStore -DefaultVault
```

Optional: skip the per-session vault-password prompt (convenience vs. security;
the store stays encrypted at rest under your Windows account):

```powershell
Set-SecretStoreConfiguration -Authentication None -Interaction None
```

### 2. Store each key

`Read-Host -AsSecureString` hides the value as you paste it:

```powershell
Set-Secret -Name OPENAI_API_KEY    -Vault deepdives -Secret (Read-Host -AsSecureString)
Set-Secret -Name ANTHROPIC_API_KEY -Vault deepdives -Secret (Read-Host -AsSecureString)
Set-Secret -Name VOYAGE_API_KEY    -Vault deepdives -Secret (Read-Host -AsSecureString)
```

### 3. Add `secrun` to your PowerShell profile

Open the profile with `notepad $PROFILE` (let it create the file if prompted),
paste this, then open a new PowerShell window:

```powershell
# Fetch DeepDives API keys from the SecretStore, inject them into ONE command's
# environment, then clear them again. They never touch a file or persist in the shell.
#   secrun python examples\01_foo.py
function secrun {
  if ($args.Count -eq 0) { Write-Error 'usage: secrun <command> [args...]'; return }
  $keys = 'ANTHROPIC_API_KEY','OPENAI_API_KEY','VOYAGE_API_KEY'
  $optKeys = 'LANGSMITH_API_KEY'   # injected if stored, skipped silently if not
  $prev = @{}
  try {
    foreach ($k in $keys) {
      $v = Get-Secret -Name $k -Vault deepdives -AsPlainText -ErrorAction Stop
      $prev[$k] = [Environment]::GetEnvironmentVariable($k, 'Process')
      [Environment]::SetEnvironmentVariable($k, $v, 'Process')
    }
    foreach ($k in $optKeys) {
      $v = Get-Secret -Name $k -Vault deepdives -AsPlainText -ErrorAction SilentlyContinue
      if ($v) {
        $prev[$k] = [Environment]::GetEnvironmentVariable($k, 'Process')
        [Environment]::SetEnvironmentVariable($k, $v, 'Process')
      }
    }
    & $args[0] @($args[1..($args.Count - 1)])
  }
  finally {
    foreach ($k in @($prev.Keys)) { [Environment]::SetEnvironmentVariable($k, $prev[$k], 'Process') }
  }
}
```

> Stored only some of the keys? `Get-Secret -ErrorAction Stop` aborts on the first
> missing one. Store all three, or trim the `$keys` list to what you have.

### 4. Run lessons with `secrun`

```powershell
secrun python check_setup.py
secrun python examples\01_foo.py
python examples\02_offline.py          # offline examples need no wrapper
```

---

## Any OS: 1Password, Doppler, Vault

Team-grade secrets managers inject secrets on demand and work identically on every
OS, often the most robust option here, with central rotation and audit on top. No
`secrun` needed: the tool *is* the wrapper.

**1Password** ([`op` CLI](https://developer.1password.com/docs/cli/)). Store the
three keys in a "DeepDives" item, then keep a small **reference** file in the repo
It holds `op://` paths, *not* secrets, so it's safe to commit:

```bash
# op.env  (references, not values)
OPENAI_API_KEY=op://Private/DeepDives/OPENAI_API_KEY
ANTHROPIC_API_KEY=op://Private/DeepDives/ANTHROPIC_API_KEY
VOYAGE_API_KEY=op://Private/DeepDives/VOYAGE_API_KEY
```

```bash
op run --env-file op.env -- python examples/01_foo.py   # resolves refs for the child only
```

**Doppler** ([CLI](https://docs.doppler.com/docs/cli)):

```bash
doppler setup                              # pick a project/config once
doppler secrets set OPENAI_API_KEY         # prompts for the value (repeat per key)
doppler run -- python examples/01_foo.py   # injects all secrets as env vars
```

**Production**: HashiCorp Vault and the cloud managers (AWS Secrets Manager, GCP
Secret Manager, Azure Key Vault) follow the same inject-on-demand pattern behind a
short-lived token or workload identity. Same goal as `secrun`: the key is never in
`.env`, your shell, or the repo.

---

## Fallback: a local `.env` (simplest, least safe)

If you can't set up a keychain right now, you *can* create a local `.env` and add
the key line yourself; the loaders will read it (`override=False` means it only
fills in what the environment doesn't already provide):

```bash
echo 'OPENAI_API_KEY=sk-...' >> .env    # NOT recommended; re-reads the risks above
```

`.env` is already in `.gitignore`, but you've now put a plaintext key back in the
repo tree. Treat this as a temporary crutch, not the destination.

---

## Rotating a key

Rotating keys is routine ops, not a fire drill: do it on a schedule, when a key
may have been exposed (it sat in a plaintext file, a screen-share, a log), or when
someone leaves a team. A rotated key makes any past exposure worthless.

1. In the provider console
   ([OpenAI](https://platform.openai.com/api-keys) ·
   [Anthropic](https://console.anthropic.com/settings/keys) ·
   [Voyage](https://www.voyageai.com/)) **create a new key and revoke the old one.**
   Copy the new key now; most consoles reveal it in full only once.
2. Replace it in your store (below). Nothing else changes; `secrun` reads the new
   value on its next run; no `.env` or profile edits.

### macOS: delete, then re-add (do **not** use `-U`)

`security add-generic-password -U` is meant to update in place, but in practice it
often **creates a duplicate** instead, and then `find-generic-password` may hand
`secrun` the *stale* copy, so you keep authenticating with the old key. Always
delete every copy first, then add exactly one. This block does that and verifies
in one go (copy the new key to your clipboard first):

```bash
K=OPENAI_API_KEY        # or ANTHROPIC_API_KEY / VOYAGE_API_KEY

# 1. remove EVERY existing copy (matches by service, so it catches duplicates)
while security delete-generic-password -s deepdives:$K >/dev/null 2>&1; do :; done

# 2. add exactly one, straight from the clipboard, with any stray newline stripped
security add-generic-password -a "$USER" -s deepdives:$K -w "$(pbpaste | tr -d '\r\n')"

# 3. verify: exactly one entry, a sane length, and the provider accepts it
security dump-keychain 2>/dev/null | grep -cE "\"svce\"<blob>=\"deepdives:$K\""   # want: 1
v=$(security find-generic-password -a "$USER" -s deepdives:$K -w); echo "length: ${#v}"
```

For OpenAI/Anthropic you can confirm the key actually works without spending
anything (listing models is free; prints only the HTTP status, never the key):

```bash
# OpenAI:
curl -s -o /dev/null -w 'HTTP %{http_code}\n' https://api.openai.com/v1/models \
  -H "Authorization: Bearer $(security find-generic-password -a "$USER" -s deepdives:OPENAI_API_KEY -w)"
# Anthropic:
curl -s -o /dev/null -w 'HTTP %{http_code}\n' https://api.anthropic.com/v1/models \
  -H "x-api-key: $(security find-generic-password -a "$USER" -s deepdives:ANTHROPIC_API_KEY -w)" \
  -H "anthropic-version: 2023-06-01"
```

`HTTP 200` = good; `401` = wrong or partial key. Then `secrun python check_setup.py`.

**Gotchas this sequence defends against** (all real, all easy to hit):

- **Duplicate entries.** `-U` can leave two items for the same service; `find`
  returns an arbitrary one. The `while … delete` loop removes *all* copies first.
- **Truncated paste.** Pasting a key with an embedded newline into the interactive
  `-w` prompt stores only the part *before* the newline (e.g. 128 of 164 chars, and
  it looks clean, just short). `pbpaste | tr -d '\r\n'` pastes the whole thing.
- **Miscounting.** When you add without `-l`, the item's label defaults to the
  service name, so `grep -c deepdives:$K` counts it **twice** (label + service).
  Count `"svce"` lines only, as above.
- **Sanity-check the length.** Roughly: OpenAI `sk-proj-…` ≈ 164, Anthropic
  `sk-ant-…` = 108, Voyage `pa-…` ≈ 46. A surprising length means a bad copy.
  (Providers change formats over time; treat these as a smell test, not a spec.)

### Linux / Windows

Simpler: the store updates in place, so just re-run the store step with the new
value; no delete dance needed:

- **Linux:** `secret-tool store --label='DeepDives OPENAI_API_KEY' service deepdives key OPENAI_API_KEY`
  (same attributes → overwrites the existing secret).
- **Windows:** `Set-Secret -Name OPENAI_API_KEY -Vault deepdives -Secret (Read-Host -AsSecureString)`.
- **1Password / Doppler:** edit the item / `doppler secrets set OPENAI_API_KEY`. `secrun`
  or `op run`/`doppler run` picks up the new value on the next run.
