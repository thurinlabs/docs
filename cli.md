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
| `--site <url>` | where `--no-key` and `--authorize` links point; default `https://thurin.id` |
| `--json` | machine-readable output on stdout |
| `--yes` | skip the confirmation before sending |

Defaults live in `~/.config/thurin/config.json`, for example `{"network":"sepolia","rpc":{"mainnet":"https://…"}}`.

Exit codes: 0 ok · 1 a check failed or no verified claim · 2 usage · 3 chain or network error.

## For agents

An agent can run everything except two prompts: the gpg passphrase (pinentry) and the keystore password (or pass `--password-file`). With `--json` and the exit codes, `thurin status`, `thurin attest --yes`, and `thurin update-key --yes` are scriptable end to end. An agent whose address holds no ETH runs `thurin attest --authorize --out auth.json` and hands the file to whoever pays (`thurin submit auth.json`). The [llms.txt](https://docs.thurin.id/llms.txt) reference describes both the browser flow and this one.

## Source

[github.com/thurinlabs/thurin-cli](https://github.com/thurinlabs/thurin-cli) · MIT. Built on [`@thurinlabs/identity-kit/core`](/sdk), so "verified" means the same thing here as on thurin.id.
