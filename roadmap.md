# Roadmap

What Thurin is building, in the order it will ship. Everything here is open source and runs with no Thurin server in the path.

## Status key

| Status | Meaning |
|---|---|
| <span class="status status-shipped">Shipped</span> | live on Ethereum mainnet |
| <span class="status status-testnet">Testnet</span> | deployed on Sepolia, being exercised |
| <span class="status status-progress">In progress</span> | code exists, not yet released |
| <span class="status status-next">Next</span> | the next thing to be built |
| <span class="status status-designed">Designed</span> | written up, not started |

## Thurin.id <span class="status status-shipped">Shipped</span>

*What if everyone knew who you were… because you let them?*

- [x] Identity explorer at [thurin.id](https://thurin.id): look up any ENS name, Ethereum address, or PGP fingerprint
- [x] On-chain identity claims at [thurin.id/attest](https://thurin.id/attest): an Ethereum address bound to a PGP key, published from the address itself
- [x] Thurin Proofs: GitHub, Codeberg, DNS, Farcaster, and Mastodon, verified in the browser against the platform itself
- [x] EFP social graph on every identity page
- [x] identity-kit: the library behind the explorer, with the `ThurinCard` component, hooks, and a one-line embed
- [x] Share cards for READMEs, forums, and link previews
- [x] ENS hosting at `id.thurinlabs.eth` and `thurinlabs.eth`
- [x] Docs and `llms.txt` for AI agents

## Registry v2 <span class="status status-shipped">Shipped</span>

*What if your online identity had a home?*

- [x] Claims readable straight from the chain with plain calls: any RPC works, no keyserver, no event logs
- [x] Email stays off-chain by default; one published name carries the proofs
- [x] Update proofs on a claim without re-signing
- [x] Replace a key in one transaction
- [x] Authorized writes: sign offline, let anyone submit; the user still pays by default
- [x] Same contract address on every network
- [x] Independent security review, all findings fixed
- [x] Deployed and verified on Sepolia
- [x] Deployed on Ethereum mainnet
- [x] identity-kit 1.0 published
- [x] thurin.id, share cards, and docs switched to v2

## Thurin CLI <span class="status status-shipped">Shipped</span>

*What if your online identity worked from a terminal?*

- [x] Attest, update a key, revoke, and check status from a terminal ([`npx @thurinlabs/thurin`](/cli))
- [x] Uses your existing gpg keyring; no keys leave your machine
- [x] Sign in the terminal, publish from a hardware or phone wallet (`--no-key` hands a link to thurin.id)
- [x] Sign an authorization offline and submit it from any funded account (`--authorize`, `thurin submit`)
- [x] Keep the Ethereum key on a card or an air-gapped machine: hand the typed data to any signer, or write it to a file and finish later (`--signer`, `--sign-out`, `thurin authorize finish`)

## Sponsored attestations <span class="status status-shipped">Shipped</span>

*What if you could prove it’s you from a terminal, with an address that has never held a coin?*

- [x] Sign an attestation without holding any ETH, in the browser or the CLI
- [x] Anyone with a wallet can open the link and pay for someone else's attestation; the claim lands under the signer
- [x] An open-source relayer anyone can run to sponsor their community (`thurin relay`)
- [x] Thurin's own relayer at relay.thurin.id: one claim per address, within a daily budget

## The keyserver <span class="status status-shipped">Shipped</span>

*What if the keyserver was Ethereum?*

- [x] A local keyserver: point gpg at it and `--recv-keys` reads Ethereum, no keyserver database anywhere (`thurin keyserver`)
- [x] A hosted copy at keys.thurin.id for gpg users without the CLI; anyone can run one
- [x] Verify signed commits and signed releases with only gpg, keys fetched from the chain ([guides](/guides/verify-commits))
- [x] A front door: open the keyserver in a browser for the dirmngr line, a search box, and the classic listing with who claims each key on-chain
- [ ] Create a fresh identity address and PGP key in one guided run
- [ ] Pseudonymous mode: fresh keys, no proofs, all network traffic over Tor by default

## ENS <span class="status status-shipped">Shipped</span>

*What if your ENS profile could prove its key?*

- [x] `id.thurin`: an ENS text record that points a name at the key its address claims; a hint any ENS viewer can show, checked from the chain ([guide](/guides/ens-record))
- [x] The identity page checks the record against the claim: matches, not set, or points elsewhere, with a one-transaction "Set it"
- [x] `thurin ens check` and `thurin ens link` in the CLI (0.8.0)
- [ ] The Thurin icon on EFP profile cards, shown when a name carries the record (pull request open)

## Records <span class="status status-progress">In progress</span>

*What if the chain could name the release, not just the key?*

- [x] A pointer record on the company claim naming each release's checksum file, so a signed release is one Thurin Labs put out, not just one its key signed (`thurin record add-release`)
- [x] Small typed values attached to a claim, set from the CLI (`thurin record set|get|clear`)
- [ ] Private records: encrypted to yourself
- [ ] Shared records: encrypted to the people you choose; the first use is a private email claim
- [ ] A Railgun record: publish your 0zk address so people can pay you privately by name
- [x] Records tab on the identity page, and the [kinds](/records) it shows: pay privately, security contact, successor key, affiliation, canary, private, disclosure

## Encrypt to an identity <span class="status status-designed">Designed</span>

*What if you could encrypt a file to a name?*

- [ ] Encrypt a message or file to any verified Thurin identity, in the browser
- [ ] Same in the CLI, with signing
- [ ] Identity page becomes tabs: Overview, Claims, Encrypt
- [ ] "Accepts encrypted mail" shown on identities whose key supports it

## Web of trust <span class="status status-designed">Designed</span>

*What if vouching for someone counted for something?*

- [ ] Vouch for a key you have checked, published on-chain
- [ ] Vouches shown on the identity page, with a link to each voucher
- [ ] Vouches weighed by the voucher's own evidence; no token, no staking

## Later

- [ ] Thurin Score: a transparent confidence rating over the evidence, including the web of trust
- [ ] Pay for an attestation from shielded funds, so an identity address never has to hold ETH in the open

---

Changes land on [GitHub](https://github.com/thurinlabs). Design notes for each item are published as they ship.
