# Research Basis — The OpenGrants Encyclopedia

The evidence behind the content architecture. Every rule in `ARTICLE-CONTRACT.md` and every requirement in `BUILD-NOTES.md` traces to something here.

Use this document two ways: to **defend** a decision when someone asks why articles are shaped this way, and to **revise** one when the evidence moves. A rule whose evidence is weak should be easy to change. A rule resting on a peer-reviewed measurement should not be.

**Distilled from** `research/08-geo-aeo-seo-spec.md`, research date **2026-08-11**. Load-bearing URLs were re-fetched at authoring time.

---

## Evidence labels

Used consistently below. **Never upgrade a label.** A vendor blog post reporting a lift is `PRACTITIONER` no matter how confident its headline.

| Label | Means |
|---|---|
| `MEASURED` | Peer-reviewed study, or a large-N observational dataset with disclosed method and sample |
| `OFFICIAL` | Platform documentation or an on-record platform statement |
| `PRACTITIONER` | Vendor or agency study; lower rigor, often self-owned properties, often no control |
| `OPINION` | Expert consensus or engineering reasoning; no controlled evidence |
| `CONTESTED` | Sources conflict, or the evidence has known validity problems |

---

## 1. Summary table — decision to evidence

Every architectural decision in this repository, and what it rests on.

| Architectural decision | Evidence | Strength |
|---|---|---|
| 8–15 inline primary-source citations per article | Princeton GEO study, KDD 2024, N=10,000 queries: *Cite Sources* +30–40% PAWC; strongest on factual queries | `MEASURED` |
| Convert qualitative claims to cited statistics | Same study: *Statistics Addition* +30–40% PAWC; **strongest in the Law & Government domain**, which is this corpus | `MEASURED` |
| At least one attributed direct quotation per article | Same study: *Quotation Addition* +30–40% PAWC | `MEASURED` |
| Plain, fluent prose; no padding | Same study: *Fluency Optimization* +15–30%; best pair is Fluency + Statistics, >5.5% over any single method | `MEASURED` |
| **Ban keyword stuffing** | Same study: measured **10% worse than baseline** on one generative engine; Google spam policy names it | `MEASURED` + `OFFICIAL` |
| **Ban authoritative tone inflation** | Same study: measured **no significant improvement** | `MEASURED` |
| One natural-language question per H2, answered in the first 40–60 words | Ahrefs, 863K SERPs / 4M AIO URLs, 2026-03-02: only **37.9%** of AI-Overview-cited URLs rank in the top 10, down from 76.1% in July 2025 — citation is shifting toward fan-out sub-queries | `MEASURED` |
| Self-contained sections, no anaphora after a heading, entity re-anchored per section | Non-Google engines chunk → embed → retrieve top-k; the retrieval unit is the chunk. Chunking research finds "chunk quality and structural coherence are more important than chunk quantity" | `OPINION`, reasoned from `MEASURED` mechanism |
| 40–60 word direct-answer block, ≤320 characters | Portent, 7,854 featured snippets from 30,000 keywords, 2021-06-03: paragraph snippets typically 40–50 words; **no snippet exceeded 324 characters** | `MEASURED`, but pre-AI-Overviews |
| ≤5 rows in the primary comparison table, ≤3 words per cell | Same Portent study: table snippets max 5 rows; 85% of cells ≤3 words | `MEASURED`, same caveat |
| Lists of 5–8 items | Same study: list snippets max 8 bullets, 5–8 most frequent | `MEASURED`, same caveat |
| Named author + named reviewer + visible dates + editorial policy + corrections log | Search Quality Rater Guidelines §2.3 (2025-09-11): grant content is YMYL Financial Security *and* Government/Civics. Google: "Of these aspects, trust is most important" | `OFFICIAL` |
| Original synthesis, not aggregation of funder listings | March 2026 core update: government, institutional, and specialist sources gained; aggregators and directory sites lost | `PRACTITIONER`, large-N |
| No gating, no interstitials, no JS-dependent body text | A page a crawler cannot read cannot be cited. Google requires a page be indexed and snippet-eligible to appear in generative features | `OFFICIAL` |
| Verify AI crawler access in `robots.txt` before anything else | Otterly reports 73% of sites have technical barriers blocking AI crawler access; a blocked crawler is a hard zero | `PRACTITIONER` (the *consequence* of a block is `OFFICIAL`/mechanical) |
| Volatility isolation into one Current Figures callout | Design solution, not a measured tactic. Supported indirectly by Google's negative signal on date manipulation | `OPINION` |
| `dateModified` changes only on substantive change | Google: "Are you changing the date of pages to make them seem fresh when the content has not substantially changed?" listed as a negative signal | `OFFICIAL` |
| Schema emitted for entity disambiguation and rich results, never as a citation tactic | Google: "there's no special schema.org markup you need to add" for generative AI search | `OFFICIAL` |
| No FAQPage or HowTo rich-result dependency | FAQPage rich results ended 2026-05-07; HowTo deprecated 2023 | `OFFICIAL` |
| Hierarchical URLs, max depth 3, immutable slugs | Google says URL structure is not a direct ranking factor. Chosen for breadcrumb legibility, cluster auditability, and citation stability | `OPINION` |
| 3–8 contextual in-body links; zero orphans; ≤3 clicks from home | LinkStorm, 2.5M contextual links across 1,700 sites, 2026-01-30: 71% of contextual links sit within the first two hierarchy levels, <6% reach depth ≥4 | `MEASURED` (descriptive, not causal) |
| 2–6 word descriptive anchors, varied phrasing | Same LinkStorm study: 81% keyword-rich anchors, 15% generic, 3% naked URLs; ~61% of anchors are 1–3 meaningful words | `MEASURED` (descriptive) |
| Stagger publication of the 75 articles | Google spam policy defines scaled content abuse as many pages generated primarily to manipulate rankings, explicitly including generative-AI production without added value | `OFFICIAL` |
| Measure brand mention share, not only referral clicks | Ahrefs, 31,000+ mentions of its own brand across a 150M-prompt database, 2025-11-26: AI assistants linked when mentioning, only 10.7%–51.6% of the time | `MEASURED`, single brand |
| Pursue off-site brand mentions over link building | Ahrefs, 75,000 brands, 2025-05-26: brand web mentions correlate 0.664 with AI Overview mentions vs 0.218 for backlinks | `MEASURED`, correlational only |
| Pillar-cluster hub architecture | No controlled evidence. Vendor consensus. Face validity via fan-out coverage | `CONTESTED` / `OPINION` |
| Quarterly figure verification, annual full review | No published methodology behind any refresh-cadence number. Operational judgment | `OPINION` |
| Publish `llms.txt` | 97% of llms.txt files got zero requests in May 2026 | `MEASURED` — publish because it is free, not because it works |

---

## 2. The Princeton GEO study — the load-bearing measurement

**Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande. *GEO: Generative Engine Optimization.* arXiv:2311.09735. Submitted 2023-11-16, final revision 2024-06-28, accepted to KDD 2024.**
https://arxiv.org/abs/2311.09735 · PDF https://arxiv.org/pdf/2311.09735 `MEASURED`

This is the only peer-reviewed controlled experiment on generative-engine citation. Four of the article contract's rules exist because of it, and two bans exist because of it.

### Method

GEO-bench: **10,000 queries** (8,000 train / 1,000 validation / 1,000 test) drawn from nine datasets across 25 domains. Nine optimization methods, each applied by LLM rewriting to one randomly selected source per query, five random seeds, averaged. Improvement is relative to the unoptimized baseline for the same source.

Two visibility metrics:

- **Position-Adjusted Word Count (PAWC)** — citation word count normalized by response length, with exponential positional decay so earlier sentences weigh more.
- **Subjective Impression (SI)** — GPT-3.5 G-Eval scoring on seven dimensions (relevance, influence, uniqueness, subjective position, subjective count, click likelihood, material diversity), normalized to PAWC's mean and variance.

### Measured results

| Method | What it does | Measured effect |
|---|---|---|
| **Cite Sources** | Add citations from reliable sources | **+30–40% PAWC**, +15–30% SI |
| **Quotation Addition** | Add direct quotes from credible sources | **+30–40% PAWC**, +15–30% SI |
| **Statistics Addition** | Replace qualitative claims with quantitative ones | **+30–40% PAWC**, +15–30% SI |
| **Fluency Optimization** | Improve prose fluency | **+15–30%** visibility |
| **Easy-to-Understand** | Simplify language | **+15–30%** visibility |
| **Technical Terms** | Add domain terminology | Positive, smaller |
| **Unique Words** | Add rare vocabulary | Marginal |
| **Authoritative** | Adopt a more persuasive, authoritative tone | ❌ **"no significant improvement"** — measured **null** |
| **Keyword Stuffing** | Add query keywords, classic SEO style | ❌ **"little to no improvement"**; on a second generative engine, **10% *worse* than baseline** — measured **negative** |

Headline claim from the abstract: **"GEO can boost visibility by up to 40% in generative engine responses."**

### The two results that changed what we ban

Most GEO advice reports only the positives. Two of this paper's findings are prohibitions, and both are written into `ARTICLE-CONTRACT.md §9`:

1. **Keyword stuffing measured negative.** Not neutral. On a second generative engine it performed **10% worse than the unoptimized baseline**. Combined with Google's spam policy — keyword stuffing is "filling a web page with keywords or numbers in an attempt to manipulate rankings" (https://developers.google.com/search/docs/essentials/spam-policies, last updated 2026-05-15, `OFFICIAL`) — the tactic is now counterproductive in both stacks at once.
2. **Authoritative tone measured null.** Writing to *sound* like an authority produced **no significant improvement**. Only in debate and historical queries did it help at all. Authority in this corpus comes from citations, named reviewers, and primary sources — not from register. This is the direct evidence basis for the contract's ban on tone inflation and its "neutral reference tone" requirement.

### Four secondary findings that matter more than the headline

1. **Combinations beat singles.** The best pair is **Fluency Optimization + Statistics Addition**, outperforming any single method by **>5.5%**. *Cite Sources* is weak alone — 8% below Quotation Addition — but strong in combination (average **31.4%**). The combination analysis ran on a 200-example subset, so its numbers are not directly comparable to the main table.
2. **GEO levels up lower-ranked pages.** *Cite Sources* produced a **+115.1% visibility increase for sites ranked 5th** in the SERP, while the **top-ranked site's visibility fell 30.3%** on average when all sources were optimized simultaneously. Directly relevant: a new encyclopedia competing against entrenched incumbents starts from the position the method helps most.
3. **Effects are domain-specific.** *Cite Sources* is strongest on factual questions. **Statistics Addition is strongest in the "Law & Government" domain** — this corpus exactly. *Quotation Addition* is strongest in "People & Society," "Explanation," and "History." *Authoritative* helps only debate and historical queries.
4. **Classic SEO keyword tactics do not transfer.** The paper's own conclusion: techniques "effective in search engines may not translate to success in this new paradigm."

### Limitations — hold these in mind `CONTESTED`

The experiments ran on **GPT-3.5-era generative engines in 2023–24**. The Subjective Impression metric is itself LLM-judged, which carries a circularity risk. **No study has replicated these lift figures on 2026-era engines.** Treat the *direction* — evidence density, quotations, statistics, fluency — as robust, and the *magnitudes* as historical. Do not quote "+40%" as a forecast.

---

## 3. Google's official position on AI optimization

Google's AI optimization guide, **last updated 2026-07-10**, verbatim `OFFICIAL`:

> "You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search (including its generative AI capabilities), as Google Search itself doesn't use them."

> "Structured data isn't required for generative AI search, and there's no special schema.org markup you need to add."

> "There's no requirement to break your content into tiny pieces for AI to better understand it."

> "You don't need to write in a specific way just for generative AI search."

> "To be eligible to be shown in generative AI features on Google Search, a page must be indexed and eligible to be shown in Google Search with a snippet."

https://developers.google.com/search/docs/fundamentals/ai-optimization-guide (2026-07-10) · https://developers.google.com/search/docs/appearance/ai-features

**No special markup and no Markdown file is required.** That is the single most-ignored fact in the GEO market, and it is the reason this repository treats schema as an entity-disambiguation and rich-result tool rather than a citation tactic, and treats `llms.txt` as free insurance rather than a lever.

Google also documents the retrieval mechanism: AI Overviews and AI Mode use **RAG grounded in core Search ranking**, plus **query fan-out** — "a set of concurrent, related queries generated by the model to request more information and fetch additional relevant search results."

### How to reconcile Google with the GEO evidence

Two stacks, two implications:

- **Google's stack retrieves from its existing Search index.** Classic SEO is the entry ticket. Nothing exotic is required or rewarded.
- **Non-Google engines run their own retrieval pipelines** — fetch, chunk, embed, retrieve top-k, rerank, generate with citations. Here the retrieval unit is the chunk, and passage-level extractability demonstrably matters.

**Build for Google's rules as the floor and passage extractability as the differentiator.** Nothing in either requires writing unnaturally. The overlap between "well structured for a human reader" and "extractable for a retriever" is close to total, which is why the article contract reads like a style guide rather than a spec sheet.

Google's one hard structured-data rule that *does* bind: **"structured data matches the visible text on the page."** `OFFICIAL`

Google's passage ranking, launched February 2021, already scores sections of a page independently. Martin Splitt, on the record: *"It is actually a ranking change"* and *"There is nothing that you need to do, you don't need to make any changes to your website."* https://www.searchenginejournal.com/google-passage-ranking-martin-splitt/388206/ (2020-11-19) `OFFICIAL`. Google says it "primarily helps poorly-structured long-form pages" — meaning good structure was never leaving value on the table, it was avoiding a penalty of omission.

---

## 4. What AI engines actually cite

### 4.1 The source studies

**Ahrefs — most-cited domains.** ~76.7M AI Overviews, 957K ChatGPT prompts, 953.5K Perplexity prompts. Published **2025-06-11**. https://ahrefs.com/blog/top-10-most-cited-domains-ai-assistants `MEASURED`

| Domain | ChatGPT | Perplexity | AI Overviews |
|---|---|---|---|
| Wikipedia | **16.3%** | 12.5% | 8.4% |
| YouTube | not top-10 | **16.1%** | 9.5% |
| Reddit | not top-10 | not top-10 | **7.4%** |
| Quora | not top-10 | not top-10 | 3.6% |
| Reuters / AP / AS.com | 2.6–4% | — | — |

**Ahrefs — engine overlap.** Published **2025-06-12**. https://ahrefs.com/blog/top-mentioned-sources-are-not-shared-across-ai-assistants `MEASURED`
**Only 14% of the top 50 most-mentioned sources are shared across all three engines** — 7 of 50. Documented biases: AI Overviews lean toward authoritative health, finance, and encyclopedic sources plus Google properties and user-generated content; ChatGPT leans on publishers and licensed partners; Perplexity pulls from a broader international corpus.

**Semrush — most-cited domains.** 230,000+ prompts, 100M+ citations, collected **2025-07-14 to 2025-10-12**, published **2025-11-10**. https://www.semrush.com/blog/most-cited-domains-ai/ `MEASURED`
Top-5 ChatGPT: Reddit, Wikipedia, Medium, Forbes, LinkedIn. AI Mode: LinkedIn (~15%), YouTube, Reddit, Google, Google Blog — Wikipedia only ~3%. Perplexity: Reddit, LinkedIn, **NIH**, Microsoft, Google.

**Similarweb — citation surface growth.** AI citation rates in ChatGPT US responses rose from **1.6% (June 2025) to 6.8% (May 2026)**. https://www.similarweb.com/blog/marketing/geo/gen-ai-stats/ `MEASURED`

**Ahrefs — AI Overview sourcing vs. rank.** 863K keyword SERPs, 4M AI Overview URLs, published **2026-03-02**. https://ahrefs.com/blog/ai-overview-citations-top-10 `MEASURED`
**37.9%** of AIO-cited URLs appear within the first 10 blocks; 31.2% rank 11–100; 31.0% rank beyond 100. The prior study — 1.9M citations, published **2025-07-21**, https://ahrefs.com/blog/search-rankings-ai-citations — found **76.1%**. Ahrefs attributes the shift to more aggressive query fan-out under Gemini 3.

**Ahrefs — mention vs. link.** 31,000+ mentions of Ahrefs' own brand, drawn from a database of 150M prompts, published **2025-11-26**. https://ahrefs.com/blog/ai-citations-vs-impressions-study `MEASURED`, single brand

| Platform | Linked when mentioned |
|---|---|
| Perplexity | 51.6% |
| AI Mode | 36.8% |
| ChatGPT | 26.9% |
| Copilot | 26.1% |
| Gemini | 16.8% |
| **AI Overviews** | **10.7%** |

Average ~28%. Weighted by search volume, linked-mention share rises substantially (78.4% Perplexity, 13.0% AI Overviews) — links cluster on high-volume queries. Note the scope honestly: this tracks one brand's mentions, not a cross-brand sample.

**Peec AI.** 30M sources, 5 platforms, **2026-03-31**. https://searchengineland.com/ai-search-engines-cite-reddit-youtube-and-linkedin-most-study-473138 `PRACTITIONER`. Reddit, YouTube, LinkedIn, Wikipedia, Forbes.

**Otterly.** 1M+ citations, Jan–Feb 2026. https://otterly.ai/blog/the-ai-citations-report-2026/ `PRACTITIONER`. Community platforms 52.5% vs brand domains 47.5%; news and media 20.3%; **73% of sites have technical barriers blocking AI crawler access**. The same report claims "reference-grade content receives 3–5× more citations" with **no disclosed methodology** — treat that claim as unverified and do not repeat it.

### 4.2 The caution that governs all of the above

**Citation source distributions are unstable quarter to quarter, and the instability is measured, not speculated.** Semrush observed patterns shifting *inside a single 90-day study window*: Reddit fell from roughly **60% to 10%** and Wikipedia from roughly **55% to 20%** of ChatGPT citations after mid-September 2025 changes. Ahrefs' own top-10 correspondence figure moved from **76.1% to 37.9% in eight months**.

Practical consequence: **never build an architecture on a citation distribution.** Any strategy of the form "engine X favors source type Y, so become Y" has a half-life of about one quarter. The durable strategy is structural — extractable passages, dense primary-source citation, entity clarity, named accountability — because it is the only thing that generalizes across engines whose overlap is 14%.

### 4.3 What follows for an owned encyclopedia

1. **Top-10 ranking is neither sufficient nor strictly necessary.** The 76% → 38% collapse means AI Overviews increasingly cite pages matching *fan-out sub-queries*. Optimize for breadth of sub-question coverage, not head-term rank. This is the strongest single argument for one-question-per-H2.
2. **Wikipedia and `.gov` are the reference-class competitors.** In finance and government topics, AI Overviews favor authoritative institutional sources. The encyclopedia must look and behave like reference material.
3. **Engine fragmentation means no single optimization target.** With 14% top-50 overlap, "optimize for AI" is not a coherent instruction.
4. **Off-site presence is the multiplier.** Web mentions correlate 0.664 with AI visibility versus 0.218 for backlinks (Ahrefs, 75,000 brands, 2025-05-26, https://ahrefs.com/blog/ai-overview-brand-correlation/ `MEASURED`, correlational). Top-quartile brands by web mentions earn up to **10× more** AI Overview mentions than the next quartile; **26% of brands had zero**. Ahrefs explicitly cautions that correlation is not causation and that all correlations are moderate-to-weak.
5. **Crawler access gates everything.** See `BUILD-NOTES.md` §1.

---

## 5. The YMYL determination

**Grant content is YMYL. This is not a judgment call, and the article contract's author, reviewer, dating, and citation requirements all descend from it.**

The Search Quality Rater Guidelines, **version dated 2025-09-11**, https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf `OFFICIAL`, define YMYL in §2.3 as topics with:

> "a high risk of harm because content about these topics could significantly impact the health, financial stability, or safety of people, or the welfare or well-being of society."

Four categories are named. Grant content lands in two of them simultaneously:

**YMYL Financial Security** — the guidelines describe this as:

> "topics that could damage a person's ability to support themselves and their families"

Grant eligibility rules, application requirements, funding amounts, indirect cost rates, audit thresholds, and deadlines directly determine whether an organization gets funded and whether it survives an audit of funds it already spent. A wrong eligibility statement costs an applicant a cycle. A wrong allowability statement costs them a disallowed cost.

**YMYL Government, Civics & Society** — the guidelines describe this as covering:

> "issues of public interest, trust in public institutions... and other governmental or civic topics"

Federal and state grant programs are government programs. Most of this corpus explains statute, regulation (2 CFR 200 and agency adoptions), and the administrative machinery of public money.

The rater standard applied to pages in these categories:

> "low quality pages could potentially negatively impact the health, financial stability, or safety of people"

Google's confirmation in its helpful-content guidance, https://developers.google.com/search/docs/fundamentals/creating-helpful-content `OFFICIAL`: it gives *"even more weight to content that aligns with strong E-E-A-T for topics that could significantly impact"* wellbeing. And, decisively for how this repository is built:

> "Of these aspects, trust is most important."

### The aggregator risk

The **March 2026 core update** reinforced the YMYL direction empirically: **government domains (Census.gov, BLS.gov), official and institutional sites, and specialist niche resources gained**, while **aggregators and directory sites lost**. Volatility was extreme — roughly 80% of top-3 results shifted and 24% of prior top-10 pages fell out of the top 100. https://searchengineland.com/march-2026-google-core-update-what-changed-474397 `PRACTITIONER`, large-N

**An encyclopedia published by a grant discovery platform is structurally at risk of reading as an aggregator.** The counter is editorial substance: original synthesis rather than reproduced funder listings, named accountable authors, primary-source citation, transparent methodology, and a visible corrections log. This is why the contract bans reproducing funder descriptions verbatim and caps product links at one per article.

### Google's Who / How / Why test `OFFICIAL`

- **Who** — is authorship obvious? Byline, author page, and `Person` schema.
- **How** — is the creation process explained? Google specifically recommends disclosing automation and AI use, and explaining *"why automation or AI was seen as useful to produce content."* The editorial policy page must do this.
- **Why** — *"perhaps the most important question."* Content must exist "primarily to help people," not to manipulate rankings.

### The dates rule

Google flags as a negative signal:

> "Are you changing the date of pages to make them seem fresh when the content has not substantially changed?"

And from the publication-dates guidance, https://developers.google.com/search/docs/appearance/publication-dates `OFFICIAL`: do not specify future dates, minimize other dates on the page, and ensure visible and structured dates match.

**Rule: `dateModified` changes only on substantive content change.** Never on a build, a typo fix, or a CSS change. Verification passes that changed nothing use the separate, non-schema "Facts verified" date on the Current Figures callout.

---

## 6. The 2026 schema deprecations

The section of any pre-2026 SEO playbook most likely to be wrong.

| Type | Status | Effective dates | Source |
|---|---|---|---|
| **FAQPage** | ❌ Rich results ended | Deprecation notice added **2025-05-08**; rich results ended **2026-05-07**; search-appearance filter, rich-results report, and Rich Results Test support removed **June 2026**; documentation removed **June 2026**; Search Console API support ended **August 2026** | `OFFICIAL` https://developers.google.com/search/docs/appearance/structured-data/faqpage · https://www.searchenginejournal.com/google-drops-faq-rich-results-from-search/574429/ |
| **HowTo** | ❌ Deprecated | Mobile **August 2023**; removed from the Search Gallery | `OFFICIAL` https://developers.google.com/search/docs/appearance/structured-data/search-gallery |
| **Dataset** | ⚠️ Narrowed | Powers **only Google Dataset Search**, not web Search results | `OFFICIAL` https://ppc.land/google-phases-out-practice-problem-and-dataset-structured-data/ (2025-11-05) |
| **Practice Problem** | ❌ Support ended | **January 2026** | `OFFICIAL` same source |
| **Course Info, ClaimReview, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing** | ❌ Reporting and testing dropped | **September 2025**. Markup is harmless but inert | `OFFICIAL` https://www.searchenginejournal.com/google-drops-search-console-reporting-for-six-structured-data-types/555560/ |
| **Article, BreadcrumbList, Organization, ProfilePage, Speakable, Dataset, Q&A, Video, Image Metadata** | ✅ Still supported | — | `OFFICIAL` https://developers.google.com/search/docs/appearance/structured-data/search-gallery |

John Mueller's framing of the 2026 cleanup: *"Understand that markup types come and go, but a precious few you should hold on to, like title and meta robots."* `OFFICIAL` https://www.stanventures.com/news/google-john-mueller-schema-update-2026-5719/

**Consequence for this repository:** FAQ sections stay in the article contract because they capture People Also Ask placements and answer fan-out sub-queries as visible prose. They do **not** stay because of markup. `FAQPage` is emitted in `schema/article.jsonld` only because it is free; no one should expect a rich result from it, and no FAQ content should ever be written *for* the schema. `DefinedTerm` and `DefinedTermSet` are likewise emitted for semantic clarity and third-party consumers — schema.org lists them in the "new" area with roughly 10K–100K implementing domains, and there is no Google rich result. https://schema.org/DefinedTerm `OFFICIAL`

---

## 7. What we do not know

The honest section. Everything below is a place where the evidence is thin, contested, or absent, and where a reasonable person could build this differently. Treat each as a revisable decision rather than a settled rule.

### 7.1 Pillar-cluster architecture — no controlled evidence `CONTESTED`

**There is no controlled experiment showing that pillar-cluster architecture causes ranking gains independent of simply publishing more good content on a topic.** Every topic-cluster source examined during research was vendor marketing or agency content with no isolated test. **Google has never endorsed the term.**

What *is* documented: internal links pass signals and aid discovery, and query fan-out rewards broad topical coverage. What *is* measured is the Ahrefs fan-out finding — pages cited in AI Overviews increasingly come from *related* SERPs rather than the primary query's SERP, so breadth of angle coverage on a topic is a retrieval asset. That is the real argument for clusters, and it is an argument for **coverage**, not for a particular link topology.

The eight-hub structure in `data/taxonomy.json` should be defended as **a content-planning discipline with strong face validity** — it makes coverage gaps visible, makes orphan auditing trivial, and gives readers a legible map. It should not be defended as a proven ranking mechanism. Cluster sizing (5 minimum, 8–15 target, ~20 ceiling) is judgment, not measurement.

### 7.2 Content decay rates and refresh cadence — vendor claims with no methodology `CONTESTED`

**There is no rigorous public study of content decay rates.** The most-cited figure — **−1.21% traffic decay per week** — traces to a 2018 AdEspresso analysis and is repeated by Animalz (https://www.animalz.co/blog/content-refresh, published 2020-11-30, updated 2026-05-01), which also claims quarterly refreshes yield **42% better results** than annual refreshes and cites a single case of **+55% weekly traffic** from one refresh.

**State this plainly: these are vendor claims with no published methodology, no sample description, and no control. Do not treat them as facts, and do not put them in a slide.**

The refresh cadence in `README.md` — quarterly for figures, annual for full review, 24 months for structural — is `OPINION`. It is calibrated to how fast grant figures actually move (fiscal-year boundaries, annual rate negotiations, periodic Uniform Guidance revision), not to any measured decay curve. If someone proposes a different cadence with a better argument about the underlying funding cycle, they are not contradicting evidence, because there is none to contradict.

What *is* supported: Google's AI guidance names RAG as a technique used to improve *"the quality, accuracy, and freshness of AI responses,"* and Google's February 2026 Discover core update explicitly aimed to surface *"more in-depth, original, and timely content from websites with expertise in a given area"* (announced 2026-02-05, completed 2026-02-27, https://developers.google.com/search/blog/2026/02/discover-core-update) `OFFICIAL`. Freshness matters. The *rate* at which it matters is unmeasured.

### 7.3 Whether schema lifts AI citation — contested, and the affirmative evidence is weak `CONTESTED`

Google says flatly no: *"there's no special schema.org markup you need to add."*

The countervailing claim comes from a single practitioner study: a 90-day experiment (February–May 2026) by Deepak Gupta tracking **50,431 citations** across six engines from 200 prompts against 240 pages on four properties **he owns**, with 12 staged changes. https://securityboulevard.com/2026/06/the-geo-measurement-study-50000-ai-citations-in-90-days-what-actually-moves-citation-share/ `PRACTITIONER`

Reported lifts: Person/Organization schema with 8+ `sameAs` entries **+34%**; visible dating and `dateModified` discipline **+22%**; chunk-level restructuring **+18%**; methodology pages **+9%**. Reported non-movers: backlinks, generic FAQ schema (described as actively devalued by some engines), length increases without new topical coverage, keyword density. Gated content drew **14 citations vs 1,847** for ungated equivalents.

**Why this is weak evidence:** self-owned properties, no control group, 12 changes staged sequentially over 13 weeks with no isolation, a single operator, and engine algorithms changing underneath the experiment. **Do not cite these numbers as fact, and do not let anyone promise citation lift from markup.**

**The honest position:** schema is not a demonstrated citation lever for Google's AI surfaces. It *is* a cheap, machine-readable way to assert entity identity and `sameAs` links, which plausibly helps entity resolution in non-Google pipelines and costs nothing to emit. **Emit it for entity disambiguation and rich results.** The one finding from the Gupta study worth acting on regardless — because it is free and correct for other reasons — is **ungate everything** and **be disciplined about dates**.

### 7.4 The 40–60 word answer block — measured, but on the wrong era `CONTESTED`

The Portent study (N=7,854 featured snippets, 30,000 keywords, desktop only, published **2021-06-03**, https://portent.com/blog/seo/featured-snippet-display-lengths-study-portent.htm `MEASURED`) is real and well-sampled. It is also **from 2021, before AI Overviews**, and featured-snippet real estate has since been substantially displaced.

Use 40–60 words because it is a good discipline that also produces a clean retrieval chunk — not because it guarantees a snippet. The firmer constraint from that study is the **~320-character display cap** (no snippet exceeded 324 characters), which is why the contract states both.

### 7.5 AI-slop suppression — directionally clear, N=2 `PRACTITIONER`

A four-month experiment (April–July 2026) launched two domains with roughly 1,000 AI-generated posts each. **Both were algorithmically suppressed with zero manual actions and no Search Console notification.** Site B collapsed from 2,426 daily impressions to 15 in four days. Site A grew to 21,700 weekly impressions by mid-May, then collapsed from 859 to 9 impressions on 25–26 June. Fictional author boxes did not save Site B. https://otterly.ai/blog/geo-experiment-2000-ai-blogs-google-penalization/ `PRACTITIONER`, well-instrumented

**Caveats that matter:** brand-new domains with no authority, a single niche, N=2, and the two sites cannibalized each other. The direction is unambiguous and matches the stated aim of the February 2026 Discover update, but this is not a measurement of how a reviewed, cited, named-author corpus on an established domain behaves.

### 7.6 The 73%-blocked figure `PRACTITIONER`

Otterly's claim that 73% of sites have technical barriers blocking AI crawler access has no disclosed methodology for how "technical barrier" was detected. **Treat the number as unverified.** It does not matter much: the check it motivates costs five minutes, the failure mode it guards against is total, and you should run it against your own logs rather than trusting anyone's population estimate.

### 7.7 One claim we reject outright

**"Listicles win 21.9% of AI citations."** Traced to source during research: **no methodology, no sample, no date disclosed.** Do not use it. It circulates widely and is worth recognizing on sight.

---

## 8. Confidence summary

| Claim | Confidence | Basis |
|---|---|---|
| Citations, quotations, and statistics increase generative citation | **High** | Peer-reviewed, KDD 2024, N=10,000 queries |
| Keyword stuffing is counterproductive in generative engines | **High** | Same paper; measured **negative** |
| Authoritative tone inflation does nothing | **High** | Same paper; measured **null** |
| Google requires no special markup, chunking, or AI text file | **High** | Google official docs, 2026-07-10 |
| llms.txt is largely unread | **High** | 97% of files got zero requests, May 2026; Ahrefs 137K domains, Originality.ai 3M+ sites |
| Grant content is YMYL Financial Security and Government/Civics | **High** | Search Quality Rater Guidelines §2.3, 2025-09-11 |
| FAQPage and HowTo rich results are dead | **High** | Google docs; FAQ effective 2026-05-07 |
| Schema values must match visible text | **High** | Google official, explicit requirement |
| Off-site brand mentions outweigh backlinks for AI visibility | **Medium-High** | Ahrefs, 75K brands; correlational only |
| Top-10 ranking is decreasingly sufficient for AIO citation | **Medium-High** | Ahrefs, 863K SERPs; 76.1% → 37.9% |
| Citation source distributions are unstable quarter to quarter | **Medium-High** | Semrush observed the shift mid-study; Ahrefs figures moved in 8 months |
| Self-contained passages help non-Google retrieval | **Medium** | Reasoned from documented chunk-and-embed mechanics; not directly measured |
| 40–60 word answer blocks | **Medium** | Portent N=7,854, but 2021, pre-AI-Overviews |
| AI-slop content gets algorithmically suppressed | **Medium** | Well-instrumented but N=2 new domains, confounded |
| Publishing volume in one topical area carries scaled-content risk | **Medium** | Google policy is official; the threshold is not published |
| Pillar-cluster architecture improves rankings | **Low** | No controlled evidence; vendor consensus only |
| Content decay rates (−1.21%/week) and refresh lift (+42%) | **Low** | Vendor claims, no published methodology |
| Schema markup lifts AI citation | **Low / contested** | Google says no; one weak practitioner study says +34% |
| "Listicles win 21.9% of AI citations" | **Rejected** | No methodology, sample, or date disclosed |

---

## 9. How to revise this document

1. **Add, do not overwrite.** When new evidence arrives, add a row and date it. Keeping the superseded claim visible is how anyone can tell whether the ground moved or the vendor did.
2. **Label first, then decide.** Assign the evidence label before deciding what to change. A `PRACTITIONER` finding does not get to override a `MEASURED` one because it is newer.
3. **Never upgrade a label.** A practitioner claim stays `PRACTITIONER` even after it is repeated a hundred times.
4. **A changed rule needs a changed contract.** If a decision in §1 is revised, update `docs/ARTICLE-CONTRACT.md` and the validator in the same change, and say so in `/corrections/` if published articles are affected.
5. **Re-verify the URLs annually.** Platform documentation moves. A dead citation in the evidence dossier for a corpus that demands live citations is not a good look.
