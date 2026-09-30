# For security teams

You publish a PGP key so researchers can send vulnerability reports privately. That key usually lives in a SECURITY.md or a security.txt, and a reporter has to trust whatever served it. Keys also go stale.

Claim the key on Thurin.id and it gets a home nobody controls: tied to an address you publish, readable from any Ethereum node, and served as a key file that stops working the moment you revoke it.

## Put your key on Thurin.id

1. **Claim it** from an Ethereum address your team controls, at [thurin.id/attest](https://thurin.id/attest) or with the [CLI](/cli).
2. **Say which address is yours**, somewhere people already trust: your website, your repository, or an ENS name. That announcement is what ties the claim to your team.
3. **Point to it** from your policy, with the snippets below.
4. **Optionally**, put your contact on the claim too: a `thurin.security` [record](/records) (`thurin record set security "mailto:security@example.org"`).

## SECURITY.md

```markdown
## Encrypted reports

Encrypt sensitive reports to our PGP key:

Fingerprint: `XXXX XXXX XXXX XXXX XXXX  XXXX XXXX XXXX XXXX XXXX`
Key: https://thurin.id/pgp/<FINGERPRINT>.asc

The key is claimed on Ethereum by `0x<TEAM_ADDRESS>` (<team>.eth).
Before you send, check that the claim is current and made by that address:
https://thurin.id/pgp/<FINGERPRINT>
```

## security.txt

```
Contact: mailto:security@example.org
Encryption: openpgp4fpr:<FINGERPRINT>
Encryption: https://thurin.id/pgp/<FINGERPRINT>.asc
Expires: 2027-09-30T00:00:00.000Z
```

The first `Encryption` line names the key by its fingerprint, the form [RFC 9116](https://www.rfc-editor.org/rfc/rfc9116) uses. The second is where to get the current copy. `Expires` is required: set it a year out and renew it.

## How a reporter checks your key

Open `thurin.id/pgp/<FINGERPRINT>`. It shows who claimed the key, whether the claim verifies, and when it was made. The address should be the one you announced. For example, Thurin Labs' key: [thurin.id/pgp/08B9374FDFBEC67EFFA24E669D3D86E35361EF7B](https://thurin.id/pgp/08B9374FDFBEC67EFFA24E669D3D86E35361EF7B).

From a terminal, any of these fetch it:

```bash
curl -s https://thurin.id/pgp/<FINGERPRINT>.asc | gpg --import
gpg --keyserver hkps://keys.thurin.id --recv-keys <FINGERPRINT>
npx @thurinlabs/thurin@latest status <FINGERPRINT>
```

With `--recv-keys`, gpg checks that the key it got is the one the fingerprint names, so nothing in between can swap it. With `curl`, compare the fingerprint gpg prints.

## Rotating or retiring the key

- **Extend the expiry:** `gpg --quick-set-expire`, then **Update key** on thurin.id (or `thurin update-key`). No new signature.
- **Move to a new key:** `thurin reattest --key <new fingerprint>` replaces the claim in one transaction, and the old claim shows as replaced. Update the fingerprint in your policy.
- **Retire it:** `thurin revoke --reason retired`. The key file stops being served, and the claim shows as revoked.
- **It was stolen:** `thurin revoke --reason compromised` (or `--compromised` on a reattest). Every page then shows the key as compromised; this is final for that address.

## What a claim proves

- **It proves** the key was published by that Ethereum address, and that the key itself signed a line naming the address. It's public and permanent, and no server can change it.
- **It doesn't prove** the address is your team's. Your announcement does that, which is why step 2 matters.
- **It doesn't replace** your disclosure process or bug bounty: it makes the key reporters encrypt to checkable.
