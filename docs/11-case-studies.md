# 11 — Case studies

How case studies ("Recent work") are shown, stored, written, and added. **Status: planned, not built yet (as of 2026-11-08).**

## Where things stand today

- The three case studies live in the `CASES` list in `app/site_content.py` as Python dicts (problem, what I built, result).
- The homepage and `/work/` show the **same full cards**. Nothing links deeper, so a visitor who wants more has nowhere to go.
- [04-site-structure.md](04-site-structure.md) already plans a page per case study (`/work/<slug>/`), and [09-architecture-and-deployment.md](09-architecture-and-deployment.md) says case studies are Markdown files. Neither was built.
- Service pages don't link to any example yet, although the service page template asks for one (step 5 in [04-site-structure.md](04-site-structure.md)).

## The plan: three levels

| Where | What it shows | Links to |
|---|---|---|
| **Homepage** | Up to 3 featured teasers: title, tag, one-line result | The detail page (or the card on `/work/` if there's no detail page), plus "See all work →" |
| **`/work/`** | Every case study as a problem / what I built / result card (the current design) | "Read the full story →" on cards that have a detail page |
| **`/work/<slug>/`** | The full write-up | The related service page, and "Book a free call" |

The detail page uses the normal site design (same header, footer, type, and colors). It reads like a short article, not like documentation.

### Why separate detail pages

- **Search and AI visibility.** One page can rank for one topic. A page about "a custom CRM for a small business" can be found and quoted; a section inside a long page mostly can't.
- **Something to link to.** Each service page can point to its matching example, and LinkedIn/Facebook "Behind the build" posts ([06-social-and-content.md](06-social-and-content.md)) get a URL.
- **Room.** Screenshots or a before/after diagram fit on the detail page without making `/work/` long.

### Detail pages are optional

A detail page only exists when there's a real story to tell: a few hundred words of detail that don't identify the client. A thin page hurts more than it helps. If a case study has no story written, it stays as a card on `/work/` with no "Read the full story" link, and its URL returns 404.

## Detail page template

1. **Summary first** (40–60 words): the problem, what was built, and the result in one paragraph. AI tools quote this part.
2. **The business**: type and size, no name ("a service business with a small office team").
3. **The problem**: what it was costing them in time, errors, or missed sales.
4. **What I built and why**: the main decisions, including what was left out on purpose.
5. **Tools used**: names spelled out, for search.
6. **Result**: real numbers only, or a plain description if nothing was measured.
7. **What the client owns**: accounts, code, documentation, and how the handover went.
8. **Related service + call to action**: link to the matching service page, then "Have a problem like this? Book a free call."

## Writing rules

- **Anonymized.** No client names, logos, or identifying details unless the client gave permission in writing ([03-services.md](03-services.md)). Blur or replace client data in screenshots.
- **Never invent anything.** No made-up numbers, quotes, or testimonials ([PRODUCT.md](../PRODUCT.md)). Start measuring on every project (hours saved, errors reduced) so later case studies have real results ([07-launch-checklist.md](07-launch-checklist.md)).
- **Site-wide rules still apply** ([08-open-decisions.md](08-open-decisions.md)): plain business language, US spelling, no prices, no time zones, no client-location claims. The tests check prices and time-zone wording on every page.

## How a case study is stored

One Markdown file per case study: `content/work/<slug>.md`. The file name is the URL slug. Keep the current slugs (`custom-crm`, `data-pipelines`, `ai-agent`) so existing `/work/#<slug>` links keep working.

```markdown
---
title: "A CRM built around one business's daily routine"
description: "How one business replaced separate tools for leads, payments and scheduling with a single custom CRM."
published: 2026-11-08
updated: 2026-11-08          # optional
tag: Custom tool
problem: "Leads, payments, scheduling and customer messages lived in separate tools."
built: "A custom CRM covering lead management, payment processing, scheduling, SMS, analytics, a product catalog and promo codes."
result: "The team works from one system instead of switching between several, and reports come from live data."
service: custom-business-tools   # optional; slug from SERVICES in app/site_content.py
featured: true                   # optional; shows on the homepage (max 3)
draft: false                     # optional; true hides it everywhere
---

The full story goes here, following the detail page template above.
Leave the body empty for a card-only case study.
```

| Field | Required | Used for |
|---|---|---|
| `title` | Yes | Card title, page H1, browser title |
| `description` | Yes | Meta description and the line under the H1. One or two sentences, under ~160 characters |
| `published` | Yes | Sort order on `/work/` (newest first), structured data, sitemap |
| `updated` | No | "Updated" date, structured data, sitemap |
| `tag` | Yes | Short label on the card ("Custom tool", "Automation", "AI agent") |
| `problem`, `built`, `result` | Yes | The three parts of the card |
| `service` | No | Links the detail page and the service page to each other |
| `featured` | No | Shows the teaser on the homepage. If more than 3 are featured, the 3 newest show |
| `draft` | No | `true` hides it (same as articles and videos) |
| Body | No | The full story. Empty = no detail page |

## Build plan

Branch: `feature/case-study-pages` from `dev` ([10-git-workflow.md](10-git-workflow.md)).

1. **Content.** Move the three `CASES` entries into `content/work/custom-crm.md`, `data-pipelines.md`, and `ai-agent.md` with no body yet (card only). Set `featured: true` on all three and add `service` slugs: custom CRM → `custom-business-tools`, data pipelines → `workflow-automation`, AI agent → `ai-assistants-and-agents`.
2. **Loader** (`app/services/content_loader.py`). Add the `work` kind. Check the extra required fields (`tag`, `problem`, `built`, `result`) for that kind only. Mark each item with whether it has a story (non-empty body).
3. **Routes.** `/work/` (`app/routes/pages.py`) reads `all_items("work")` instead of `C.CASES`. Add `/work/<slug>/` to `app/routes/content.py`. It returns 404 for unknown slugs and card-only case studies.
4. **Templates.**
   - `pages/home.html`: up to 3 featured teasers and a "See all work →" link.
   - `pages/work.html`: same cards, plus "Read the full story →" when there's a detail page.
   - New `content/case.html`: page head with the tag, a problem / what I built / result summary box, the story, the related service link, then the booking close.
5. **Service pages** (`pages/service.html`). Add an "Example" block listing case studies whose `service` matches.
6. **SEO.**
   - `app/routes/seo.py`: add detail pages to `sitemap.xml` and list them in `llms.txt`.
   - `app/services/schema.py`: `Article` and `BreadcrumbList` (Work → case study) JSON-LD for detail pages.
7. **Clean up.** Remove `CASES` from `app/site_content.py`.
8. **Tests** (`tests/test_site.py`).
   - Detail pages render with exactly one H1 and pass the price and time-zone checks.
   - Card-only case studies return 404 at `/work/<slug>/`.
   - The homepage shows at most 3 teasers.
   - The loader rejects a case study with a missing required field.
9. **Docs.**
   - Add a "Case studies" section to `content/README.md`.
   - Update the "Where things live" row in `README.md`.
   - Change this doc's status to built.

## How to add or update a case study (after the build)

### From the browser (GitHub web editor)

1. On github.com, switch to the `dev` branch and open `content/work/`.
2. **Add file → Create new file**, name it `<slug>.md`, and paste the template above (or copy an existing case study). To update one, open its file and click the pencil icon.
3. Commit to a **new branch** named `content/<short-name>` and open a pull request into `dev`.
4. CI runs the tests. Merge into `dev`. There's no test site, so for anything more than a text tweak, preview it locally first (below).
5. Release it: a pull request from `dev` into `main`, a version tag, and `./deploy.sh` on the server ([10-git-workflow.md](10-git-workflow.md), "Releasing"). Then check `/work/` and the detail page on **ronsystemsai.com**.

### Locally

```bash
git switch dev && git pull
git switch -c content/<short-name>
# add or edit content/work/<slug>.md
uv run flask --app wsgi run --debug   # preview at http://127.0.0.1:5000/work/
uv run python -m pytest -q
```

Then push the branch and follow steps 3–5 above.

- **Updating:** edit the file and set `updated:` to today's date.
- **Hiding:** set `draft: true`. **Removing:** delete the file.

## Later: editing through a form

There's no admin panel, on purpose. There's no database at launch ([09-architecture-and-deployment.md](09-architecture-and-deployment.md)), and a few case studies a year don't justify one.

If someone non-technical needs to edit, or publishing becomes frequent, add a **Git-based CMS** such as Decap CMS:

- It gives a form editor at `/admin` that saves the same Markdown files to the repo, so the deploy flow stays the same.
- It needs GitHub sign-in (OAuth) set up.
- It can be added later without changing anything above.

A custom Flask admin panel is not planned.

## Open questions

- **Full stories for the current three.** Each needs details only Ron has: business type and size, what it was like before, key decisions, and any measured results. They stay card-only until written.
- **Dates on detail pages.** Show the published date like articles do, or keep it only in structured data? Case studies don't go out of date the way articles do.
- **Next case studies.** [PRODUCT.md](../PRODUCT.md) lists two more from real work: the self-hosted business stack on Proxmox/TrueNAS, and OCR/RAG/local-LLM document processing.
