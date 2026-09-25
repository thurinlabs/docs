# Mastodon

Your fingerprint on your profile: in a profile field, or in your bio.

## 1. Add it to your profile

In your server's profile settings, add a field:

- **Label:** `Thurin.id` (or anything)
- **Value:** `thurin-id=openpgp4fpr:YOUR_FINGERPRINT`

For a clickable link instead, use `https://thurin.id/pgp/YOUR_FINGERPRINT` as the value; it contains the fingerprint too. Either works in your bio as well. Mastodon is the one provider that also accepts the 16-character key ID in place of the full fingerprint.

## 2. Add the notation

With your profile's URL ([how](/guides/gnupg)):

```
proof@thurin.id=https://mastodon.social/@alice
```

## 3. Update the key on your claim

[One transaction, no new signature](/guides/gnupg?id=update-the-key-on-your-claim).

## What's checked

The account is fetched from its own server's public API, and a profile field or the bio must contain your fingerprint (or key ID). It checks the profile itself, not a post, so there's nothing to delete by accident; just keep the fingerprint there. Works with any Mastodon-compatible server.

On thurin.id it shows as `✓ MASTODON @alice@mastodon.social`, linking to the profile.
