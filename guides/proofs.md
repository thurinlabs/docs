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

The fingerprint is the full one, any case: 40 hex characters for most keys, 64 for newer (v6) keys. The check looks for `openpgp4fpr:` followed by your fingerprint (Mastodon also takes the bare fingerprint or the 16-character key ID); the `thurin-id=` label just tells a reader what the line is for.

## How a proof is checked

When someone looks you up, their browser (or the CLI, which checks unless run with `--no-proofs`):

1. reads the key stored in your claim, and checks your claim's signature against it;
2. reads the `proof@thurin.id` notations on the published name and lists them, marked **not checked**;
3. when they press **Check proofs**, fetches each proof from its platform, and checks it contains your fingerprint and belongs to the account named;
4. shows a check mark, or the reason it failed.

Proofs are checked only when asked because checking tells each platform the reader's IP and which identity they're looking at. Someone who wants every page checked can choose "Always check" in the thurin.id footer; it's saved in their browser. Until then, a handle is just text anyone could have typed into their own key, so it never shows a check mark.

It all runs on the reader's side. The only requests go to an Ethereum node and, once asked, to the platforms themselves. Nothing caches proofs: one you delete stops verifying the next time someone checks.

## Before you start

- A [claim](/guides/getting-started) on thurin.id.
- A name on your key without an email. Notations on names that contain an email are left off the published key, unless you chose to include your email.
