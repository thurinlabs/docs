# Farcaster

A public cast with your fingerprint in it.

## 1. Post a cast

From any Farcaster client:

```
Verifying my identity with @thurinlabs

thurin-id=openpgp4fpr:YOUR_FINGERPRINT
```

Any other text is fine, as long as the cast contains `openpgp4fpr:` followed by your fingerprint. A link to `https://thurin.id/pgp/YOUR_FINGERPRINT` is a nice touch.

## 2. Add the notation

With the cast's URL ([how](/guides/gnupg)):

```
proof@thurin.id=https://farcaster.xyz/USERNAME/0xCASTHASH
```

## 3. Update the key on your claim

[One transaction, no new signature](/guides/gnupg?id=update-the-key-on-your-claim).

## What's checked

The username in the URL is resolved to its Farcaster account, and the cast is looked up among that account's casts, so it must be one you posted. Its text must contain your fingerprint. By default this is read from a public Farcaster node that needs no key (Quilibrium's Hypersnap node); the [library](/sdk) can use another. Don't delete the cast: it's checked on every lookup.

On thurin.id it shows as `✓ FARCASTER @username`, linking to your profile and to the cast.
