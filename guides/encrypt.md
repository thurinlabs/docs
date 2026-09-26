# Encrypt to an identity

Every verified claim carries a full PGP key, usually with an encryption subkey. Thurin.id finds the right one for a name, so you can encrypt a message or a file to `bendoubleu.eth` without asking anyone for their key. Only the owner's key can open it.

## In the browser

Open the identity and choose **Encrypt**: `thurin.id/ens/<name>/encrypt`. Write a message or choose a file, then **Encrypt**.

- A message comes back as an armored block to copy or download (`message-for-<name>.asc`).
- A file comes back as `<file>.gpg`.

Everything happens in the tab. The page uses the key it already checked, fetches nothing new, and uploads nothing; Thurin never sees the message. Deliver it any way you like: email, chat, a USB stick. The recipient opens it with `gpg --decrypt`.

## From a terminal

```bash
echo "meet at noon" | thurin encrypt bendoubleu.eth > note.asc   # a message, armored
thurin encrypt bendoubleu.eth report.pdf                         # writes report.pdf.gpg
thurin encrypt bendoubleu.eth report.pdf --sign                  # signed with your own key too
```

The CLI hands the chosen key to gpg with `--recipient-file`, so nothing is imported into your keyring, and `--sign` works with your usual key. `-o` picks the output; `--armor` armors a file.

## Which key, and when it refuses

Only the **claim that counts**: the newest active claim that verifies. An unverified claim could be someone else's fake claim for that address, so it is never used. The page and the CLI refuse, in one sentence, when:

- no claim counts for the identity;
- its newest claim doesn't verify;
- its key has no encryption subkey (it can sign but not receive);
- its encryption subkey has expired.

When the key arrived in the **last 7 days**, both warn first: "This key was added 3 days ago. If you were expecting a different one, check with them another way." Someone holding a stolen wallet can only bring in their own key with a new claim, and a new claim is dated.

## What the message reveals

- **The recipient is hidden.** A normal PGP message names its recipient's key ID; with keys on-chain next to names, that would point straight at the person. Thurin.id leaves the ID out (gpg's `--throw-keyids`), and gpg finds the right key by trying each of the recipient's own: "anonymous recipient; trying secret key …". Lines like `ecdh failed … Checksum error` along the way only mean gpg tried a key that wasn't the one; it keeps going. With several keys on cards, it may ask for more than one PIN. `thurin encrypt --show-recipient` names the recipient, if you want that.
- **The sender is not proven.** The browser doesn't sign (a web page never holds your private key), so anyone could have sent it. To sign, use `thurin encrypt --sign`.

## For the recipient

Nothing to set up: `gpg --decrypt note.asc`. A hardware key works like any other message. Keep your encryption subkey current (`gpg --quick-set-expire <fingerprint> 2y '*'`, then **Update key** at [thurin.id/attest](https://thurin.id/attest)); an expired one means nobody can encrypt to you.
