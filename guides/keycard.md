# Your key on a Keycard Shell

The [Keycard Shell](https://keycard.tech) can hold your PGP key. It makes the key from its own seed, shows exactly what it signs on its own screen, and talks to thurin.id by QR code. Nothing to install: the computer or phone is only the camera.

> **Firmware first.** PGP signing on the Shell is in review ([keycard-shell #227](https://github.com/keycard-tech/keycard-shell/pull/227)). Until a firmware release includes it, this works only on test builds.

## Claim a key with the Shell

1. Open [thurin.id/attest](https://thurin.id/attest) and connect the wallet for your address.
2. In step 2, choose **Key on a signing device? Sign by QR instead**.
3. **The first time, create the key on the Shell:** choose **No key on the device yet? Create one** and give it a name (plain letters and punctuation; no email needed). Scan the QR with the Shell, check the name it shows, approve, and enter its PIN. Then **Scan the answer** on the page.
   - **Download your public key** and keep the file. The Shell makes keys but can't show one again; the page shows the key's creation time, and the same name at that same time makes the same key. Once claimed, the key is on-chain too: `thurin.id/pgp/<fingerprint>.asc`.
   - **Already made one?** Paste or open that file instead.
4. **Sign:** scan the page's QR with the Shell. It shows the line to sign (`I control the Ethereum address: 0x…`), your key's fingerprint, and the date. Approve, then **Scan the answer**.

From there it's the same as with gpg: the page checks the signature against the key and the exact line, shows what goes on-chain, and **Publish** asks your wallet.

## The camera

- It turns on only when you press **Scan the answer**, and off as soon as the answer is read or you leave the step. Pictures stay in the tab; nothing is uploaded.
- Only thurin.id's own page can ask for it; frames inside the page can't.
- No camera? **or a photo of it** reads a single QR from a picture. Answers that span several frames need the camera.

## Notes

- The Shell's PGP key is secp256k1, made from the Shell's seed on its own path, apart from your wallet accounts.
- The CLI takes the same key and a detached signature from any tool that reads the Shell's QR: `thurin attest --key-file … --statement-file …` ([details](/cli?id=no-eth-on-this-machine)).
- The QR format is plain OpenPGP inside `UR:BYTES`: the request names the line and two times, the answer is a standard key or signature. Another device that speaks it would work the same way.
