# Build Notes — The OpenGrants Encyclopedia

The implementation checklist for the agent building this corpus into the marketing site. This repository is content only; nothing here renders itself.

Read `docs/RESEARCH-BASIS.md` if you want to know *why* any of this is required. Read `docs/ARTICLE-CONTRACT.md` if you need to know what the content guarantees. This document is the *what to build*.

Working order: **§1 gates everything. Do it first, before you write a line of template code.**

---

## 1. Pre-launch technical gates

### 1.1 AI crawler access in `robots.txt` — do this first

**Nothing else in this document matters if a crawler cannot fetch the page.** A blocked crawler is a hard zero regardless of content quality, citation density, reviewer credentials, or schema. Verify access before you build anything else, and verify it again the day before launch.

Confirm every one of these user agents can fetch `/encyclopedia/` and a sample article:

| User agent | Operator | Purpose |
|---|---|---|
| `GPTBot` | OpenAI | Training crawler |
| `OAI-SearchBot` | OpenAI | Search index for ChatGPT Search |
| `ChatGPT-User` | OpenAI | User-initiated fetch during a conversation |
| `PerplexityBot` | Perplexity | Search index |
| `ClaudeBot` | Anthropic | Training crawler |
| `Claude-SearchBot` | Anthropic | Search index |
| `Claude-User` | Anthropic | User-initiated fetch during a conversation |
| `Google-Extended` | Google | Gemini grounding and training controls |
| `Bingbot` | Microsoft | Bing index, which feeds Copilot |
| `Applebot-Extended` | Apple | Apple Intelligence |

Note that `Google-Extended` and `Applebot-Extended` are **opt-out controls, not crawlers** — they govern whether already-crawled content may be used in AI features. Blocking them does not stop the crawl; it removes you from the surface. Treat them the same as the rest for this check.

**The failure mode is almost never a deliberate block.** It is one of:

- **Host-level defaults.** Some CDN and hosting providers ship a managed `robots.txt` or a "block AI bots" toggle that is on by default. The site owner never wrote the rule and does not know it exists.
- **Anti-bot challenges.** A WAF, bot-management product, or rate limiter serving a JavaScript challenge, CAPTCHA, or 403 to a non-browser user agent.
- **A wildcard rule with an unnoticed scope.** `Disallow: /` under `User-agent: *` inherited from a staging config.

**A challenge page served to a crawler is functionally identical to a block.** The crawler receives HTTP 200 with an interstitial body, records a page with no encyclopedia content, and moves on. Nothing in Search Console or your `robots.txt` will tell you this happened. One practitioner report puts the share of sites with technical barriers to AI crawlers at 73% — the number is unverified (`docs/RESEARCH-BASIS.md` §7.6), but the check costs five minutes and the failure it catches is total.

**How to verify, in this order:**

1. Fetch `https://opengrants.io/robots.txt` and read it in full. Check for wildcard disallows and for any AI-bot block list.
2. `curl` a published article with each user agent string above and assert HTTP 200 **and** that the response body contains a known sentence of body prose — not just a 200 status. Status alone does not distinguish an article from a challenge page.
3. Check the CDN, WAF, and bot-management dashboards for managed rules affecting non-browser user agents. Toggle names vary; look for anything about "AI scrapers," "bot fight," or "known bots."
4. Confirm no rate limit will trip on a crawler pulling 75 URLs in one session.
5. After launch, monitor crawler hit rates in server logs (§9). A user agent that appeared and then went silent is the signal that a rule changed underneath you.

Wire steps 1 and 2 into CI as a scheduled production check, not a one-time manual task. The regression is silent and someone else's deploy causes it.

### 1.2 The rest of the pre-launch gates

- [ ] `/encyclopedia/` and all 75 URLs return 200, server-rendered, with body prose in the initial HTML response
- [ ] Self-referencing canonical on every page
- [ ] No `noindex` inherited from staging
- [ ] XML sitemap live and referenced from `robots.txt`
- [ ] `/authors/sedale-turbovsky/`, `/editorial-policy/`, `/corrections/` all live (§3) — every article links all three
- [ ] Every article's `reviewer.name` replaced with a real named human; `validate.py --publish` exits 0
- [ ] Schema validates and every schema value appears in the visible text
- [ ] Zero orphans per `data/link-graph.json`
- [ ] Current Figures callout renders as its own component with visible verification dates

---

## 2. URL structure and routing

Routing is fully determined by `data/taxonomy.json`. Do not invent paths.

```
/encyclopedia/                                  root index          content/index.md
/encyclopedia/glossary/                         glossary            content/glossary.md
/encyclopedia/{hub}/                            hub page            content/{hub}/index.md
/encyclopedia/{hub}/{slug}/                     cluster article     content/{hub}/{slug}.md
/encyclopedia/glossary/{term}/                  glossary term       data/glossary.json (optional, see below)
```

The patterns live in `taxonomy.json` under `conventions` — read them from there rather than hardcoding, so a taxonomy change cannot desync from the router.

**Rules:**

- **Maximum depth 3 segments.** `/encyclopedia/{hub}/{slug}/` is the deepest article URL. If a hub ever needs sub-hubs, split the hub rather than adding a fourth segment.
- **Trailing slashes, consistently.** Every URL in `taxonomy.json`, `manifest.json`, and `link-graph.json` ends in `/`. Emit and canonicalize the same way. Redirect the non-slash form 301 to the slash form.
- **Slugs are immutable.** A stable URL is the atom of citation accrual — a cited page that moves loses the accrual, and in a corpus whose entire strategy is being cited, that is the most expensive avoidable mistake available. Never rename a slug post-publication. If a title changes, the slug does not. If an article is genuinely superseded, 301 the old URL and keep it forever.
- **Self-referencing canonical on every page**, absolute, matching the URL exactly including the trailing slash. Bing's duplicate-content guidance (2025-12-19) specifically recommends canonical tags plus IndexNow.
- **Lowercase, hyphenated, no dates, no stop words.** Already true of every slug in the taxonomy; enforce it for anything new.
- **Glossary term pages are optional.** 180 terms live in `data/glossary.json` and render inside `/encyclopedia/glossary/`. If you split them into individual URLs, they must carry real content and `DefinedTerm` schema — 180 thin pages is a scaled-content risk (§8), not a win. Default to the single glossary page.

**Breadcrumbs** follow the reader's path, not the file tree: `Home › Encyclopedia › {Hub title} › {Article title}`. Google's rule is to "provide breadcrumbs that represent a typical user path to a page, instead of mirroring the URL structure." Here the two coincide, which is one of the reasons the hierarchy was chosen.

---

## 3. Required pages that do not exist yet

Every one of the 75 articles links all three of these in its footer or byline. Shipping the encyclopedia without them produces 75 broken trust signals and 75 broken links.

### `/authors/sedale-turbovsky/`

The author entity every article's schema `@id`-references. Must contain:

- **150+ word biography** in visible prose. Relevant experience, not a marketing blurb.
- **Credentials**, stated plainly. The frontmatter carries "Founder and CEO, OpenGrants"; the page should say what that means for grant expertise specifically.
- **Photograph** of the actual person.
- **Minimum three `sameAs` links**, visible on the page and mirrored in schema. Two are already in every article's frontmatter: `https://www.linkedin.com/in/sedaleturbovsky/` and `https://opengrants.io/about`. **A third must be added by a human** — ORCID, a personal site, a professional registry, a Wikidata entity, or a conference/speaker profile. Do not invent one.
- **`ProfilePage` + `Person` schema**, with `mainEntity` pointing at the Person. Recommended additions: `dateCreated`, `dateModified`, `description` (the byline credential string), `image`, `sameAs`, `identifier`.
- **A list of articles authored**, linking into the encyclopedia. This also gives the corpus a second non-hub inbound link source.

Google names author pages as an explicit valid use case for `ProfilePage`. Every value in the schema must appear in the visible text.

### `/editorial-policy/`

Referenced from every article footer and from the `disclosure` frontmatter line. Must cover, each as its own section:

- **Sourcing standards.** Primary sources preferred, `.gov` and `.edu` weighted, every number carries a linked source, nothing cited that was not read.
- **Review process.** Every article has a named author and a separate named reviewer with domain credentials. State that the encyclopedia sits in a YMYL category and what that means for the standard applied.
- **Correction policy.** How errors are reported, the target turnaround (72 hours from discovery for a substantive error), and that corrections are logged publicly.
- **Update and verification cadence.** Quarterly verification of figures in Current Figures callouts, annual full review, and the rule that `dateModified` only moves on substantive change.
- **AI-use disclosure.** State plainly how drafting was done and why. Google's Who/How/Why guidance specifically recommends explaining *"why automation or AI was seen as useful to produce content"* — and this corpus was drafted with AI assistance against fetched primary sources, then fact-checked and human-reviewed. Say that. Concealing it is both a trust failure and a policy risk; disclosing it plainly is neither.
- **Commercial disclosure.** OpenGrants is a commercial grant discovery platform publishing a reference work about grants. State the conflict, state the one-product-link-per-article rule, and state that editorial content is not sold.

### `/corrections/`

The trust signal almost no competitor will have, and the destination of the "Report an outdated figure" link inside every Current Figures callout.

- **A public, dated, reverse-chronological log.** Each entry: date, affected article (linked), what was wrong, what it now says, and how it was found.
- **A reporting form or a monitored address**, reachable without an account.
- **Per-article filtering**, so a reader on one article can see whether it has ever been corrected.
- **Entries are never deleted.** A corrections log that gets cleaned up is not a corrections log.
- The page must be reachable and indexable. Do not `noindex` it.

---

## 4. Rendering requirements

Non-negotiable, and cheap to get right if designed in from the start.

- **Body text is server-rendered.** The full article prose must be present in the initial HTML response. Verify with `curl` and JavaScript disabled, not with a browser devtools inspection of the hydrated DOM.
- **No gating of any kind.** No email walls, no registration prompts blocking content, no "read more" expanders that hide prose behind a click, no paywalls, no partial-content teasers.
- **No interstitials.** No modal on entry, no cookie wall that blocks content, no newsletter overlay before the reader reaches the first paragraph.
- **No JS-dependent prose.** Tables, callouts, FAQ answers, and citation links must all exist in the HTML. Accordion FAQ patterns are acceptable only if the answer text is in the DOM at load and hidden with CSS, never if it is fetched or injected on click.
- **Citations are real anchors** with `href` attributes in the server-rendered HTML, not click handlers.
- **The Current Figures callout is in the HTML**, not fetched from an API at runtime (§5).
- **Reasonable performance.** Not a ranking argument — a crawl-budget and rendering-reliability one.

A page a crawler cannot read is worth nothing, and the failure is invisible: the page looks perfect to you and empty to everything else.

---

## 5. The Current Figures callout — build it as a component

**This is the single most important component decision in the build.** The corpus's evergreen strategy depends entirely on volatile facts being structurally isolated rather than scattered through prose. If the callout renders as ordinary blockquote markup, the isolation exists in the writing but not in the system, and the maintenance advantage evaporates the first time someone needs to audit 75 articles.

Build it as a distinct, named component. Four requirements:

**1. Structurally isolated.** A dedicated component with a stable class or data attribute (`data-component="current-figures"`), not a styled blockquote. Machine-selectable across the whole corpus, so a single query answers "show me every figure on the site and when it was last verified."

**2. Visibly time-bound.** The design must communicate that these numbers have an expiry and the surrounding prose does not. Verification date displayed prominently, not in fine print. A visual treatment distinct from every other callout style on the site. Every row's source link is a real deep link to the primary source. The "Report an outdated figure" link points to `/corrections/`. When a figure passes its staleness threshold, the component should be able to render a visible caveat rather than silently continuing to assert a stale number.

**3. Driven from `volatileFacts` frontmatter, not from the Markdown table.** Each article's frontmatter carries the authoritative array:

```yaml
volatileFacts:
  - item: "De minimis indirect cost rate"
    value: "up to 15% of MTDC"
    source: "https://www.ecfr.gov/current/title-2/section-200.414"
    verified: "2026-08-11"
```

The Markdown table in the body exists so the article reads correctly as a plain file. **The rendered component must be generated from the frontmatter array**, so there is exactly one source of truth and no possibility of the visible table and the machine-readable array disagreeing. Add a validator check that the two match if you want belt and braces.

**4. Batch-auditable.** Because the data is structured, this works today against `data/manifest.json`:

```bash
python3 -c "
import json
m = json.load(open('data/manifest.json'))
for a in m['articles']:
    for f in a['volatileFacts']:
        print(f['verified'], a['url'], f['item'])
" | sort
```

Build the equivalent as a real report: every figure, its article, its source, its verification date, sorted oldest first, with anything past 90 days flagged. That report is the quarterly refresh work queue. Without it, quarterly verification means re-reading 75 articles, which means it will not happen.

**One further rule for the build:** volatile numbers appear **only** inside the callout. If you find a dollar figure or percentage in body prose, that is a content bug — file it, do not paper over it in the template.

---

## 6. Schema emission

Templates live in `schema/`. Read `schema/README.md` before implementing — it carries the `@id` conventions and the visible-text rule.

| Page type | Graph contents | Template |
|---|---|---|
| Cluster article | `Article` (or `TechArticle`), `WebPage`, `BreadcrumbList`, `Person` (author), `Person` (reviewer), `Organization` ref, `DefinedTerm` refs via `about`, `citation[]`, optional `FAQPage` | `schema/article.jsonld` |
| Hub page | `Article`, `WebPage`, `BreadcrumbList`, `ItemList` enumerating children, `Person`, `Organization` ref | `schema/hub.jsonld` |
| Glossary | `DefinedTermSet` with `DefinedTerm` members, `WebPage`, `BreadcrumbList` | `schema/glossary.jsonld` |
| Author page | `ProfilePage` + `Person` (`mainEntity`) | build from `schema/article.jsonld`'s Person node |
| Site-wide | `Organization`, emitted once, `@id`-referenced everywhere | `schema/organization.jsonld` |

**Three rules that bind:**

1. **Every schema value must appear in the visible text of the page.** Google's explicit requirement. If `dateModified` says one thing and the visible "Last reviewed" line says another, that is a defect, not a detail. This applies to `headline`, `description`, dates, author name, reviewer name, and every `citation` entry.
2. **`@id` references, never duplicated entity definitions.** The `Organization` is defined once at `https://opengrants.io/#organization`. Every other page references `{"@id": "https://opengrants.io/#organization"}` and emits nothing further. Same for the author `Person` at `https://opengrants.io/authors/sedale-turbovsky/#person` and for each `DefinedTerm` in the glossary set. Duplicating a full entity definition on 75 pages creates 75 competing assertions of the same entity, which is the opposite of what entity markup is for.
3. **Schema is for entity disambiguation and rich results. It is not a citation tactic.** Google states there is no special markup for generative AI search (`docs/RESEARCH-BASIS.md` §3). Emit it because it is cheap and correct. Do not let anyone promise citation lift from it, and do not shape content around it.

**The `citation` array is the one to get right.** One `CreativeWork` per external source, with `name` and `url`, populated from each article's `externalSources` in `data/manifest.json`. It is underused across the web and it encodes the highest-confidence measured lever — dense source citation — in machine-readable form.

**Do not emit** `HowTo`, `Practice Problem`, or `Course` — all deprecated. `FAQPage` is included in the article template because it is free, but no Google rich result exists for it; see `schema/README.md`.

---

## 7. Dates

- **Visible `Published:` and `Last reviewed:`** at the top of every article, near the byline, above the fold.
- **Visible values and schema values must match exactly.** `datePublished` and `dateModified` in the graph, ISO 8601 with timezone, identical to what the reader sees.
- **`dateModified` changes only on substantive content change.** Never on a build, a deploy, a typo fix, a CSS change, or a link repair. Google explicitly names date manipulation without substantive change as a negative signal. The build must not touch `dateModified` automatically — treat any automated write to that field as a bug.
- **The Current Figures `verified` date is separate and non-schema.** A quarterly verification pass that confirms every figure is still correct changes the callout's `verified` date and nothing else.
- **No future dates.** Minimize other dates on the page.
- `lastFactCheck` and `nextReviewDue` are operational fields. Surface `nextReviewDue` in an internal dashboard, not in the schema.

---

## 8. Sitemap, submission, and discovery

- **XML sitemap** at `/sitemap.xml`, including all 75 encyclopedia URLs plus `/authors/sedale-turbovsky/`, `/editorial-policy/`, and `/corrections/`. `lastmod` mirrors `dateModified` — which means it does not move on a build either.
- **Reference the sitemap from `robots.txt`.**
- **IndexNow** for Bing, Yandex, and participating engines: ping on publish and on substantive update only. Bing's duplicate-content guidance recommends IndexNow alongside canonical tags. Do not ping on every deploy; that is a spam signal and it wastes the quota that makes IndexNow useful.
- **Bing Webmaster Tools and Google Search Console** both verified before launch. Bing matters more than its search share suggests, since it feeds Copilot.
- **Breadcrumbs rendered visibly** as well as in schema.
- **Internal navigation** must reach every article within 3 clicks of the homepage.
- Publish `llms.txt` at the site root, regenerated with `python3 scripts/gen-llms-txt.py` whenever the taxonomy changes. It is free; it is not a channel (`docs/RESEARCH-BASIS.md` §8).

---

## 9. CI checks

Wire all five. The first is a merge gate; the rest can start as warnings and graduate.

**1. `python3 scripts/validate.py --publish` as a merge gate.** This is the contract enforcement. It validates frontmatter, structure, citation counts, banned phrases, link targets, and the reviewer gate. It currently reports **0 errors, 17 advisory warnings, and 75 open publish gates** — every gate is an unassigned reviewer. Merges to the publish branch must fail while any gate is open. Do not add a bypass flag; the gate is the YMYL control.

**2. Orphan detection from `data/link-graph.json`.** Every published URL needs at least one inbound internal link from a page other than its hub and other than the sitemap or nav. An orphan is invisible to crawlers regardless of quality.

```bash
python3 -c "
import json, collections
g = json.load(open('data/link-graph.json'))
inbound = collections.defaultdict(set)
for e in g['edges']:
    inbound[e['to']].add(e['from'])
for n in g['nodes']:
    if n['hub'] is None:      # root index and glossary reach readers via nav
        continue
    srcs = {s for s in inbound[n['url']] if not s.endswith(f\"/{n['hub']}/\")}
    if not srcs:
        print('ORPHAN', n['url'])
"
```

Against the current corpus this prints nothing. The two nodes with `hub: null` — `/encyclopedia/` and `/encyclopedia/glossary/` — are skipped by design: both are reached from site navigation, and the root index is the thing everything else hangs off. Give them both a real inbound link from the site nav and from `/editorial-policy/` anyway.

**3. Dead external link sweep.** Roughly 1,141 external citations, weighted toward `.gov`. Government URLs move — eCFR sections get renumbered, agency pages get reorganized, CRS reports get new version suffixes. Run weekly, not on every commit. Report 404s and 301 chains separately: a 301 to a still-correct page is a citation to update at leisure, a 404 in a YMYL corpus is urgent. Rate-limit politely and allow for `.gov` sites that block generic user agents.

**4. Semantic-similarity duplicate check.** Embed each article and flag any pair above **0.85 cosine similarity** for merge review before publishing anything new. Near-duplicate articles on the same entity are doorway pages under Google's spam policy — "sites or pages are created to rank for specific, similar search queries." One entity, one canonical article. Consolidate rather than split.

**5. Crawler access regression check.** §1.1, run against production on a schedule. Assert 200 **and** body content for each of the ten user agents. This is the check most likely to catch a problem you did not cause.

Optional but useful: `python3 scripts/gen-llms-txt.py --check` to fail if `llms.txt` has drifted from the taxonomy, and `python3 scripts/sync-counts.py --check` for frontmatter count drift.

---

## 10. Staggered publication

**Do not publish 75 articles at once.**

Google's spam policy defines **scaled content abuse** as *"when many pages are generated for the primary purpose of manipulating search rankings and not helping users,"* explicitly including *"Using generative AI tools or other similar tools to generate many pages without adding value for users."* (https://developers.google.com/search/docs/essentials/spam-policies, last updated 2026-05-15.)

Seventy-five articles appearing simultaneously in one topical area on a commercial domain is **structurally indistinguishable, from the outside, from exactly that pattern**. The things that actually distinguish this corpus — named authorship, a named reviewer per article, roughly 1,141 primary-source citations, original synthesis, human fact-checking — are all real, and none of them are visible in a publication-volume signal. The corpus's quality is a defense at the article level and no defense at all at the pattern level.

There is no published threshold for what volume trips this. That is itself a reason for caution: you cannot calibrate against a number Google has not disclosed. The mitigation is free.

**Recommended cadence — roughly six months, hub by hub:**

| Wave | Weeks | Publish | Rationale |
|---|---|---|---|
| 1 | 1–2 | `/encyclopedia/` root + `foundations` hub + its 7 children | Establishes the root entity and one complete, defensible cluster |
| 2 | 3–5 | `finding-funding` (7) | Highest search intent; validates the pattern before scaling |
| 3 | 6–8 | `readiness` (6) + glossary | Glossary lands after enough articles exist for its cross-links to resolve |
| 4 | 9–13 | `proposal-craft` (11) | Largest hub; spread across the window rather than dropped in a day |
| 5 | 14–17 | `budgets` (8) | |
| 6 | 18–21 | `evidence` (7) | |
| 7 | 22–26 | `funding-tracks` (9) | |
| 8 | 27–32 | `award-management` (10) | |

Within a wave, **publish 2–4 articles per week, not the whole hub in one day.** Publish the hub page first so children are never orphans on arrival.

Three practical benefits beyond the policy risk:

- **Reviewer throughput is the real constraint.** Every article needs a named human reviewer with domain credentials. Ninety-plus days of staggered publishing is roughly what a serious review process takes anyway. The schedule is a forcing function, not a delay.
- **You get to learn.** Wave 1's indexation, citation behavior, and crawler logs tell you something before you have committed 75 URLs to a pattern.
- **Internal linking resolves cleanly.** Articles link to siblings that already exist, so no wave ships with dangling internal links. The validator will tell you which cross-hub links are not yet live; hold those articles or soften the link until the target publishes.

If someone needs the whole corpus live sooner, compress to about three months, but keep it hub by hub and keep the per-week ceiling.

---

## 11. Measurement

**Measure mention share, not just clicks.** This is the section most likely to be set up wrong, and the wrong setup makes a working strategy look like a failing one.

Ahrefs tracked more than 31,000 mentions of its own brand across a 150M-prompt database (2025-11-26, https://ahrefs.com/blog/ai-citations-vs-impressions-study). When AI assistants mentioned the brand, they included a **link only 10.7% to 51.6% of the time** — 10.7% on AI Overviews, 16.8% Gemini, 26.1% Copilot, 26.9% ChatGPT, 36.8% AI Mode, 51.6% Perplexity, averaging around 28%.

**Read that consequence plainly: on AI Overviews, roughly nine out of ten times the encyclopedia is named, there will be no click to attribute it to.** A dashboard built only on referral sessions will report near-zero for a surface that is working. Caveat the finding honestly — it tracks one brand, not a cross-brand sample — but the direction is not in doubt, and the reporting failure it causes is.

**Track, in rough priority order:**

1. **AI mention share.** How often OpenGrants and the encyclopedia are named in answers to grant-related prompts, whether or not a link appears. Build a standing prompt set from the `primaryQuestion` and `secondaryQuestions` fields in `data/manifest.json` — that is 680 real questions the corpus is written to answer, and it is a better benchmark set than anything you would invent. Run it monthly across ChatGPT, Perplexity, Gemini/AI Mode, Copilot, and Claude. Record mention, link, and which URL was cited.
2. **Citation share by URL.** Which articles get cited, on which engines. Expect low overlap between engines — only 14% of the top 50 most-mentioned sources are shared across the three major ones — so report per engine and do not average into a single meaningless number.
3. **GA4 AI referral channel group.** Create a custom channel group isolating AI assistant referrers so AI traffic stops being bucketed as direct or generic referral. Cover at minimum `chatgpt.com`, `perplexity.ai`, `claude.ai`, `copilot.microsoft.com`, `gemini.google.com`, and `bing.com` with Copilot parameters. Track sessions, engaged sessions, and conversions separately from organic search — AI-referred visitors arrive with more context and behave differently.
4. **Crawler health.** From server logs, per user agent from §1.1: request volume, status codes, and bytes served. Alert when a previously active agent goes silent. This is your early warning that a rule changed.
5. **Classic search**, still. Search Console impressions, clicks, and average position per URL; Bing Webmaster Tools separately. Google's AI surfaces retrieve from the Search index, so index health remains the entry ticket.
6. **Off-site brand mentions.** Track unlinked mentions of OpenGrants and of encyclopedia articles on Reddit, LinkedIn, YouTube, university research-office pages, and nonprofit blogs. Ahrefs measured brand web mentions correlating **0.664** with AI Overview mentions versus **0.218** for backlinks (75,000 brands, 2025-05-26). It is correlational, and it is the strongest correlate anyone has published.
7. **Corpus health.** Figures past their verification window, dead external links, orphans, articles past `nextReviewDue`. All queryable from `data/manifest.json`.

Set the reporting expectation before the first wave ships, not after someone asks why referral traffic is flat.

---

## 12. What the build cannot fix

Two things that no amount of implementation quality will compensate for. Both should be said out loud to whoever owns the launch.

**1. Unreviewed YMYL content.** Every article currently carries `reviewer.name: REVIEWER_REQUIRED`, and `validate.py --publish` fails on all 75 for that reason. This is deliberate. Grant content sits in Google's YMYL Financial Security *and* Government/Civics categories, where the Search Quality Rater Guidelines direct raters to treat low-quality pages as capable of negatively affecting people's financial stability, and where Google says *"of these aspects, trust is most important."*

No technical measure substitutes for a second credentialed human reading each article and taking accountability for it. Perfect schema on an unreviewed article is a well-marked-up liability. The reviewer step is the most expensive part of shipping this and the one with no engineering workaround. **Do not build a bypass flag for the publish gate.** If schedule pressure arrives, publish fewer articles — which the staggered schedule in §10 already assumes.

**2. Off-site brand mentions matter more than anything on the page.** Ahrefs' 75,000-brand analysis found brand web mentions correlating **0.664** with AI Overview visibility against **0.218** for backlinks — roughly three times stronger. Top-quartile brands by web mentions earned up to **10× more** AI Overview mentions than the next quartile, and **26% of brands had zero mentions at all**. The measurement is correlational and Ahrefs says so directly.

The implication is uncomfortable for a build team: **the highest-value remaining work is not in this repository.** An encyclopedia that becomes the thing people cite by name in grant-writing forums, on r/nonprofit, in university research-office resource pages, and in nonprofit consultants' newsletters is doing more for AI visibility than any on-page change available to you. Ship the technical work properly — it is the necessary floor and it is entirely within your control — and then make sure someone owns getting the corpus mentioned off-site. Nobody currently does.
