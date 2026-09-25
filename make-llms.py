#!/usr/bin/env python3
"""Build llms.txt from the pages, in sidebar order. Run after editing any page: python3 make-llms.py"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = 'https://docs.thurin.id'

HEADER = f"""# Thurin.id docs, in one file

> Every page of {SITE}, in the sidebar's order, for AI agents and anyone who wants it all at once.
> Built from the pages by make-llms.py; the pages are the source.

Thurin.id puts a PGP key on an Ethereum address: a claim in a contract nobody controls, checkable with gpg and
any Ethereum node. Proofs on the key link it to accounts elsewhere. An agent can drive everything with the CLI
(`npx @thurinlabs/thurin`, `--json`, exit codes) or with only `cast` and gpg (see PGPRegistry below).
"""


def pages():
    """Page paths in sidebar order, the home page first."""
    out = ['README.md']
    for m in re.finditer(r'\]\((/[^)\s]*)\)', (ROOT / '_sidebar.md').read_text()):
        p = m.group(1).strip('/')
        if p:
            out.append(p + '.md')
    return out


def absolute(text):
    """Site links → full docs URLs (docsify routes through #/), so they work outside the site."""
    def fix(m):
        path, anchor = m.group(1), m.group(2) or ''
        return f']({SITE}/#{path or "/"}{anchor})'
    return re.sub(r'\]\((/[^)\s?#]*)(\?id=[^)\s]*)?\)', fix, text)


def demote(text):
    """Page headings drop one level so each page sits under its own ## title; code blocks untouched."""
    out, fence = [], False
    for line in text.splitlines():
        if line.startswith('```'):
            fence = not fence
        if not fence and re.match(r'#{1,5} ', line):
            line = '#' + line
        out.append(line)
    return '\n'.join(out)


parts = [HEADER]
for p in pages():
    body = (ROOT / p).read_text().strip()
    url = f'{SITE}/#/' + ('' if p == 'README.md' else p[:-3])
    parts.append(f'---\n\n<!-- {url} -->\n\n' + demote(absolute(body)))
(ROOT / 'llms.txt').write_text('\n\n'.join(parts) + '\n')
print(f'llms.txt: {len(parts) - 1} pages')
