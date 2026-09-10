# Managing Notations with GnuPG

This guide covers how to add, list, and remove `proof@thurin.id` notations from your PGP key using GnuPG (GPG).

## Adding a Notation

Open your key for editing:

```bash
gpg --edit-key YOUR_FINGERPRINT
```

Select your user ID, then add the notation:

```
gpg> uid 1
gpg> notation
```

Enter the notation as `proof@thurin.id=VALUE`:

```
proof@thurin.id=dns:example.com?type=TXT
```

Save and exit:

```
gpg> save
```

You can add multiple `proof@thurin.id` notations — one per proof. Repeat the `notation` command for each.

## Listing Notations

From inside `--edit-key`:

```
gpg> showpref
```

This shows all preferences including notations at the bottom.

Or from the command line:

```bash
gpg --list-options show-notations --list-sigs YOUR_FINGERPRINT
```

## Removing a Notation

Open your key for editing:

```bash
gpg --edit-key YOUR_FINGERPRINT
```

Select your user ID, then remove a specific notation by prefixing it with `-`:

```
gpg> uid 1
gpg> notation
```

Enter the notation to remove with a minus sign:

```
-proof@thurin.id=dns:example.com?type=TXT
```

Save:

```
gpg> save
```

## Uploading to the Keyserver

After any notation changes, upload your updated key to `keys.openpgp.org`:

```bash
gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_FINGERPRINT
```

Or export and upload manually:

```bash
gpg --export --armor YOUR_FINGERPRINT | curl -T - https://keys.openpgp.org
```

You can also use the web upload at [keys.openpgp.org/upload](https://keys.openpgp.org/upload).

> **Note:** Thurin fetches keys from the keyserver. Your updated notations won't appear in Thurin until the key is uploaded.

## Re-attesting on-chain

If your on-chain key data is outdated, you may also need to re-attest at [thurin.id/attest](https://thurin.id/attest) so the on-chain key matches the keyserver version. Thurin prefers the keyserver copy when available.
