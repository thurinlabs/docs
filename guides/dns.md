# DNS

A TXT record on your domain with your fingerprint in it.

## 1. Add a TXT record

On the domain itself (name `@` or blank), with the value:

```
thurin-id=openpgp4fpr:YOUR_FINGERPRINT
```

It doesn't interfere with other records. Check it's live with `dig TXT example.com +short`. A subdomain such as `_thurin.example.com` works too; use it in the notation below.

## 2. Add the notation

```
proof@thurin.id=dns:example.com?type=TXT
```

([how](/guides/gnupg)). For a subdomain: `proof@thurin.id=dns:_thurin.example.com?type=TXT`.

## 3. Update the key on your claim

[One transaction, no new signature](/guides/gnupg?id=update-the-key-on-your-claim).

## What's checked

The domain's TXT records are fetched through Cloudflare's DNS-over-HTTPS resolver, and one of them must contain `openpgp4fpr:` followed by your fingerprint. New records can take a few minutes to show.

On thurin.id it shows as `✓ DNS example.com`, linking to the domain.
