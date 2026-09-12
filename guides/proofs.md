# Thurin Proofs

Thurin Proofs are a decentralized identity verification system that links your PGP key to your online accounts. By adding cryptographic proofs to your PGP key and publishing verification tokens on supported platforms, you create a verifiable chain of identity that anyone can check using [Thurin](https://thurin.id).

## How It Works

Thurin Proofs use a **bidirectional linking** model:

1. **Your PGP key points to your account** — A `proof@thurin.id` notation in your PGP key contains a URL to a proof on a platform (a GitHub gist, a DNS TXT record, a Farcaster cast, a Codeberg repo, a Mastodon profile).

2. **Your account points back to your key** — The proof contains your PGP fingerprint in `openpgp4fpr:FINGERPRINT` format.

Anyone can independently verify both directions, confirming that the same person controls both the PGP key and the account.

```
┌──────────────┐    proof@thurin.id notation    ┌────────────────────┐
│              │ ─────────────────────────────→ │    Platform        │
│   PGP Key    │    (URL to proof post)         │  (GitHub, DNS,     │
│              │                                │  Farcaster,        │
│              │ ←───────────────────────────── │  Codeberg, etc.)   │
└──────────────┘    openpgp4fpr:FINGERPRINT     └────────────────────┘
```

## Prerequisites

1. **A PGP key** attested on-chain at [thurin.id/attest](https://thurin.id/attest) (on-chain identity claim)
2. **GnuPG** installed locally to edit your key ([managing notations guide](/guides/gnupg))
3. **A published name** — a user ID on your key with no email address; proof notations go on it, and after adding them you update the key stored on your claim (*Your claims → Update* on thurin.id/attest)

## Supported Providers

| Provider | Proof Method | Notation Example |
|---|---|---|
| [Codeberg](/guides/codeberg) | Repo description | `proof@thurin.id=https://codeberg.org/user/repo` |
| [DNS](/guides/dns) | TXT record | `proof@thurin.id=dns:example.com?type=TXT` |
| [Farcaster](/guides/farcaster) | Public cast | `proof@thurin.id=https://farcaster.xyz/user/0xhash` |
| [GitHub](/guides/github) | Public gist | `proof@thurin.id=https://gist.github.com/user/id` |
| [Mastodon](/guides/mastodon) | Profile metadata | `proof@thurin.id=https://mastodon.social/@user` |

## Proof Content Format

All proofs must contain your PGP fingerprint using the `openpgp4fpr:` token:

```
openpgp4fpr:FINGERPRINT
```

Where `FINGERPRINT` is your full 40-character hex PGP fingerprint (case-insensitive).

The recommended format for proof content — used consistently across every provider — is:

```
thurin-id=openpgp4fpr:FINGERPRINT
```

Lead with the `thurin-id=` label so anyone who sees the proof knows what it is and why it's there. This exact string works on every provider: the `openpgp4fpr:` token satisfies GitHub, Codeberg, DNS, and Farcaster, and the embedded fingerprint satisfies Mastodon. The `thurin-id=` label itself is not required by verification (Thurin only checks for `openpgp4fpr:` followed by a matching fingerprint), so proofs created before this convention still work — but new proofs should include it.

## Verification Flow

When Thurin looks up an identity:

1. Reads the PGP public key stored in the on-chain attestation (after checking that the stored signature binds it to the address)
2. Parses `proof@thurin.id` notations from the key
3. For each notation, identifies the platform and fetches the proof content
4. Checks that the proof contains `openpgp4fpr:FINGERPRINT` matching the key
5. Displays a green checkmark for verified proofs, or an X with a reason for failures

All verification happens client-side in the browser. No backend, keyserver, or API keys are needed — the only network calls are to Ethereum and to the proof platforms themselves.
