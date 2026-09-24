# Identity Kit

React SDK for embedding Thurin identity data. Drop-in components and hooks for displaying on-chain identity claims, PGP verification, social proofs, and EFP social graph data.

**npm:** [`@thurinlabs/identity-kit`](https://www.npmjs.com/package/@thurinlabs/identity-kit)
**Source:** [GitHub](https://github.com/thurinlabs/identity-kit)

## Install

```bash
npm install @thurinlabs/identity-kit
```

Peer dependencies: `react`, `react-dom`, `wagmi`, `viem`, `@tanstack/react-query`

## Quick Start

```tsx
import { IdentityKitProvider, ThurinCard } from '@thurinlabs/identity-kit'
import '@thurinlabs/identity-kit/styles'

function App() {
  return (
    <IdentityKitProvider>
      <ThurinCard ens="vitalik.eth" theme="thurin" />
    </IdentityKitProvider>
  )
}
```

## ThurinCard

A self-contained identity card that fetches and displays all available identity data.

```tsx
<ThurinCard ens="vitalik.eth" theme="thurin" />
<ThurinCard address="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" theme="dark" />
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `ens` | `string` | — | ENS name to look up |
| `address` | `string` | — | ETH address to look up |
| `theme` | `'thurin' \| 'dark' \| 'light'` | `'thurin'` | Visual theme |

Displays: ENS avatar, name, address, on-chain attestation count, verified proof count, EFP follower count, proof provider badges, and a link to the full Thurin profile.

## Provider

Wrap your app (or just the part using identity-kit) in `IdentityKitProvider`. If you already have a `WagmiProvider`, the SDK detects it and uses your existing config.

```tsx
// Zero config — uses public RPC, no Farcaster verification
<IdentityKitProvider>
  <ThurinCard ens="vitalik.eth" />
</IdentityKitProvider>

// With options
<IdentityKitProvider
  rpcUrl="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
  neynarApiKey="YOUR_NEYNAR_KEY"
  baseUrl="https://thurin.id"
>
  <ThurinCard ens="vitalik.eth" />
</IdentityKitProvider>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `rpcUrl` | `string` | publicnode | Ethereum RPC endpoint |
| `neynarApiKey` | `string` | — | Neynar API key for Farcaster proof verification |
| `network` | `'mainnet' \| 'sepolia' \| 'local'` | `'mainnet'` | Which chain to read the registry on |
| `baseUrl` | `string` | `https://thurin.id` | Base URL for "View on Thurin" links |

## Hooks

For custom UI, use the hooks directly instead of `ThurinCard`.

### useThurinIdentity

Combined identity data — ENS, on-chain attestations, PGP proofs, and EFP social graph.

```tsx
const identity = useThurinIdentity('vitalik.eth')
// or
const identity = useThurinIdentity('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045')
```

Returns `ThurinIdentity` with `address`, `ensName`, `ensAvatar`, `claims`, `totalClaims`, `activeClaims`, `currentFingerprint`, `pgpKeyInfo`, `proofs`, `efp`, `isLoading`, `error`.

`ensAvatar` is set only when loading it can't show the viewer to the name's owner: IPFS, Arweave, inline data, a content-addressed NFT, or `euc.li` (where the ENS app stores uploaded avatars). An avatar on the owner's own server is left out, since loading it would hand that server every viewer's IP. The rule is `avatarUrl()` in `@thurinlabs/identity-kit/core` (1.3.3).

### useAttestations

On-chain attestation data from the PGPRegistry contract.

```tsx
const { claims, totalClaims, activeClaims, currentFingerprint, isLoading } =
  useAttestations('0xd8dA...')
```

### useEFPGraph

EFP (Ethereum Follow Protocol) social graph data.

```tsx
const { efp, isLoading } = useEFPGraph('0xd8dA...')
// efp.followers, efp.following, efp.top8, efp.hasEfp
```

### usePGPProofs

PGP key info and verified social proofs, parsed from the key stored in the on-chain attestation. No keyserver is consulted.

```tsx
const { keyInfo, proofs, isLoading } = usePGPProofs(fingerprint, attestation.pgpPublicKey)
// proofs[].provider, proofs[].status, proofs[].displayUrl
```

### useEnsHint

```tsx
const { state, record, reason, isLoading } = useEnsHint('ben.thurinlabs.eth', identity.currentFingerprint)
```

The name's `id.thurin` text record against the key the registry verifies for its address: `match`, `unset`, or `mismatch` with a `reason`. See [Point your ENS name at your claim](/guides/ens-record).

## Core Utilities

The verification and data logic is also exported as plain framework-agnostic functions — no React, no provider. This is the layer the `ThurinCard`, the hooks, and the thurin.id explorer all build on, so a "verified" result is consistent everywhere. Use it directly when you need the validated data behind your own UI.

### Proofs

```ts
import { identifyProof, verifyProof, displayUrl, proofHref } from '@thurinlabs/identity-kit'

const proof = identifyProof({ name: 'proof@thurin.id', value: 'https://gist.github.com/alice/abc123' })
const result = await verifyProof(proof, fingerprint, neynarApiKey) // neynarApiKey only for Farcaster
// → { verified: boolean, reason?: string }
```

`verifyProof` runs the real per-provider check — for GitHub it confirms the gist is **owned** by the claimed user, so a proof can't be forged by pointing at someone else's gist.

### PGP

```ts
import { parsePgpKey, verifyAttestation } from '@thurinlabs/identity-kit'

const keyInfo = await parsePgpKey(armoredKey)
// → { fingerprint, userIDs, algorithm, created, expires, notations, subkeys } | null

const verification = await verifyAttestation({ pgpPublicKey, pgpSignature, fingerprint, ethAddress })
// → { verified: boolean, reason?: string }
```

### EFP

```ts
import { fetchEFPGraph } from '@thurinlabs/identity-kit'

const graph = await fetchEFPGraph(address)
// → { followers, following, top8: string[], hasEfp } | null
```

### ENS record

```ts
import { fetchEnsHint, ensHintFor, ensHintWrite, ENS_HINT_KEY } from '@thurinlabs/identity-kit/core'

const hint = await fetchEnsHint(publicClient, name, verifiedFingerprint)   // { state, record, fingerprint, expected, reason? }
const call = ensHintWrite(name, verifiedFingerprint)                        // the setText call; look the resolver up at write time
```

### Contract constants

```ts
import { REGISTRY_ADDRESS, REGISTRY_ABI, CONTRACT_DEPLOY_BLOCK } from '@thurinlabs/identity-kit'
```

`REGISTRY_ABI` is read-only (events + `attestationCount` + `getAttestation`). Apps that write claims need their own ABI with `attest`/`revoke`.

## Key algorithms

Any curve openpgp.js can compute is verified: Ed25519, Cv25519, NIST P-256/384/521, brainpool, RSA, and secp256k1. openpgp.js rejects secp256k1 by default because RFC 9580 does not list it; identity-kit removes secp256k1 from that list and leaves the rest of it alone (1.3.2). A secp256k1 PGP key doubles as an Ethereum key (the address is derived from the same public point), so anything that can sign with the PGP key can sign Ethereum transactions. Hold one if you like; do not fund its derived address.

## Themes

Three built-in themes: `thurin`, `dark`, `light`. All styles are scoped under `[data-thurin-theme]` with `thurin-` prefixed class names to avoid conflicts with your app's styles.

Import styles when using `ThurinCard`:

```tsx
import '@thurinlabs/identity-kit/styles'
```

Hooks-only consumers don't need to import styles.

## Embed (No React Required)

For static sites, Jekyll blogs, WordPress, or any HTML page — use the standalone embed script. Everything runs client-side; there's no Thurin backend in the path.

```html
<div
  data-thurin-card="bendoubleu.eth"
  data-theme="thurin"
  data-rpc-url="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
></div>

<script src="https://cdn.jsdelivr.net/npm/@thurinlabs/identity-kit@1/dist/embed.global.js"></script>
```

| Attribute | Description |
|-----------|-------------|
| `data-thurin-card` | ENS name or ETH address to look up (required) |
| `data-theme` | `thurin`, `dark`, or `light` (default: `thurin`). Change it after render and the card follows, so a page with a theme switch can keep the card in step. |
| `data-rpc-url` | Optional. Any Ethereum RPC — the card reads the v2 registry with plain calls, so the keyless public default works. |
| `data-neynar-key` | Optional. A [Neynar](https://neynar.com) API key, only to verify Farcaster proofs. Without it, Farcaster shows as unverified. |
| `data-base-url` | Optional. Where the card's "View on Thurin" link points (default `https://thurin.id`). A page served from ENS can pass its own name so the link stays on ENS. |

The card talks directly to Ethereum and each proof platform — no intermediary, no keyserver. Cards render automatically on page load and for dynamically added elements.

## Card Image (No JavaScript Required)

For places where scripts can't run — GitHub READMEs, forum posts, emails — embed a server-rendered PNG identity card instead. Cards are 640×200, generated on the fly, and cached for an hour.

```
https://thurin.id/card/ens/:name
https://thurin.id/card/eth/:address
https://thurin.id/card/pgp/:fingerprint
```

A trailing `.png` on the identifier is accepted, which helps platforms that expect an image extension:

```markdown
[![Thurin identity](https://thurin.id/card/ens/bendoubleu.eth.png)](https://thurin.id/ens/bendoubleu.eth)
```

| Route | Looks up by |
|-------|-------------|
| `/card/ens/:name` | ENS name |
| `/card/eth/:address` | ETH address |
| `/card/pgp/:fingerprint` | PGP fingerprint |

The card shows the ENS avatar and name, address, on-chain attestation count, verified proof count, and EFP follower count — the same live data as `ThurinCard`. Full-size 1200×630 share cards are also available at the matching `/og/ens/:name`, `/og/eth/:address`, and `/og/pgp/:fingerprint` routes; those are what social platforms receive automatically when a Thurin link is shared, so you rarely need to link them directly.
