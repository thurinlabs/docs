# PGPRegistry Contract

The `PGPRegistry` contract stores on-chain PGP-to-Ethereum identity claims created at [thurin.id/attest](https://thurin.id/attest). Each claim binds an Ethereum address to a PGP key fingerprint and stores, readably, the clearsigned message that proves key control and the armored public key that carries the owner's proof notations.

This page describes **v2** (2026-09). It is permissionless and immutable: no owner, no admin, no fees, no upgrade path, and no on-chain PGP parsing — verification happens in [identity-kit](/sdk) from the stored data.

## Contract Details

| Item | Value |
|------|-------|
| Address (all networks) | `0x9302E02e2869e129aC8516fE5eFFd51EA3082c09` |
| Ethereum Mainnet | deployed 2026-09-12, block 25962908 ([Etherscan](https://etherscan.io/address/0x9302E02e2869e129aC8516fE5eFFd51EA3082c09)) |
| Sepolia | deployed 2026-09-11, block 11683667 ([Etherscan](https://sepolia.etherscan.io/address/0x9302E02e2869e129aC8516fE5eFFd51EA3082c09)) |
| Source | [github.com/thurinlabs/pgp-registry](https://github.com/thurinlabs/pgp-registry) |
| Compiler | solc 0.8.24, via-IR, optimizer 200 runs, no metadata hash (address depends only on code) |

The contract is deployed with CREATE2 and a fixed salt, so it has the same address on every network. `VERSION()` returns `2`.

The v1 registry at [`0xf7a45BC662A78a6fb417ED5f52b3766cbf13EbBb`](https://etherscan.io/address/0xf7a45BC662A78a6fb417ED5f52b3766cbf13EbBb) remains on mainnet but is no longer read by Thurin.

## What is stored

```solidity
struct Attestation {
    bytes   fingerprint;     // raw fingerprint: 20 bytes (v4 key) or 32 bytes (v6 key)
    uint64  createdAt;
    uint64  revokedAt;       // 0 = active
    uint8   messageVersion;  // 1 = "I control the Ethereum address: <lowercase address>"
    address keyPtr;          // data contract holding the armored public key
    address sigPtr;          // data contract holding the clearsigned message
}
```

The signature and key live in SSTORE2 data contracts (the bytes are the contract's code), which is why every read below is a plain `eth_call` that any RPC can serve. Limits: key ≤ 8192 bytes, signature ≤ 4096 bytes, record ≤ 1024 bytes. One **active** claim per (address, fingerprint); history is append-only.

## Writing

```solidity
function attest(bytes fingerprint, bytes pgpSignature, bytes pgpPublicKey) returns (uint256 index);
function reattest(uint256 revokeIndex, bytes fingerprint, bytes pgpSignature, bytes pgpPublicKey) returns (uint256 index);
function updateKey(uint256 index, bytes pgpPublicKey);
function revoke(uint256 index);
function setRecord(uint256 index, bytes32 kind, bytes value);   // empty value clears (allowed on revoked entries too)
function cancelAuthorization();                                  // burn the caller's current nonce
```

- `attest` publishes a new claim from `msg.sender`. The clearsigned message must be exactly `I control the Ethereum address: 0x<lowercase address>`.
- `reattest` revokes one of your claims and publishes a new one in the same transaction (same key with new notations, or a rotated key).
- `updateKey` replaces the stored key of an active claim — same fingerprint, new notations, no new signature. This is how proofs are added after attesting.
- `setRecord` attaches a small typed value to a claim; readers ignore kinds they don't know, and should only trust a record while the claim is active.
- `cancelAuthorization` invalidates every authorization signed with the caller's current nonce. Direct writes do not consume nonces, so use this if a signed authorization is out in the wild and you no longer want it submittable.

### Authorized writes

Every write has a twin that anyone can submit with the owner's EIP-712 signature: `attestFor`, `reattestFor`, `updateKeyFor`, `revokeFor`, `setRecordFor`. The owner signs a typed struct that binds every argument, their current `nonces(owner)`, and a `deadline`; whoever submits pays the gas and is recorded as `submitter` in the event. The submitter cannot alter, reuse, or delay an authorization. Contract wallets are checked through EIP-1271.

The direct functions are the default — thurin.id uses them and the user pays gas. The `…For` door exists for cold wallets, command-line tooling, and anyone who wants to sponsor claims. Thurin runs no relayer.

Domain: `{ name: "Thurin PGPRegistry", version: "2", chainId, verifyingContract }`. Types:

```
Attest(address owner,bytes fingerprint,bytes pgpSignature,bytes pgpPublicKey,uint256 nonce,uint256 deadline)
Reattest(address owner,uint256 revokeIndex,bytes fingerprint,bytes pgpSignature,bytes pgpPublicKey,uint256 nonce,uint256 deadline)
UpdateKey(address owner,uint256 index,bytes pgpPublicKey,uint256 nonce,uint256 deadline)
Revoke(address owner,uint256 index,uint256 nonce,uint256 deadline)
SetRecord(address owner,uint256 index,bytes32 kind,bytes value,uint256 nonce,uint256 deadline)
```

identity-kit exports helpers (`attestTypedData` and friends) that build exactly these structs for `signTypedData`.

## Reading

```solidity
function attestationCount(address owner) view returns (uint256);
function getAttestation(address owner, uint256 index) view returns (Attestation);
function getPayload(address owner, uint256 index) view returns (bytes pgpSignature, bytes pgpPublicKey);
function attestationsOf(address owner) view returns (Attestation[]);
function current(address owner) view returns (bool found, uint256 index, Attestation);
function record(address owner, uint256 index, bytes32 kind) view returns (bytes);
function addressesFor(bytes32 fingerprintHash) view returns (address[]);   // keccak256(raw fingerprint bytes)
function fingerprintsForKeyId(bytes8 keyId) view returns (bytes[]);       // long key ID (RFC 9580: v4 = last 8 bytes, v6 = first 8)
function nonces(address owner) view returns (uint256);

// paginated forms — the arrays above are unbounded and, since attesting is permissionless,
// growable by anyone; readers that must stay responsive use these
function attestationsOfRange(address owner, uint256 start, uint256 count) view returns (Attestation[]);
function addressesForCount(bytes32 fingerprintHash) view returns (uint256);
function addressesForRange(bytes32 fingerprintHash, uint256 start, uint256 count) view returns (address[]);
function fingerprintsForKeyIdCount(bytes8 keyId) view returns (uint256);
function fingerprintsForKeyIdRange(bytes8 keyId, uint256 start, uint256 count) view returns (bytes[]);
```

`addressesFor` lists every address that has ever attested a fingerprint — check `revokedAt` on each claim for whether it is still active. `fingerprintsForKeyId` turns a long key ID into the fingerprint(s) attested with it, so no keyserver lookup is needed.

## Events

```solidity
event Attested(address indexed owner, bytes32 indexed fingerprintHash, uint256 indexed index, bytes fingerprint, uint8 messageVersion, address keyPtr, address sigPtr, address submitter);
event KeyUpdated(address indexed owner, bytes32 indexed fingerprintHash, uint256 indexed index, address oldKeyPtr, address newKeyPtr, address submitter);
event Revoked(address indexed owner, bytes32 indexed fingerprintHash, uint256 indexed index, address submitter);
event RecordSet(address indexed owner, uint256 indexed index, bytes32 indexed kind, address submitter);
event NonceUsed(address indexed owner, uint256 nonce);
```

Events are for indexers and notifications; nothing needs them to read the registry.

## Reading from JavaScript

Use [`@thurinlabs/identity-kit`](/sdk) for verified results, or read directly with viem. Any RPC works, including the keyless public ones:

```typescript
import { createPublicClient, http, hexToString } from 'viem'
import { mainnet } from 'viem/chains'
import { REGISTRY_ABI, REGISTRY_ADDRESS, bytesToFingerprint } from '@thurinlabs/identity-kit'

const client = createPublicClient({ chain: mainnet, transport: http() })

const [found, index, claim] = await client.readContract({
  address: REGISTRY_ADDRESS,
  abi: REGISTRY_ABI,
  functionName: 'current',
  args: ['0xYourAddress'],
})

if (found) {
  const [signature, publicKey] = await client.readContract({
    address: REGISTRY_ADDRESS,
    abi: REGISTRY_ABI,
    functionName: 'getPayload',
    args: ['0xYourAddress', index],
  })
  console.log(bytesToFingerprint(claim.fingerprint), hexToString(publicKey))
}
```

From the command line:

```bash
cast call 0x9302E02e2869e129aC8516fE5eFFd51EA3082c09 "attestationCount(address)(uint256)" 0xYourAddress --rpc-url https://ethereum-rpc.publicnode.com
```

## Trust model

The contract does not verify PGP signatures. A claim is meaningful only if the stored clearsigned message verifies against the stored key, the key's fingerprint matches the claim, and the signed text names the exact owner address. identity-kit performs all of that off-chain, so a fake claim can never block or impersonate the real key owner — it simply shows as unverified.
