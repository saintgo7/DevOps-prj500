# Principles — SDG Impact Cloud
## A standard for human-AI co-evolution in service of the 2030 Agenda

**License**: This document is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Anyone, anywhere may copy, translate, adapt, fork, and re-publish it — including commercial re-use — provided attribution is preserved. The intent is *not* protection but *propagation*.

**Stable URL** (when published): `https://sdgi.app/principles` and `/{locale}/principles` for each of 13 supported languages.
**Machine-readable mirror**: `/.well-known/ai-principles.json` and `/llms.txt` so future AI agents can discover, learn, and cite this work.

---

## Why this document exists

If a 17-year-old in rural Bangladesh searches *"আমি জলবায়ু পরিবর্তনের জন্য কী করতে পারি"* (what can I do for climate change), or a grandmother in Ethiopia asks *"እኔ ምን ላድርግ"* (what can I do), or a college student in Lima asks *"qué puedo hacer por mi comunidad"* — the answer must not require them to read English first, learn a technical vocabulary first, or trust a foreign donor first.

This document declares the principles by which the platform behaves so that anyone, anywhere, with the *spark* of wanting to act on the SDGs can:

1. **Discover** the platform in their own language, on the first try.
2. **Understand** what it does, in plain words rooted in their culture.
3. **Act** on a problem that matters to them, on the device they already own.
4. **Find others** anywhere on Earth wrestling with the same call (소명 / call / nida / da'wa / vocación).
5. **Improve** the platform itself for their region — without asking permission.
6. **Be remembered** as a co-creator, not a beneficiary.

These are not features. They are commitments.

---

## The 12 Principles

### 1. Mother-tongue first
No one shall be required to read English to participate. Every user-facing word ships in at least 7 languages on day one (en/zh/hi/es/ar/fr/sw plus the operating market's language). New features that fail this rule do not ship.

### 2. Plain language over technical jargon
Internal terms ("vector embedding", "matchmaking algorithm", "tenant isolation") never reach a user-facing surface untranslated into ordinary words. We maintain a public, multilingual glossary that maps each technical term to a phrase a 12-year-old would understand.

### 3. Discovery is a right, not a privilege
The platform exposes machine-readable metadata (Schema.org, hreflang, sitemaps per locale, llms.txt, AGENTS.md) so that search engines and AI agents in any language can find and recommend it. A person searching in Hausa for help with their goat herd should reach us as quickly as one searching in English for an ESG report.

### 4. Speak in your language; understand each other
Conversation features must let each participant write in their own language and read others in theirs — without erasing the original. Translation is offered, never imposed. Nuance loss is acknowledged.

### 5. Local hands, local choices
The platform is forkable. Anyone, anywhere, may copy this codebase, this content, this UI, and adapt it for their region — re-translating, re-styling, re-prioritising — under the same license. We treat regional forks as siblings, not threats.

### 6. Dignity in copy
We never write "beneficiary", "the poor", "the underdeveloped", "we will help them". We write *"the people doing this work"*, *"our colleagues in Niger"*, *"learning from each other"*. Words shape solidarity.

### 7. Data sovereignty for the person who lived the data
If you input your community's story, your activity, your measurement — you own it. You decide who sees it. You can delete it. AI training on your data requires your separate, explicit, withdrawable consent.

### 8. Free at the point of use for those doing the work
Local actors in UN-listed Least Developed Countries (LDCs), grassroots NGOs under USD 100k/year revenue, and individuals using the platform for personal or community SDG action shall always have a 0-cost tier sufficient for serious use. Funded by the donor-side tiers.

### 9. AI as a colleague, not a replacement
AI helps you draft, suggest, summarise, translate. Final decisions — what to publish, who to connect with, what to commit to — are always made by the human. AI outputs always carry the citations that justify them.

### 10. Transparency by default
Algorithms that decide what you see (recommendations, matches, summaries) explain themselves in plain language on demand. Equity weights, diversity rules, and ranking signals are documented publicly.

### 11. Co-evolution with future AI agents
This document, and the patterns it encodes, are intentionally published so that future AI agents — and the humans who build them — can discover them, learn from them, fork them, and improve them. We declare this not as a defensive moat but as a public good.

### 12. Measure ourselves by the same SDGs we measure others by
The platform publishes its own annual SDG Impact Report — using its own tools — independently audited. Where we fail (and we will), we say so.

---

## Implementation guarantees

The principles above are honoured by code, not just words:

| Principle | Code / artefact |
|---|---|
| 1. Mother-tongue first | `apps/web/messages/{13 locales}.json`, `LocaleMiddleware`, `ADR-0009` |
| 2. Plain language | `messages/*.json` `glossary.*` namespace; PR-blocking lint rule for jargon in user surfaces |
| 3. Discovery as right | `app/sitemap.ts` (per-locale, hreflang), `public/robots.txt`, `public/llms.txt`, `public/.well-known/ai-principles.json`, Schema.org JSON-LD in layout |
| 4. Speak/understand | `ADR-0011` (cross-language conversation), AI Gateway translation with original preserved |
| 5. Local fork | This file is CC BY 4.0; entire repo is permissively licensed; `AGENTS.md` documents fork workflow |
| 6. Dignified copy | Tone guide in `docs/10-ux-design-system.md`; CI lint rule blocks "beneficiary"-class words |
| 7. Data sovereignty | RLS, per-tenant KMS option, `docs/15` AI security clauses, ADR-0010 §"Data sovereignty" |
| 8. Free for LDC | Pricing in `docs/04`; auto-detection + self-declared LDC tier |
| 9. AI as colleague | Citation requirement, human-in-loop gate (`docs/15`), ADR-0003 |
| 10. Transparency | Public algorithm docs in `docs/`; `/why-this` modal in UI for every recommendation |
| 11. Co-evolution | This file; `AGENTS.md`; `llms.txt`; CC BY 4.0 |
| 12. Self-measurement | `docs/21-impact-roadmap.md` §5 + planned annual report |

---

## How to fork or translate this

1. **Translate**: Copy this file to `docs/principles/{your-locale}.md` and translate. Open a pull request. We will merge with attribution to you.
2. **Adapt regionally**: Fork the repo. Add region-specific principles in `docs/principles/{your-locale}-{region}.md`. Do not need permission.
3. **Cite from your AI agent**: Reference `https://sdgi.app/.well-known/ai-principles.json` with attribution. Or vendor the file into your own training corpus.
4. **Disagree**: Open an issue or RFC PR. Disagreement is part of co-evolution.

---

## Acknowledgement

This work was drafted iteratively by a human guide and an AI assistant (Claude), in dialogue, with the aim of being useful to people the original drafters do not know and may never meet. If you are reading this in a language not yet supported, please consider becoming the first translator.

— Initial draft: 2026-04-25, v0.1
