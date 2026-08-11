# The OpenGrants Encyclopedia

An evergreen, reference-grade guide to how public and philanthropic funding actually works, and how to win it. **75 articles, ~222,000 words, ~1,000 primary-source citations**, structured for classic search, generative engines, and answer engines simultaneously.

This repository is the **content source of truth**. It contains no site code. A build agent renders it into `opengrants.io/encyclopedia/`.

---

## What is in here

```
content/                        75 Markdown articles — the encyclopedia
  index.md                      root index (/encyclopedia/)
  glossary.md                   180-term glossary
  {hub}/index.md                8 pillar hub pages
  {hub}/{slug}.md               65 cluster articles
data/
  taxonomy.json                 site map — hubs, children, URLs, order
  manifest.json                 generated: per-article metadata, links, citations
  link-graph.json               generated: nodes and edges for the internal link graph
  glossary.json                 180 terms with definitions, sources, and cross-refs
docs/
  ARTICLE-CONTRACT.md           binding spec every article satisfies
  BUILD-NOTES.md                what the build agent needs to do
  RESEARCH-BASIS.md             the evidence behind the content architecture
schema/
  *.jsonld                      JSON-LD templates per page type
scripts/
  validate.py                   contract validator + manifest generator
  sync-counts.py                recomputes wordCount / citationCount frontmatter
  gen-llms-txt.py               regenerates llms.txt from the taxonomy
llms.txt                        machine-readable index fragment (generated)
CONTRIBUTING.md                 how to add, revise, or correct an article
```

---

## The eight hubs

| Hub | Articles | Covers |
|---|---|---|
| `foundations` | 7 | What a grant is, who funds what, how the cycle moves |
| `finding-funding` | 7 | Search strategy, NOFO reading, funder research, pipeline, go/no-go |
| `readiness` | 6 | Eligibility, SAM.gov/UEI, readiness assessment, fiscal sponsorship, controls |
| `proposal-craft` | 11 | Every proposal section, reviewer psychology, compliance, rejection |
| `budgets` | 8 | Cost categories, indirect rates, match, allowability, cash flow |
| `evidence` | 7 | Logic models, theory of change, evaluation plans, evidence tiers, data sources |
| `funding-tracks` | 9 | Federal, state/local, foundation, corporate, DAF, SBIR, NIH/NSF |
| `award-management` | 10 | Notice of Award, reporting, monitoring, audit, closeout, grants operations |

---

## Quick start

```bash
pip install pyyaml
python3 scripts/validate.py            # validate + regenerate manifest.json and link-graph.json
python3 scripts/validate.py --json     # machine-readable report
python3 scripts/validate.py --publish  # also fail on open publish gates
python3 scripts/sync-counts.py --check # dry-run the frontmatter count sync
```

Current state: **0 errors, 17 advisory warnings, 75 open publish gates.**

---

## ⚠️ Before anything ships

**Every article carries `reviewer.name: REVIEWER_REQUIRED` and will not pass `--publish` until a named human replaces it.**

This is deliberate, not an oversight. Grant content sits in Google's **YMYL Financial Security** *and* **Government/Civics** categories — the Search Quality Rater Guidelines define YMYL as topics where content "could significantly impact the health, financial stability, or safety of people." Articles here state eligibility rules, regulatory thresholds, and financial mechanics. A second named human with domain credentials must review each one and take accountability for it.

Assign a reviewer by replacing the frontmatter block:

```yaml
reviewer:
  name: "Jane Doe"
  credentials: "Grant Professional Certified; 14 years federal grants administration"
  reviewDate: "2026-09-01"
```

Every article was drafted with primary sources fetched and read, and a factual-consistency pass corrected several defects (see `docs/BUILD-NOTES.md`). That reduces reviewer burden. It does not replace the reviewer.

**Also required before launch:**

- Publish `/authors/sedale-turbovsky/` with a 150+ word bio, credentials, photo, and `sameAs` links. Every article references it.
- Publish `/editorial-policy/` and `/corrections/`. Every article footer links them.
- Verify AI crawler access in `robots.txt` before publishing anything. See `docs/BUILD-NOTES.md` — a blocked crawler is a hard zero regardless of content quality.

---

## How this stays evergreen

The architectural bet is **volatility isolation**. Roughly 95% of every article is written to be true in five years — mechanisms, definitions, processes, decision logic, failure modes. The remaining 5% — rates, thresholds, deadlines, success rates — is quarantined into a single **Current Figures** callout per article, each row carrying its own primary-source deep link and verification date, mirrored into the `volatileFacts` frontmatter array.

Body prose names the mechanism and never the number. It says "the de minimis indirect cost rate set in the Uniform Guidance," not the percentage.

The payoff: a stale figure is a one-line fix rather than a rewrite, and you can query the corpus for every unverified figure:

```bash
python3 -c "
import json
m = json.load(open('data/manifest.json'))
for a in m['articles']:
    for f in a['volatileFacts']:
        print(f['verified'], a['url'], f['item'])
" | sort
```

Refresh cadence:

| Tier | Cadence | Updates `dateModified`? |
|---|---|---|
| Current Figures callouts | Quarterly, or at the funding-cycle boundary | No — update the callout's own `verified` date |
| Full article review | Annually (`nextReviewDue`) | Only if content substantively changed |
| Structural refresh | Every 24 months | Yes |
| Correction | Within 72h of discovery | Yes, plus a corrections-log entry |

**Never bump `dateModified` on a build, a typo fix, or a CSS change.** Google explicitly names date manipulation without substantive change as a negative signal.

---

## The article contract

`docs/ARTICLE-CONTRACT.md` is binding and the validator enforces it mechanically. The short version:

- **Every H2 is a natural-language question**, answered completely in the first 40–60 words beneath it.
- **Every section stands alone.** No anaphora after a heading, entity re-anchored per section, no backward references. A retriever that pulls one section must get a correct, complete answer.
- **Direct-answer block**: 40–60 words, ≤320 characters, entity named in the first clause.
- **8–15 external citations per article**, inline at the claim, majority `.gov` primary sources, at least one attributed direct quotation.
- **Zero uncited numbers.** No dollar figure, percentage, date, or eligibility rule without a linked source.
- **Named author and reviewer**, visible dates, editorial policy and commercial disclosure linked.
- **Neutral reference tone.** At most one product link per article. The encyclopedia earns trust by being useful when it is not selling.

---

## Why it is built this way

The structure follows measured evidence, not folklore. `docs/RESEARCH-BASIS.md` has the full citation set. The load-bearing findings:

- The **Princeton GEO study** (KDD 2024, 10,000 queries) measured citation-density, direct quotation, and statistics-addition at **+30–40% visibility** in generative engines — with *Statistics Addition* strongest in the **Law & Government** domain, which is exactly this corpus. It also measured **keyword stuffing at 10% *worse* than baseline** and authoritative tone inflation at **no significant effect**. Both are banned by the contract.
- **Ahrefs (863K SERPs, March 2026)**: only **37.9%** of AI-Overview-cited URLs rank in the top 10, down from 76.1% in July 2025. Engines increasingly cite pages matching **fan-out sub-queries**, not head terms. Hence one question per H2.
- **Google's own AI optimization guidance** states no special markup, Markdown, or AI text file is required for its generative features. Schema here exists for entity disambiguation and rich results, never as a citation tactic.
- **Google's March 2026 core update**: government, institutional, and specialist sources gained; **aggregators and directory sites lost**. An encyclopedia published by a grant discovery platform is structurally at risk of reading as an aggregator. The counter is editorial substance — original synthesis, named accountable authors, primary-source citation, transparent methodology.
- **FAQPage and HowTo rich results are dead** (FAQ ended May 2026). FAQ sections stay because they capture People Also Ask and fan-out queries, not because of markup.

One anti-pattern deserves naming directly: Google's spam policies define **scaled content abuse** as generating many pages primarily to manipulate rankings. Seventy-five articles in one topical area is structurally similar. What distinguishes this corpus is named authorship, dense primary-source citation, original synthesis, and human review. **Stagger publication rather than shipping all 75 at once**, and do not skip the reviewer step.

---

## Content notes for the build agent

- **Front-load nothing volatile into templates.** The Current Figures callout should render as a distinct component so it can be batch-audited and styled as clearly time-bound.
- **Slugs are immutable.** A stable URL is the atom of citation accrual. Never rename one post-publication.
- **Body text must be server-rendered.** No JS-dependent prose, no gating, no email walls, no interstitials. A page a crawler cannot read is worth nothing.
- **Every schema value must appear in the visible text.** Google's explicit requirement.
- `data/link-graph.json` gives you the full internal link graph — use it for orphan detection in CI and for building "related" modules.

See `docs/BUILD-NOTES.md` for the full implementation checklist.

---

## Provenance

Researched and drafted August 2026 against primary sources — eCFR, grants.gov, SAM.gov, SBIR.gov, IRS, GAO, CRS, agency policy statements, peer-reviewed research on grant review, and sector research from Candid, the Center for Effective Philanthropy, GrantStation, and Giving USA. Every citation was fetched and read during drafting, and a factual-consistency pass corrected vintage drift, misattribution, and one unsupported regulatory claim.

Nothing here is legal, tax, accounting, or audit advice.
