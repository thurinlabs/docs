# Identity Kit

The library behind thurin.id, the CLI, and the share cards: it reads claims from the registry, checks them with openpgp.js, and checks the proofs on the key. One core, so "verified" means the same thing everywhere.

**npm:** [`@thurinlabs/identity-kit`](https://www.npmjs.com/package/@thurinlabs/identity-kit) · **Source:** [GitHub](https://github.com/thurinlabs/identity-kit)

```bash
npm install @thurinlabs/identity-kit
```

Two entry points:

- `@thurinlabs/identity-kit`: React hooks and their provider, plus everything in core. Peer dependencies: `react`, `react-dom`, `wagmi`, `viem`, `@tanstack/react-query`.
- `@thurinlabs/identity-kit/core`: plain functions, no React. For Node, workers, and your own UI.

## React

Wrap your app in the provider, then use the hooks below:

```tsx
import { IdentityKitProvider, useThurinIdentity } from '@thurinlabs/identity-kit'

<IdentityKitProvider>
  <YourApp />
</IdentityKitProvider>
```

`IdentityKitProvider` works with no props: it reads through a keyless public node. If your app already has a `WagmiProvider`, it uses that.

| Prop | Default | |
|---|---|---|
| `rpcUrl` | `https://ethereum.publicnode.com` | any Ethereum RPC; reads are plain `eth_call` |
| `network` | `mainnet` | `mainnet`, `sepolia`, or `local` (anvil, chain 31337) |
| `registryAddress` | `REGISTRY_ADDRESS` | override, e.g. a local deploy that landed elsewhere |
| `farcasterHub` | `https://haatz.quilibrium.com` | Farcaster node for Farcaster proofs (keyless) |
| `neynarApiKey` | none | read Farcaster through Neynar instead |

## Hooks

```tsx
const id = useThurinIdentity('thurinlabs.eth')   // or an address
// id.address, ensName, ensAvatar, claims, totalClaims, activeClaims,
// currentFingerprint, pgpKeyInfo, proofs, isLoading, error, errorKind, retry()
```

`currentFingerprint` is the newest active claim whose signature verifies. Nothing from an unverified claim (proofs, names) is shown.

| Hook | Returns |
|---|---|
| `useAttestations(address)` | `claims`, `totalClaims`, `activeClaims`, `currentFingerprint`, `isLoading`, `error`, `refetch` |
| `usePGPProofs(fingerprint, armoredKey)` | `keyInfo`, `proofs` (each with `status`: verified, unverified, pending, skipped) |
| `useRecords(address, index, kinds?, armoredKey?)` | `records` (parsed), `isLoading`, `refetch` |
| `useEnsHint(name, fingerprint)` | the name's `id.thurin` record against the key: `match`, `unset`, or `mismatch` |
| `useSafeAvatar(name, chainId)` | an avatar URL that can't reveal the viewer to the name's owner, or null |

`ensAvatar` and `useSafeAvatar` only return avatars on IPFS, Arweave, inline data, a content-addressed NFT, or `euc.li` (where the ENS app stores uploads). An avatar on the owner's own server would hand it every viewer's IP, so it's left out.

## Reading claims yourself

```ts
import { createPublicClient, http } from 'viem'
import { mainnet } from 'viem/chains'
import { REGISTRY_ADDRESS, REGISTRY_ABI, bytesToFingerprint, payloadText, verifyAttestation } from '@thurinlabs/identity-kit/core'

const client = createPublicClient({ chain: mainnet, transport: http('https://ethereum.publicnode.com') })
const owner = '0xYourAddress' as `0x${string}`

const claims = await client.readContract({ address: REGISTRY_ADDRESS, abi: REGISTRY_ABI, functionName: 'claimsOf', args: [owner] })
for (const c of claims) {
  const key = await client.readContract({ address: REGISTRY_ADDRESS, abi: REGISTRY_ABI, functionName: 'keyBytes', args: [owner, c.index] })
  const sig = await client.readContract({ address: REGISTRY_ADDRESS, abi: REGISTRY_ABI, functionName: 'signatureBytes', args: [owner, c.index] })
  const v = await verifyAttestation({ pgpPublicKey: key, pgpSignature: sig, fingerprint: bytesToFingerprint(c.fingerprint), ethAddress: owner })
  console.log(c.index, c.state, c.revokeReason, v.verified ? 'verified' : v.kind)
}
const armored = await payloadText(await client.readContract({ address: REGISTRY_ADDRESS, abi: REGISTRY_ABI, functionName: 'keyBytes', args: [owner, 0n] }), 'key')
```

`REGISTRY_ADDRESS` is the same on Ethereum mainnet and Sepolia (`NETWORKS` has each network's chain id, explorer, and default RPC; `getRegistry(network)` picks one). `REGISTRY_ABI` is the whole contract, writes included. The functions themselves are on the [contract page](/contracts).

`verifyAttestation` takes the key and signature as the registry stores them (raw bytes) or as armored text. It checks that the key has the claimed fingerprint, that the signature is over exactly `I control the Ethereum address: <lowercase address>`, and that the key is valid today, as gpg judges it. `kind` says why a claim doesn't count: `expired`, `signing-key-expired`, `revoked`, `compromised`, `signing-key-revoked`, `unsupported` (e.g. DSA), or `bad-signature`. Show people words, not the raw `reason`:

```ts
import { claimCheckText, expiresSoon, expiresSoonText, claimFates, claimFateText } from '@thurinlabs/identity-kit/core'

claimCheckText(v)        // { label, sentence, fix }; show `fix` to the owner only
const soon = expiresSoon(v)
if (soon) expiresSoonText(soon)   // 'Key expires in 12 days (Mar 6, 2027).'

const fates = claimFates(claims)                  // `claims` from useAttestations, keyed by index
claimFateText(fates.get(0)!)                      // 'Replaced by claim #1 on Oct 3, 2026.'
```

A fate is `active`, `revoked` (with the owner's reason), or `replaced` (by a reattest, with the new index). A replaced claim whose key was later marked compromised says so.

**Is this key compromised?** Ask the contract: `keyStatus(owner, fingerprint)` returns `none`, `active`, `revoked`, or `compromised`. Don't infer it from the newest claim: a key can be marked compromised on an older claim while a newer one keeps its own reason. And it is per owner. Anyone can post a claim on any fingerprint and mark it compromised under their own address, so never count "compromised" across all owners of a key.

## Proofs

```ts
import { identifyProof, verifyProof, displayUrl, proofHref } from '@thurinlabs/identity-kit/core'

const proof = identifyProof({ name: 'proof@thurin.id', value: 'https://gist.github.com/alice/abc123' })
if (proof) {
  const result = await verifyProof(proof, fingerprint, { farcasterHub })   // options optional
  // { verified, reason? }
}
```

Each provider has its own check. GitHub gists and repositories, and Codeberg repositories, must belong to the account in the URL, so pointing at someone else's doesn't work. The providers and what each checks: [Proofs](/guides/proofs).

## Records

```ts
import { REGISTRY_ADDRESS, REGISTRY_ABI, kindName, pickRecords, parseRecord } from '@thurinlabs/identity-kit/core'

kindName('security')   // 'thurin.security'; a name without a dot gets thurin. in front
const [names, values] = await client.readContract({ address: REGISTRY_ADDRESS, abi: REGISTRY_ABI, functionName: 'recordsOf', args: [owner, 0n] })
for (const r of pickRecords(names, values)) {
  const rec = await parseRecord(r.kind, r.text, { armoredKey: armored ?? undefined })
  // { kind, text, bytes, valid, reason?, data }
}
```

`pickRecords` keeps the `thurin.` kinds in display order; pass `null` as a third argument for every record. `parseRecord` never throws: a value that doesn't fit its kind comes back `valid: false` with a reason, and is still shown. With `armoredKey`, a clearsigned canary is checked against the claim's key. `pageRecords(names, values)` is the order an identity page uses: Thurin's kinds first, then anyone else's. `checkKindName` and `checkRecordValue` apply the registry's limits before you spend gas. `parseReleases`, `addRelease`, and `renderReleases` handle `thurin.releases`, a release list. The kinds: [Records](/records).

## Writing by permission

Every owner write has a `…For` form that anyone can submit with the owner's EIP-712 signature. These build the typed data for viem's `signTypedData`:

```ts
import { attestTypedData, revokeTypedData, markCompromisedTypedData } from '@thurinlabs/identity-kit/core'

const nonce = await client.readContract({ address: REGISTRY_ADDRESS, abi: REGISTRY_ABI, functionName: 'nonces', args: [owner] })
const typed = revokeTypedData(1, REGISTRY_ADDRESS, { owner, index: 0n, reason: 'retired', nonce, deadline })
const permission = await wallet.signTypedData({ account: owner, ...typed })
// anyone: revokeFor(owner, 0n, 'retired', deadline, permission)
```

Also `reattestTypedData`, `updateKeyTypedData`, `setRecordTypedData`. A `Revoke` permission only revokes an active claim; to mark a claim that's already revoked or replaced as compromised, sign `markCompromisedTypedData` alone. `OWNER_REVOKE_REASONS` is what an owner can pick (`superseded` comes only from a reattest).

## ENS record

```ts
import { fetchEnsHint, ensHintWrite } from '@thurinlabs/identity-kit/core'

const hint = await fetchEnsHint(client, 'ben.thurinlabs.eth', verifiedFingerprint)   // { state: 'match' | 'unset' | 'mismatch', record, expected, reason? }
const call = ensHintWrite('ben.thurinlabs.eth', verifiedFingerprint)                 // setText(node, 'id.thurin', FPR); look the resolver up at write time
```

See [Point your ENS name at your claim](/guides/ens-record).

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
