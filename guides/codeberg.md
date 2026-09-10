# Codeberg Proof

Verify your Codeberg identity by creating a repository with your PGP fingerprint in its description.

## 1. Create a Proof Repository

Go to [codeberg.org](https://codeberg.org) and create a new repository.

- **Name:** `thurin-proof` (or anything you like)
- **Description:**

```
thurin-id=openpgp4fpr:YOUR_FINGERPRINT
```

The description can contain additional text. Thurin only looks for `openpgp4fpr:` followed by your fingerprint.

Make sure your account visibility is set to **Public**.

## 2. Add the Notation to Your PGP Key

Copy the repository URL and add it as a notation ([GnuPG guide](/guides/gnupg)):

```bash
gpg --edit-key YOUR_FINGERPRINT
uid 1
notation proof@thurin.id=https://codeberg.org/USERNAME/thurin-proof
save
```

## 3. Upload Your Updated Key

```bash
gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_FINGERPRINT
```

## What Thurin Checks

1. Extracts the username and repo name from the Codeberg URL
2. Fetches the repository via the Codeberg API (`/api/v1/repos/:user/:repo`)
3. Searches the repository description for `openpgp4fpr:FINGERPRINT`
4. Shows a green checkmark if the fingerprint matches

## What It Looks Like on Thurin

```
✓  CODEBERG  username  [proof]
```

The username links to your Codeberg profile. The `[proof]` link opens the proof repository.

## Requirements

- The repository must be **public**
- Your account visibility must be set to **Public**
- The repo URL must match `https://codeberg.org/:username/:repo`
- Do not delete the repository — Thurin re-verifies on each lookup

## Notes

- Codeberg runs on Forgejo, so this approach is compatible with the Keyoxide Forgejo proof method
- Verification uses the public Codeberg API (no authentication required)
- The repo can be empty — only the description matters
