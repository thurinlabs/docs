# CROPS

> **Checked 24 September 2026**, on the live sites, against the [CROPS review checklist](https://ethskills.com/crops/SKILL.md) from ETHSKILLS, which turns the Ethereum Foundation's CROPS principles ([EF Mandate](https://blog.ethereum.org/2026/03/13/ef-mandate)) into concrete checks. This is our own review; the Ethereum Foundation did not review Thurin.id.

The Ethereum Foundation asks every project to answer four questions: can someone block you (**C**ensorship resistance), can you see and fork all of it (**O**pen source and free), what does it learn about you (**P**rivacy), and what happens if it fails or the team disappears (**S**ecurity). This page is Thurin.id's answer, including what we have not solved.

## The short version

Your claim lives in a contract on Ethereum that nobody controls: no owner, no admin, no pause, no fees, no upgrades. Everything Thurin Labs runs is a convenience on top of it, and each one can be replaced by something you run yourself. If Thurin Labs disappeared tomorrow, every claim would still be readable from any Ethereum node and checkable with gpg.

## Censorship resistance

**Who could block you:** our web server, our relay, our keyserver, and the public Ethereum node the site reads from by default. All of them run on one server we operate.

**Why it doesn't matter much:** none of them is needed. The [registry](/contracts) at `0xFa6956c11163517249f8A67F5560a4406B519451` takes claims from anyone, directly, and you can use it with only Etherscan or `cast` and gpg.

**Your way around us:**
- Publish from any wallet, or from a terminal with the [CLI](/cli); the relay is only there if you want someone else to pay.
- Read through your own node: the thurin.id footer lets you change it, and the CLI takes `--rpc`.
- Run your own keyserver (`thurin keyserver`) or relay (`thurin relay`).
- Open the sites through ENS (`id.thurinlabs.eth`, `thurinlabs.eth`) if thurin.id is down.

## Open source and free

**Everything that runs Thurin.id is public:** the contract (verified on Etherscan), the library, the CLI, the sites, the share-card service. MIT license, docs Apache-2.0. Fork it, run it, change it; no permission needed.

**You can check that what runs is what's published:**
- Every site deploy is a signed `deploy-…` tag in that site's repository, naming the IPFS content it put live. thurin.id also shows its commit in the page source.
- Every CLI release since 0.5.1 is signed with the company key, and from 0.13.0 on it is also named on-chain from thurinlabs.eth ([how to check](/guides/verify-release)). Library releases are signed git tags from 1.3.2 on, and the library refuses to publish from uncommitted code.
- Scripts are served by the sites themselves, never pulled from a CDN at view time.

**Rebuild it yourself:** every site rebuilds from its deploy tag to the identical content ID, which we've checked for all four and for Node 20, 22, and 24. The steps: [Verify a deploy](/guides/verify-deploy).

## Privacy

**What is public, forever:** your claim. Your Ethereum address, your PGP key with the names on it, the proofs you chose to add, any records you set, and when. That is the product, and the attest page shows you exactly what will be published before you publish it. Email addresses stay off the key and out of the signature by default. Replacing the key or clearing a record doesn't erase the old one: the chain keeps its history.

**What Thurin Labs learns about you:** nothing we keep.
- No accounts, no cookies, no analytics, no telemetry.
- Our servers keep no access logs. The keyserver and relay record no IP addresses; the keyserver's log never says what was looked up. A failed web request can leave one line in an error log, which is deleted after two weeks.
- The pages are fetched from IPFS through our server, which tells the IPFS gateway nothing about you.
- Our pages tell outside services nothing about which page asked (no referrer).
- Nothing is sent to WalletConnect unless you choose to connect a phone wallet.

**Who else your browser talks to**, and what they see (your IP, and which identity you looked at):
- An Ethereum node, on every lookup. By default PublicNode (`ethereum.publicnode.com`), which needs no key. Change it in the thurin.id footer; the choice stays in your browser.
- The platforms behind each proof, **only when you press Check proofs**: GitHub, Codeberg, Cloudflare's DNS resolver, a public Farcaster node (Quilibrium's, by default), and the Mastodon server named in the proof, which the identity's owner picks. "Always check" in the footer turns that on for every page, in your browser only.
- For profile pictures: euc.li (where the ENS app stores avatars), an IPFS gateway (Filebase, with Pinata's as a fallback), or arweave.net. Never a server the name's owner picked, so they can't see who looks.
- For an ENS name that keeps its data on its owner's server (an "offchain" name): that server, but only when you typed the name yourself.

Links to Etherscan, the ENS app, and EFP contact nothing until you click them. Card images are drawn by our server, so a README or page showing one asks no one else.

**If that is too much:** use the CLI against your own node, with `thurin status --no-proofs` to ask nothing else. A mode that sends everything over Tor is [planned](/roadmap).

Details: [privacy policy](https://thurinlabs.id/privacy/).

## Security

**What we can't do to you:** the contract has no admin. We can't change, freeze, or delete your claim, and no one can move funds through it; it holds none.

**What could go wrong, and what we do about it:**
- *Someone steals your Ethereum key or ENS name.* They could replace the key on your claim or revoke it, even as compromised, and so could you: it becomes a race. Keep the Ethereum key on hardware. If it leaks, claim your key again from a fresh address; your PGP key is unaffected, and a "compromised" mark on the old address doesn't follow it.
- *Someone steals your PGP key.* Revoke the claim as compromised, or replace it with a new key and mark the old one in the same transaction. Once marked, that address can never claim the key again.
- *The Ethereum node lies to the page.* A dishonest node could show a claim that isn't there. Use a node you trust for anything that matters; the CLI works against your own.
- *Our relay's wallet.* It pays gas unattended, capped at a small daily budget. It can't touch your claim.
- *A bad release or deploy.* Releases and deploys are signed and tied to public commits, and the library won't publish from uncommitted code. Check before you trust ([how](/guides/verify-release)).

**The contract review:** before launch the registry had three adversarial reviews, each by an agent that didn't write the code. The last one checked every write path against an independent model of the rules, over hundreds of thousands of random calls. Every finding was fixed before mainnet. This was not a third-party audit.

**If everything we run disappears:** your claim stays readable from any Ethereum node, gpg still verifies every signature, the code is mirrored on Codeberg, and the CLI runs against any node. There is nothing to migrate.

## What we accept

- Claims are public by design. The fix is choosing what to publish, not hiding it.
- One person runs the hosted pieces on one server. Each has a do-it-yourself path, and the contract needs none of them.
- Checking a proof means asking the platform it points at.
- A public Ethereum node sees what you look up unless you pick your own.

Found something we got wrong? Contact details are on [thurinlabs.eth's claim](https://thurin.id/ens/thurinlabs.eth/records) (the `security` record).
