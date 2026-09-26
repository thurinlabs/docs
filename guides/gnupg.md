# Managing notations

A proof is a `proof@thurin.id` notation on your key. This page adds, lists, and removes them with gpg, then puts the updated key on your claim.

## Add a notation

```bash
gpg --edit-key YOUR_FINGERPRINT
```

Pick the name without an email (the one that gets published), then add the notation:

```
gpg> list
gpg> uid 1
gpg> notation
Enter the notation: proof@thurin.id=dns:example.com?type=TXT
gpg> save
```

`uid 1` selects the first name; `list` shows which number is which, and a `*` marks the selected one. Repeat `notation` for each proof.

In one line, without the prompt:

```bash
printf 'uid 1\nnotation\nproof@thurin.id=dns:example.com?type=TXT\nsave\n' | gpg --batch --command-fd 0 --edit-key YOUR_FINGERPRINT
```

## List them

```bash
gpg --list-options show-notations --list-sigs YOUR_FINGERPRINT
```

## Remove one

Same as adding, with a `-` in front of the value:

```
gpg> uid 1
gpg> notation
Enter the notation: -proof@thurin.id=dns:example.com?type=TXT
gpg> save
```

## Update the key on your claim

thurin.id reads proofs from the key stored in your claim, never from a keyserver. After any change, put the new key on-chain: one transaction, no new signature.

**On the site:** open [thurin.id/attest](https://thurin.id/attest), connect the wallet that holds the claim, open **Your claims**, and click **Update**. Paste the output of the command the page shows:

```bash
gpg --export-options export-minimal,no-export-attributes --armor --export YOUR_FINGERPRINT
```

Check the summary (names, proof count), then **Update key**.

**From a terminal:** `thurin update-key`. See the [CLI](/cli).

Names containing an email stay off unless you chose to include your email.

## Moving to a new key

Make the new key, then add it with **New claim** on the attest page and pick your current claim under **Replace an existing claim**. The old claim is revoked and the new one published in the same transaction, and your records move to the new claim. If the old key may be in someone else's hands, tick **The old key was compromised**: that marks it so, and this address can never claim it again.

Found out later? Under **Your claims**, a revoked or replaced claim has **Mark compromised**. It works once per claim.
