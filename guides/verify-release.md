# Verify a Thurin release

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

## 2. Verify the signature

```bash
gpg --verify SHA256SUMS.asc SHA256SUMS
```

```
gpg: Good signature from "Thurin Labs <hello@thurin.id>"
```

## 3. Verify the file

```bash
sha256sum -c SHA256SUMS
```

```
thurinlabs-thurin-0.5.1.tgz: OK
```

## 4. Check it is what npm serves

```bash
curl -sL https://registry.npmjs.org/@thurinlabs/thurin/-/thurin-0.5.1.tgz | sha256sum
```

The hash must match the line in `SHA256SUMS`. If it does, `npx @thurinlabs/thurin` runs exactly the bytes that were signed.

## What this proves, and what it doesn't

It proves the release was signed by whoever holds the Thurin Labs key, and that the key is the one claimed on-chain from thurinlabs.eth with four proofs. Thurin's part is answering "whose key is this"; the rest is gpg and sha256sum.

It does not yet prove this release is one Thurin Labs put out. Nothing on-chain names the release, so anyone holding the key could sign a tarball with this version number. The fix is a [pointer record](/roadmap) on the company claim naming each release's checksum file; then the chain names the key *and* the sums, and a reader trusts nothing but Ethereum and gpg. It does not prove the code is good either; read it, it is MIT. And a keyserver, including ours, can withhold a revocation. If that matters, fetch from your own `thurin keyserver`.

## Releases

| Version | Date | Signed by |
|---|---|---|
| [0.5.1](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.5.1) | 2026-09-19 | 08B9…EF7B |
