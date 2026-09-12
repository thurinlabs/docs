# Getting Started

This guide walks you through everything you need to set up a Thurin identity — from creating a PGP key to verifying your first proof on Thurin.

## 1. Install GnuPG

GnuPG 2.2+ is required. 2.4+ is recommended.

Check if you already have it:

```bash
gpg --version
```

If not installed or too old:

- **macOS:** `brew install gnupg`
- **Debian/Ubuntu:** `sudo apt install gnupg`
- **Fedora/RHEL:** `sudo dnf install gnupg2`
- **Arch:** `sudo pacman -S gnupg`
- **Windows:** [Gpg4win](https://www.gpg4win.org/)

## 2. Generate a PGP Key

**Ed25519 is recommended** — fast, small keys/signatures, widely supported.

```bash
gpg --quick-gen-key "Your Name <your@email.com>" ed25519
```

You'll be prompted for a passphrase to protect your private key.

After creation, get your fingerprint:

```bash
gpg --fingerprint "Your Name"
```

Output looks like:

```
pub   ed25519 2024-11-23 [SC]
      03E5 3D80 7CE3 8C13 0ED4  2ECE CD3D 0D7F 0C9E 5FB8
uid           [ultimate] Your Name <your@email.com>
sub   cv25519 2024-11-23 [E]
```

Your fingerprint is the 40-character hex string: `03E53D807CE38C130ED42ECECD3D0D7F0C9E5FB8`

## 3. Give Your Key a Published Name

Attesting stores your public key on-chain, permanently and publicly. By default Thurin publishes only the names on your key that contain **no email address**, so add one — any name you like; `thurin` is the suggestion:

```bash
gpg --quick-add-uid YOUR_FINGERPRINT thurin
```

Proof notations go on this name (see [Managing Notations](/guides/gnupg)). Your email stays off-chain unless you choose "Include my email" when attesting. No keyserver upload is needed — Thurin never reads from one.

## 4. Attest on-chain

[thurin.id/attest](https://thurin.id/attest) creates an on-chain link between your PGP key and your Ethereum address. You'll need a browser wallet (MetaMask, etc.) and a little ETH for gas.

1. **Connect your wallet** on [thurin.id/attest](https://thurin.id/attest) and open **New claim**
2. **Choose what to publish** — *Keep my email off-chain* (recommended) or *Include my email*
3. **Enter your PGP fingerprint** — paste your `gpg --fingerprint` output; the page picks out the 40-character fingerprint
4. **Sign your ETH address with GnuPG** — the page shows the exact command:
   ```bash
   echo "I control the Ethereum address: 0xYOUR_ADDRESS" | gpg --clearsign --armor -u YOUR_FINGERPRINT
   ```
   Paste the signed output, then paste your exported public key (the page shows that command too). It verifies the signature and shows exactly what will go on-chain: the published name, the proofs on it, and anything left out
5. **Publish to the registry** — confirm the transaction in your wallet. That transaction, sent from your connected address, binds the address to your key

Afterwards your identity is at `https://thurin.id/eth/YOUR_ADDRESS`.

**What goes on-chain:** your address, the key's fingerprint, the signed message, and the key with its published name(s) and proof notations. It is readable by anyone from any Ethereum node and cannot be deleted, only revoked.

## 5. Add Your First Proof

Proofs link your PGP key to your accounts on other platforms. Each proof is a two-way link:

- Your PGP key points to the account (via a `proof@thurin.id` notation)
- Your account points back to your key (via a fingerprint token)

Pick a provider and follow its guide:

- [Codeberg](/guides/codeberg) — repo description
- [DNS](/guides/dns) — TXT record
- [Farcaster](/guides/farcaster) — public cast
- [GitHub](/guides/github) — public gist
- [Mastodon](/guides/mastodon) — profile metadata

The general flow for any provider:

1. **Create the proof on the platform** (gist, TXT record, cast, repo, profile field)
2. **Add the notation to your published name** ([GnuPG guide](/guides/gnupg))
3. **Update the key on your claim** — *Your claims → Update* on [thurin.id/attest](https://thurin.id/attest), paste a fresh export, confirm one transaction
4. **Verify on Thurin** — look up your address and check for the green checkmark

> **Tip:** Create the proof content on the platform *before* adding the notation to your key. That way Thurin can verify it immediately.

## Next Steps

- [Managing Notations](/guides/gnupg) — add, list, and remove proof notations
- [Thurin Proofs](/guides/proofs) — how the proof system works
- [Identity Kit](/sdk) — embed your identity card on any website
