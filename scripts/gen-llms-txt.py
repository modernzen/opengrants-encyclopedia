#!/usr/bin/env python3
"""Generate llms.txt from data/taxonomy.json, data/manifest.json, and article frontmatter.

llms.txt is a derived artifact. Never hand-edit it — edit the taxonomy or the
article frontmatter and regenerate, so the file cannot drift from the corpus.

    python3 scripts/gen-llms-txt.py            # write llms.txt
    python3 scripts/gen-llms-txt.py --check    # exit 1 if llms.txt is stale

Titles come from data/taxonomy.json. URLs come from the taxonomy's URL
conventions. One-line descriptions are each article's own `metaDescription`
frontmatter value, verbatim — no descriptions are written by hand here.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY = ROOT / "data" / "taxonomy.json"
MANIFEST = ROOT / "data" / "manifest.json"
OUT = ROOT / "llms.txt"

META_RE = re.compile(r'^metaDescription:\s*"(.*)"\s*$', re.M)
URL_RE = re.compile(r'^url:\s*"(.*)"\s*$', re.M)

HEADER_NOTE = """<!--
llms.txt for the OpenGrants Encyclopedia.

Honest framing: this file is cheap insurance, not a demonstrated growth lever.
Google states plainly that it does not use AI text files of any kind. Ahrefs,
reading server logs from 137,000 domains, found that 97% of llms.txt files
received zero requests in May 2026, and AI retrieval bots accounted for 1.1% of
the requests that did arrive; Originality.ai's scan of 3M+ sites shows adoption
up 8.8x year over year while reads stay near zero.
https://ppc.land/llms-txt-adoption-rises-8-8x-but-97-of-files-get-zero-ai-requests/
We publish it because it costs nothing. Nothing in the encyclopedia's
architecture depends on it, and no one should report on it as a channel.

GENERATED FILE — do not hand-edit. Regenerate with:
    python3 scripts/gen-llms-txt.py
Source of truth: data/taxonomy.json, data/manifest.json, article frontmatter.
-->"""

INTRO = """> OpenGrants is a commercial grant discovery platform. The OpenGrants \
Encyclopedia is its open reference work on how public and philanthropic funding \
actually works: what a grant is and who gives them out, how to find and qualify \
opportunities, what a funder requires before it will fund you, how to write and \
budget a proposal, how to build an evidence base, how each funding track \
(federal, state, foundation, corporate, DAF, SBIR) differs, and what happens \
after an award lands. {count} articles, roughly {words:,} words, {cites:,} \
external citations weighted toward primary government sources."""

BODY_NOTE = """Every article names a human author and a human reviewer, carries \
visible published and last-reviewed dates, cites primary sources inline at the \
claim, and quarantines every figure that can change into a single dated "Current \
figures" callout with its own source links. Figures in those callouts are \
verified on a quarterly cadence and should still be checked against the linked \
source before anyone relies on them. Corrections: https://opengrants.io/corrections/"""


def load_meta_descriptions() -> dict[str, str]:
    """Map article URL -> metaDescription, read from content frontmatter."""
    out: dict[str, str] = {}
    for path in sorted((ROOT / "content").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        url = URL_RE.search(text)
        meta = META_RE.search(text)
        if url and meta:
            out[url.group(1)] = meta.group(1).strip()
    return out


def build() -> str:
    tax = json.loads(TAXONOMY.read_text(encoding="utf-8"))
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    descs = load_meta_descriptions()

    base = tax["baseUrl"].rstrip("/")
    root_path = tax["rootPath"]
    hub_pattern = tax["conventions"]["hubUrlPattern"]
    url_pattern = tax["conventions"]["urlPattern"]

    def absolute(path: str) -> str:
        return f"{base}{path}"

    def line(title: str, path: str) -> str:
        desc = descs.get(path, "")
        suffix = f": {desc}" if desc else ""
        return f"- [{title}]({absolute(path)}){suffix}"

    parts: list[str] = [HEADER_NOTE, "", f"# {tax['name']}", ""]
    parts.append(
        INTRO.format(
            count=man["articleCount"],
            words=man["totalWords"],
            cites=man["totalCitations"],
        )
    )
    parts += ["", BODY_NOTE, "", "## Start here", ""]
    parts.append(line("The OpenGrants Encyclopedia", root_path))
    parts.append(line("Grant Funding Glossary", "/encyclopedia/glossary/"))
    parts.append("")

    for hub in sorted(tax["hubs"], key=lambda h: h["order"]):
        hub_url = hub.get("url") or hub_pattern.format(hub=hub["slug"])
        parts.append(f"## {hub['title']}")
        parts.append("")
        parts.append(f"{hub['description']}")
        parts.append("")
        parts.append(line(f"{hub['title']} (hub)", hub_url))
        for child in hub["children"]:
            child_url = url_pattern.format(hub=hub["slug"], slug=child["slug"])
            parts.append(line(child["title"], child_url))
        parts.append("")

    parts += [
        "## Editorial",
        "",
        "Accountability surfaces for the encyclopedia. Every article links all three.",
        "",
        f"- [Author: Sedale Turbovsky]({base}/authors/sedale-turbovsky/): "
        "Bio, credentials, and verified profiles for the encyclopedia's author.",
        f"- [Editorial policy]({base}/editorial-policy/): Sourcing standards, "
        "review process, correction policy, AI-use disclosure, and commercial disclosure.",
        f"- [Corrections]({base}/corrections/): Public dated log of every correction, "
        "and the form for reporting an outdated figure.",
        "",
    ]
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if llms.txt does not match the taxonomy")
    args = ap.parse_args()

    generated = build()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != generated:
            print("llms.txt is stale — run: python3 scripts/gen-llms-txt.py",
                  file=sys.stderr)
            return 1
        print("llms.txt is current.")
        return 0

    OUT.write_text(generated, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} "
          f"({generated.count(chr(10)) + 1} lines).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
