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
gpg --fingerprint your@email.com
```

Output looks like:

```
pub   ed25519 2024-11-23 [SC]
      03E5 3D80 7CE3 8C13 0ED4  2ECE CD3D 0D7F 0C9E 5FB8
uid           [ultimate] Your Name <your@email.com>
sub   cv25519 2024-11-23 [E]
```

Your fingerprint is the 40-character hex string: `03E53D807CE38C130ED42ECECD3D0D7F0C9E5FB8`

## 3. Upload to the Keyserver

Upload your public key to [keys.openpgp.org](https://keys.openpgp.org):

```bash
gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_FINGERPRINT
```

**Important:** After uploading, check your email — keys.openpgp.org sends a verification link. You must click it or your key won't be discoverable, and Thurin won't be able to fetch it.

You can verify your key is live at: `https://keys.openpgp.org/search?q=YOUR_FINGERPRINT`

## 4. Attest on-chain

[thurin.id/attest](https://thurin.id/attest) creates an on-chain link between your PGP key and your Ethereum address. This is a one-time setup.

You'll need a browser wallet (MetaMask, etc.) and ETH for gas.

1. **Connect your wallet** on [thurin.id/attest](https://thurin.id/attest)
2. **Sign your PGP fingerprint with your wallet** — paste your `gpg --fingerprint` output into the attest page, then click "Sign with Wallet"
3. **Sign your ETH address with GnuPG** — the attest page shows you a command to run:
   ```bash
   echo "I control the Ethereum address: 0xYOUR_ADDRESS" | gpg --clearsign --armor -u YOUR_FINGERPRINT
   ```
   Paste the full signed output back into the attest page
4. **Publish to the registry** — confirm the transaction in your wallet

After publishing, verify on Thurin: `https://thurin.id/eth/YOUR_ADDRESS`

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
2. **Add the notation to your PGP key** ([GnuPG guide](/guides/gnupg))
3. **Upload your updated key** to the keyserver
4. **Verify on Thurin** — look up your fingerprint and check for the green checkmark

> **Tip:** Create the proof content on the platform *before* adding the notation to your key. That way Thurin can verify it immediately.

## Next Steps

- [Managing Notations](/guides/gnupg) — add, list, and remove proof notations
- [Thurin Proofs](/guides/proofs) — how the proof system works
- [Identity Kit](/sdk) — embed your identity card on any website
