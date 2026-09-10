# DNS Proof

Verify domain ownership by adding a TXT record containing your PGP fingerprint.

## 1. Add a DNS TXT Record

Add a TXT record to your domain with the value:

```
thurin-id=openpgp4fpr:YOUR_FINGERPRINT
```

This can be a root-level TXT record (name: `@` or blank). You can verify it's live:

```bash
dig TXT example.com +short
```

> **Tip:** You can also use a subdomain like `_thurin.example.com` to keep things organized. Just adjust the notation URI accordingly.

## 2. Add the Notation to Your PGP Key

Use the `dns:` URI scheme ([GnuPG guide](/guides/gnupg)):

```bash
gpg --edit-key YOUR_FINGERPRINT
uid 1
notation proof@thurin.id=dns:example.com?type=TXT
save
```

If using a subdomain:

```
proof@thurin.id=dns:_thurin.example.com?type=TXT
```

## 3. Upload Your Updated Key

```bash
gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_FINGERPRINT
```

## What Thurin Checks

1. Extracts the domain from the `dns:` URI
2. Queries TXT records via Cloudflare DNS-over-HTTPS:
   ```
   https://cloudflare-dns.com/dns-query?name=example.com&type=TXT
   ```
3. Searches all TXT records for `openpgp4fpr:FINGERPRINT`
4. Shows a green checkmark if the fingerprint matches

## What It Looks Like on Thurin

```
✓  DNS  example.com
```

The domain links to `https://example.com`.

## Requirements

- The TXT record must be publicly resolvable
- The notation URI must use the format `dns:DOMAIN?type=TXT`
- The TXT record value must contain `openpgp4fpr:` followed by your 40-character fingerprint

## Notes

- DNS propagation can take up to 48 hours, though most providers propagate within minutes
- The TXT record won't conflict with existing MX, A, SPF, or other records
- Verification happens entirely client-side via Cloudflare's DoH endpoint (supports CORS)
