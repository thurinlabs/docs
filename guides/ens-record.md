# Point your ENS name at your claim

An ENS profile lists the accounts a name owns: `com.github`, `com.twitter`, `url`. None of them is checked by anyone. A Thurin claim is the one thing on a profile that can be: the name owner set the address, and the address signed the claim, on-chain.

`id.thurin` is an ENS text record that points a name at that claim. It is a hint for ENS viewers, not a proof. The proof is the claim.

## The record

| key | value |
|---|---|
| `id.thurin` | the fingerprint of the key claimed by the address the name resolves to, 40 hex characters, uppercase, no spaces, no `0x` |

For example, `ben.thurinlabs.eth` carries:

```
id.thurin = 6E0053911942A889426C1866E34D9266098F7FE7
```

`id.thurin` is a service key under [ENSIP-5](https://docs.ens.domains/ensip/5): reverse-dot of the domain that owns it. [ENSIP-18](https://docs.ens.domains/ensip/18) asks that service-key values carry no formatting, so the value is the bare fingerprint. Readers should accept case, spaces, and a `0x` prefix anyway.

## What a reader does

1. Resolve the name to its address.
2. Read the address's current claim from the [registry](/contracts) and verify it, which is what identity-kit, thurin.id, and the CLI already do.
3. Read `id.thurin` and compare.

Three answers:

| state | meaning |
|---|---|
| matches | the record names the verified key. Show it as verified. |
| not set | the name has no record. Nothing is wrong; the claim still stands. |
| points elsewhere | the record names a key the address has not claimed, or is not a fingerprint at all. A signal worth showing. |

The record never adds trust. Step 2 is complete without it. What it adds is a pointer that any ENS viewer can render, the same way it renders `com.github`, so someone looking at a name has a place to go.

## Set it

From [thurin.id](https://thurin.id): open your name. Under the current fingerprint, the line reads `id.thurin not set`. Connect the wallet that manages the name and press **Set it**. One transaction, on the name's own resolver.

From the CLI:

```bash
thurin ens check ben.thurinlabs.eth            # what the record says now
thurin ens link ben.thurinlabs.eth             # set it from the keystore
thurin ens link ben.thurinlabs.eth --calldata  # print the transaction for a wallet elsewhere
```

From the [ENS app](https://app.ens.domains): add a text record with key `id.thurin` and the fingerprint as its value. Check the result with `thurin ens check <name>`.

The transaction must come from an account that may write the name's records: the owner, or a manager. The wallet holding the Thurin claim need not be that account, and often isn't.

## ENSv2

Nothing changes for the record: ENSv2 keeps ENSIP-5 text records as they are. Two notes for anyone writing one:

- ENSv2 gives every account its own resolver. Look the resolver up at write time; never hardcode one. Thurin's tools do.
- Migrating a name from v1 may clear its records. Set `id.thurin` again after migrating.

## Verification badges in ENS apps

There is no ENS-level verification. What a profile shows as verified is a choice each app makes. The ENS manager's "Verifications" button currently reports no providers. An app that wants to show a Thurin claim as verified reads the registry, through [identity-kit](/sdk) or on its own, and `id.thurin` tells it where to look.

## From code

```ts
import { fetchEnsHint, ensHintWrite } from '@thurinlabs/identity-kit/core'

const hint = await fetchEnsHint(publicClient, 'ben.thurinlabs.eth', verifiedFingerprint)
// hint.state: 'match' | 'unset' | 'mismatch'; hint.reason on a mismatch

const call = ensHintWrite('ben.thurinlabs.eth', verifiedFingerprint)   // setText(namehash, 'id.thurin', 'FPR…')
const resolver = await publicClient.getEnsResolver({ name: call.name })
```

React: `useEnsHint(name, fingerprint)` returns the same, live.
