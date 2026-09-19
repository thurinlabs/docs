# Verify signed commits from the chain

GitHub's green "Verified" badge means GitHub has a copy of the signer's key. That is trust in GitHub. This page checks a commit signature against a key fetched from Ethereum, with nothing but gpg.

## 1. Point gpg at the chain

One line, once:

```bash
echo "keyserver hkps://keys.thurin.id" >> ~/.gnupg/dirmngr.conf
gpgconf --kill dirmngr
```

[keys.thurin.id](/cli#be-a-keyserver) answers gpg's key requests by reading the Thurin registry. It also speaks plain HKP on port 11371, so a bare `--keyserver keys.thurin.id` works; `hkps://` is the one to put in your config. It has no upload and no database: a key is there because its owner published a claim from their own address. To trust nobody at all, run the same server on your own machine with `thurin keyserver` and point the line at `hkp://127.0.0.1:11371`.

## 2. Fetch the signer's key

Every Thurin Labs commit is signed by the key `6E00 5391 1942 A889 426C 1866 E34D 9266 098F 7FE7`, claimed on-chain from **ben.thurinlabs.eth**: a subname the company issued, pointing at an address only its holder controls. The org vouches for the name; the person holds the key.

```bash
gpg --recv-keys 6E0053911942A889426C1866E34D9266098F7FE7
```

gpg checks that the key it received hashes to the fingerprint it asked for, so a keyserver cannot substitute one. Always fetch by the full fingerprint, never a short key ID.

## 3. Verify

```bash
git clone https://github.com/thurinlabs/thurin-cli && cd thurin-cli
git log -1 --show-signature
```

```
gpg: Good signature from "Ben Woodall (Ben Thurin Key) <ben@thurin.id>"
```

That signature was checked against a key that came from Ethereum, not from GitHub. `[unknown]` after the name is gpg's web-of-trust marker, which is separate; the signature itself is good.

## 4. Check who the key belongs to

The key's on-chain claim carries proofs. [thurin.id/ens/ben.thurinlabs.eth](https://thurin.id/ens/ben.thurinlabs.eth) shows the claim and its GitHub proof for `benwoody`, the account the commits come from. From a terminal:

```bash
npx @thurinlabs/thurin status ben.thurinlabs.eth
```

So the chain says: thurinlabs.eth issued the name ben.thurinlabs.eth; that address claims this key; this key proves this GitHub account. The commit's signature closes the loop. No server of ours is anywhere in it, and the address never held any ETH: the claim was published through Thurin's [relayer](/cli#run-a-relayer).

## Let gpg fetch keys on its own

With this in `~/.gnupg/gpg.conf`, verification pulls unknown keys from the chain as it goes, and `git log --show-signature` on any repo whose signers have claims just works:

```
auto-key-retrieve
```

## Revocation

If a signing key is compromised, its owner revokes the claim on-chain. `gpg --refresh-keys` then stops receiving it. A commit signed after the revocation shows as signed by an unknown key.

## Your own commits

1. [Attest your key](https://thurin.id/attest), with a [GitHub proof](/guides/github) on it.
2. `git config --global commit.gpgsign true` and `user.signingkey <your fingerprint>`.
3. Send people here instead of to a badge.
