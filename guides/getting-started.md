# Getting started

From nothing to a claim with a proof on it. You'll need gpg in a terminal, a wallet, and a little ETH for the fee.

## 1. Install gpg

GnuPG 2.2 or newer. Check with `gpg --version`.

- **macOS:** `brew install gnupg`
- **Debian/Ubuntu:** `sudo apt install gnupg`
- **Fedora:** `sudo dnf install gnupg2`
- **Arch:** `sudo pacman -S gnupg`
- **Windows:** [Gpg4win](https://www.gpg4win.org/)

## 2. Make a key

If you already have one, skip ahead. A new Ed25519 key with your name and no email, plus an encryption subkey:

```bash
gpg --quick-gen-key "Your Name" ed25519 sign 2y
gpg --quick-add-key YOUR_FINGERPRINT cv25519 encr 2y
```

gpg prints the fingerprint when it makes the key; `gpg --fingerprint "Your Name"` shows it again. It's the 40-character hex string, like `03E5 3D80 7CE3 8C13 0ED4 2ECE CD3D 0D7F 0C9E 5FB8`.

## 3. Check it has a name without an email

Your claim publishes the key on-chain for good, and by default only the names on it that contain no email. If every name on your key has an email, add one without:

```bash
gpg --quick-add-uid YOUR_FINGERPRINT "Your Name"
```

The attest page spots this too and shows the command with your name filled in. Proofs go on this name. Your email stays off-chain unless you choose to include it.

## 4. Add your key to your address

1. Open [thurin.id/attest](https://thurin.id/attest) and connect your wallet.
2. Copy the one command the page shows and run it. It signs the line `I control the Ethereum address: 0x…` with your key and prints your public key. Paste the whole output back.
3. The page checks the signature and shows exactly what goes on-chain: the name, any proofs, and what it left out.
4. **Publish** and confirm in your wallet.

The command uses the first key gpg can sign with. If the page names the wrong key, click **Use a different key**.

Your identity is then at `https://thurin.id/eth/YOUR_ADDRESS`.

**Share your key** with a plain link: `https://thurin.id/eth/YOUR_ADDRESS.asc` is the key file itself, and so are `/ens/YOUR_NAME.asc` (once your ENS name points at the address) and `/pgp/YOUR_FINGERPRINT.asc`. Put it in an email signature, a profile, or a security.txt. It always serves your current verified key, and stops when you revoke it.

Rather use a terminal? `npx @thurinlabs/thurin@latest attest` does the same; see the [CLI](/cli).

## 5. Add a proof

A proof links your key to an account elsewhere, both ways: the key names the account, and the account shows your fingerprint.

1. Put `thurin-id=openpgp4fpr:YOUR_FINGERPRINT` on the platform: [GitHub](/guides/github), [DNS](/guides/dns), [Farcaster](/guides/farcaster), [Codeberg](/guides/codeberg), or [Mastodon](/guides/mastodon).
2. Add a `proof@thurin.id` notation to your key that points at it ([how](/guides/gnupg)).
3. Put the updated key on your claim ([how](/guides/gnupg?id=update-the-key-on-your-claim)). One transaction, no new signature.

Look yourself up on thurin.id and press **Check proofs**: the proof gets a check mark.
