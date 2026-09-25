# Proofs

A proof links your PGP key to an account on another platform, in both directions:

1. **The key points at the account.** A `proof@thurin.id` notation on your key holds a URL: a GitHub gist, a DNS name, a Farcaster cast, a Codeberg repo, a Mastodon profile.
2. **The account points back at the key.** What's at that URL contains your fingerprint as `openpgp4fpr:FINGERPRINT`.

Anyone can check both, so both must be controlled by the same person.

```
┌──────────┐   proof@thurin.id notation (a URL)   ┌──────────────────┐
│ PGP key  │ ───────────────────────────────────→ │ GitHub, DNS,     │
│          │ ←─────────────────────────────────── │ Farcaster, …     │
└──────────┘   openpgp4fpr:FINGERPRINT            └──────────────────┘
```

## Providers

| Provider | Where the fingerprint goes | Notation |
|---|---|---|
| [GitHub](/guides/github) | a public gist (or, for an organisation, a repo description) | `proof@thurin.id=https://gist.github.com/user/id` |
| [DNS](/guides/dns) | a TXT record | `proof@thurin.id=dns:example.com?type=TXT` |
| [Farcaster](/guides/farcaster) | a public cast | `proof@thurin.id=https://farcaster.xyz/user/0xhash` |
| [Codeberg](/guides/codeberg) | a repo description | `proof@thurin.id=https://codeberg.org/user/repo` |
| [Mastodon](/guides/mastodon) | a profile field or your bio | `proof@thurin.id=https://mastodon.social/@user` |

## What to put on the platform

The same line everywhere:

```
thurin-id=openpgp4fpr:YOUR_FINGERPRINT
```

The fingerprint is the full 40 hex characters, any case. The check only looks for `openpgp4fpr:` followed by your fingerprint; the `thurin-id=` label just tells a reader what the line is for.

## How a proof is checked

When someone looks you up, their browser (or the CLI):

1. reads the key stored in your claim, and checks your claim's signature against it;
2. reads the `proof@thurin.id` notations on the published name;
3. fetches each proof from its platform, and checks it contains your fingerprint and belongs to the account named;
4. shows a check mark, or the reason it failed.

It all runs on the reader's side. The only requests go to an Ethereum node and to the platforms themselves. Lookups don't cache proofs: one you delete stops verifying the next time someone looks.

## Before you start

- A [claim](/guides/getting-started) on thurin.id.
- A name on your key without an email. Notations on names that contain an email are left off the published key, unless you chose to include your email.
