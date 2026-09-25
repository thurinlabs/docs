# Records

A record is a short text on a claim: one per name, up to 1 KB, set only by the owner, readable by anyone. The registry lists every record on a claim (`recordsOf`), so nothing needs to know a name in advance. This page says what the `thurin.` names mean.

An identity page shows its records under the **Records** tab: [thurin.id/ens/thurinlabs.eth/records](https://thurin.id/ens/thurinlabs.eth/records), the `thurin.` kinds first, then anyone else's as plain text. Connect the wallet that holds the claim and the same tab lets you set and clear Thurin.id's plain kinds, and clear the others. Or from the CLI:

```bash
thurin record set canary "All keys under my control as of 2026-09-25."
thurin record get thurinlabs.eth canary
thurin record clear canary
```

Names are `a-z 0-9 - .`, up to 31 bytes. `thurin.` is the default, so `canary` means `thurin.canary`. `--no-key` and `--authorize` work on records as on claims, so the address that owns the claim never has to hold ETH.

When you replace a claim, its records move to the new one. If the key changed, sign a new canary: the old one was signed by the old key.

## Kinds Thurin.id defines

| kind | what it says | value |
|---|---|---|
| `thurin.railgun` | pay me privately by name | a Railgun `0zk1…` address |
| `thurin.security` | send sensitive reports here | a URL or a contact line; encrypt to the key on the claim |
| `thurin.successor` | my next key | the fingerprint of the key that replaces this one |
| `thurin.affiliation` | I'm with this identity | `{"v":1,"with":"<address or name>","role":"…"}`; `role` optional |
| `thurin.canary` | nothing compromised as of a date | a dated line (`2026-09-25`), clearsigned with the claim's key; an unsigned one shows as unsigned |
| `thurin.releases` | the releases I put out | a list of releases, each with the sha256 of its checksum file; kept by `thurin record add-release` ([how people check one](/guides/verify-release)) |
| `thurin.private` | a box only I can read | an armored PGP message encrypted to your own key (read-only; see below) |
| `thurin.disclosure` | a box for people I choose | an armored PGP message encrypted to their keys (read-only; see below) |

Simple kinds are UTF-8 text. Structured kinds are small JSON with a `v`; readers ignore fields they do not know. Encrypted kinds are armored PGP messages, shown as "encrypted, N bytes" and never decrypted by the page.

Thurin.id's tools read and show the encrypted kinds but don't help you write them, on purpose. A record stays in the chain's history forever, so anything encrypted there can be read by whoever gets a recipient's key later, however many years later. A PGP message also names the keys it was encrypted to, which ties you to those people in public. Share secrets some other way.

A value that does not fit its kind is still shown, as text, with the reason. Nothing is hidden and nothing is trusted.

## What a record proves

That the owner of the claim said it, at the block it was set, and has not cleared it. That is all. A `thurin.railgun` record says "pay me here"; it does not prove control of the 0zk address. A `thurin.affiliation` record is one side's statement until the other side sets a matching one. A `thurin.successor` record names a key; the named key's own claim is the proof.

## Your own kinds

Anyone can define a kind. Use a reverse-dot name from a domain you control, `com.example.thing`, within 31 bytes, and document its value format where people can find it. Set it with `thurin record set com.example.thing "<value>"`, or `setRecord` on the [contract](/contracts). Thurin.id's tools read it (`thurin record get <identity> com.example.thing`), and the identity page shows it as text; there, the owner can clear it but not edit it. No registration, no permission.

## Records are forever

Clearing a record takes it off the claim, but every value it ever had stays in the chain's history, in the `RecordSet` event of the transaction that set it. Don't publish anything you'd want back.
