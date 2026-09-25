# Thurin CLI

`thurin` does what thurin.id does, from a terminal: look anyone up, and add, change, or end your own claim. Every check runs before any gas is spent. Every command has `--json` output and exit codes, so scripts and agents can drive it.

Two rules:

- **It is not a wallet.** It makes, imports, lists, and exports keystores. No balances, no transfers.
- **It never holds a PGP secret, and it doesn't make keys.** Every PGP step is your own `gpg`; passphrases go through pinentry.

## Install

```bash
npm install -g @thurinlabs/thurin
# or, without installing:
npx @thurinlabs/thurin status thurinlabs.eth
```

Node 20 or newer. GnuPG 2.2 or newer for anything that touches a key. Releases are signed; [Verify a release](/guides/verify-release) shows how to check one.

`thurin --help` is one screen. `thurin help <command>` has the rest (`status`, `key`, `wallet`, `attest`, `no-eth`, `record`, `ens`, `keyserver`, `relay`, `options`).

## Look someone up

```
$ thurin status alice.eth
alice.eth  0x8f3C…2b41  (mainnet)
claims      2 total · 1 active · 1 revoked
fingerprint 9C4E27B1D0835F6A2E71C4B8093DA5F16B2E8C47  ✓ verified
name        Alice
key         Ed25519 · created 2026-03-02 · claimed 2026-10-01 · expires 2028-03-01
proofs
  ✓ GitHub     alice
  ✓ DNS        alice.example
efp         12 followers · 4 following
history
  #0 1A2B3C4D…5E6F7A8B 2026-06-10 replaced → #1
  #1 9C4E27B1…6B2E8C47 2026-10-01 verified
```

It takes an ENS name, an address, a fingerprint, or a 16-character key ID. Exit code 1 means no verified claim.

When a claim doesn't count, the line says why: `✗ key expired`, `✗ key revoked`, `✗ key compromised`, `✗ signing key expired`, `✗ not supported`, or `✗ doesn't verify`. A key that expires within 30 days gets `⚠ key expires in 12 days`. If a keystore on this machine holds the address, the line adds the fix, for example `extend it (gpg --quick-set-expire), then thurin update-key`.

## Add your key

gpg makes the key. Leave the email off if you don't want it published:

```bash
gpg --quick-gen-key "Your Name" ed25519 sign 2y
gpg --quick-add-key <fingerprint> cv25519 encr 2y
```

Then an address, and the claim:

```bash
thurin wallet create identity     # a fresh address; the 12 words are shown once
thurin attest --key <fingerprint>
```

The address needs a little ETH for the fee. No ETH there? See [below](/cli?id=no-eth-on-this-machine).

Before it asks you to confirm, `attest`:

- exports a minimal copy of the key and leaves out every name with an email (`--include-email` keeps them);
- has gpg sign `I control the Ethereum address: 0x…`;
- checks that signature the same way thurin.id will, plus the size limits and that this address hasn't revoked the key as compromised;
- shows the names, proof count, and size that will go on-chain.

`--account` takes a name from `thurin wallet list` or a path to any V3 keystore, Foundry's included. `THURIN_PRIVATE_KEY` in the environment also works, for scripts.

## Change or end a claim

```bash
thurin update-key                        # new names or proofs, same key, no new signature
thurin reattest --key <new fingerprint>  # replace the claim in one transaction
thurin revoke --reason retired           # end it; it stays in the history
```

Each takes an optional claim index (`thurin status` lists them). With one active claim it's picked for you.

- **update-key:** after adding a proof notation ([how](/guides/gnupg)), extending the expiry, or adding a subkey. The fingerprint stays, so the claim stays; only the stored key changes.
- **reattest:** the old claim is revoked and the new one published together. Its records move to the new claim; `--drop-records` leaves them behind. If the old key was stolen, add `--compromised` to mark it in the same transaction.
- **revoke:** `--reason compromised`, `retired`, or `other`, or none. **Compromised is final:** this address can never claim that key again. Found out later? `thurin revoke <index> --reason compromised` marks a claim that's already revoked or replaced, once.

## No ETH on this machine

Three ways, depending on where things are.

**Your ETH wallet is elsewhere** (a hardware wallet, a phone):

```bash
thurin attest --no-key --owner you.eth
```

It signs and checks everything, then prints a `https://thurin.id/attest#handoff=…` link. Open it where the wallet is, connect the address you named, and publish. The key and signature ride in the part after `#`, which browsers never send to a server. `reattest` and `update-key` take `--no-key` too.

**No ETH anywhere:** sign a permission instead of a transaction. It's free.

```bash
thurin attest --authorize                   # a link anyone can publish and pay for
thurin attest --authorize --out auth.json   # or a file
thurin attest --authorize --deadline 1d     # default 7d
```

Anyone can then publish it: a friend opening the link on thurin.id with any wallet, or `thurin submit auth.json` from a funded keystore. The claim lands under your address. `reattest`, `update-key`, `revoke`, and `record set` take `--authorize` too.

Before handing it out, the CLI checks that the permission recovers to your address and that the registry would take it. It can be used once, only before its deadline, and it can't be recalled without ETH, so the deadline is printed every time. `--relayer <url>` posts it to a [relayer](/cli?id=run-a-relayer) that pays, with no link at all.

**The PGP key isn't here** (a card, an air-gapped machine):

```bash
thurin attest --statement --owner you.eth    # prints the line to sign
# where the key is:
#   printf '%s' 'I control the Ethereum address: 0x…' | gpg --detach-sign --textmode > s.sig
#   gpg --export <fingerprint> > pub.gpg
thurin attest --key-file pub.gpg --statement-file s.sig --owner you.eth --no-key
```

Sign the line with no line break after it (`printf '%s'`, not `echo`). A clearsigned statement works too. From there every check runs as usual. `update-key` takes `--key-file` alone.

**The Ethereum key isn't here either.** `--authorize` needs one EIP-712 signature, and anything that signs typed data can make it:

```bash
thurin attest --authorize --owner you.eth --signer "my-card-tool sign"   # typed data on stdin, signature on stdout

thurin attest --authorize --owner you.eth --sign-out slip.json           # air gap: writes what to sign, stops
thurin authorize finish slip.json --signature 0x…                        # checks it, then the link
```

A signature from anyone but `--owner` is refused.

`--site <url>` points links somewhere other than thurin.id, such as a local build.

## Records

Small values on your claim, readable by anyone. The kinds and what they mean are on the [Records](/records) page.

```bash
thurin record get thurinlabs.eth                # every record on the claim
thurin record get thurinlabs.eth canary         # one value, so it pipes
thurin record get thurinlabs.eth canary | gpg --verify
thurin record set security "mailto:security@example.com"
thurin record set canary --file canary.asc
thurin record clear security
```

A name without a dot gets `thurin.` in front. `--index <n>` picks the claim when the address has more than one active.

`record add-release` names a release on-chain by its checksum file:

```bash
thurin record add-release "thurin-cli 0.13.0" SHA256SUMS --url https://github.com/thurinlabs/thurin-cli/releases/tag/v0.13.0
thurin record get thurinlabs.eth pointer
```

A signature proves *this key signed it*. The record adds *this identity named it*, which a stolen PGP key can't do without a transaction everyone can see. The list keeps the newest releases that fit in 1 KB; older ones drop off but stay in the chain's history. See [Verify a release](/guides/verify-release).

## ENS

```bash
thurin ens check ben.thurinlabs.eth             # does the name's id.thurin record match its claim?
thurin ens link ben.thurinlabs.eth              # set it from the keystore
thurin ens link ben.thurinlabs.eth --calldata   # print the transaction for the wallet that manages the name
```

`link` refuses a name without a verified claim and does nothing when the record already matches. See [the guide](/guides/ens-record).

## Keys

```bash
thurin key list                   # your keys, with the names and proofs that would be published
thurin key export <fingerprint>   # the minimal armored export
thurin key fetch thurinlabs.eth   # the key stored on-chain; --import adds it to your keyring
thurin key default <fingerprint>  # the key to use when --key isn't given
```

## Wallet, which is not a wallet

```bash
thurin wallet create <name>    # encrypted keystore in ~/.config/thurin/keystores
thurin wallet import <name>    # a private key, 12 words, or --from keystore.json
thurin wallet list
thurin wallet export <name>    # the encrypted file; --private-key prints the key
thurin wallet default <name>
```

Keystores are the V3 format `cast`, geth, and most wallets import. `--password-file <path>` for scripts.

## Be a keyserver

gpg fetches keys from keyservers with one HTTP request. `thurin keyserver` answers it from the registry.

```bash
thurin keyserver    # hkp://127.0.0.1:11371
gpg --keyserver hkp://127.0.0.1:11371 --recv-keys 08B9374FDFBEC67EFFA24E669D3D86E35361EF7B
```

Make it gpg's default and everything built on gpg reads Ethereum:

```bash
echo "keyserver hkp://127.0.0.1:11371" >> ~/.gnupg/dirmngr.conf
gpgconf --kill dirmngr
```

- `gpg --refresh-keys` picks up revocations: a revoked claim isn't served.
- `--locate-keys` and `--search-keys` work by fingerprint, key ID, Ethereum address, or ENS name.
- With `auto-key-retrieve` in `gpg.conf`, `git log --show-signature` and signed mail fetch unknown keys on their own.
- Open it in a browser for a search page.

What it won't do:

- **Search by email.** Emails are off-chain unless the owner chose otherwise.
- **Take uploads.** There's no `/pks/add`; a key is published by its owner attesting, so nobody can flood yours with signatures.
- **Keep anything.** No database; chain reads and a 60-second cache.

A fetch by full fingerprint checks itself: gpg makes sure the key hashes to what it asked for, so a keyserver can withhold a key but never swap one. Pick how much you trust that:

| where | you trust | how |
|---|---|---|
| `hkps://keys.thurin.id` | Thurin's server not to withhold | `gpg --keyserver hkps://keys.thurin.id --recv-keys <fpr>` |
| your own server | your server | `thurin keyserver --host 0.0.0.0` behind TLS |
| this machine | nobody | `thurin keyserver` |

Write the `hkps://`: a bare `keys.thurin.id` means plain HKP to gpg.

## Run a relayer

A relayer is `thurin submit` behind an HTTP port: it takes permissions, runs the same checks, and pays for them from a hot keystore, within limits. Anyone can run one. Thurin runs one at relay.thurin.id.

```bash
thurin wallet create hot                   # fund it with pocket money
thurin relay --account hot --budget 0.01   # ETH per day
```

| option | default | |
|---|---|---|
| `--budget` | 0.01 | ETH it may spend per rolling 24 hours |
| `--free-attests` | 1 | `attest` calls it pays for per address; other writes are only rate-limited |
| `--per-hour` | 10 | requests per caller |
| `--max-gas` | 3000000 | per transaction |
| `--port`, `--host` | 8787, 127.0.0.1 | put a TLS proxy in front |

`POST /` with what `--authorize --out` writes. The answer is `{hash, block, owner, identity}`, or `{error}` with 400 (bad permission), 403 or 429 (limits), 502 (the chain refused), or 503 (budget spent). `GET /` shows the network, payer, budget, and today's spend.

People use it with `--relayer <url>` or `"relayer"` in their config. It's the one command that spends without asking, gas only, one transaction at a time.

## Options

| option | |
|---|---|
| `--network mainnet\|sepolia\|local` | which chain (default mainnet; `local` is anvil on 8545) |
| `--rpc <url>` | your own node |
| `--account <name\|path>` | the keystore that signs or pays |
| `--password-file <path>` | the keystore password, for scripts |
| `--key <fingerprint>` | which PGP key |
| `--site <url>` | where links point (default https://thurin.id) |
| `--json` | data on stdout |
| `--yes` | don't ask before sending |

Defaults live in `~/.config/thurin/config.json`, for example `{"network":"sepolia","rpc":{"mainnet":"https://…"},"account":"identity"}`.

Exit codes: 0 ok · 1 a check failed · 2 usage · 3 chain or network error.

The registry is `0xFa6956c11163517249f8A67F5560a4406B519451`, the same address on Ethereum mainnet and Sepolia ([contract](/contracts)).

## For agents

Everything runs unattended except two prompts: the gpg passphrase (pinentry) and the keystore password (`--password-file`). With `--json`, `--yes`, and the exit codes, `status`, `attest`, `update-key`, and `record set` script end to end. An agent whose address holds no ETH runs `thurin attest --authorize --out auth.json` and hands the file to whoever pays. [llms.txt](https://docs.thurin.id/llms.txt) has the whole reference in one file.

## Source

[github.com/thurinlabs/thurin-cli](https://github.com/thurinlabs/thurin-cli) · MIT. Built on [identity-kit](/sdk), so "verified" means the same here as on thurin.id.
