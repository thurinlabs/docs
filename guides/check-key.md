# Check a key before you encrypt to it

Your page ships a PGP key so visitors can encrypt to you. Whoever controls your server can swap that key for their own, and every message after that is theirs to read. Check the key against its owner's claim on Ethereum first: a swapped key won't match, and the page refuses to encrypt.

<iframe src="demo/check-key.html" title="Check a key: live demo" style="width: 100%; height: 420px; border: 1px solid var(--sidebar-border-color, #3a3a2c); border-radius: 6px;"></iframe>

Try it: **Real key** is thurinlabs.eth's key as [claimed](https://thurin.id/ens/thurinlabs.eth/claims); **Swapped key** is a throwaway key standing in for a swap. Or paste your own key and name. [Open the demo on its own page](demo/check-key.html ':ignore') to read its source: it's the whole integration.

## Add it to a page

For a site with no build step. Copy two files next to your other scripts (see [Get the file](/guides/check-key?id=get-the-file)), then load the check:

```html
<script src="js/thurin-check.js"></script>
```

Say whose key each recipient's is. Recipients without an owner work exactly as before:

```js
const owners = { security: 'security.example.eth', legal: '0x1234…abcd' }   // an ENS name or an address
```

Before encrypting:

```js
const owner = owners[recipient]
if (owner) {
  const r = await ThurinCheck.checkKeyFor({ key: armoredKey, owner })
  if (r.status === 'mismatch') throw new Error(r.reason)   // never encrypt to it
  showStatus(r)                                           // r.reason is one sentence, ready to show
}
// your encryption continues unchanged
```

| `status` | Means | The page |
|---|---|---|
| `verified` | The key matches an active, verified claim by the owner | Show it: "Key verified on Ethereum" |
| `mismatch` | The owner's verified key is another one, the owner revoked this one, or it isn't a key | Refuse to encrypt |
| `unverified` | Nothing verified to compare with: no claim, a claim that doesn't verify, a name with no address | Carry on as without the check |
| `unreachable` | The Ethereum node couldn't be asked | Warn, or refuse if you'd rather |

The answer also carries both fingerprints (`fingerprint`, `claimedFingerprint`), so a mismatch can show what the key should be. Any active, verified claim counts, not only the newest: an owner moving to a new key can keep the old one claimed until your page catches up.

## With a build step, or in Node

The same check is in the kit, with your own [viem](https://viem.sh) client:

```ts
import { checkKeyFor } from '@thurinlabs/identity-kit'

const r = await checkKeyFor(client, { key: armoredKey, owner: 'security.example.eth' })
```

Useful in a build step too: fail the deploy if a bundled key doesn't match.

## What it protects against

- **A swapped key file.** A bad commit, a bad deploy, or someone who can change files on the server but not the owner's claim. The owner's claim can only be written with the owner's Ethereum key.
- **A revoked key.** If the owner revokes the key (lost, retired, compromised), pages still shipping it refuse it.

What it doesn't:

- **A server that serves its own JavaScript.** Whoever can change your scripts can remove the check. The fix for that is a content-addressed site (IPFS + an ENS contenthash, as [thurin.id](https://thurin.id) is served) or a build anyone can verify: see [Verify a deploy](/guides/verify-deploy).
- **Recipients without a claim.** The check only protects keys that have been [claimed](/guides/getting-started). No ETH needed: the relay can pay for the claim.
- **Metadata.** Who writes to whom, and when, is outside the check.

The registry doesn't read PGP. The check does the full verification in the browser: the claim's signature, the key's validity, and the match. "Has a claim" is never enough.

## Which node, and what it sees

The check asks an Ethereum node about the owner, so the node sees which recipient a visitor picked. With no `rpc` it uses a public node (`ethereum.publicnode.com`); pass your own to keep that to yourself:

```js
ThurinCheck.checkKeyFor({ key, owner, rpc: 'https://your-node.example' })
```

- **Content-Security-Policy:** allow the node's host in `connect-src`.
- **Testing on Sepolia:** add `network: 'sepolia'`. Sepolia has its own ENS, so give owners as addresses there.
- **When it runs:** only when your page calls it. Nothing is fetched when the script loads.

## Get the file

`thurin-check.js` comes with each [kit release](https://github.com/thurinlabs/identity-kit/releases), next to `thurin-check.LICENSES.txt` and a `SHA256SUMS` signed by thurinlabs.eth's key and named on-chain: check it as in [Verify a release](/guides/verify-release). Copy both files into your site rather than loading them from someone else's server. The file bundles [OpenPGP.js](https://openpgpjs.org) (LGPL-3.0) and MIT packages, and the licenses travel with it.

```bash
sha256sum -c SHA256SUMS --ignore-missing   # in the folder with the files you downloaded
```

It isn't minified, so you can read what you ship: each part is labelled with the package it comes from. It's about 316 KB gzipped, most of it OpenPGP.js. It's also in the npm package at `dist/thurin-check.js`, or build it yourself from the release's tag with `npm ci && npm run build`; it should match the release.
