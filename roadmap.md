# Roadmap

What Thurin.id is building, in the order it will ship. Everything here is open source and runs with no Thurin Labs server in the path.

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
- [x] Proofs: GitHub, Codeberg, DNS, Farcaster, and Mastodon, checked in the browser against the platform itself, when the visitor asks
- [x] A link to each identity's EFP profile
- [x] identity-kit: the one library behind the site, the CLI, and the cards
- [x] A card image for READMEs, and link previews, drawn by thurin.id's server
- [x] ENS hosting at `id.thurinlabs.eth` and `thurinlabs.eth`
- [x] Docs and `llms.txt` for AI agents

## Registry v3 <span class="status status-progress">In progress</span>

*What if the contract was the whole tool?*

- [x] Usable with only Etherscan or `cast` and gpg: the key comes out ready for `gpg --import`, the claim ready for `gpg --verify` ([how](/contracts?id=use-it-with-gpg-and-cast))
- [x] Keys and signatures stored as raw bytes: a first claim costs about a third less than on v2, a later one about half
- [x] Revoke with a reason; "compromised" is final, and can be marked later if you find out afterwards
- [x] Replace a stolen key and mark it compromised in one transaction
- [x] Records as named text, listed by the contract, and they follow a claim when it's replaced
- [x] Three adversarial reviews, the last with a model-based test of every claim state; every finding fixed (not a third-party audit; see [CROPS](/crops))
- [x] Deployed and verified on Sepolia (Etherscan and Sourcify)
- [ ] Deployed on Ethereum mainnet, the same address as Sepolia
- [ ] identity-kit 2.0, the CLI, and thurin.id switched to v3; existing claims re-published

## Thurin CLI <span class="status status-shipped">Shipped</span>

*What if your online identity worked from a terminal?*

- [x] Attest, update a key, revoke, and check status from a terminal ([`npx @thurinlabs/thurin`](/cli))
- [x] Uses your existing gpg keyring; no keys leave your machine
- [x] Sign in the terminal, publish from a hardware or phone wallet (`--no-key` hands a link to thurin.id)
- [x] Sign a permission offline and submit it from any funded account (`--authorize`, `thurin submit`)
- [x] Keep the Ethereum key on a card or an air-gapped machine: hand the typed data to any signer, or write it to a file and finish later (`--signer`, `--sign-out`, `thurin authorize finish`)
- [x] Attest with a PGP key that isn't on this machine: print the line, sign it where the key is, bring two files back (`--statement`, `--key-file`)

## Sponsored claims <span class="status status-shipped">Shipped</span>

*What if you could prove it’s you from a terminal, with an address that has never held a coin?*

- [x] Sign a claim without holding any ETH, in the browser or the CLI
- [x] Anyone with a wallet can open the link and pay for someone else's claim; it lands under the signer
- [x] An open-source relay anyone can run to sponsor their community (`thurin relay`)
- [x] Thurin Labs' own relay at relay.thurin.id: one claim per address, within a daily budget

## The keyserver <span class="status status-shipped">Shipped</span>

*What if the keyserver was Ethereum?*

- [x] A local keyserver: point gpg at it and `--recv-keys` reads Ethereum, no keyserver database anywhere (`thurin keyserver`)
- [x] A hosted copy at keys.thurin.id for gpg users without the CLI; anyone can run one
- [x] Verify signed commits and signed releases with only gpg, keys fetched from the chain ([guides](/guides/verify-commits))
- [x] A front door: open the keyserver in a browser for the dirmngr line, a search box, and the classic listing with who claims each key on-chain
- [ ] Pseudonymous mode: fresh keys, no proofs, all network traffic over Tor by default

## ENS <span class="status status-shipped">Shipped</span>

*What if your ENS profile could prove its key?*

- [x] `id.thurin`: an ENS text record that points a name at the key its address claims; a hint any ENS viewer can show, checked from the chain ([guide](/guides/ens-record))
- [x] The identity page checks the record against the claim: matches, not set, or points elsewhere, with a one-transaction "Set it"
- [x] `thurin ens check` and `thurin ens link` in the CLI
- [ ] The Thurin.id icon on EFP profile cards, shown when a name carries the record (pull request open)

## Records <span class="status status-shipped">Shipped</span>

*What if the chain could name the release too?*

- [x] A release list on any claim naming each release's checksum file, so a signed release is one its publisher put out, not only one its key signed (`thurin record add-release`); Thurin Labs names every CLI release this way
- [x] Small values attached to a claim, set from the page or the CLI (`thurin record set|get|clear`)
- [x] A Railgun record: publish your 0zk address so people can pay you privately by name
- [x] Records tab on the identity page, and the [kinds](/records) it shows: private payments, security contact, successor key, affiliation, canary, releases, private, disclosure

## Privacy and trust <span class="status status-shipped">Shipped</span>

*What if the tools that check identities kept nothing about the people using them?*

- [x] No accounts, cookies, analytics, or telemetry on any Thurin Labs site
- [x] Our servers keep no access logs; the keyserver and relay record no IP addresses
- [x] Pick the Ethereum node your browser reads from (thurin.id footer); no API key ships in any page
- [x] Light and dark on thurin.id, thurinlabs.id, and these docs
- [x] Profile pictures only from sources the name's owner can't watch
- [x] Scripts and fonts served by our own sites, not pulled from CDNs
- [x] Every site deploy a signed tag naming what went live; releases signed and matched to their commits
- [x] A public [CROPS](/crops) review, checked against the live sites

## Encrypt to an identity <span class="status status-progress">In progress</span>

*What if you could encrypt a file to a name?*

- [x] Encrypt a message or file to any verified Thurin.id identity, in the browser ([how](/guides/encrypt))
- [x] Same in the CLI, with signing
- [x] An Encrypt tab on the identity page, next to Overview, Claims, and Records
- [x] A warning when an identity's key changed recently, before you encrypt to it
- [x] "Can receive encrypted messages" shown on identities whose key supports it
- [x] The recipient left out of the message, so an intercepted one doesn't point at a name

## Web of trust <span class="status status-designed">Designed</span>

*What if vouching for someone counted for something?*

- [ ] Vouch for a key you have checked, published on-chain
- [ ] Vouches shown on the identity page, with a link to each voucher
- [ ] Vouches weighed by the voucher's own evidence; no token, no staking

## Later

- [ ] Thurin Score: a transparent confidence rating over the evidence, including the web of trust
- [ ] Pay for a claim from shielded funds, so an identity address never has to hold ETH in the open

---

Changes land on [GitHub](https://github.com/thurinlabs).
