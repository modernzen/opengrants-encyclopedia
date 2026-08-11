#!/usr/bin/env python3
"""
Validator for the OpenGrants Encyclopedia.

Checks every article in content/ against docs/ARTICLE-CONTRACT.md and against
data/taxonomy.json, then writes data/manifest.json and data/link-graph.json.

Usage:
    python3 scripts/validate.py              # validate + write manifest
    python3 scripts/validate.py --check      # validate only, non-zero exit on error
    python3 scripts/validate.py --json       # machine-readable report to stdout

Exit codes:
    0  no errors (warnings may exist)
    1  errors found
    2  could not run (missing files, bad taxonomy)

No third-party dependencies beyond PyYAML.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required:  pip install pyyaml\n")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DATA = ROOT / "data"

# ---------------------------------------------------------------- constants

REQUIRED_FRONTMATTER = [
    "title", "slug", "url", "hub", "hubUrl", "articleType", "schemaType",
    "metaDescription", "primaryEntity", "primaryQuestion", "secondaryQuestions",
    "definedTerms", "author", "reviewer", "lastFactCheck", "nextReviewDue",
    "volatileFacts", "isAccessibleForFree", "disclosure",
]

ARTICLE_TYPES = {"concept", "process", "program", "comparison", "glossary", "hub"}
SCHEMA_TYPES = {"Article", "TechArticle"}

# Contract §9 — banned phrasing. Matched case-insensitively on word boundaries.
BANNED_PHRASES = [
    r"in today's fast-paced world", r"it's important to note that",
    r"it is important to note that", r"\bdelve\b", r"navigate the complexities",
    r"the landscape of", r"\bunlock\b", r"\bharness\b", r"robust ecosystem",
    r"stakeholder alignment", r"in conclusion", r"game-changing",
    r"game changing", r"revolutionary", r"at the end of the day",
    r"when it comes to", r"that being said", r"\bsynergies\b",
    r"paradigm.shift",
]

# Contract §5 — banned temporal markers in body prose.
BANNED_TEMPORAL = [
    r"\bcurrently\b", r"\brecently\b", r"as of this writing",
    r"at the time of writing", r"\bthis year\b", r"\bthe new rule\b",
    r"\bjust announced\b", r"\bthe latest\b", r"\bnowadays\b",
]

# Contract §6 — anaphora banned as first referring expression after a heading.
ANAPHORA_OPENERS = re.compile(
    r"^(this|these|those|it|they|the above|as mentioned|the former|the latter|"
    r"such|that)\b",
    re.IGNORECASE,
)

MAX_ANSWER_CHARS = 320
ANSWER_WORDS = (35, 70)          # tolerance band around the 40–60 target
MIN_CITATIONS = 8
MAX_PARAGRAPH_WORDS = 120
SECTION_WORDS = (100, 500)       # tolerance band around the 150–350 target

MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")

# Contract §10 — the Related topics block, from its H2 to the next H2 or EOF.
RELATED_TOPICS_BLOCK = re.compile(
    r"^##[ \t]+Related topics[ \t]*$.*?(?=^##[ \t]|\Z)",
    re.MULTILINE | re.DOTALL | re.IGNORECASE,
)


# ---------------------------------------------------------------- helpers

def split_frontmatter(text: str):
    """Return (frontmatter_dict, body_str). Raises ValueError on malformed input."""
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("unterminated YAML frontmatter")
    raw = text[3:end]
    body = text[end + 4:]
    fm = yaml.safe_load(raw)
    if not isinstance(fm, dict):
        raise ValueError("frontmatter is not a mapping")
    return fm, body


def strip_noncontent(body: str) -> str:
    """Remove fenced code, blockquote callouts, and tables before prose checks."""
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"^\s*>.*$", "", body, flags=re.MULTILINE)      # callouts
    body = re.sub(r"^\s*\|.*$", "", body, flags=re.MULTILINE)     # tables
    return body


def strip_related_topics(body: str) -> str:
    """Remove the Related topics block — contract §10 carve-out.

    Related topics is a navigation surface, not prose: it may link the hub and
    every sibling it names even when the body already linked them.
    """
    return RELATED_TOPICS_BLOCK.sub("", body)


def sections(body: str):
    """Yield (level, heading_text, section_body) for every heading."""
    lines = body.split("\n")
    idx = [(i, m) for i, l in enumerate(lines) if (m := HEADING.match(l))]
    for n, (i, m) in enumerate(idx):
        end = idx[n + 1][0] if n + 1 < len(idx) else len(lines)
        yield len(m.group(1)), m.group(2).strip(), "\n".join(lines[i + 1:end])


def first_words(text: str, limit: int) -> str:
    return " ".join(text.split()[:limit])


def paragraphs(text: str):
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block or block.startswith(("#", "|", ">", "-", "*", "1.")):
            continue
        yield block


# ---------------------------------------------------------------- validation

class Report:
    """Three severities.

    error  — contract violation; must be fixed.
    gate   — publish gate, expected to be open during drafting (e.g. no named
             reviewer yet). Blocks `--publish` but not authoring.
    warn   — advisory.
    """

    def __init__(self):
        self.errors: list[tuple[str, str]] = []
        self.gates: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []

    def error(self, path, msg):
        self.errors.append((str(path), msg))

    def gate(self, path, msg):
        self.gates.append((str(path), msg))

    def warn(self, path, msg):
        self.warnings.append((str(path), msg))


def validate_article(path: Path, fm: dict, body: str, taxonomy_urls: set,
                     rep: Report) -> dict:
    rel = path.relative_to(ROOT)
    is_hub = fm.get("articleType") == "hub"

    # -- frontmatter ------------------------------------------------------
    for key in REQUIRED_FRONTMATTER:
        if key not in fm:
            rep.error(rel, f"frontmatter missing required key: {key}")

    if fm.get("articleType") not in ARTICLE_TYPES:
        rep.error(rel, f"invalid articleType: {fm.get('articleType')!r}")
    if fm.get("schemaType") not in SCHEMA_TYPES:
        rep.error(rel, f"invalid schemaType: {fm.get('schemaType')!r}")

    reviewer = fm.get("reviewer") or {}
    if reviewer.get("name") in (None, "", "REVIEWER_REQUIRED"):
        rep.gate(rel, "awaiting named human reviewer (YMYL publish gate)")

    meta = fm.get("metaDescription") or ""
    if not 120 <= len(meta) <= 200:
        rep.warn(rel, f"metaDescription is {len(meta)} chars (target 150–160)")

    # volatileFacts rows must be structured and sourced
    for i, vf in enumerate(fm.get("volatileFacts") or []):
        if not isinstance(vf, dict):
            rep.error(rel, f"volatileFacts[{i}] is not a mapping")
            continue
        for k in ("item", "value", "source", "verified"):
            if k not in vf:
                rep.error(rel, f"volatileFacts[{i}] missing key: {k}")

    # -- headings ---------------------------------------------------------
    h1s = [t for lvl, t, _ in sections(body) if lvl == 1]
    if len(h1s) != 1:
        rep.error(rel, f"expected exactly 1 H1, found {len(h1s)}")
    elif h1s[0].strip() != str(fm.get("title", "")).strip():
        rep.error(rel, "H1 does not match frontmatter title")

    structural_h2 = {
        "key takeaways", "frequently asked questions", "related topics",
        "sources", "how the pieces fit together", "where should you start",
    }
    h2s = [t for lvl, t, _ in sections(body) if lvl == 2]
    for h in h2s:
        norm = h.rstrip("?").strip().lower()
        if norm in structural_h2:
            continue
        if not h.strip().endswith("?"):
            rep.error(rel, f"H2 is not a question: {h!r}")

    for lvl, heading, sec in sections(body):
        if lvl != 2:
            continue
        clean = strip_noncontent(sec).strip()
        if not clean:
            continue
        opener = clean.lstrip("*_ ").split("\n", 1)[0]
        if ANAPHORA_OPENERS.match(opener):
            rep.error(rel, f"anaphora opens section {heading!r}: "
                           f"{first_words(opener, 8)!r}")
        wc = len(clean.split())
        if not SECTION_WORDS[0] <= wc <= SECTION_WORDS[1] and \
                heading.rstrip("?").strip().lower() not in structural_h2:
            rep.warn(rel, f"section {heading!r} is {wc} words "
                          f"(target {SECTION_WORDS[0]}–{SECTION_WORDS[1]})")

    # -- direct answer block ----------------------------------------------
    after_h1 = body.split("\n", 1)[1] if "\n" in body else ""
    m = HEADING.search(after_h1)
    lead = after_h1[:m.start()] if m else after_h1
    lead_paras = list(paragraphs(strip_noncontent(lead)))
    if not lead_paras:
        rep.error(rel, "no direct-answer block found after H1")
    else:
        ans = lead_paras[0]
        n = len(ans.split())
        if not ANSWER_WORDS[0] <= n <= ANSWER_WORDS[1]:
            rep.error(rel, f"direct-answer block is {n} words (target 40–60)")
        if len(ans) > MAX_ANSWER_CHARS:
            rep.error(rel, f"direct-answer block is {len(ans)} chars "
                           f"(max {MAX_ANSWER_CHARS})")
        if ANAPHORA_OPENERS.match(ans):
            rep.error(rel, "direct-answer block opens with anaphora")

    # -- prose checks -----------------------------------------------------
    prose = strip_noncontent(body)
    low = prose.lower()
    for pat in BANNED_PHRASES:
        if re.search(pat, low):
            rep.error(rel, f"banned phrase: {pat}")
    for pat in BANNED_TEMPORAL:
        if re.search(pat, low):
            rep.error(rel, f"banned temporal marker in body prose: {pat}")

    for para in paragraphs(prose):
        n = len(para.split())
        if n > MAX_PARAGRAPH_WORDS:
            rep.warn(rel, f"paragraph is {n} words (max {MAX_PARAGRAPH_WORDS}): "
                          f"{first_words(para, 8)}…")

    # -- links ------------------------------------------------------------
    links = MD_LINK.findall(body)
    internal, external = [], []
    for anchor, href in links:
        (internal if href.startswith("/") else external).append((anchor, href))

    for anchor, href in links:
        if anchor.strip().lower() in {"click here", "read more", "this article",
                                      "here", "link"}:
            rep.error(rel, f"non-descriptive anchor text: {anchor!r}")

    for anchor, href in internal:
        base = href.split("#")[0]
        if base and base not in taxonomy_urls:
            rep.error(rel, f"internal link to unknown URL: {href}")

    ext_urls = {h for _, h in external}
    if not is_hub and len(ext_urls) < MIN_CITATIONS:
        rep.error(rel, f"only {len(ext_urls)} unique external citations "
                       f"(minimum {MIN_CITATIONS})")

    # duplicate internal targets. Contract §10 carve-outs: Related topics and the
    # glossary are navigation surfaces, so repeat links there are not duplicates.
    seen = defaultdict(int)
    if path.name != "glossary.md":
        for _, href in MD_LINK.findall(strip_related_topics(body)):
            if href.startswith("/"):
                seen[href.split("#")[0]] += 1
    hub_url = fm.get("hubUrl")
    for href, count in seen.items():
        if count > 1 and href != hub_url:
            rep.warn(rel, f"internal target linked {count}× : {href}")

    words = len(prose.split())
    per_1k = len(internal) / max(words / 1000, 1)
    if per_1k > 8 and not is_hub:
        rep.warn(rel, f"{per_1k:.1f} internal links per 1,000 words (max 8)")

    # -- required sections -------------------------------------------------
    lowered = [h.lower() for h in h2s]
    for req in ("sources",):
        if not any(req in h for h in lowered):
            rep.error(rel, f"missing required section: {req}")
    if not is_hub and not any("related topics" in h for h in lowered):
        rep.warn(rel, "missing Related topics section")

    return {
        "slug": fm.get("slug"),
        "title": fm.get("title"),
        "url": fm.get("url"),
        "hub": fm.get("hub"),
        "articleType": fm.get("articleType"),
        "schemaType": fm.get("schemaType"),
        "primaryQuestion": fm.get("primaryQuestion"),
        "secondaryQuestions": fm.get("secondaryQuestions") or [],
        "definedTerms": fm.get("definedTerms") or [],
        "wordCount": words,
        "citationCount": len(ext_urls),
        "internalLinks": sorted({h.split("#")[0] for _, h in internal}),
        "externalSources": sorted(ext_urls),
        "volatileFacts": fm.get("volatileFacts") or [],
        "lastFactCheck": str(fm.get("lastFactCheck") or ""),
        "nextReviewDue": str(fm.get("nextReviewDue") or ""),
        "reviewerAssigned": reviewer.get("name") not in
                            (None, "", "REVIEWER_REQUIRED"),
        "path": str(path.relative_to(ROOT)),
    }


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="validate only; do not write manifest")
    ap.add_argument("--json", action="store_true",
                    help="emit a machine-readable report on stdout")
    ap.add_argument("--publish", action="store_true",
                    help="also fail on open publish gates (unassigned reviewers)")
    args = ap.parse_args()

    taxonomy_path = DATA / "taxonomy.json"
    if not taxonomy_path.exists():
        sys.stderr.write("data/taxonomy.json not found\n")
        return 2
    taxonomy = json.loads(taxonomy_path.read_text())

    expected: dict[str, dict] = {}
    taxonomy_urls = {"/encyclopedia/", "/encyclopedia/glossary/",
                     "/editorial-policy/", "/corrections/",
                     "/authors/sedale-turbovsky/"}
    for hub in taxonomy["hubs"]:
        taxonomy_urls.add(hub["url"])
        for child in hub["children"]:
            url = f"{hub['url']}{child['slug']}/"
            taxonomy_urls.add(url)
            expected[url] = {"hub": hub["key"], **child}

    rep = Report()
    manifest_articles = []
    seen_urls = set()

    for path in sorted(CONTENT.rglob("*.md")):
        try:
            fm, body = split_frontmatter(path.read_text())
        except ValueError as exc:
            rep.error(path.relative_to(ROOT), f"frontmatter error: {exc}")
            continue
        entry = validate_article(path, fm, body, taxonomy_urls, rep)
        manifest_articles.append(entry)
        if entry["url"] in seen_urls:
            rep.error(path.relative_to(ROOT), f"duplicate url: {entry['url']}")
        seen_urls.add(entry["url"])

    # coverage against taxonomy
    for url, meta in expected.items():
        if url not in seen_urls:
            rep.error("taxonomy", f"declared in taxonomy but no file: {url}")
    for hub in taxonomy["hubs"]:
        if hub["url"] not in seen_urls:
            rep.error("taxonomy", f"hub page missing: {hub['url']}")

    # orphan check — every article needs an inbound link from a non-hub page
    inbound = defaultdict(set)
    for a in manifest_articles:
        for target in a["internalLinks"]:
            inbound[target].add(a["url"])
    for a in manifest_articles:
        if a["articleType"] == "hub":
            continue
        sources = inbound.get(a["url"], set())
        non_hub = {s for s in sources
                   if s not in {h["url"] for h in taxonomy["hubs"]}}
        if not sources:
            rep.error(a["path"], "ORPHAN: no inbound internal links")
        elif not non_hub:
            rep.warn(a["path"], "only inbound link is from its hub")

    # ---------------------------------------------------------------- output
    if not args.check:
        manifest = {
            "generator": "scripts/validate.py",
            "name": taxonomy["name"],
            "baseUrl": taxonomy["baseUrl"],
            "articleCount": len(manifest_articles),
            "totalWords": sum(a["wordCount"] for a in manifest_articles),
            "totalCitations": sum(a["citationCount"] for a in manifest_articles),
            "articlesAwaitingReviewer": sum(
                1 for a in manifest_articles if not a["reviewerAssigned"]),
            "articles": sorted(manifest_articles, key=lambda a: a["url"]),
        }
        (DATA / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

        graph = {
            "nodes": [{"url": a["url"], "title": a["title"], "hub": a["hub"],
                       "type": a["articleType"]} for a in manifest_articles],
            "edges": [{"from": a["url"], "to": t}
                      for a in manifest_articles for t in a["internalLinks"]],
        }
        (DATA / "link-graph.json").write_text(json.dumps(graph, indent=2) + "\n")

    if args.json:
        print(json.dumps({
            "errors": [{"path": p, "message": m} for p, m in rep.errors],
            "gates": [{"path": p, "message": m} for p, m in rep.gates],
            "warnings": [{"path": p, "message": m} for p, m in rep.warnings],
            "articleCount": len(manifest_articles),
        }, indent=2))
    else:
        by_path = defaultdict(list)
        for p, m in rep.errors:
            by_path[p].append(("ERROR", m))
        for p, m in rep.gates:
            by_path[p].append(("gate ", m))
        for p, m in rep.warnings:
            by_path[p].append(("warn ", m))
        for p in sorted(by_path):
            print(f"\n{p}")
            for level, msg in by_path[p]:
                print(f"  {level}  {msg}")
        print(f"\n{len(manifest_articles)} articles · "
              f"{sum(a['wordCount'] for a in manifest_articles):,} words · "
              f"{len(rep.errors)} errors · {len(rep.gates)} publish gates · "
              f"{len(rep.warnings)} warnings")

    if rep.errors:
        return 1
    if args.publish and rep.gates:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
