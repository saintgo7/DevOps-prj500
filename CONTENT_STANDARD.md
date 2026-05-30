# Content Standard — what counts as "good-influence" SDG content

> **License**: This document is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Anyone may copy, translate, and adapt it. The intent is to make the editorial criteria *legible* and *forkable*, not proprietary.
> **Stable URL** (when published): `https://sdgi.app/CONTENT_STANDARD.md` and per-locale at `/{locale}/standard`.
> **Machine-readable mirror**: `/.well-known/sdgi-content-standard.json` (see ADR-0013).

This document defines what may be selected, summarised, and republished as "this week's findings" or in a "daily column" on the platform. Editors, contributors, AI assistants, and partner organisations all use this standard.

---

## 1. Why a standard

Without explicit criteria, daily content drifts toward the loudest sources, English-only outlets, donor narratives, and uncited claims. SDG implementation deserves better. The standard exists so:

- A reader anywhere can trust that what they see was selected by published criteria, not editorial whim.
- An AI assistant drafting a column can self-check against the criteria.
- A partner organisation republishing our feeds knows what they are passing on.
- A future fork knows exactly what they are inheriting and where they may want to differ.

---

## 2. Scope — what we curate

We curate findings that meet **all** of:

1. **SDG-relevant**: maps to at least one of the 17 UN Sustainable Development Goals or their 169 targets, in non-trivial substance (not a passing mention).
2. **Action-ready or action-relevant**: a reader can do something about it — learn, fund, partner, advocate, replicate, or formally cite.
3. **Public**: the source URL is reachable without payment or login from the global internet.
4. **Verifiable**: the source is identifiable (DOI, ISSN, publisher, named author, government domain, registered NGO, recognised network) — not anonymous social-media claims.
5. **Attribution-clean**: republishing a short excerpt + summary respects the source's licence and our attribution rule (§5).

We exclude (no exceptions):

- Anonymous or pseudonymous social-media-only claims that cannot be traced to a verifiable origin.
- Content behind a paywall whose summary cannot honestly be conveyed without quoting protected text.
- Content that names individuals (especially minors, victims, marginalised people) without their evident consent.
- Content whose primary effect is to surveil grassroots organisers or to score communities for donor eligibility without consent (see [`PRINCIPLES.md §7`](./PRINCIPLES.md#7-data-sovereignty-for-the-person-who-lived-the-data)).
- Content from sanctioned entities under UN Security Council sanctions.

---

## 3. Source classes (with their evidence requirements)

| Class | Evidence required | Default trust weight |
|---|---|---|
| **Peer-reviewed paper** | DOI or arXiv id; venue named | 1.00 |
| **UN body report** | Official UN domain; document number | 0.95 |
| **Government / official statistics** | `.gov.*` or recognised national stats office | 0.90 |
| **Multilateral / IFI** | Official org domain; report id | 0.90 |
| **Bilateral donor (KOICA / JICA / GIZ / AFD / FCDO / USAID …)** | Official donor domain | 0.85 |
| **Recognised research institute / think tank** | Named author + publisher | 0.80 |
| **Established NGO / network** | Registered org page | 0.75 |
| **Local civil society / grassroots** | Named org or person; verifiable contact | 0.70 |
| **Civic tech / open-source project** | Stable repo; named maintainer | 0.65 |
| **Reputable news outlet** | Editorial masthead + correction policy | 0.60 |
| **Funding call** | Issuing body + deadline | n/a (categorical) |

The trust weight informs **ranking and visibility**, not eligibility. A grassroots finding (0.70) is not "less true" than a UN report (0.95) — but the system asks for proportionally more independent evidence before promoting it to the daily column. Equity weight (see [PRINCIPLES.md §10](./PRINCIPLES.md#10-transparency-by-default)) compensates against trust weight to avoid systematically silencing grassroots voices.

---

## 4. SDG mapping requirement

Every published finding declares:

- One or more `SDG-{1..17}` goals.
- Optionally one or more targets (`SDG-{n}.{m}`) and indicators (`SDG-{n}.{m}.{k}`).
- The mapping rationale in plain language ("This study measures rural electrification, mapping to SDG-7.1 access to electricity").
- The confidence of the mapping (0.0–1.0) and whether it is AI-suggested or human-confirmed.

Mappings that are AI-only and below 0.70 confidence are flagged for human review before publication.

---

## 5. Attribution and excerpt rules

- **Original-text excerpt**: up to 250 words, verbatim, with a direct link to the source. This is the *quotation* under fair-use / fair-dealing analogues.
- **Plain-language summary**: written by an editor or AI, distinct from the excerpt, in the reader's language. This summary cites the excerpt by paragraph or sentence.
- **Attribution block** at the top of every column or feed entry includes:
  - Source title
  - Author(s) where named
  - Publisher
  - Publication date
  - DOI / URL
  - Source licence (where declared)
- **Translation handling**: when the source is in language A and the column is in language B, both are linked. The translated summary is clearly marked as translation, not reproduction. Contested terms keep the original in parentheses.
- **Correction**: any source contesting our excerpt or summary may request correction; we publish the correction within 7 days and link it to the original column.

---

## 6. Geographic & demographic balance

The platform sets monthly minimums to avoid donor-side over-representation:

- **At least 30% of columns** in any rolling 30-day window draw from a **least-developed country (LDC)** source as defined by the [UN list of LDCs](https://www.un.org/ohrlls/content/list-ldcs).
- **At least 40% of columns** include at least one **non-English original source language**.
- **No more than 25% of columns** in any 30-day window come from a single source organisation.
- The system reports these proportions publicly each month.

If the queue cannot hit these minimums, the system **delays** rather than silently filling with over-represented sources. A delay is logged and visible.

---

## 7. AI use

- AI may **draft** columns (excerpt selection, summary, translation, SDG mapping suggestion).
- AI **never publishes** without human approval (§9).
- Every AI-drafted segment carries the model name, the prompt template version, the confidence, and the citations the model used.
- Where AI translation is uncertain, the column shows the original alongside.

See [`PRINCIPLES.md §9 (AI as colleague)`](./PRINCIPLES.md#9-ai-as-a-colleague-not-a-replacement) and [ADR-0003](./docs/adr/0003-claude-as-primary-llm.md).

---

## 8. Eligibility checklist (the system enforces this on every draft)

A column proceeds to the approval queue **only if all are true**:

- [ ] At least one verifiable source per §3
- [ ] At least one SDG mapping per §4 with confidence ≥ 0.70 *or* human confirmation
- [ ] Original-text excerpt ≤ 250 words **and** present
- [ ] Plain-language summary present in at least the publishing locale
- [ ] Attribution block per §5 complete
- [ ] No private personal information without evident consent
- [ ] Source not on UN sanctions list
- [ ] If AI was involved, model name + prompt version recorded

If any item fails, the system explains in plain language which item failed and what is missing.

---

## 9. Approval (this is the door before publication)

Every column requires **at least one human approver** to publish; sensitive categories (medical claims, legal status, child protection, conflict zones) require **at least two**. Approvers may approve, reject, or request revision via:

- A signed link sent to **email** *and* **SMS** (one-tap approve / reject / view).
- A page in the platform showing pending approvals.
- A signed callback to a partner approval endpoint (for organisations with internal approval flows).

The approval token is single-use, expires in 72 hours, and never embeds personal data. Approval decisions are logged immutably (audit trail) and the column metadata records who approved, when, and via which channel.

See [ADR-0013](./docs/adr/0013-daily-columns-approval-partners.md) for the full approval architecture.

---

## 10. Partner integration

A column that has been approved is published. At that moment the system can fan it out to **partner organisations** that have registered to receive it. Partners receive an HMAC-signed webhook with the canonical JSON-LD; they are also free to pull from the public Atom feed under CC BY 4.0.

Partners are **never** automatically given access to user-private data (subscriptions, collaboration interests, drafts). They receive only what is on the public column page.

---

## 11. Versioning of this standard

This document is versioned with the platform. Each published column records the **standard version** it was approved under, so historical decisions remain interpretable as the standard evolves.

Current version: **v0.1** (2026-04-25)
