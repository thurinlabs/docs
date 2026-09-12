# Managing Notations with GnuPG

This guide covers how to add, list, and remove `proof@thurin.id` notations from your PGP key using GnuPG (GPG).

## Adding a Notation

Open your key for editing:

```bash
gpg --edit-key YOUR_FINGERPRINT
```

Select your **published name** — the user ID without an email that Thurin publishes on-chain (see [Getting Started](/guides/getting-started)). List the user IDs with `list`, pick its number, then add the notation:

```
gpg> list
gpg> uid 1
gpg> notation
```

A `*` marks the selected user ID. Notations on a user ID that contains an email address are left out when the key is published, so they won't show on Thurin.

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

## Publishing the Updated Key on Thurin

Thurin reads proofs from the key stored in your on-chain claim. After any notation change, put the new key on-chain — one transaction, no new signature:

1. Open [thurin.id/attest](https://thurin.id/attest), connect the wallet that holds your claim, and open **Your claims**.
2. Click **Update** on the active claim and paste a fresh export:
   ```bash
   gpg --export-options export-minimal,no-export-attributes --armor --export YOUR_FINGERPRINT
   ```
3. Check the summary (published name, proof count), click **Update key**, and confirm.

Keyservers are optional and unrelated: Thurin never reads from keys.openpgp.org, so uploading there neither helps nor hurts your Thurin identity.

## Rotating to a New Key

If you move to a different key, run the attest flow again with the new key. At the publish step, choose to replace your existing claim — it is revoked and the new one published in the same transaction.
