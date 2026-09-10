# PGPRegistry Contract

The `PGPRegistry` contract stores on-chain PGP-to-Ethereum identity claims created via [thurin.id/attest](https://thurin.id/attest).

## Contract Details

| Item | Value |
|------|-------|
| Network | Ethereum Mainnet |
| Address | [`0xf7a45BC662A78a6fb417ED5f52b3766cbf13EbBb`](https://etherscan.io/address/0xf7a45BC662A78a6fb417ED5f52b3766cbf13EbBb) |
| Deploy Block | 24515891 |
| Source | [github.com/thurinlabs/pgp-registry](https://github.com/thurinlabs/pgp-registry) |

## Functions

### `attestationCount(address)`

Returns the number of attestations for an address.

```solidity
function attestationCount(address addr) external view returns (uint256)
```

### `getAttestation(address, uint256)`

Returns attestation details by index.

```solidity
function getAttestation(address addr, uint256 index)
  external view returns (string fingerprint, uint256 createdAt, bool revoked)
```

### `Attested` Event

Emitted when a new attestation is created.

```solidity
event Attested(
  address indexed ethAddress,
  string indexed fingerprintHash,
  string fingerprint,
  string pgpSignature,
  string pgpPublicKey,
  uint256 index,
  uint256 timestamp
)
```

## Reading from JavaScript

Use the [`@thurinlabs/identity-kit`](/sdk) SDK for the easiest integration, or read directly with viem:

```typescript
import { createPublicClient, http } from 'viem'
import { mainnet } from 'viem/chains'

const client = createPublicClient({
  chain: mainnet,
  transport: http(),
})

const count = await client.readContract({
  address: '0xf7a45BC662A78a6fb417ED5f52b3766cbf13EbBb',
  abi: [/* see identity-kit source for full ABI */],
  functionName: 'attestationCount',
  args: ['0xYourAddress'],
})
```
