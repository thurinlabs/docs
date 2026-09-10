# GitHub Proof

Verify your GitHub identity by creating a public gist containing your PGP fingerprint.

## 1. Create a Public Gist

Go to [gist.github.com](https://gist.github.com) and create a **public** gist.

- **Filename:** `thurin-proof.md` (or any name)
- **Content:**

```
thurin-id=openpgp4fpr:YOUR_FINGERPRINT
```

The gist can contain additional text. Thurin only looks for `openpgp4fpr:` followed by your fingerprint.

## 2. Add the Notation to Your PGP Key

Copy the gist URL and add it as a notation ([GnuPG guide](/guides/gnupg)):

```bash
gpg --edit-key YOUR_FINGERPRINT
uid 1
notation proof@thurin.id=https://gist.github.com/USERNAME/GIST_ID
save
```

## 3. Upload Your Updated Key

```bash
gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_FINGERPRINT
```

## What Thurin Checks

1. Extracts the gist ID from the notation URL
2. Fetches the gist via the GitHub API (`api.github.com/gists/:id`)
3. Searches all file contents for `openpgp4fpr:FINGERPRINT`
4. Shows a green checkmark if the fingerprint matches

## What It Looks Like on Thurin

```
✓  GITHUB  username  [proof]
```

The username links to your GitHub profile. The `[proof]` link opens the gist directly.

## Requirements

- The gist must be **public**
- The gist URL must match `https://gist.github.com/:username/:gist_id`
- Do not delete the gist — Thurin re-verifies on each lookup

## Notes

- GitHub API allows 60 requests/hour without authentication, which is fine for a lookup tool
- Verification happens entirely client-side (GitHub API supports CORS)
