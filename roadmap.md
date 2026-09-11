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

- [x] Identity explorer at [thurin.id](https://thurin.id): look up any ENS name, Ethereum address, or PGP fingerprint
- [x] On-chain identity claims at [thurin.id/attest](https://thurin.id/attest): an Ethereum address bound to a PGP key, published from the address itself
- [x] Thurin Proofs: GitHub, Codeberg, DNS, Farcaster, and Mastodon, verified in the browser against the platform itself
- [x] EFP social graph on every identity page
- [x] identity-kit: the library behind the explorer, with the `ThurinCard` component, hooks, and a one-line embed
- [x] Share cards for READMEs, forums, and link previews
- [x] ENS hosting at `id.thurinlabs.eth` and `thurinlabs.eth`
- [x] Docs and `llms.txt` for AI agents

## Registry v2 <span class="status status-testnet">Testnet</span>

- [x] Claims readable straight from the chain with plain calls: any RPC works, no keyserver, no event logs
- [x] Email stays off-chain by default; one published name carries the proofs
- [x] Update proofs on a claim without re-signing
- [x] Replace a key in one transaction
- [x] Authorized writes: sign offline, let anyone submit; the user still pays by default
- [x] Same contract address on every network
- [x] Independent security review, all findings fixed
- [x] Deployed and verified on Sepolia
- [ ] Deployed on Ethereum mainnet
- [ ] identity-kit 1.0 published
- [ ] thurin.id, share cards, and docs switched to v2

## Thurin CLI <span class="status status-next">Next</span>

- [ ] Attest, update a key, revoke, and check status from a terminal
- [ ] Sign an authorization offline and submit it from any funded account
- [ ] Uses your existing gpg keyring; no keys leave your machine

## Encrypt to an identity <span class="status status-designed">Designed</span>

- [ ] Encrypt a message or file to any verified Thurin identity, in the browser
- [ ] Same in the CLI, with signing
- [ ] Identity page becomes tabs: Overview, Claims, Encrypt
- [ ] "Accepts encrypted mail" shown on identities whose key supports it

## Records <span class="status status-designed">Designed</span>

- [ ] Small typed values attached to a claim
- [ ] Private records: encrypted to yourself
- [ ] Shared records: encrypted to the people you choose; the first use is a private email claim
- [ ] Pointer records to larger content
- [ ] Records tab on the identity page

## Web of trust <span class="status status-designed">Designed</span>

- [ ] Vouch for a key you have checked, published on-chain
- [ ] Vouches shown on the identity page, with a link to each voucher
- [ ] Vouches weighed by the voucher's own evidence; no token, no staking

## Later

- [ ] Thurin Score: a transparent confidence rating over the evidence, including the web of trust

---

Changes land on [GitHub](https://github.com/thurinlabs). Design notes for each item are published as they ship.
