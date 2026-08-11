#!/usr/bin/env python3
"""
Sync the derived `citationCount` and `wordCount` frontmatter values in every
article under content/ with what the file actually contains.

Both figures are computed exactly the way scripts/validate.py computes them, so
the frontmatter and the generated manifest always agree:

    citationCount  unique external links in the body (href not starting with "/")
    wordCount      body words after stripping fenced code, blockquote callouts,
                   and tables

Only those two scalar values are rewritten, in place, by line. Every other key,
its order, and the surrounding YAML formatting are left untouched.

Usage:
    python3 scripts/sync-counts.py            # rewrite files that are out of date
    python3 scripts/sync-counts.py --check    # report only, exit 1 if any drift
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import MD_LINK, split_frontmatter, strip_noncontent  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

COUNT_LINE = re.compile(r"^(citationCount|wordCount):[ \t]*(\S+)[ \t]*$")


def counts(body: str) -> dict[str, int]:
    external = {href for _, href in MD_LINK.findall(body)
                if not href.startswith("/")}
    return {
        "citationCount": len(external),
        "wordCount": len(strip_noncontent(body).split()),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report drift without rewriting")
    args = ap.parse_args()

    drift = 0
    files = 0
    for path in sorted(CONTENT.rglob("*.md")):
        text = path.read_text()
        try:
            _, body = split_frontmatter(text)
        except ValueError as exc:
            sys.stderr.write(f"{path.relative_to(ROOT)}: {exc}\n")
            return 2

        want = counts(body)
        end = text.find("\n---", 3)
        head, tail = text[:end], text[end:]

        lines = head.split("\n")
        changed = []
        for i, line in enumerate(lines):
            m = COUNT_LINE.match(line)
            if not m:
                continue
            key, old = m.group(1), m.group(2)
            new = str(want[key])
            if old != new:
                lines[i] = f"{key}: {new}"
                changed.append(f"{key} {old} -> {new}")

        if not changed:
            continue
        drift += len(changed)
        files += 1
        print(f"{path.relative_to(ROOT)}: {', '.join(changed)}")
        if not args.check:
            path.write_text("\n".join(lines) + tail)

    verb = "out of date" if args.check else "updated"
    print(f"\n{drift} values {verb} across {files} files")
    return 1 if (args.check and drift) else 0


if __name__ == "__main__":
    sys.exit(main())
