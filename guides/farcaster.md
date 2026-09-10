# Farcaster Proof

Verify your Farcaster identity by publishing a cast containing your PGP fingerprint.

## 1. Publish a Proof Cast

Post a cast on Farcaster (via any client). The cast text must include the `openpgp4fpr:` token with your fingerprint. Use the standard Thurin format so it's self-explanatory:

```
Verifying my identity with @thurinlabs

thurin-id=openpgp4fpr:YOUR_FINGERPRINT
```

You can add any other text — a clickable link to your Thurin profile (`https://thurin.id/pgp/YOUR_FINGERPRINT`) is a nice touch — as long as the cast contains `openpgp4fpr:` followed by your fingerprint.

## 2. Add the Notation to Your PGP Key

Copy the cast URL from Farcaster and add it as a notation ([GnuPG guide](/guides/gnupg)):

```bash
gpg --edit-key YOUR_FINGERPRINT
uid 1
notation proof@thurin.id=https://farcaster.xyz/USERNAME/0xCASTHASH
save
```

## 3. Upload Your Updated Key

```bash
gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_FINGERPRINT
```

## What Thurin Checks

1. Extracts the cast hash from the Farcaster URL
2. Fetches the cast via a Farcaster Hub REST API
3. Searches the cast text for `openpgp4fpr:FINGERPRINT`
4. Shows a green checkmark if the fingerprint matches

## What It Looks Like on Thurin

```
✓  FARCASTER  @username  [proof]
```

The username links to your Farcaster profile. The `[proof]` link opens the specific cast.

## Requirements

- The cast must be public (not a direct cast or channel-restricted)
- The cast URL must match `https://farcaster.xyz/:username/0x:hash`
- Do not delete the cast — Thurin re-verifies on each lookup

## Notes

- Your proof cast is permanent on the Farcaster protocol — even if deleted from a client, it may persist on hubs
- Verification is client-side via the [Neynar](https://neynar.com) Farcaster Hub API
