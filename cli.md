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
claims      2 total · 1 active · 1 ended
fingerprint 9C4E27B1D0835F6A2E71C4B8093DA5F16B2E8C47  ✓ verified
name        Alice
key         Ed25519 · created 2026-03-02 · claimed 2026-09-12 · expires 2028-03-01
proofs
  ✓ GitHub     alice
  ✓ DNS        alice.example
history
  #0 1A2B3C4D…5E6F7A8B 2026-06-10 replaced → #1
  #1 9C4E27B1…6B2E8C47 2026-09-12 active verified
```

It takes an ENS name, an address, a fingerprint, or a 16-character key ID. Exit code 1 means no verified claim. `status` checks proofs, since you asked; `--no-proofs` asks nothing but the Ethereum node and lists them as not checked.

When a claim doesn't count, the line says why: `✗ key expired`, `✗ key revoked`, `✗ key compromised`, `✗ signing key expired`, `✗ signing key revoked`, `✗ not supported`, or `✗ doesn't verify`. A key that expires within 30 days gets `⚠ key expires in 12 days`. If a keystore on this machine holds the address, the line adds the fix, for example `extend it (gpg --quick-set-expire), then thurin update-key`.

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

- exports a minimal copy of the key and leaves out every name with an email (`--include-email` keeps them); every subkey stays, an SSH (authentication) one included;
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
- **revoke:** `--reason compromised`, `retired`, or `other`, or leave it off. **Compromised is final:** this address can never claim that key again. Found out later? `thurin revoke <index> --reason compromised` marks a claim that's already revoked or replaced, once.

## No ETH on this machine

Three ways, depending on where things are.

**Your ETH wallet is elsewhere** (a hardware wallet, a phone):

```bash
thurin attest --no-key --owner you.eth
```

It signs and checks everything, then prints a `https://thurin.id/attest#handoff=…` link. Open it where the wallet is, connect the address you named, and publish. The key and signature ride in the part after `#`, which browsers never send to a server. `reattest`, `update-key`, and `record set` take `--no-key` too.

**No ETH anywhere:** sign a permission instead of a transaction. It's free.

```bash
thurin attest --authorize                   # a link anyone can publish and pay for
thurin attest --authorize --out auth.json   # or a file
thurin attest --authorize --deadline 1d     # default 7d
```

Anyone can then publish it: a friend opening the link on thurin.id with any wallet, or `thurin submit auth.json` from a funded keystore. The claim lands under your address. `reattest`, `update-key`, `revoke`, and `record set` take `--authorize` too.

Before handing it out, the CLI checks that the permission recovers to your address and that the registry would take it. It can be used once, only before its deadline, which is printed every time. To stop it sooner, `thurin cancel` spends it (and any other unused permission you've signed) with a transaction of your own, so that one needs ETH. Without the CLI, call `cancelAuthorization()` on the [registry](/contracts) from the same address. `--relay <url>` posts it to a [relay](/cli?id=run-a-relay) that pays, with no link at all.

**The PGP key isn't here** (a card, an air-gapped machine):

```bash
thurin attest --statement --owner you.eth    # prints the line to sign
# where the key is:
#   printf '%s' 'I control the Ethereum address: 0x…' | gpg --detach-sign --textmode --disable-signer-uid > s.sig
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

`record add-release` names a release on-chain by its checksum file. Anyone who ships software can keep a list:

```bash
thurin record add-release "thurin-cli 0.13.3" SHA256SUMS --url https://github.com/thurinlabs/thurin-cli/releases/tag/v0.13.3
thurin record get thurinlabs.eth releases
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
thurin key ssh bendoubleu.eth     # its SSH keys, as authorized_keys lines
thurin key default <fingerprint>  # the key to use when --key isn't given
```

## Encrypt to someone

```bash
echo "meet at noon" | thurin encrypt bendoubleu.eth > note.asc   # stdin → armored message on stdout
thurin encrypt bendoubleu.eth report.pdf                         # writes report.pdf.gpg
thurin encrypt bendoubleu.eth report.pdf --sign -o out.gpg       # signed with your key, named output
```

Only to the claim that counts, and only while its encryption subkey is valid; otherwise one sentence says why and it exits 1. It warns when the key arrived in the last 7 days. gpg encrypts with `--recipient-file`, so nothing lands in your keyring. The recipient's key ID is left out of the message (`--show-recipient` puts it back). More: [Encrypt to an identity](/guides/encrypt).

## Log in with SSH

Add an authentication subkey to your PGP key, and your claim carries an SSH key too:

```bash
gpg --quick-add-key <fingerprint> ed25519 auth 2y
thurin update-key          # or claim the key for the first time with thurin attest
```

`thurin key ssh <identity>` prints every valid SSH key from the claim that counts, one `authorized_keys` line each, like `github.com/<user>.keys` with no one in control. Append them to a file, or let sshd ask at every login:

```
# /etc/ssh/sshd_config
AuthorizedKeysCommand /usr/bin/thurin key ssh 0x<address> --rpc http://127.0.0.1:8545
AuthorizedKeysCommandUser nobody
```

Revoke the claim, or mark the key compromised, and the next login is refused. Use the address, not an ENS name: a name can be pointed somewhere else. **Use your own Ethereum node** (`--rpc`): sshd trusts whatever the node answers, and a node that lies could hand it someone else's key. The default node is PublicNode, a third party; fine for looking people up, not for letting them into your server. Put every flag on the command line: sshd runs it as `nobody`, which can't read your `~/.config/thurin`. sshd needs the absolute path (`command -v thurin`), and Node must be installed system-wide: sshd's minimal PATH won't find one from nvm. The command asks the node at every login, so if the node can't be reached nobody gets in; keep a local key or a console as a way back. Ed25519, RSA, and NIST ECDSA keys work; OpenSSH has no Ed448, brainpool, or secp256k1.

## Wallet, which is not a wallet

```bash
thurin wallet create <name>    # encrypted keystore in ~/.config/thurin/keystores
thurin wallet import <name>    # a private key, 12 words, or --from keystore.json
thurin wallet list
thurin wallet export <name>    # the encrypted file; --private-key prints the key
thurin wallet default <name>
```

Keystores are the V3 format `cast`, geth, and most wallets import. `--password-file <path>` for scripts. `wallet create` and `export --private-key` print their secret only to a terminal, never to a pipe or a file.

## Be a keyserver

gpg fetches keys from keyservers with one HTTP request. `thurin keyserver` answers it from the registry.

```bash
thurin keyserver    # hkp://127.0.0.1:11371; add --rpc <url> to read through your own node
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
- **Keep anything.** No database; chain reads and a short cache (60 seconds by default; keys.thurin.id uses 120).

A fetch by full fingerprint checks itself: gpg makes sure the key hashes to what it asked for, so a keyserver can withhold a key but never swap one. Pick how much you trust that:

| where | you trust | how |
|---|---|---|
| `hkps://keys.thurin.id` | Thurin Labs' server not to withhold | `gpg --keyserver hkps://keys.thurin.id --recv-keys <fpr>` |
| your own server | your server | `thurin keyserver --host 0.0.0.0` behind TLS |
| this machine | nobody | `thurin keyserver` |

Write the `hkps://`: a bare `keys.thurin.id` means plain HKP to gpg.

## Run a relay

A relay is `thurin submit` behind an HTTP port: it takes permissions, runs the same checks, and pays for them from a hot keystore, within limits. Anyone can run one. Thurin Labs runs one at relay.thurin.id.

```bash
thurin wallet create hot                   # fund it with pocket money
thurin relay --account hot --budget 0.01   # ETH per day
```

| option | default | |
|---|---|---|
| `--budget` | 0.01 | ETH it may spend per rolling 24 hours |
| `--free-attests` | 1 | `attest` calls it pays for per address; other writes are only rate-limited |
| `--per-hour` | 10 | requests per caller |
| `--max-gas` | 6000000 | per transaction |
| `--port`, `--host` | 8787, 127.0.0.1 | put a TLS proxy in front |

`POST /` with what `--authorize --out` writes. The answer is `{hash, block, owner, op, proofs, payer, identity}`, or `{error}` with 400 (a bad permission, or the registry's reason for refusing it), 403 or 429 (limits), 502 (the chain or RPC failed), 503 (budget spent), or 500 (anything else). `GET /` shows the network and chain id, payer, budget, and today's spend; thurin.id offers the relay only when its network matches.

People use it with `--relay <url>` or `"relay"` in their config. It's the one command that spends without asking, gas only, one transaction at a time.

## Options

| option | |
|---|---|
| `--network mainnet\|sepolia\|local` | which chain (default mainnet; `local` is anvil on 8545) |
| `--rpc <url>` | your own node (also `THURIN_RPC_URL`) |
| `--account <name\|path>` | the keystore that signs or pays |
| `--password-file <path>` | the keystore password, for scripts |
| `--key <fingerprint>` | which PGP key |
| `--site <url>` | where links point (default https://thurin.id) |
| `--json` | data on stdout |
| `--yes` | don't ask before sending |
| `--show-network` | list the hosts the command contacted, when it ends (also `THURIN_SHOW_NETWORK=1`) |

Defaults live in `~/.config/thurin/config.json`, for example `{"network":"sepolia","rpc":{"mainnet":"https://…"},"account":"identity"}`.

Exit codes: 0 ok · 1 a check failed · 2 usage · 3 chain or network error.

The registry is `0xFa6956c11163517249f8A67F5560a4406B519451`, the same address on Ethereum mainnet and Sepolia ([contract](/contracts)).

## For agents

Everything runs unattended except two prompts: the gpg passphrase (pinentry) and the keystore password (`--password-file`). With `--json`, `--yes`, and the exit codes, `status`, `attest`, `update-key`, and `record set` script end to end. An agent whose address holds no ETH runs `thurin attest --authorize --out auth.json` and hands the file to whoever pays. [llms.txt](/llms.txt ':ignore') is the index for agents; [llms-full.txt](/llms-full.txt ':ignore') has every page in one file. An agent never runs `thurin wallet create`, `wallet import`, or `wallet export --private-key` for someone: those handle the secret, so the person runs them in their own terminal.

## Source

[github.com/thurinlabs/thurin-cli](https://github.com/thurinlabs/thurin-cli) · MIT. Built on [identity-kit](/sdk), so "verified" means the same here as on thurin.id.
