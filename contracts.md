# PGPRegistry

The contract that holds every Thurin.id claim. A claim puts a PGP key on an Ethereum address: the key, and a signature by that key over a line naming the address. Anyone can write one, only the address can change it, and nobody can take it down. There is no owner, no admin, no fee, and no upgrade.

Everything on this page works from Etherscan or `cast` with gpg. thurin.id, the CLI, and the library are conveniences on top.

| | |
|---|---|
| Address | `0xFa6956c11163517249f8A67F5560a4406B519451` |
| Networks | Ethereum mainnet and Sepolia, same address ([Etherscan](https://etherscan.io/address/0xFa6956c11163517249f8A67F5560a4406B519451) · [Sepolia Etherscan](https://sepolia.etherscan.io/address/0xFa6956c11163517249f8A67F5560a4406B519451)) |
| Source | [github.com/thurinlabs/pgp-registry](https://github.com/thurinlabs/pgp-registry), verified on Etherscan and Sourcify |
| Build | solc 0.8.37, via-IR, optimizer 200, EVM cancun; deployed through the CREATE2 deployer with salt `keccak256("thurin.pgp-registry.v3")` |

`VERSION()` returns `3`.

## A claim

- **The key**, as raw bytes (`gpg --export`). Keep it minimal: your names and proofs, no third-party signatures. Up to 16 KB.
- **The signature**: the key's detached text-mode signature over `statementFor(owner)`, which is `I control the Ethereum address: 0x…` with the address in lowercase, no line break after it. Up to 8 KB. A whole clearsigned message of the same line also works.
- **The fingerprint**: 20 bytes for a v4 key, 32 for v6.

The contract checks sizes and that the bytes look like a key and a signature. It does not check the PGP signature itself; readers do (gpg, identity-kit, the CLI). A claim that doesn't verify is shown as unverified and hurts no one else.

One active claim per address and key. Claims are never deleted: revoking one keeps it in the history.

## Use it with gpg and cast

Reads need no wallet. Any RPC works; `ethereum.publicnode.com` needs no key.

```bash
export ETH_RPC_URL=https://ethereum.publicnode.com
REG=0xFa6956c11163517249f8A67F5560a4406B519451
OWNER=0x…   # the address to look up
ME=0x…      # your own address, when making a claim

cast call $REG "summary(address)(uint256,uint256,bool,uint256)" $OWNER        # total, active, has current, its index
cast call $REG "armoredKey(address,uint256)(string)" $OWNER 0 | jq -r . | gpg --import
cast call $REG "clearsigned(address,uint256)(string)" $OWNER 0 | jq -r . | gpg --verify
```

`gpg --verify` should say *Good signature* and the text should name `$OWNER`. That is the whole check.

To make a claim, sign the statement and export the key, then send both as bytes:

```bash
cast call $REG "statementFor(address)(string)" $ME | jq -r . | tr -d '\n' | gpg --detach-sign --textmode --disable-signer-uid > claim.sig
gpg --export-options export-minimal --export YOUR_FINGERPRINT > claim.key
cast send $REG "attest(bytes,bytes,bytes)" 0xYOUR_FINGERPRINT \
  0x$(xxd -p claim.sig | tr -d '\n') 0x$(xxd -p claim.key | tr -d '\n') --account you
```

Leave out names with an email address unless you want them public (add `--export-filter keep-uid='uid !~ @'`).

**On Etherscan** the forms want bytes. Paste an armored key or signature into `armorToBytes` under *Read Contract* and it hands back the bytes to paste into `attest` under *Write Contract*. It copes with the line breaks the form drops.

## Writes

The owner sends these directly:

```solidity
attest(bytes fingerprint, bytes signature, bytes key) → uint256 index
reattest(uint256 revokeIndex, bytes fingerprint, bytes signature, bytes key, bool keepRecords) → uint256 index
updateKey(uint256 index, bytes key)
revoke(uint256 index, string reason)                    // "", "compromised", "retired", "other"
setRecord(uint256 index, string kind, string value)     // "" clears
multicall(bytes[] calls) → bytes[]
cancelAuthorization()
```

- `updateKey` swaps the stored key for a new export of the same key: new names or proofs, no new signature.
- `reattest` revokes one claim and publishes another in one transaction, for a new key or a fresh signature. The old claim reads *replaced* and points at the new one. With `keepRecords` its records move to the new claim.
- `revoke` ends a claim. **"compromised" is final:** this address can never claim that key again. A claim already revoked or replaced can be revoked again as "compromised" once, later, if you find out afterwards. That fails while the same key still has an active claim here; revoke that one first.
- To replace a stolen key in one transaction: `multicall([reattest(old, …), revoke(old, "compromised")])`.

## Permissions: someone else pays

Each write has a `…For` twin that anyone can send with the owner's EIP-712 signature, so the owner's address never needs ETH: `attestFor`, `reattestFor`, `updateKeyFor`, `revokeFor`, `setRecordFor`, and `markCompromisedFor`. Each takes the same arguments plus `owner`, `deadline`, and `permission` (the signature). Contract wallets sign through ERC-1271.

`revokeFor` only revokes an active claim. Marking a revoked claim compromised later is `markCompromisedFor`, its own permission, so a revoke you signed once can't be reused to lock a key months later.

Domain: `{ name: "Thurin PGPRegistry", version: "3", chainId, verifyingContract }`.

```
Attest(address owner,bytes fingerprint,bytes signature,bytes key,uint256 nonce,uint256 deadline)
Reattest(address owner,uint256 revokeIndex,bytes fingerprint,bytes signature,bytes key,bool keepRecords,uint256 nonce,uint256 deadline)
UpdateKey(address owner,uint256 index,bytes key,uint256 nonce,uint256 deadline)
Revoke(address owner,uint256 index,string reason,uint256 nonce,uint256 deadline)
SetRecord(address owner,uint256 index,string kind,string value,uint256 nonce,uint256 deadline)
MarkCompromised(address owner,uint256 index,uint256 nonce,uint256 deadline)
```

`nonces(owner)` is the next nonce. A permission is spent only when it lands; one that fails stays usable until its deadline. To kill every permission you've signed at the current nonce, call `cancelAuthorization()`. identity-kit builds these structs (`attestTypedData` and the rest); the CLI's `--authorize` signs them.

## Reads

For people, as text:

```solidity
statementFor(address owner) → string                 // the line to sign
armoredKey(address owner, uint256 index) → string    // for gpg --import
clearsigned(address owner, uint256 index) → string   // for gpg --verify
claim(address owner, uint256 index) → (ClaimView, string key, string statement, string[] recordNames)
summary(address owner) → (uint256 total, uint256 active, bool hasCurrent, uint256 currentIndex)
keyStatus(address owner, bytes fingerprint) → string // "none", "active", "revoked", "compromised"
recordsOf(address owner, uint256 index) → (string[] names, string[] values)
recordText(address owner, uint256 index, string kind) → string
armorToBytes(string armored) → bytes
```

For tools:

```solidity
claimsOf(address owner) → ClaimView[]                // oldest first
claimsOfRange(address owner, uint256 start, uint256 count) → ClaimView[]
claimCount(address owner) → uint256
current(address owner) → (bool found, uint256 index, ClaimView)   // newest active claim
keyBytes(address owner, uint256 index) → bytes
signatureBytes(address owner, uint256 index) → bytes
ownersOf(bytes fingerprint) → address[]              // + ownersOfCount, ownersOfRange
fingerprintsForKeyId(bytes8 keyId) → bytes[]         // + …Count, …Range
nonces(address owner) → uint256
```

```solidity
struct ClaimView {
    uint256 index;
    bytes   fingerprint;
    uint64  createdAt;       // Unix seconds
    uint64  revokedAt;       // 0 = active
    string  state;           // "active", "revoked", or "replaced"
    uint256 replacedBy;      // the new claim's index, when replaced
    string  revokeReason;    // "", "compromised", "retired", "superseded", or "other"
    uint8   messageVersion;  // 0 = clearsigned as sent, 1 = detached signature
}
```

Reading them right:

- **Is this key compromised?** Ask `keyStatus(owner, fingerprint)`. A late mark changes only the claim it was made on, so the newest claim on a key can still show another reason. `revokedAt` keeps the date the claim ended, not the date it was marked.
- **"Compromised" belongs to one address.** Anyone can post a claim on any fingerprint and revoke it as compromised. It says what that address thinks, nothing more. Never count it across the owners of a key.
- `ownersOf` and `fingerprintsForKeyId` list everyone who ever claimed, and anyone can add to them. Check each owner's claims, and use the `Range` forms when a list could be long.
- A long key ID is the last 8 bytes of a v4 fingerprint, or the first 8 of a v6 one.

## Records

Short text on a claim: up to 1 KB, one per name, set by the owner, readable by anyone. Names are `a-z 0-9 - .`, up to 31 bytes; a name without a dot means `thurin.<name>`, so `canary` is `thurin.canary`. Setting needs an active claim; clearing works on any. What the names mean: [Records](/records).

## Events

```solidity
Attested(address indexed owner, bytes32 indexed fingerprintHash, uint256 indexed index, bytes fingerprint, address payload, uint8 messageVersion, address submitter)
KeyUpdated(address indexed owner, bytes32 indexed fingerprintHash, uint256 indexed index, address oldPayload, address newPayload, address submitter)
Revoked(address indexed owner, bytes32 indexed fingerprintHash, uint256 indexed index, string reason, uint256 replacedBy, address submitter)
RecordSet(address indexed owner, uint256 indexed index, bytes32 indexed kindHash, string kind, string value, address submitter)
RecordsMoved(address indexed owner, uint256 indexed fromIndex, uint256 indexed toIndex)
NonceUsed(address indexed owner, uint256 nonce)
```

Nothing needs events to read the registry; they're the history. `fingerprintHash` is `keccak256` of the fingerprint bytes. `Revoked.replacedBy` is the new index + 1, or 0. A late compromised mark emits a second `Revoked`. After `RecordsMoved`, a clear on the old index still emits `RecordSet` but changes nothing: the records live on the new claim.

## What it can't protect

- **Your Ethereum key.** Whoever holds it can replace or revoke your claims. Keep it on hardware. If it leaks, revoke and claim again from a new address; the PGP key is fine.
- **Records are forever.** Clearing a record removes it from the contract, but every value stays in the chain's history and in `RecordSet`. Don't put anything there you'd want back.
