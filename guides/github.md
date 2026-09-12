# GitHub Proof

Verify your GitHub identity with a public gist containing your PGP fingerprint. An **organisation** can't own a gist, so it uses a repository instead: see [For organisations](#for-organisations) below.

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

## 3. Publish the Updated Key on Thurin

Thurin reads proofs from the key stored in your on-chain claim, not from a keyserver, so the new notation goes live when the stored key is updated:

1. Open [thurin.id/attest](https://thurin.id/attest), connect the wallet that holds your claim, and open **Your claims**.
2. Click **Update** on the active claim and paste a fresh export of your key:
   ```bash
   gpg --export-options export-minimal,no-export-attributes --armor --export YOUR_FINGERPRINT
   ```
3. Check the summary (published name, proof count), click **Update key**, and confirm the transaction.

No new signature is needed — the fingerprint is unchanged. Names that contain an email address are left out automatically unless you chose to include them when you attested.

## For organisations

Gists belong to user accounts. An organisation proves its GitHub with a **repository description** instead, the same way a Codeberg proof works:

1. Create a public repository under the organisation, for example `thurin-proof`, and set its **description** to:
   ```
   thurin-id=openpgp4fpr:YOUR_FINGERPRINT
   ```
2. Add the repository URL as the notation on the organisation's key:
   ```
   proof@thurin.id=https://github.com/ORG/thurin-proof
   ```
3. Update the key on the organisation's claim as in step 3 above.

Thurin fetches the repository through the GitHub API, checks that its owner is the account named in the URL, and looks for the fingerprint token in the description. The proof shows the organisation's name and links to the repository. A personal account can use this form too.

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
- The gist URL must match `https://gist.github.com/:username/:gist_id`, or the repository URL `https://github.com/:owner/:repo`
- Do not delete the gist — Thurin re-verifies on each lookup

## Notes

- GitHub API allows 60 requests/hour without authentication, which is fine for a lookup tool
- Verification happens entirely client-side (GitHub API supports CORS)
