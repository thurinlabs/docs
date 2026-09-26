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
thurinlabs-thurin-0.13.2.tgz: OK
```

## 4. Check the chain names this release

```bash
npx @thurinlabs/thurin record get thurinlabs.eth releases
```

```
thurin-cli 0.13.2      2026-09-26  sha256 5e470ab66782faadbd5a146915ada6c701e1562f3ddb8450124e2d93aed0e057  https://github.com/thurinlabs/thurin-cli/releases/tag/v0.13.2
```

The same list is on the Records tab at [thurin.id/ens/thurinlabs.eth/records](https://thurin.id/ens/thurinlabs.eth/records).

Compare the hash to your own `sha256sum SHA256SUMS`. If they match, thurinlabs.eth itself named this checksum file on-chain: the release is one Thurin Labs put out, not merely one its key signed.

## 5. Check it is what npm serves

```bash
npm pack @thurinlabs/thurin@0.13.2 && sha256sum thurinlabs-thurin-0.13.2.tgz
```

The hash must match the line in `SHA256SUMS`. If it does, `npx @thurinlabs/thurin` runs exactly the bytes that were signed. (Fetch through `npm pack` rather than the registry's direct tarball URL, which can answer 404 for a while after a publish.)

## What this proves, and what it doesn't

It proves the release was signed by whoever holds the Thurin Labs key, and that the key is the one claimed on-chain from thurinlabs.eth with four proofs. Thurin.id's part is answering "whose key is this"; the rest is gpg and sha256sum.

With step 4, it also proves the release is one Thurin Labs put out: the chain names the key *and* the checksum file, so a reader trusts nothing but Ethereum and gpg. The current registry names 0.13.2, 0.13.1, and 0.11.0 to 0.12.0 (carried over from the registry before it). For anything older, stop at step 3: those were named only on the old registry, which Thurin's tools no longer read. It does not prove the code is good; read it, it is MIT. And a keyserver, including ours, can withhold a revocation. If that matters, fetch from your own `thurin keyserver`.

## Anyone's releases

Steps 2 to 4 work for any project that names its releases on its claim: fetch its key, then `thurin record get <its name> releases`. To name your own, sign your `SHA256SUMS` and run `thurin record add-release "<name> <version>" SHA256SUMS --url <release page>` from the address that holds your claim ([CLI](/cli?id=records)).

## Releases

| Version | Date | Signed by |
|---|---|---|
| [0.13.2](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.13.2) | 2026-09-26 | 08B9…EF7B |
| [0.13.1](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.13.1) | 2026-09-26 | 08B9…EF7B |
| [0.12.0](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.12.0) | 2026-09-24 | 08B9…EF7B |
| [0.11.1](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.11.1) | 2026-09-24 | 08B9…EF7B |
| [0.11.0](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.11.0) | 2026-09-24 | 08B9…EF7B |
| [0.10.0](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.10.0) | 2026-09-23 | 08B9…EF7B |
| [0.9.0](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.9.0) | 2026-09-22 | 08B9…EF7B |
| [0.8.0](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.8.0) | 2026-09-21 | 08B9…EF7B |
| [0.7.0](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.7.0) | 2026-09-20 | 08B9…EF7B |
| [0.6.0](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.6.0) | 2026-09-19 | 08B9…EF7B |
| [0.5.1](https://github.com/thurinlabs/thurin-cli/releases/tag/v0.5.1) | 2026-09-19 | 08B9…EF7B |
