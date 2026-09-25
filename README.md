# Thurin.id

> Prove more. Reveal less.

Thurin.id puts your PGP key on your Ethereum address. The claim lives in a contract on Ethereum that nobody controls, and anyone can check it with gpg and any Ethereum node. Proofs on the key link it to your accounts elsewhere: GitHub, a domain, Farcaster, Codeberg, Mastodon.

There's no Thurin server in the middle. [thurin.id](https://thurin.id), the CLI, and the library all read the chain directly.

## Start here

- [Getting started](/guides/getting-started): a key, a claim, and your first proof
- [Proofs](/guides/proofs): how a key points at an account and back
- [Managing notations](/guides/gnupg): adding and removing proofs with gpg

## Tools

- [thurin.id](https://thurin.id): look anyone up, or [add your key](https://thurin.id/attest)
- [Thurin CLI](/cli): the same from a terminal, plus a keyserver gpg can use
- [Identity Kit](/sdk): the library, a React card, and an embed for any page
- [PGPRegistry](/contracts): the contract, usable on its own from Etherscan or `cast`

## More

- [Records](/records): small values on a claim, like a security contact or a canary
- [Verify commits](/guides/verify-commits), [a release](/guides/verify-release), or [a deploy](/guides/verify-deploy) with nothing but gpg and the chain
- [Roadmap](/roadmap) · [CROPS](/crops): what we can and can't do to you
- For AI agents: [llms.txt](https://docs.thurin.id/llms.txt), everything on one page
