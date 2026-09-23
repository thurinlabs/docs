# Records

A record is a small value hung on a claim: one per claim per kind, up to 1 KB, set only by the owner, readable by anyone, clearable. The registry looks a record up by kind and cannot list them, so readers ask for the kinds they know. This page is that list.

An identity page shows its records under the **Records** tab: [thurin.id/ens/thurinlabs.eth/records](https://thurin.id/ens/thurinlabs.eth/records). Set one from the CLI:

```bash
thurin record set canary "All keys under my control as of 2026-09-23."
thurin record get thurinlabs.eth canary
thurin record clear canary
```

`thurin.` is the default namespace, so `canary` means `thurin.canary`. `--no-key` and `--authorize` work on record writes as on claims, so the address that owns the claim never has to hold ETH.

## Kinds Thurin defines

| kind | what it says | value |
|---|---|---|
| `thurin.railgun` | pay me privately by name | a Railgun `0zk1…` address |
| `thurin.security` | send sensitive reports here | a URL or a contact line; encrypt to the key on the claim |
| `thurin.successor` | my next key | the fingerprint of the key that replaces this one |
| `thurin.affiliation` | I'm with this identity | `{"v":1,"with":"<address or name>","role":"…"}`; `role` optional |
| `thurin.canary` | nothing compromised as of a date | a statement containing an ISO date, clearsigned or plain |
| `thurin.private` | a box only I can read | an armored PGP message encrypted to your own key |
| `thurin.disclosure` | a box for people I choose | an armored PGP message encrypted to their keys |
| `thurin.pointer` | what Thurin Labs put out | the release list behind [Verify a release](/guides/verify-release); not shown on identity pages |

Simple kinds are UTF-8 text. Structured kinds are small JSON with a `v`; readers ignore fields they do not know. Encrypted kinds are armored PGP messages, shown as "encrypted, N bytes" and never decrypted by the page.

A value that does not fit its kind is still shown, as text, with the reason. Nothing is hidden and nothing is trusted.

## What a record proves

That the owner of the claim said it, at the block it was set, and has not cleared it. That is all. A `thurin.railgun` record says "pay me here"; it does not prove control of the 0zk address. A `thurin.affiliation` record is one side's statement until the other side sets a matching one. A `thurin.successor` record names a key; the named key's own claim is the proof.

## Your own kinds

Anyone can define a kind. Use a reverse-dot name from a domain you control, `com.example.thing`, and document its value format where people can find it. Thurin's tools will read it (`thurin record get <identity> com.example.thing`) and the identity page will show it as text. No registration, no permission.

The kind on-chain is `keccak256` of the name. Every set emits a `RecordSet` event, so history survives a clear.
