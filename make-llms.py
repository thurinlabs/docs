#!/usr/bin/env python3
"""Build llms.txt from the pages, in sidebar order. Run after editing any page: python3 make-llms.py"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = 'https://docs.thurin.id'

HEADER = f"""# Thurin.id docs, in one file

> Every page of {SITE}, in the sidebar's order, for AI agents and anyone who wants it all at once.
> The "For agents" section is written for this file; everything after it is built from the pages.

Thurin.id puts a PGP key on an Ethereum address: a claim in a contract nobody controls, checkable with gpg and
any Ethereum node. Proofs on the key link it to accounts elsewhere. An agent can drive everything with the CLI
(`npx @thurinlabs/thurin`, `--json`, exit codes) or with only `cast` and gpg (see PGPRegistry below).

---

## For agents: helping someone set up Thurin.id

### What you can do, and what only they can

You can run every command here. Only the person can:
- type their gpg passphrase (gpg asks through pinentry) and their keystore password (or give you a `--password-file`);
- confirm a transaction in their own wallet (browser extension, phone, hardware);
- post the proof on their accounts (a gist, a DNS record, a cast, a repo, a profile field), unless they've given you
  those tools (`gh`, a DNS API);
- decide what goes public. A claim is public and permanent: it can be revoked, never deleted. Tell them before you publish.

Never ask for or handle a private key or passphrase in chat. If you need one, stop and let them type it.

### The path, in order

Check each step before doing it; skip what's already done.

1. **gpg 2.2 or newer.** Check: `gpg --version`. Install: `brew install gnupg`, `sudo apt install gnupg`,
   `sudo dnf install gnupg2`, `sudo pacman -S gnupg`, or Gpg4win.
2. **A PGP key.** Check: `gpg -K --with-colons` (a `sec` line means they have one). If they have several, ask which.
   Make one: `gpg --quick-gen-key "Their Name" ed25519 sign 2y`, then
   `gpg --quick-add-key <fingerprint> cv25519 encr 2y`. Thurin never makes keys; gpg does.
3. **A name without an email on the key.** Only those names are published (unless they opt in with
   `--include-email`), and proofs must sit on one. Check: `gpg --list-keys <fingerprint>`. Add one:
   `gpg --quick-add-uid <fingerprint> "Their Name"`.
4. **An Ethereum address, and a way to pay.** The claim goes on the address that signs. Pick one:
   - their wallet has a little ETH: the browser at https://thurin.id/attest, or the CLI with a keystore
     (`thurin wallet import <name>` or `thurin wallet create <name>`);
   - their ETH is in a wallet elsewhere: `thurin attest --no-key --owner <address or ENS>` prints a link they
     open where the wallet is;
   - no ETH at all: `thurin attest --authorize` signs a free permission; anyone can publish it
     (`--relayer https://relay.thurin.id` posts it to Thurin's relayer, which pays for one claim per address
     within a daily budget).
5. **The claim.** `thurin attest --key <fingerprint>` exports the key, has gpg sign
   `I control the Ethereum address: 0x…`, checks everything the way thurin.id will, shows what will go
   on-chain, and asks once (`--yes` skips the question; show the person the summary first).
6. **Proofs.** For each account: put `thurin-id=openpgp4fpr:<fingerprint>` on the platform, add the
   `proof@thurin.id=<url>` notation to the key with gpg, then `thurin update-key` (one transaction, no new
   signature). Each provider's page below says exactly where the line goes and what URL to use.
7. **Confirm.** `thurin status <address or ENS> --json`.

### Checking your work

`thurin status <identity> --json` returns `identities[0]` with `current` (the newest active claim, or null),
`claims` (all of them), and `proofs`. Exit code 0 means a verified claim, 1 means no verified claim,
2 means bad usage, and 3 means a chain or network error.

- `current.verification.kind`: `verified`, or why the claim doesn't count: `expired`, `signing-key-expired`,
  `revoked`, `compromised`, `signing-key-revoked`, `unsupported` (e.g. DSA), or `bad-signature`.
- `proofs[]`: `{{provider, display, url, verified, reason}}`. A proof with `verified: false` has a `reason`;
  fix what it says and look again (proofs are checked live, nothing is cached).
- `claims[].state`: `active`, `revoked`, or `replaced`; `revokeReason` says why it ended.

The person can also look at https://thurin.id/eth/<address>.

### Mistakes to avoid

- Keyservers play no part. Thurin reads the key from the chain. Don't tell anyone to upload to or wait on
  keys.openpgp.org.
- Signing by hand: the statement has no line break after it. Use `printf '%s'`, never `echo`.
- The wrong key: with several keys, gpg signs with its default one. Pass `--key <fingerprint>`.
- Proofs added but not showing: the notation is on a name with an email (left out), or the key on the claim
  wasn't updated afterwards (`thurin update-key`).
- Claiming the same key again: an address has one active claim per key. To change keys, use
  `thurin reattest --key <new>`; to refresh names or proofs, use `update-key`.
- "compromised" is final for that address and key. Only use it when the key may really be in someone
  else's hands.

### Practice first, and cost

`--network sepolia` runs everything on Ethereum's test network: the same contract address, and test ETH
from any Sepolia faucet. It's a good first run for someone unsure.

On mainnet a claim is about 430,000 gas, and `update-key` about 300,000. At 1 gwei that's 0.00043 ETH and
0.0003 ETH; check the gas price with `cast gas-price` or a gas tracker.

### Later changes

- New proofs or names on the same key: `thurin update-key`.
- A new key: `thurin reattest --key <new>` (records move with it). If the old key was stolen, add `--compromised`.
- End a claim: `thurin revoke <index> --reason retired|other|compromised`.
- Records (a security contact, a canary, a release list): `thurin record set <name> <value>`; see Records below.
"""


def pages():
    """Page paths in sidebar order, the home page first."""
    out = ['README.md']
    for m in re.finditer(r'\]\((/[^)\s]*)\)', (ROOT / '_sidebar.md').read_text()):
        p = m.group(1).strip('/')
        if p:
            out.append(p + '.md')
    return out


def absolute(text):
    """Site links → full docs URLs (docsify routes through #/), so they work outside the site."""
    text = re.sub(r"\]\((/[^)\s]+) ':ignore'\)", lambda m: f']({SITE}{m.group(1)})', text)   # plain files
    def fix(m):
        path, anchor = m.group(1), m.group(2) or ''
        return f']({SITE}/#{path or "/"}{anchor})'
    return re.sub(r'\]\((/[^)\s?#]*)(\?id=[^)\s]*)?\)', fix, text)


def demote(text):
    """Page headings drop one level so each page sits under its own ## title; code blocks untouched."""
    out, fence = [], False
    for line in text.splitlines():
        if line.startswith('```'):
            fence = not fence
        if not fence and re.match(r'#{1,5} ', line):
            line = '#' + line
        out.append(line)
    return '\n'.join(out)


parts = [HEADER]
for p in pages():
    body = (ROOT / p).read_text().strip()
    url = f'{SITE}/#/' + ('' if p == 'README.md' else p[:-3])
    parts.append(f'---\n\n<!-- {url} -->\n\n' + demote(absolute(body)))
(ROOT / 'llms.txt').write_text('\n\n'.join(parts) + '\n')
print(f'llms.txt: {len(parts) - 1} pages')
