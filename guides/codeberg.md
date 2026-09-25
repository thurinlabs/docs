# Codeberg

A repository whose description holds your fingerprint.

## 1. Make a repository

On [codeberg.org](https://codeberg.org), create a public repository, for example `thurin-proof`, with this description:

```
thurin-id=openpgp4fpr:YOUR_FINGERPRINT
```

It can be empty; only the description matters. Your account's visibility must be **Public**.

## 2. Add the notation

With the repository's URL ([how](/guides/gnupg)):

```
proof@thurin.id=https://codeberg.org/USERNAME/thurin-proof
```

## 3. Update the key on your claim

[One transaction, no new signature](/guides/gnupg?id=update-the-key-on-your-claim).

## What's checked

The repository is fetched from the Codeberg API. It must belong to the account in the URL, and its description must contain `openpgp4fpr:` followed by your fingerprint. It's checked whenever someone checks your proofs, so keep it public.

On thurin.id it shows as `✓ CODEBERG username`, linking to your profile and to the repository.
