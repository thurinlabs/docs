# Verify a deploy

Every Thurin site is a folder on IPFS, named by its content ID (CID). This guide rebuilds a site from its public source and checks you get the same CID, which proves the site you load is exactly that code, with nothing added.

You need `git`, Node 20 or newer (for thurin.id), and [kubo](https://docs.ipfs.tech/install/command-line/) (`ipfs`). Nothing is uploaded and no IPFS daemon is needed: kubo only computes the hash. Run `ipfs init` once if you have never used it.

## 1. Find the live CID

thurin.id and thurinlabs.id are also published under ENS names, and any ENS gateway reports the CID it serves:

```bash
curl -sI https://id.thurinlabs.eth.limo/ | grep -i x-ipfs-roots     # thurin.id
curl -sI https://thurinlabs.eth.limo/ | grep -i x-ipfs-roots        # thurinlabs.id
```

Or read the contenthash of `id.thurinlabs.eth` / `thurinlabs.eth` in any ENS app.

## 2. Find the deploy tag

Every deploy is a signed tag in the site's repository, named `deploy-YYYY-MM-DD-HHMM` (UTC), whose message names the CID it put live. Pick the tag whose CID matches step 1 and check its signature:

```bash
git clone https://github.com/thurinlabs/thurin-id && cd thurin-id    # or docs, thurinlabs, mathom-site
git tag -l 'deploy-*' --format='%(refname:short)  %(contents:body)' | grep -B1 -A2 <CID>
gpg --keyserver hkps://keys.thurin.id --recv-keys 6E0053911942A889426C1866E34D9266098F7FE7
git tag -v deploy-YYYY-MM-DD-HHMM
```

The key `6E00…7FE7` is claimed on-chain by [ben.thurinlabs.eth](https://thurin.id/ens/ben.thurinlabs.eth); `keys.thurin.id` serves it from the registry.

## 3a. Rebuild docs, thurinlabs.id, or mathom

These sites have no build step. The published folder is exactly the files in the tagged commit:

```bash
mkdir /tmp/site && git archive deploy-YYYY-MM-DD-HHMM | tar -x -C /tmp/site
ipfs add --only-hash -r -Q --cid-version 1 --hidden /tmp/site
```

The printed CID should equal the one in the tag and step 1.

## 3b. Rebuild thurin.id

thurin.id bundles [identity-kit](/sdk) from a sibling folder, at the kit commit the tag names (`identity-kit <commit>` in the tag message). The production build settings are committed in `.env.production`.

```bash
mkdir /tmp/rebuild && cd /tmp/rebuild
git clone https://github.com/thurinlabs/identity-kit
git clone https://github.com/thurinlabs/thurin-id
git -C identity-kit checkout <kit commit from the tag message>
git -C thurin-id checkout deploy-YYYY-MM-DD-HHMM
(cd identity-kit && npm ci && npm run build)
cd thurin-id && npm ci
THURIN_COMMIT=$(git rev-parse HEAD) npm run build
ipfs add --only-hash -r -Q --cid-version 1 --hidden dist
```

The printed CID should equal the one in the tag and step 1. We checked this with Node 20, 22, and 24: the lockfiles pin everything that matters, so the Node version doesn't change the result. `THURIN_COMMIT` is the commit stamp that thurin.id shows in its page source (`<meta name="thurin-commit">`).

## If it doesn't match

- Make sure you used the tag, not a branch, and for thurin.id the kit commit from the tag message.
- Deploys of docs, thurinlabs.id, and mathom before 24 September 2026, 16:54 UTC uploaded the working folder rather than the commit, and deploys of thurin.id before 24 September 2026, 17:36 UTC used settings that weren't committed; those can't be rebuilt this way.
- Anything else is worth reporting: see the `security` record on [thurinlabs.eth](https://thurin.id/ens/thurinlabs.eth/records).
