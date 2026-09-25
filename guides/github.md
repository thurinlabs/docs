# GitHub

A public gist with your fingerprint in it. An organisation can't own a gist, so it uses a repository description instead ([below](/guides/github?id=for-an-organisation)).

## 1. Make a public gist

At [gist.github.com](https://gist.github.com), create a **public** gist with any filename and this content:

```
thurin-id=openpgp4fpr:YOUR_FINGERPRINT
```

Other text around it is fine.

## 2. Add the notation

With the gist's URL ([how](/guides/gnupg)):

```
proof@thurin.id=https://gist.github.com/USERNAME/GIST_ID
```

## 3. Update the key on your claim

[One transaction, no new signature](/guides/gnupg?id=update-the-key-on-your-claim).

## For an organisation

1. Create a public repository under the organisation, for example `thurin-proof`, and set its **description** to `thurin-id=openpgp4fpr:YOUR_FINGERPRINT`.
2. Add `proof@thurin.id=https://github.com/ORG/thurin-proof` as the notation on the organisation's key.
3. Update the key on the organisation's claim.

A personal account can use a repository too.

## What's checked

The gist (or repository) is fetched from the GitHub API. It must belong to the account in the URL, so pointing at someone else's gist doesn't work, and its content (or description) must contain `openpgp4fpr:` followed by your fingerprint. It's checked on every lookup, so keep it public and don't delete it.

On thurin.id it shows as `✓ GITHUB username`, linking to your profile and to the gist.
