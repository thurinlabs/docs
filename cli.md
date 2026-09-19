# Thurin CLI

`thurin` does what thurin.id does, from a terminal: look up any identity, and attest, update, replace, or revoke your own claim. Every check the site runs happens before a single unit of gas is spent, and every command has `--json` output and meaningful exit codes, so scripts and agents can drive it.

Two rules it never breaks:

- **It is not a wallet.** It creates, imports, lists, and exports keystores. No balances, no transfers.
- **It never holds a PGP secret.** Every PGP operation is your own `gpg`; passphrases go through pinentry.

## Install

```bash
npm install -g @thurinlabs/thurin
# or, without installing:
npx @thurinlabs/thurin status bendoubleu.eth
```

Node 20 or newer. GnuPG 2.2 or newer for anything that touches a key.

## Look up an identity

```
$ thurin status thurinlabs.eth
thurinlabs.eth  0x539C7e1E454296Dc150B95a0acCC05bCa3b33538  (mainnet)
claims      1 total · 1 active · 0 revoked
fingerprint 08B9374FDFBEC67EFFA24E669D3D86E35361EF7B  ✓ verified
name        Thurin Labs
name        Thurin Labs <hello@thurin.id>
key         Ed25519 · created 2026-09-12 · expires 2028-09-11
proofs
  ✓ GitHub     thurinlabs
  ✓ DNS        thurin.id
  ✓ DNS        thurinlabs.id
  ✓ Codeberg   thurinlabs
efp         2 followers · 0 following
```

Takes an ENS name, an address, a PGP fingerprint, or a 16-character key ID. Exit code 1 means no verified claim. `--json` prints the same as data.

## Attest in three commands

```bash
thurin key create thurin         # Ed25519 key with a published name and no email; gpg asks for a passphrase
thurin wallet create identity    # a fresh address; 12 words shown once, keystore saved encrypted
thurin attest                    # sign, check everything, publish
```

The address needs a little ETH for the fee. Already have a key and a wallet?

```bash
thurin attest --key <fingerprint> --account <keystore name or path>
```

`--account` takes a name from `thurin wallet list` or a path to any V3 keystore file, including Foundry's `~/.foundry/keystores/*`. `THURIN_PRIVATE_KEY` in the environment also works, for scripts.

What `attest` does before it asks you to confirm: exports a minimal copy of the key, leaves out every name containing an email (`--include-email` keeps them), signs `I control the Ethereum address: 0x…` with your key through gpg, verifies that signature against the export exactly as thurin.id will, checks the size limits and that no active claim already exists for that key, estimates the gas, and shows you the names, proof count, and size that will go on-chain.

## Change a claim

```bash
thurin update-key      # after adding a proof notation: same fingerprint, new notations, no new signature
thurin reattest        # revoke the current claim and publish a new key in one transaction
thurin revoke          # mark the claim inactive; it stays in chain history
```

Each takes an optional claim index (`thurin status <address>` lists them); with one active claim it is picked for you. Adding a proof to a key is one gpg line, see [Managing Notations](/guides/gnupg).

## When your ETH is on a hardware wallet or a phone

The CLI can't drive a Ledger or a phone wallet, but it can still do the PGP half:

```bash
thurin attest --no-key --owner yourname.eth      # or --owner 0x…
```

It signs, exports, and runs every check, then prints a `https://thurin.id/attest#handoff=…` link instead of sending. Open that link where the wallet is, connect the address you named, check the summary, and publish. `reattest` and `update-key` take `--no-key` too.

The signed statement and the key ride in the URL fragment, the part after `#`. Browsers keep fragments on the device and never send them in a request, so the payload goes from your terminal to your browser and through no server, not even Thurin's. Nothing on this machine needs a keystore, a password, or ETH. Links are made for one network; `--site <url>` points them at a local build for testing.

## When your address has no ETH

An identity address should never need to hold a coin. Sign a permission slip instead of a transaction:

```bash
thurin attest --authorize                  # the keystore signs typed data, which is free
thurin attest --authorize --deadline 1d    # default 7d; 30m, 12h, 3d, 1w, or a unix timestamp
thurin attest --authorize --out auth.json  # write a file instead of printing a link
```

The registry has a twin of every write (`attestFor`, `reattestFor`, `updateKeyFor`, `revokeFor`) that takes the owner's EIP-712 signature, so anyone can submit it and pay: a friend opening the link on thurin.id/attest with any wallet, or a funded keystore running `thurin submit <link or file>`. The claim lands under the owner's address. `reattest`, `update-key`, and `revoke` take `--authorize` too.

Before handing the slip out, the CLI proves the signature recovers to your address and simulates the call against the registry, so a slip that would be rejected is never printed. The slip binds the network, the owner's current nonce, and a deadline. It can be used once, and an owner with no ETH cannot recall it before the deadline, so the deadline is printed every time. The link is the same JSON as the file, base64url-encoded after `#handoff=`; the typed data is rebuilt from its fields on both ends rather than carried, so what the page shows is what was signed.

With a relayer, there is no link at all: `thurin attest --authorize --relayer https://relay.example` posts the slip to a service that runs the same checks and pays. See [Run a relayer](#run-a-relayer).

## Records: the chain names what you put out

A record is a small value hung on a claim: one per claim per kind, up to 1 KB, set only by the owner (or by anyone with the owner's `setRecordFor` authorization), readable by anyone, clearable. Kinds are names like `thurin.pointer`, hashed.

The first kind is the **pointer record**: the things an identity has put out, each named by the sha256 of its checksum file.

```bash
thurin record add-release "thurin-cli 0.6.0" SHA256SUMS --url https://github.com/thurinlabs/thurin-cli/releases/tag/v0.6.0
thurin record get thurinlabs.eth pointer          # anyone; prints the list
thurin record set <kind> <value | --file f>       # any kind, raw
thurin record clear <kind>
```

What it changes: a signed release proves *this key signed it*. The pointer record adds *this identity named it*. A stolen key can still sign a tarball with the right version number, but it cannot make the chain name that tarball without a transaction from the owner's address, which everyone can see. See [Verify a release](/guides/verify-release), step 4.

The record holds a list, newest first, and replaces itself on each release. About ten fit in the slot; older ones drop off but remain in chain history, since every set emits an event.

## Be a keyserver

gpg has asked keyservers for keys the same way since the 1990s: one HTTP request, "give me the key with this fingerprint". Anything that answers it is a keyserver to gpg, and to git, mutt, and every package tool built on gpg. `thurin keyserver` answers it by reading the registry.

```bash
thurin keyserver                          # serves hkp://127.0.0.1:11371; --port, --host, --cache-seconds 60
gpg --keyserver hkp://127.0.0.1:11371 --recv-keys 08B9374FDFBEC67EFFA24E669D3D86E35361EF7B
```

Make it gpg's default keyserver and everything built on gpg reads Ethereum from then on:

```bash
echo "keyserver hkp://127.0.0.1:11371" >> ~/.gnupg/dirmngr.conf
gpgconf --kill dirmngr
```

- `gpg --refresh-keys` picks up on-chain revocations. A revoked claim is not served, so a burned key stops refreshing. Put it in cron and legacy gpg gets live revocation checking.
- `gpg --locate-keys` and `--search-keys` work by fingerprint, key ID, Ethereum address, or ENS name.
- With `auto-key-retrieve` in `gpg.conf`, signature verification fetches unknown keys on its own: `git log --show-signature`, signed mail, release checks. Software that will never know Thurin exists gets chain-backed keys with no change in habit.

What it will not do, on purpose:

- **Search by email returns nothing.** Emails are off-chain unless the owner chose otherwise. Fingerprint and key ID were the only keyserver searches that were ever safe; use the full fingerprint, never a short key ID.
- **No upload.** There is no `/pks/add`. Keys are published by their owner attesting, so nobody can attach signatures or garbage to yours. The certificate-flooding attack that broke the SKS network is structurally impossible here.
- **Stateless.** No database, only chain reads and a short cache. The keyserver protocol survives; the writable, poisonable database behind it is what dies.

A fetch by full fingerprint is self-authenticating: gpg checks that the key it received hashes to the fingerprint it asked for, so even a hostile keyserver cannot hand you a wrong key. What a keyserver *can* do is withhold, including withholding a revocation. That is the whole trust question, and it is why there are three rungs:

| Rung | Trusts | Command |
|---|---|---|
| `hkps://keys.thurin.id` | Thurin's instance not to withhold | `gpg --keyserver hkps://keys.thurin.id --recv-keys <fpr>` |
| your own server | your own box | `thurin keyserver --host 0.0.0.0` behind TLS |
| local | nobody; chain-fresh | `thurin keyserver` |

Each rung down loses only convenience. Every rung can be walked away from.

## Run a relayer

A relayer is `thurin submit` behind an HTTP port. It accepts the same JSON a hand-off link carries, runs the same checks, applies a budget and rate limits, and pays for the `…For` call from a hot keystore. Anyone can run one for their community; Thurin runs one with a small budget.

```bash
thurin wallet create hot                  # fund it with pocket money, on the network it will serve
thurin relay --account hot --budget 0.01  # ETH per rolling day
```

| Option | Default | Meaning |
|---|---|---|
| `--budget <eth>` | 0.01 | most it may spend per rolling 24 h |
| `--free-attests <n>` | 1 | `attest` calls it pays for per owner address; updates and revokes are only rate-limited |
| `--per-hour <n>` | 10 | requests per caller per hour |
| `--port`, `--host` | 8787, 127.0.0.1 | listens on localhost; put a TLS proxy in front |

Requests: `POST /` with the hand-off JSON (what `--authorize --out` writes), answer `{hash, block, owner, identity}` or `{error}` with 400 (bad slip), 403 (limit), 429 (rate), 502 (the registry or chain refused), 503 (budget spent). `GET /` reports the network, payer, budget, and spend. Every call must fit `--max-gas` (default 3M, enough for the largest key the registry allows), which bounds a contract wallet that burns gas in its signature check.

Users point at it with `--relayer <url>` or `"relayer"` in their config; `--no-relayer` gets a link instead. It is the one command that spends unattended, gas only, one transaction at a time. Treat the key as pocket money.

A systemd unit, if you run it on a server:

```ini
[Unit]
Description=Thurin relayer
After=network-online.target

[Service]
User=thurin
ExecStart=/usr/bin/npx --yes @thurinlabs/thurin relay --account hot --password-file /etc/thurin/hot.pw --budget 0.01 --port 8787
Environment=THURIN_CONFIG_DIR=/etc/thurin
Restart=always

[Install]
WantedBy=multi-user.target
```

with nginx proxying `relay.example` to `127.0.0.1:8787` and setting `X-Forwarded-For`.

## Keys

```bash
thurin key list                     # your keys: published name, encryption subkey, proof count
thurin key add-name <fpr> thurin    # give an email-only key a name to publish under
thurin key export <fpr>             # the minimal armored export
thurin key fetch bendoubleu.eth     # the key stored on-chain for an identity; --import adds it to your keyring
thurin key default <fpr>
```

`key fetch` is the first piece of the keyserver work on the [roadmap](/roadmap): a key comes from the chain, not from a keyserver.

## Wallet, which is not a wallet

```bash
thurin wallet create <name>     # BIP-39 mnemonic → encrypted V3 keystore under ~/.config/thurin/keystores
thurin wallet import <name>     # a private key, a mnemonic, or --from <keystore.json>
thurin wallet list
thurin wallet export <name>     # the encrypted file; --private-key prints the key, with a warning
thurin wallet default <name>
```

Keystores are the format `cast`, geth, and every wallet import. `--password-file <path>` for non-interactive use.

## Options

| Option | Meaning |
|---|---|
| `--network mainnet\|sepolia\|local` | which chain; `local` is a running anvil |
| `--rpc <url>` | your own node; the default is a public one |
| `--account <name\|path>` | the keystore that pays |
| `--password-file <path>` | keystore password for scripts |
| `--no-key --owner <address\|ens>` | sign here, publish from a wallet elsewhere: prints a link instead of sending |
| `--authorize [--deadline 7d] [--out f.json]` | no ETH here: sign a permission slip anyone can publish |
| `--relayer <url>` / `--no-relayer` | post an authorization to a relayer that pays, or force a link |
| `--site <url>` | where `--no-key` and `--authorize` links point; default `https://thurin.id` |
| `--json` | machine-readable output on stdout |
| `--yes` | skip the confirmation before sending |

Defaults live in `~/.config/thurin/config.json`, for example `{"network":"sepolia","rpc":{"mainnet":"https://…"}}`.

Exit codes: 0 ok · 1 a check failed or no verified claim · 2 usage · 3 chain or network error.

## For agents

An agent can run everything except two prompts: the gpg passphrase (pinentry) and the keystore password (or pass `--password-file`). With `--json` and the exit codes, `thurin status`, `thurin attest --yes`, and `thurin update-key --yes` are scriptable end to end. An agent whose address holds no ETH runs `thurin attest --authorize --out auth.json` and hands the file to whoever pays (`thurin submit auth.json`). The [llms.txt](https://docs.thurin.id/llms.txt) reference describes both the browser flow and this one.

## Source

[github.com/thurinlabs/thurin-cli](https://github.com/thurinlabs/thurin-cli) · MIT. Built on [`@thurinlabs/identity-kit/core`](/sdk), so "verified" means the same thing here as on thurin.id.
