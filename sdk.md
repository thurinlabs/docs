# Identity Kit

The library behind thurin.id, the CLI, and the share cards: it reads claims from the registry, checks them with openpgp.js, and checks the proofs on the key. One core, so "verified" means the same thing everywhere.

**npm:** [`@thurinlabs/identity-kit`](https://www.npmjs.com/package/@thurinlabs/identity-kit) · **Source:** [GitHub](https://github.com/thurinlabs/identity-kit)

```bash
npm install @thurinlabs/identity-kit
```

Runs in Node, workers, and browsers; the only peer dependency is `viem`. `@thurinlabs/identity-kit/core` is the same entry.

## Read an address

```ts
import { createPublicClient, http } from 'viem'
import { mainnet } from 'viem/chains'
import { readClaims, keyStanding } from '@thurinlabs/identity-kit'

const client = createPublicClient({ chain: mainnet, transport: http('https://ethereum.publicnode.com'), batch: { multicall: true } })
const owner = '0x539C7e1E454296Dc150B95a0acCC05bCa3b33538'

const claims = await readClaims(client, owner)
const { kind, claim } = keyStanding(claims)
```

`readClaims` returns every claim, oldest first: `index`, `fingerprint` (lowercase), `createdAt`, `state`, `revokeReason`, `replacedBy`, the armored `pgpPublicKey` and `pgpSignature`, and `verification`. It reads and verifies the newest 50 (`{ limit }` changes that); older claims come back with `verification: null`, because an address can hold 65,535 claims and each one checked costs two reads and a signature check. `batch: { multicall: true }` turns the reads into one request.

`keyStanding` says where the key stands:

| `kind` | `claim` |
|---|---|
| `verified` | the newest active claim that verifies: show its key |
| `not-counted` | the newest active claim; none verify, and its `verification` says why |
| `inactive` | the newest claim; every claim has ended |
| `none` | `null`; the address never claimed a key |

Nothing from a claim that doesn't verify (its proofs, its names) should be shown: the stored key isn't the owner's until its signature binds it to the address.

`findOwners(client, { fingerprint })` or `{ keyId }` goes the other way: every address that ever claimed the key, each with the fingerprint it claimed (a key ID can match more than one key). ENS is up to you: resolve the name with viem first.

In React, wrap it in whatever you use for data:

```tsx
const { data: claims } = useQuery({ queryKey: ['claims', owner], queryFn: () => readClaims(client, owner) })
```

**Avatars:** `avatarUrl` and `avatarFallbacks` only return avatars on IPFS, Arweave, inline data, a content-addressed NFT, or `euc.li` (where the ENS app stores uploads). An avatar on the owner's own server would hand it every viewer's IP, so it's left out.

`REGISTRY_ADDRESS` is the same on Ethereum mainnet and Sepolia (`NETWORKS` has each network's chain id, explorer, and default RPC; `getRegistry(network)` picks one). `REGISTRY_ABI` is the whole contract, writes included. The functions themselves are on the [contract page](/contracts).

`readClaims` calls `verifyAttestation`, which you can also call yourself; it takes the key and signature as the registry stores them (raw bytes) or as armored text. It checks that the key has the claimed fingerprint, that the signature is over exactly `I control the Ethereum address: <lowercase address>`, and that the key is valid today, as gpg judges it. `kind` says why a claim doesn't count: `expired`, `signing-key-expired`, `revoked`, `compromised`, `signing-key-revoked`, `unsupported` (e.g. DSA), or `bad-signature`. Show people words, not the raw `reason`:

```ts
import { claimCheckText, expiresSoon, expiresSoonText, claimFates, claimFateText } from '@thurinlabs/identity-kit'

const v = claim.verification
claimCheckText(v)        // { label, sentence, fix }; show `fix` to the owner only
const soon = expiresSoon(v)
if (soon) expiresSoonText(soon)   // 'Key expires in 12 days (Mar 6, 2027).'

const fates = claimFates(claims)                  // `claims` from readClaims, keyed by index
claimFateText(fates.get(0)!)                      // 'Replaced by claim #1 on Oct 3, 2026.'
```

A fate is `active`, `revoked` (with the owner's reason), or `replaced` (by a reattest, with the new index). A replaced claim whose key was later marked compromised says so.

**Is this key compromised?** Ask the contract: `keyStatus(owner, fingerprint)` returns `none`, `active`, `revoked`, or `compromised`. Don't infer it from the newest claim: a key can be marked compromised on an older claim while a newer one keeps its own reason. And it is per owner. Anyone can post a claim on any fingerprint and mark it compromised under their own address, so never count "compromised" across all owners of a key.

## Proofs

```ts
import { identifyProof, verifyProof, displayUrl, proofHref } from '@thurinlabs/identity-kit'

const proof = identifyProof({ name: 'proof@thurin.id', value: 'https://gist.github.com/alice/abc123' })
if (proof) {
  const result = await verifyProof(proof, fingerprint, { farcasterHub })   // options optional
  // { verified, reason? }
}
```

Each provider has its own check. GitHub gists and repositories, and Codeberg repositories, must belong to the account in the URL, so pointing at someone else's doesn't work. The providers and what each checks: [Proofs](/guides/proofs).

## Records

```ts
import { REGISTRY_ADDRESS, REGISTRY_ABI, kindName, pickRecords, parseRecord } from '@thurinlabs/identity-kit'

kindName('security')   // 'thurin.security'; a name without a dot gets thurin. in front
const [names, values] = await client.readContract({ address: REGISTRY_ADDRESS, abi: REGISTRY_ABI, functionName: 'recordsOf', args: [owner, 0n] })
for (const r of pickRecords(names, values)) {
  const rec = await parseRecord(r.kind, r.text, { armoredKey: claim.pgpPublicKey ?? undefined })
  // { kind, text, bytes, valid, reason?, data }
}
```

`pickRecords` keeps the `thurin.` kinds in display order; pass `null` as a third argument for every record. `parseRecord` never throws: a value that doesn't fit its kind comes back `valid: false` with a reason, and is still shown. With `armoredKey`, a clearsigned canary is checked against the claim's key. `pageRecords(names, values)` is the order an identity page uses: Thurin's kinds first, then anyone else's. `checkKindName` and `checkRecordValue` apply the registry's limits before you spend gas. `parseReleases`, `addRelease`, and `renderReleases` handle `thurin.releases`, a release list. The kinds: [Records](/records).

## Writing by permission

Every owner write has a `…For` form that anyone can submit with the owner's EIP-712 signature. These build the typed data for viem's `signTypedData`:

```ts
import { attestTypedData, revokeTypedData, markCompromisedTypedData } from '@thurinlabs/identity-kit'

const nonce = await client.readContract({ address: REGISTRY_ADDRESS, abi: REGISTRY_ABI, functionName: 'nonces', args: [owner] })
const typed = revokeTypedData(1, REGISTRY_ADDRESS, { owner, index: 0n, reason: 'retired', nonce, deadline })
const permission = await wallet.signTypedData({ account: owner, ...typed })
// anyone: revokeFor(owner, 0n, 'retired', deadline, permission)
```

Also `reattestTypedData`, `updateKeyTypedData`, `setRecordTypedData`. A `Revoke` permission only revokes an active claim; to mark a claim that's already revoked or replaced as compromised, sign `markCompromisedTypedData` alone. `OWNER_REVOKE_REASONS` is what an owner can pick (`superseded` comes only from a reattest).

## ENS record

```ts
import { fetchEnsHint, ensHintWrite } from '@thurinlabs/identity-kit'

const hint = await fetchEnsHint(client, 'ben.thurinlabs.eth', verifiedFingerprint)   // { state: 'match' | 'unset' | 'mismatch', record, expected, reason? }
const call = ensHintWrite('ben.thurinlabs.eth', verifiedFingerprint)                 // setText(node, 'id.thurin', FPR); look the resolver up at write time
```

See [Point your ENS name at your claim](/guides/ens-record).

## Encrypt

```ts
import { readClaims, encryptionKeyFor, encryptRefusalText, keyChangedText, encryptTo } from '@thurinlabs/identity-kit'

const k = await encryptionKeyFor(await readClaims(client, owner))   // the claim that counts, or a reason
if (!k.ok) throw new Error(encryptRefusalText(k))                   // no claim / unverified / no encryption subkey / expired
const warning = keyChangedText(k)                                   // non-null when the key arrived in the last 7 days
const armored = await encryptTo(k.key, 'meet at noon')              // recipient hidden by default
const bytes = await encryptTo(k.key, fileBytes, { filename: 'report.pdf' })
```

`encryptTo` uses the kit's openpgp settings, so keys on secp256k1 (what a Keycard holds) work too. `{ hideRecipient: false }` names the recipient's key ID. See [Encrypt to an identity](/guides/encrypt).

## Key algorithms

Anything openpgp.js can verify: Ed25519, Cv25519, NIST P-256/384/521, brainpool, RSA, and secp256k1. openpgp.js refuses secp256k1 by default; the kit allows it and nothing else. A secp256k1 PGP key is also an Ethereum key (same public point), so whatever can sign with it can sign transactions. Don't fund its address.

## README card

A 640×200 image of an identity: its name, address, PGP key, and whether the key is verified on Ethereum (or why not). thurin.id's server draws it and caches it for an hour, so showing it makes the reader's browser ask no one else; on GitHub, its image proxy fetches it, so not even thurin.id sees your readers.

```
https://thurin.id/card/ens/:name
https://thurin.id/card/eth/:address
https://thurin.id/card/pgp/:fingerprint
```

A trailing `.png` is accepted, and `?theme=light` draws it in light colours. In a README, this picks the one that matches the reader's GitHub theme:

```html
<a href="https://thurin.id/ens/thurinlabs.eth">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://thurin.id/card/ens/thurinlabs.eth.png">
    <img alt="thurinlabs.eth on Thurin.id" src="https://thurin.id/card/ens/thurinlabs.eth.png?theme=light">
  </picture>
</a>
```

Or just one: `[![Thurin.id](https://thurin.id/card/ens/thurinlabs.eth.png)](https://thurin.id/ens/thurinlabs.eth)`.

The same content at 1200×630, at `/og/ens/:name`, `/og/eth/:address`, and `/og/pgp/:fingerprint`, is what social sites show when a thurin.id link is shared.
