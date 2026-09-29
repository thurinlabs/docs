# Verify a Thurin CLI release

Every Thurin CLI release is signed by the Thurin Labs key, claimed on-chain from thurinlabs.eth. This page checks a release with only gpg and the chain. No Thurin software is involved until the key has arrived from Ethereum.

## What a release contains

On the [GitHub release](https://github.com/thurinlabs/thurin-cli/releases), three files:

| File | What it is |
|---|---|
| `thurinlabs-thurin-<version>.tgz` | the package, byte-identical to what npm serves |
| `SHA256SUMS` | its checksum |
| `SHA256SUMS.asc` | the checksum file, signed by the Thurin Labs key |

The tarball is built and signed on a person's machine, not in CI. CI never holds a key.

## 1. Get the key from the chain

```bash
gpg --keyserver hkps://keys.thurin.id --recv-keys 08B9374FDFBEC67EFFA24E669D3D86E35361EF7B
```

That is the Thurin Labs key, `08B9 374F DFBE C67E FFA2 4E66 9D3D 86E3 5361 EF7B`. Its on-chain claim proves the GitHub organisation, both domains, and the Codeberg organisation: [thurin.id/ens/thurinlabs.eth](https://thurin.id/ens/thurinlabs.eth). To trust no server at all, run `thurin keyserver` locally instead.

Or, leaving gpg's keyserver settings alone:

```bash
curl -s https://thurin.id/pgp/08B9374FDFBEC67EFFA24E669D3D86E35361EF7B.asc | gpg --import
```

gpg prints `key 9D3D86E35361EF7B: public key "Thurin Labs" imported`: the last 16 characters of the fingerprint above. To see the whole fingerprint before importing, use `gpg --import-options show-only --import`.

## 2. Verify the signature

```bash
gpg --verify SHA256SUMS.asc SHA256SUMS
```

```
gpg: Good signature from "Thurin Labs"
```

## 3. Verify the file

```bash
sha256sum -c SHA256SUMS
```

```
thurinlabs-thurin-<version>.tgz: OK
```

## 4. Check the chain names this release

```bash
npx @thurinlabs/thurin record get thurinlabs.eth releases
```

```
thurin-cli <version>   <date>  sha256 <hash of SHA256SUMS>  https://github.com/thurinlabs/thurin-cli/releases/tag/v<version>
```

The same list is on the Records tab at [thurin.id/ens/thurinlabs.eth/records](https://thurin.id/ens/thurinlabs.eth/records).

Find the line for the version you downloaded and compare its hash to your own `sha256sum SHA256SUMS`. If they match, thurinlabs.eth itself named this checksum file on-chain: the release is one Thurin Labs put out, not merely one its key signed.

## 5. Check it is what npm serves

```bash
npm pack @thurinlabs/thurin@<version> && sha256sum thurinlabs-thurin-<version>.tgz
```

The hash must match the line in `SHA256SUMS`. If it does, `npx @thurinlabs/thurin` runs exactly the bytes that were signed. (Fetch through `npm pack` rather than the registry's direct tarball URL, which can answer 404 for a while after a publish.)

## What this proves, and what it doesn't

It proves the release was signed by whoever holds the Thurin Labs key, and that the key is the one claimed on-chain from thurinlabs.eth with four proofs. Thurin.id's part is answering "whose key is this"; the rest is gpg and sha256sum.

With step 4, it also proves the release is one Thurin Labs put out: the chain names the key *and* the checksum file, so a reader trusts nothing but Ethereum and gpg. The current registry names every release from 0.13.1 on, and 0.11.0 to 0.12.0 (carried over from the registry before it). For anything older, stop at step 3: those were named only on the old registry, which Thurin's tools no longer read. It does not prove the code is good; read it, it is MIT. And a keyserver, including ours, can withhold a revocation. If that matters, fetch from your own `thurin keyserver`.

## Anyone's releases

Steps 2 to 4 work for any project that names its releases on its claim: fetch its key, then `thurin record get <its name> releases`. To name your own, sign your `SHA256SUMS` and run `thurin record add-release "<name> <version>" SHA256SUMS --url <release page>` from the address that holds your claim ([CLI](/cli?id=records)).

## All releases

Every release is on [GitHub releases](https://github.com/thurinlabs/thurin-cli/releases) with its three files, and named on-chain: the Records tab at [thurin.id/ens/thurinlabs.eth/records](https://thurin.id/ens/thurinlabs.eth/records), or `thurin record get thurinlabs.eth releases`. The chain's list keeps the newest releases that fit in 1 KB; older ones stay in its history.
