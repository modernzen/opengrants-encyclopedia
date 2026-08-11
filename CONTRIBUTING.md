# Contributing to the OpenGrants Encyclopedia

How to add an article, revise one, or fix something that is wrong.

Two documents govern everything here and neither is optional reading:

- **`docs/ARTICLE-CONTRACT.md`** — binding. The validator enforces it mechanically.
- **`docs/RESEARCH-BASIS.md`** — why the contract says what it says, with evidence labels. Read it before proposing a change to the contract itself.

---

## The workflow

Six steps, in order. Skipping step 2 wastes a week. Skipping step 4 can cost the property.

### 1. Propose against the taxonomy

Every article belongs to exactly one hub in `data/taxonomy.json`. Before writing anything, open a proposal that answers four questions:

- **Which hub?** If it does not fit one of the eight, the proposal is either out of scope or a hub restructure — say which.
- **What is the primary entity?** One entity per article. "SBIR Phase I" is an entity. "SBIR stuff" is not.
- **What is the primary question?** The natural-language question a practitioner would type, phrased exactly as they would type it.
- **What are the 5–10 secondary questions?** These are the fan-out targets and they determine when the article is finished. If you cannot name eight real questions the article answers, the topic is probably a section of an existing article rather than a new one.

Add the entry to `data/taxonomy.json` — `slug`, `title`, `articleType`, `primaryQuestion` — as part of the proposal, not after drafting. Hub sizing runs 5 children minimum, 8–15 target, roughly 20 ceiling; past that, propose a hub split instead.

### 2. Check for duplication before you draft

**One entity, one canonical article.** Near-duplicate articles covering the same entity from slightly different angles are doorway pages under Google's spam policy — "sites or pages are created to rank for specific, similar search queries" — and they cannibalize each other regardless of policy.

Three checks:

1. **Search the existing corpus** for your primary entity and each secondary question. `data/manifest.json` carries every article's `primaryQuestion` and `secondaryQuestions` — 680 questions in total. If three of your eight questions are already answered elsewhere, you are proposing a section, not an article.
2. **Run the semantic-similarity check** against the corpus once a draft exists. Anything above **0.85 cosine similarity** with an existing article goes to merge review before it can be published.
3. **Prefer consolidating.** Expanding an existing article is almost always better than adding a near-neighbour. The corpus wins by being the canonical answer, not by having more URLs.

### 3. Draft against the contract

`docs/ARTICLE-CONTRACT.md` end to end, before writing. The parts most often missed:

- **Every H2 is a natural-language question ending in `?`**, and the first 40–60 words beneath it answer that question completely.
- **Every section stands alone.** No anaphora as the first referring expression after a heading. Re-anchor the primary entity by full name in every section. No "as defined above."
- **Zero volatile numbers in body prose.** See "Handling a volatile fact" below.
- **Neutral reference tone**, at most one product link, no pitch in the body.
- **Banned phrases are hard bans** (§9). The validator catches many of them; a reviewer catches the rest.

Copy the frontmatter block from `docs/ARTICLE-CONTRACT.md` §3 exactly. Do not rename or omit keys — the build reads them.

### 4. Verify every citation at source

**Open every URL. Read the passage. Confirm the claim it supports.**

Not "this looks like the right CFR section." Not "a search result said so." Not a citation carried over from another article without re-checking. Open it, read it, confirm it.

The standard the corpus is held to:

- **8–15 external citations per 2,000 words**, minimum 8.
- **Inline at the claim**, never batched only at the end.
- **Zero uncited numbers.** No dollar figure, percentage, date, count, or eligibility rule without a linked source.
- **Majority primary sources.** eCFR, Federal Register, grants.gov, SAM.gov, SBIR.gov, agency policy statements, GAO, CRS, IRS, Census. Secondary sources are welcome, labeled as what they are.
- **At least one attributed direct quotation**, in quotation marks, with a link.
- **Deep links**, to the specific section, not a program homepage.
- **Sources section** at the end: numbered, with publisher, title, URL, and access date.

### 5. Run the validator

```bash
pip install pyyaml
python3 scripts/validate.py              # validate + regenerate manifest.json and link-graph.json
python3 scripts/validate.py --json       # machine-readable report
python3 scripts/validate.py --publish    # also fails on open publish gates
python3 scripts/sync-counts.py --check   # dry-run the wordCount / citationCount sync
python3 scripts/gen-llms-txt.py          # regenerate llms.txt if the taxonomy changed
```

**Zero errors before review.** Warnings are advisory but each one needs a reason, not a shrug. Commit the regenerated `data/manifest.json` and `data/link-graph.json` alongside the article.

`--publish` will fail while `reviewer.name` is `REVIEWER_REQUIRED`. That is the gate working, not a bug. There is no bypass flag and none should be added.

### 6. Assign a reviewer

**A second named human with domain credentials, not the author.** Grant content sits in Google's YMYL Financial Security *and* Government/Civics categories: it states eligibility rules, regulatory thresholds, and financial mechanics that determine whether an organization gets funded and survives an audit. An unreviewed article is not publishable.

Replace the frontmatter block with real values:

```yaml
reviewer:
  name: "Jane Doe"
  credentials: "Grant Professional Certified; 14 years federal grants administration"
  reviewDate: "2026-09-01"
```

The reviewer checks factual accuracy and domain judgment — not prose. Their name goes on the published page. Give them time and give them the sources.

---

## Fabrication

**Fabrication is the one unrecoverable error.**

Do not invent a figure. Do not approximate a citation. Do not cite a source you did not open. Do not attribute a quotation you did not find. Do not carry a number from memory, from another article, or from a model's confident recollection into this corpus without opening the source and reading it.

If you cannot verify a figure, **omit it**. Say the qualitative thing plainly instead. A missing statistic costs nothing. A wrong one, in a corpus that tells people what they are eligible for and what they may charge to a federal award, costs a reader real money and costs the whole property its credibility at once.

This applies with equal force to facts about OpenGrants. Never invent an employee count, a founding date, an address, a customer number, or a performance metric. If a fact about the company is needed and cannot be verified, use a `{{placeholder}}` and let a human fill it.

There is no deadline that justifies an unverified number.

---

## Handling a volatile fact

The corpus stays evergreen by **quarantining every fact that can change into one structurally isolated block**. Body prose names the mechanism and never the number.

**Is it volatile?** Ask whether it could be different in two years. Award ceilings, rates, thresholds, deadlines, success rates, form versions, application windows, and contact details are all volatile. Concepts, mechanisms, processes, decision logic, definitions, and failure modes are not.

**If it is volatile, three things happen:**

**1. It goes in the Current Figures callout** — one per article, immediately after the direct-answer block, every row carrying a primary-source deep link:

```markdown
> **Current figures — verified 2026-08-11**
>
> | Item | Value | Source |
> |---|---|---|
> | De minimis indirect cost rate | up to 15% of MTDC | [2 CFR 200.414(f)](https://www.ecfr.gov/current/title-2/section-200.414) |
>
> These figures change. Verify against the linked source before relying on them.
> [Report an outdated figure](/corrections/)
```

**2. It is mirrored into `volatileFacts` frontmatter**, which is what the rendered component and the staleness report are actually built from:

```yaml
volatileFacts:
  - item: "De minimis indirect cost rate"
    value: "up to 15% of MTDC"
    source: "https://www.ecfr.gov/current/title-2/section-200.414"
    verified: "2026-08-11"
```

**3. The body never repeats the number.** Write "the de minimis indirect cost rate set in the Uniform Guidance," not the percentage. Write "the Single Audit threshold," not the dollar figure.

**Banned in body prose, without exception:** "currently," "recently," "as of this writing," "this year," "at the time of writing," "in 2026," "the new rule," "just announced," "the latest." If you need temporal framing, name the durable mechanism instead.

**Verification, not modification.** When a quarterly pass confirms a figure is still correct, update the callout's `verified` date and the `volatileFacts` entry. **Do not touch `dateModified`.** Google names date manipulation without substantive change as a negative signal, and a verification that changed nothing is not a substantive change.

---

## Filing a correction

Every article carries a link to `/corrections/`, and readers use it. Corrections are a trust asset, and treating them as an embarrassment to be minimized destroys the asset.

**Turnaround: within 72 hours of discovery** for anything substantive — a wrong figure, a wrong eligibility rule, a misattributed quotation, a broken regulatory citation.

**The process:**

1. **Fix the article.** For a figure, that is usually a one-line change in the callout and its `volatileFacts` entry.
2. **Decide whether it is substantive.** A wrong number, a wrong rule, or a wrong attribution is substantive: update `dateModified`. A typo, a broken link repaired to the same destination, or a formatting fix is not: leave `dateModified` alone.
3. **Log it publicly** at `/corrections/` with the date, the affected article, what was wrong, what it now says, and how it was found. Entries are never deleted.
4. **Check the neighbours.** A wrong figure has usually been repeated. Grep the corpus for it and for the source URL before closing.
5. **Fix the cause where there is one.** If a figure went stale because it was never in the callout, move it. If a citation broke because the agency reorganized its site, check the other citations to that agency.

**Do not quietly edit and move on.** An unlogged correction in a YMYL corpus is the failure mode the corrections log exists to prevent.

---

## Slugs never change

**A slug is immutable from the moment the article is published.** So is a glossary term slug.

A stable URL is the atom of citation accrual. Every external link, every forum answer, every AI system's memory of where an answer lives, and every internal reference points at that URL. Renaming it discards all of it, and in a corpus whose entire strategy is being cited, that is the most expensive avoidable mistake available.

- **Titles can change. Slugs cannot.** A better headline is not a reason to touch the URL.
- **Glossary term slugs are equally frozen** — article `about` schema references them by `@id`, so a rename silently breaks every article pointing at the term.
- **If an article is genuinely superseded**, 301 the old URL to the replacement and keep the redirect permanently. Never delete.
- **Get it right before publishing.** Lowercase, hyphenated, ≤5 words, no dates, no stop words. The slug is the last thing that is cheap to change and the first thing that becomes permanent.

---

## Before you open the pull request

Work through the **pre-publish checklist in `docs/ARTICLE-CONTRACT.md` §11** — structure, evergreen, evidence, E-E-A-T, linking, and voice. It is not duplicated here on purpose; one copy means one thing to keep current.

Then confirm the three things the checklist assumes:

- `python3 scripts/validate.py` exits with **zero errors**, and every warning has a stated reason.
- Regenerated `data/manifest.json` and `data/link-graph.json` are committed with the article.
- A named reviewer with domain credentials has agreed to review it, and is named in the frontmatter before merge to the publish branch.
