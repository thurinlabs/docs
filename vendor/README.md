# vendor/

The docs site's scripts and theme, served from this site instead of a CDN: no third party
sees visitors, and an upstream release changes nothing here until a file is replaced. Each
file is copied unchanged from the npm package named (MIT licensed).

| file | from (npm) | sha256 |
|---|---|---|
| docsify.min.js | `docsify@4.13.1` `lib/docsify.min.js` | `9123f808d3f6ad736b4a8f99944a611f87c5d4f9328030080a5c029ed5f450a5` |
| theme-simple-dark.css | `docsify-themeable@0.9.0` `dist/css/theme-simple-dark.css` | `a05dac59df1ac7850a59d64c54a23c8763fb204fe80c0f6d000dc8a8ff78231f` |
| prism-typescript.min.js | `prismjs@1.30.0` `components/prism-typescript.min.js` | `852f5513bb9ca9db247f86ecfce74acc91c541749d34929157240518fef8152a` |
| prism-solidity.min.js | `prismjs@1.30.0` `components/prism-solidity.min.js` | `02cb534101e8aa8b4e77b373ddfc327087ae2b5603fc1e82d56b4fba4d046dec` |
| prism-bash.min.js | `prismjs@1.30.0` `components/prism-bash.min.js` | `6260814110e5182f2956e3bd257429548d9dbf2a9b66a63719b26cf9fac966a7` |

To update: `npm pack <pkg>@<version>`, copy the file from `package/`, check `sha256sum`, update the row.
