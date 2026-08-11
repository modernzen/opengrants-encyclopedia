# Schema Templates

JSON-LD templates for the encyclopedia, one per page type. `{{PLACEHOLDER}}` tokens are filled from article frontmatter, `data/taxonomy.json`, `data/manifest.json`, and `data/glossary.json` — never by hand. Each file's `_comment` block lists exactly what fills each token.

| File | Emitted on | Contains |
|---|---|---|
| `organization.jsonld` | Homepage or `/about` only, **once** | `Organization`, `WebSite` |
| `article.jsonld` | Every cluster article | `Article`/`TechArticle`, `WebPage`, `BreadcrumbList`, author `Person`, reviewer `Person`, `Organization` ref, `about` → `DefinedTerm` refs, `citation[]`, `FAQPage` |
| `hub.jsonld` | Each of the 8 hubs and the root index | `Article`, `CollectionPage`, `ItemList` of children, `BreadcrumbList`, `Person`, `Organization` ref |
| `glossary.jsonld` | `/encyclopedia/glossary/` | `DefinedTermSet` with `DefinedTerm` members, `WebPage`, `BreadcrumbList` |

The author page at `/authors/sedale-turbovsky/` emits `ProfilePage` with the author `Person` as `mainEntity`. It has no template here because it is a single hand-built page; use the `Person` node from `article.jsonld` verbatim so the `@id` matches.

---

## Rule 1 — schema must match visible text

**Every value emitted in JSON-LD must appear in the visible text of the page that emits it.** This is Google's explicit requirement, and it is the rule most likely to be broken accidentally by a templating system that has access to more data than the page renders.

Concretely:

- `headline` equals the visible H1, character for character.
- `description` equals the direct-answer block or its trimmed `metaDescription` form — text a reader can see.
- `datePublished` and `dateModified` equal the visible **Published** and **Last reviewed** lines exactly. If the byline says "Last reviewed 3 September 2026," the schema says `2026-09-03` with timezone, and nothing else.
- `author.name` and the reviewer's `name` equal the visible byline names.
- Every `citation` entry corresponds to a source actually linked in the article body and listed in its Sources section.
- Every `ItemList` child on a hub is also visibly linked in the hub's prose.
- Every `DefinedTerm` description is the definition a reader can read on the glossary page.

If a value has no visible counterpart, either render it or drop it from the schema. Do not use JSON-LD as a place to assert things the page does not say.

**Google's author-markup rules apply too:** include all authors, one `author` field per person and never merged, use `url` or `sameAs` for disambiguation, and put **only the name** in `author.name` — job titles and honorifics go in separate properties (`jobTitle`, `description`). `Person` for humans, `Organization` for companies. https://developers.google.com/search/docs/appearance/structured-data/article

---

## Rule 2 — `@id` references, never duplicate definitions

Every entity that appears on more than one page is **defined once** and **referenced everywhere else** by `@id`.

| Entity | Canonical `@id` | Defined in |
|---|---|---|
| Organization | `https://opengrants.io/#organization` | `organization.jsonld`, homepage only |
| WebSite | `https://opengrants.io/#website` | `organization.jsonld`, homepage only |
| Author (Person) | `https://opengrants.io/authors/sedale-turbovsky/#person` | the author page |
| Glossary term set | `https://opengrants.io/encyclopedia/glossary/#termset` | `glossary.jsonld` |
| A glossary term | `https://opengrants.io/encyclopedia/glossary/#term-{slug}` | `glossary.jsonld` |

A reference is a bare node with only the `@id`:

```json
{ "publisher": { "@id": "https://opengrants.io/#organization" } }
```

Not this:

```json
{ "publisher": { "@type": "Organization", "name": "OpenGrants", "url": "..." } }
```

**Why it matters:** duplicating a full `Organization` definition across 75 articles publishes 75 separate assertions of the same entity, which invites conflict the moment one page drifts. `@id` referencing gives every consumer a single node to resolve, which is the entire point of emitting entity markup for a corpus this size.

The author `Person` node in `article.jsonld` and `hub.jsonld` is shown with full properties because most build systems need the shape. **If the author page is live, prefer emitting the bare `@id` reference on article pages** and let the profile page carry the definition.

Page-scoped `@id`s use a URL fragment on the page's own URL: `{url}#article`, `{url}#webpage`, `{url}#breadcrumb`, `{url}#reviewer`. These are unique per page by construction.

Glossary term `@id`s are referenced from article `about` arrays. **A term slug is as immutable as an article slug** — changing one silently breaks every article pointing at it.

---

## Rule 3 — what schema is for here, and what it is not

**Emit schema for entity disambiguation and rich results. Not as a citation tactic.**

Google states plainly that structured data is not required for generative AI search and that there is no special schema.org markup to add for it (https://developers.google.com/search/docs/fundamentals/ai-optimization-guide, 2026-07-10). One practitioner study claims a +34% citation lift from `Person`/`Organization` schema with deep `sameAs`; it ran on self-owned properties with no control group and twelve changes staged over thirteen weeks. `docs/RESEARCH-BASIS.md` §7.3 has the full assessment.

The honest position: schema is a cheap, machine-readable way to assert entity identity and `sameAs` links, which plausibly helps entity resolution in non-Google retrieval pipelines and costs nothing to emit. **Do not let anyone promise citation lift from markup, and never shape content around schema.**

The one property worth extra care is **`citation`**. One `CreativeWork` per external source, populated from `externalSources` in `data/manifest.json`. It is underused across the web, and it encodes in machine-readable form the highest-confidence measured lever available — dense primary-source citation (Princeton GEO study, KDD 2024: *Cite Sources* +30–40%).

---

## Rule 4 — what not to emit

| Type | Status | Do |
|---|---|---|
| `HowTo` | Deprecated on mobile August 2023, removed from the Search Gallery | Do not emit |
| `Practice Problem` | Support ended January 2026 | Do not emit |
| `Course`, `ClaimReview`, `Estimated Salary`, `Learning Video`, `Special Announcement`, `Vehicle Listing` | Reporting and testing dropped September 2025 | Do not emit |
| `Dataset` | Surfaces only in Google Dataset Search, not web results | Only if actual downloadable datasets are published |
| `speakable` | Still in the gallery, but limited to news use cases in practice | Skip; no demonstrated ROI for an encyclopedia |

### `FAQPage` — included, but understand why

`article.jsonld` emits `FAQPage`, and **no Google rich result exists for it**. FAQ rich results were deprecated with a notice on 2025-05-08 and **ended on 2026-05-07**; the search-appearance filter, rich-results report, and Rich Results Test support were removed in June 2026, documentation was removed in June 2026, and Search Console API support ended in August 2026.

It stays in the template for one reason: Google confirms the markup "won't cause problems," and it costs nothing if the CMS emits it from FAQ content that already exists as visible prose. One practitioner source reports that some engines actively devalue generic FAQ schema — unverified, but a reason not to over-invest.

**The rule that matters: FAQ sections exist as visible prose because they capture People Also Ask placements and answer fan-out sub-queries. They do not exist for the markup. Never write an FAQ question in order to fill a schema slot.** If your CMS makes `FAQPage` emission awkward, drop it and lose nothing.

---

## Validation before launch

1. **Google Rich Results Test** and the **Schema.org validator** on one article, one hub, the glossary, and the author page.
2. **`@id` resolution check** — crawl the emitted JSON-LD across all pages and assert that every `@id` referenced somewhere is defined exactly once somewhere.
3. **Visible-text diff** — for each page, assert `headline`, `description`, `datePublished`, `dateModified`, `author.name`, and reviewer `name` all appear in the rendered HTML.
4. **Placeholder sweep** — grep the production HTML for `{{`. A shipped `{{PLACEHOLDER}}` is worse than an omitted property.
5. **Reviewer gate** — never emit an article graph while `reviewer.name` is `REVIEWER_REQUIRED`. That article is not publishable at all.
