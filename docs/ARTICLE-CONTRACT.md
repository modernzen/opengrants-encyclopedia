# Article Contract — The OpenGrants Encyclopedia

**This document is binding.** Every article in `content/` must satisfy every rule here. It is derived from the research in `docs/RESEARCH-BASIS.md` and encodes the evidence on SEO, GEO (generative engine optimization), and AEO (answer engine optimization) as of August 2026.

Read it end to end before writing. A reviewer or CI check will validate against it.

---

## 1. The governing principle

> Write the reference page a skeptical practitioner would bookmark, cite in a forum answer, and still find correct in three years.

Everything below is downstream of that. Three consequences:

1. **Evergreen by construction.** Volatile facts are quarantined in one structurally isolated block. Body prose contains no dates, no dollar figures, no "currently," no "recently," no "as of this year."
2. **Extractable by construction.** Every section must be correct and complete if it is the *only* passage an AI retriever pulls.
3. **Cited by construction.** Every number, eligibility rule, deadline mechanic, and legal claim carries a primary-source link at the point of the claim.

---

## 2. Evidence basis for these rules

Not folklore. The rules trace to specific findings — cite these in any internal debate about the format.

| Rule | Evidence | Strength |
|---|---|---|
| Dense primary-source citation | Princeton GEO study (KDD 2024, N=10,000 queries): "Cite Sources" +30–40% visibility; strongest on **factual** queries | High — peer reviewed |
| Convert qualitative claims to statistics | Same study: "Statistics Addition" +30–40%; **strongest in the 'Law & Government' domain**, which is exactly this encyclopedia's domain | High |
| Include direct quotations | Same study: "Quotation Addition" +30–40% | High |
| Fluent, plain prose | Same study: "Fluency Optimization" +15–30%; best pair is Fluency + Statistics (>5.5% over any single method) | High |
| **Never keyword-stuff** | Same study: measured **10% worse than baseline** on a generative engine | High |
| **Never inflate tone to sound authoritative** | Same study: measured **no significant effect** | High |
| Question-shaped H2s, answer-first | Ahrefs (863K SERPs, Mar 2026): only **37.9%** of AI-Overview-cited URLs rank in the top 10, down from 76.1% in Jul 2025 — engines increasingly cite pages that match **fan-out sub-queries**, not head terms | Medium-High |
| Self-contained passages | Non-Google engines chunk → embed → retrieve top-k. The retrieval unit is the chunk, not the page | Reasoned from mechanism |
| Named authors, review dates, editorial policy | Google Search Quality Rater Guidelines §2.3: grant content is **YMYL Financial Security** *and* **YMYL Government/Civics**. Google gives "even more weight to E-E-A-T" here, and "of these aspects, trust is most important" | High — official |
| No gating, no JS-only body text | A blocked or unreadable page is a hard zero regardless of quality | High |
| Original synthesis, not aggregation | Google's March 2026 core update: government, institutional, and specialist sources gained; **aggregators and directory sites lost** | Medium-High |

Two rules exist because of what the evidence says *does not* work:

- **Do not write for schema.** Google states plainly that no special markup, Markdown, or AI text file is required for its generative features, and that structured data is not a generative-AI ranking input. We emit schema for entity disambiguation and rich results only.
- **Do not pad.** There is no credible evidence that word count causes rankings. Length targets in §8 are a *consequence* of covering the question set, never a target to hit.

---

## 3. Frontmatter — required on every article

YAML, exactly these keys. The build reads them; do not rename or omit.

```yaml
---
title: "Full Article Title"                # ≤ 60 chars, matches H1 exactly
slug: "kebab-case-slug"                    # ≤ 5 words, IMMUTABLE after publish
url: "/encyclopedia/{hub}/{slug}/"
hub: "finding-funding"                     # pillar key; null only on a hub page
hubUrl: "/encyclopedia/finding-funding/"
articleType: "concept"                     # concept | process | program | comparison | hub
schemaType: "Article"                      # Article | TechArticle

metaDescription: "…"                       # 150–160 chars; = the direct-answer block, trimmed
primaryEntity: "Notice of Funding Opportunity"
primaryQuestion: "How do you read a Notice of Funding Opportunity?"
secondaryQuestions:                        # 5–10 fan-out targets, natural language
  - "What are the sections of a NOFO?"
  - "…"
definedTerms: ["nofo", "foa", "cfda-assistance-listing"]   # glossary slugs introduced here

clusterSiblings:                           # 2–4 sibling slugs in the same hub
  - "how-to-search-for-grants"
  - "go-no-go-decision"

author:
  name: "Sedale Turbovsky"
  profileUrl: "/authors/sedale-turbovsky/"
  credentials: "Founder and CEO, OpenGrants"
  sameAs:
    - "https://www.linkedin.com/in/sedaleturbovsky/"
    - "https://opengrants.io/about"
reviewer:
  name: "REVIEWER_REQUIRED"                # ← must be replaced by a named human before publish
  credentials: ""
  reviewDate: ""

datePublished: null                        # build sets on first publish
dateModified: null                         # build sets ONLY on substantive change
lastFactCheck: "2026-08-11"
nextReviewDue: "2027-08-11"

volatileFacts: []                          # see §5; [] means no Current Figures callout
citationCount: 12
wordCount: 2100
isAccessibleForFree: true
disclosure: "OpenGrants is a commercial grant discovery platform. See /editorial-policy."
---
```

**`reviewer.name` must be a real, named human with domain credentials before any article ships.** The encyclopedia states eligibility rules and financial mechanics in a YMYL category. An unreviewed article is not publishable. The build must fail on `REVIEWER_REQUIRED`.

---

## 4. Section order

Fixed. Sections marked *(menu)* are chosen to fit the article — pick 5–9 of them, keep this relative order, and always phrase them as questions.

```
1.  H1                              — matches `title` exactly
2.  Direct answer block             — 40–60 words, ≤320 chars, NO heading
3.  Current figures callout         — only if volatileFacts is non-empty
4.  ## Key takeaways                — 3–5 bullets, ≤15 words each
5.  ## What is {entity}?            (menu — near-mandatory)
6.  ## Who is eligible …?           (menu)
7.  ## How does {entity} work?      (menu)
8.  ## How much …?                  (menu)
9.  ## How do you {do the thing}?   (menu — ordered list, 5–8 steps)
10. ## What is the timeline …?      (menu)
11. ## {entity} vs {alternative}?   (menu — comparison table ≤5 rows)
12. ## What goes wrong …?           (menu — near-mandatory; the failure modes)
13. ## Frequently asked questions   — 5–8 H3 questions, 40–60 word answers
14. ## Related topics               — hub link + 2–4 siblings
15. ## Sources                      — numbered, full citations
```

---

## 5. The volatility rule — how we stay evergreen

**Every fact that can change lives in exactly one place: the Current Figures callout. Body prose refers to it and never repeats the number.**

Three tiers, and you must consciously assign every sentence to one:

| Tier | Share of words | Content | Example |
|---|---|---|---|
| **Stable** | ~80% | Concepts, mechanisms, processes, decision logic, definitions, failure modes | "The de minimis rate applies to modified total direct costs, which excludes equipment and the portion of each subaward above a set threshold." |
| **Slow-moving** | ~15% | Statutory frameworks, program structures, agency roles | "2 CFR 200 is the government-wide rule set; each agency adopts it into its own title of the CFR." |
| **Volatile** | ~5% | Award ceilings, rates, thresholds, deadlines, success rates, form versions | The actual percentage, the actual dollar amount |

Callout format — render as a distinct component so it can be batch-audited:

```markdown
> **Current figures — verified 2026-08-11**
>
> | Item | Value | Source |
> |---|---|---|
> | De minimis indirect cost rate | up to 15% of MTDC | [2 CFR 200.414(f)](https://www.ecfr.gov/current/title-2/section-200.414) |
> | Single Audit threshold | $1,000,000 in federal awards expended per fiscal year | [2 CFR 200.501](https://www.ecfr.gov/current/title-2/section-200.501) |
>
> These figures change. Verify against the linked source before relying on them.
> [Report an outdated figure](/corrections/)
```

Rules:
1. **One callout per article**, immediately after the direct-answer block.
2. Volatile numbers appear **only** inside the callout. Body prose says "the de minimis rate" or "the audit threshold," never the figure.
3. The callout carries its own `verified` date, independent of `dateModified`.
4. Every row names a primary source with a deep link.
5. Mirror every row in the `volatileFacts` frontmatter array so the build can generate a staleness report.

**Banned in body prose, without exception:** "currently," "recently," "as of this writing," "this year," "at the time of writing," "in 2026," "the new rule," "just announced," "the latest." If you need temporal framing, name the durable mechanism instead: not *"the rate was recently raised to 15%"* but *"the rate is set in 2 CFR 200.414(f) and has been revised periodically; see the current figures above."*

---

## 6. Structural rules (extractability)

These are simultaneously good writing and good retrieval engineering. There is no tension.

1. **Section independence.** Every H2 must be correct and complete read alone, with zero memory of prior sections.
2. **No anaphora after a heading.** "This," "these," "it," "the above," "as mentioned," "the former" are banned as the *first referring expression* after any heading. Re-nominalize.
3. **Entity re-anchoring.** Restate the primary entity by full name at least once in every H2 section. First mention in each section is the canonical name, never a pronoun or abbreviation.
4. **Answer-first.** The first 40–60 words after each H2 completely answer that H2. Nuance, exceptions, and caveats follow. Never build to an answer.
5. **Self-contained paragraphs.** One claim per paragraph, stated in the first sentence. 40–90 words; hard ceiling 120.
6. **No backward dependencies.** If a later section needs an earlier definition, restate it in a clause. Do not write "as defined above."
7. **Sections run 150–350 words** between H2s.
8. **Tables are self-describing.** One prose sentence stating what the table shows immediately before it. Full column headers, no abbreviations. Entity name in the first column. ≤5 rows for the primary comparison table (add a longer one below if needed), ≤3 words per cell where possible.
9. **Lists: 5–8 items**, bold lead-in phrase per item, preceded by a stem sentence containing the count ("There are six ways a budget fails review:").
10. **Never split an atomic fact across a heading boundary.** A rule and its qualifying conditions stay in one contiguous block.

### Heading conventions

- **One H1.** Matches `title` exactly.
- **H2s are natural-language questions ending in `?`**, containing the primary entity by name, ≤12 words.
- **No bare-noun headings.** `## Eligibility` is wrong. `## Who is eligible for a federal grant?` is right.
- **H3 only** for FAQ items and sub-questions. Never go below H3.

---

## 7. Evidence and citation rules

- **8–15 external citations per 2,000 words.** Minimum 8. This is the highest-confidence lever available.
- **Inline at the claim**, never batched only at the end. Format: `…the threshold is set in the Uniform Guidance ([2 CFR 200.501](url)).`
- **Zero uncited numbers.** No dollar figure, percentage, date, count, or eligibility rule without a linked source.
- **Majority primary sources.** `.gov` and `.edu` preferred: eCFR, Federal Register, grants.gov, SBIR.gov, SAM.gov, agency policy statements, GAO, CRS, IRS, Census. Secondary sources (Candid, Giving USA, CEP, university research offices, peer-reviewed papers) are welcome but should be labeled as what they are.
- **At least one direct quotation** from a credible named source per article, in quotation marks, attributed, with a link.
- **Prefer the quantitative form.** "Most applications fail on compliance" is weaker than a cited count. If you cannot find a number, say the qualitative thing plainly rather than inventing precision.
- **Sources section** at the end: numbered, with publisher, title, URL, and access date.

**Fabrication is the one unrecoverable error.** If you cannot verify a figure, omit it. Never approximate a citation, never cite a source you did not read, never attribute a quotation you did not find. A missing statistic costs nothing. A wrong one in a YMYL category costs the whole property.

---

## 8. Length guidance

Targets, not quotas. **If you have answered every question in `secondaryQuestions` in fewer words, the article is done.** If you have hit the word count without answering them, it is not.

| Article type | Words | H2 sections | Citations |
|---|---|---|---|
| Concept | 1,400–2,000 | 5–7 | 8–12 |
| Process / how-to | 1,600–2,400 | 6–8 | 8–14 |
| Program entry | 1,800–2,600 | 7–9 | 10–15 |
| Comparison | 1,300–1,900 | 5–7 | 8–12 |
| Hub page | 2,000–3,000 | 8–12 | 8–12 |

---

## 9. Voice

From `brand-strategy.md`: **plainspoken, infrastructural, quietly anti-bureaucratic.** A senior grants strategist who has worked both sides — applicant and funder — and refuses to dress bureaucracy up in jargon.

- **First person plural** ("we") sparingly. Mostly write in the second person to the practitioner ("you"), or in neutral reference voice.
- **Neutral reference tone in the body.** This is an encyclopedia, not a landing page. No pitch inside the article body.
- **Concrete over abstract.** Name the form, the CFR section, the office, the field on the screen.
- **Respect the reader's intelligence.** They are competent, time-poor, and skeptical of vendors.

### Banned phrasing

Hard bans. These are AI-slop markers and reviewers will flag them:

> "In today's fast-paced world" · "It's important to note that" · "delve" · "navigate the complexities" · "the landscape of" · "unlock" · "harness" · "leverage" (as a verb) · "robust ecosystem" · "stakeholder alignment" · "In conclusion" · "game-changing" · "revolutionary" · "at the end of the day" · "when it comes to" · "that being said"

Also banned:
- **Scarcity manipulation.** No "you're missing $X in funding right now."
- **Outcome promises.** Never state or imply that following the guide produces an award.
- **Naming competitors negatively.** Discuss gaps in the category, not named rivals.
- **Section-ending summary sentences** that restate the section you just read.
- **Uniform paragraph length.** Vary it.

### The originality test

Every article must contain at least one thing a language model could not produce without doing the research: a specific figure with a primary-source link, a named procedural detail, a synthesized comparison that exists nowhere else, or a failure mode described concretely enough to be actionable.

---

## 10. Internal linking

| Position | What | Anchor text |
|---|---|---|
| First 200 words | 1 link to the hub page | The hub's primary entity name |
| Body | 3–6 contextual links at natural mention points | 2–6 descriptive words naming the target |
| Comparison section | 1–2 to compared entities | Entity names |
| Related topics | Hub + 2–4 siblings | Full target titles |
| Glossary | First occurrence of each term only | The term itself |

Rules: never link the same target twice **in the body**. Never exceed 8 in-body links per 1,000 words. Ban "click here," "read more," "this article." Every article needs at least one inbound link from a page other than its hub — the build enforces this.

**Two carve-outs from the no-duplicate rule.** Both are navigation surfaces, not prose, and a reader arriving at either expects working links:

1. **Related topics** may link the hub and every sibling even when the body already linked them.
2. **The glossary** may link the same explainer article from every term that points to it. Each glossary entry is an independent record and must work read alone.

The validator implements both carve-outs; do not "fix" a duplicate it reports inside these sections.

**Product links.** At most **one** link to an OpenGrants product surface per article, and only where it is genuinely the most useful next action for the reader. It belongs in Related topics or a single natural body mention — never in the direct-answer block, never in the first section, never more than once. The encyclopedia earns trust by being useful when it is *not* selling.

---

## 11. Pre-publish checklist

**Structure**
- [ ] Direct-answer block: 40–60 words, ≤320 chars, entity named in the first clause, no anaphora, no forward reference
- [ ] Every H2 is a natural-language question ending in `?`
- [ ] First 40–60 words after each H2 fully answer it
- [ ] Every section standalone-comprehensible; entity re-anchored in each
- [ ] Zero anaphora as the first referring expression after any heading
- [ ] Sections 150–350 words; paragraphs 40–90 words
- [ ] Tables preceded by a prose stem; ≤5 rows in the primary comparison
- [ ] Lists 5–8 items with bold lead-ins and a counted stem sentence

**Evergreen**
- [ ] Zero volatile numbers in body prose
- [ ] All volatile facts in the callout, each with source link and verify date
- [ ] Callout rows mirrored in `volatileFacts` frontmatter
- [ ] Zero banned temporal phrases
- [ ] Article would still be substantially correct in three years

**Evidence**
- [ ] 8–15 external citations; ≥1 per major claim
- [ ] Zero uncited numbers, dates, dollar figures, or eligibility rules
- [ ] Majority primary sources
- [ ] ≥1 attributed direct quotation with a link
- [ ] Nothing fabricated; every citation is real and was read

**E-E-A-T**
- [ ] Named author with credentials and ≥2 `sameAs`
- [ ] `reviewer.name` is a real person (not `REVIEWER_REQUIRED`)
- [ ] Neutral reference tone; no pitch in the body; ≤1 product link
- [ ] Disclosure line present in frontmatter

**Linking**
- [ ] 1 hub link in the first 200 words
- [ ] 3–6 contextual body links, descriptive anchors, no duplicates
- [ ] Related topics section with hub + 2–4 siblings
- [ ] All internal URLs match real slugs in `data/manifest.json`

**Voice**
- [ ] Zero banned phrases
- [ ] No outcome promises, no scarcity framing, no named-competitor criticism
- [ ] Passes the originality test
