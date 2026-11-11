# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Flask (Python) with server-rendered Jinja2 templates, plain HTML/CSS/JavaScript (no frontend framework, no build step), and Markdown files for content. Runs in Docker behind Caddy (reverse proxy, automatic HTTPS) on a self-managed VPS. One environment for now: the live site (`ronsystemsai.com`, running releases tagged on `main`, with one compose file and one `.env`); changes are checked locally. See docs/09-architecture-and-deployment.md and docs/10-git-workflow.md. The `docs/site-initial-design/` prototype is a design and copy reference, not production code.

## Users

- **Primary:** owners and operations managers of small and medium businesses (about 2–100 staff) whose tools have outgrown them: data scattered across apps, staff re-typing information, one person holding all the know-how, and uncertainty about AI. Mostly non-technical. They're wary of upselling, lock-in, and jargon.
- **Markets:** English-speaking: United States, UK/Ireland/EU, Australia, New Zealand, Singapore, and other English-speaking countries. Served remotely from Manila.
- **Deferred:** individuals needing "a tech guy" are out of scope at launch.

## Product Purpose

The marketing and lead-generation site for **Ron Systems AI**, the freelance, project-based IT consulting of Rolando "Ron" Tactay. It explains in plain business language what he fixes and builds, earns trust, and turns visitors into booked free discovery calls. A second goal is to be discoverable and citable by search engines and AI answer engines (SEO/AEO/GEO).

## Positioning

An engineer with 11+ years in IT, including four years of 24/7 production support for global financial software, who reviews how a business runs, gives honest vendor-neutral advice, and builds systems that keep working: automations, practical AI assistants and agents, and well-planned environments. One accountable person who covers apps, data, infrastructure, and AI, documents everything, and hands over full ownership.

## Operating Context

Visitors arrive from Google and Bing, AI assistants (ChatGPT, Perplexity, Gemini, Claude, Copilot), YouTube, Facebook, LinkedIn, and referrals. The conversion path is a free 30-minute phone call booked through a Proton Calendar booking page, with email or a LinkedIn message as alternatives (no contact form). Engagement path: discovery call → tech check-up and roadmap → implementation project → optional monthly support, each scoped and quoted before work starts.

## Capabilities and Constraints

- Services: tech check-up and roadmap; workflow automation (n8n, Zapier, Make, Power Automate, Python); AI assistants and agents (GPT/Claude models, Hermes, OpenClaw, RAG, OCR, local LLMs); software selection/app evaluation; systems setup and architecture (cloud, self-hosted, migration); custom business tools; ongoing support.
- Copy rule: headlines state business outcomes, body explains in plain English, and tool names appear only as supporting detail.
- No price figures anywhere on the site.
- Language: English, US spelling.
- Every page is server-rendered HTML with structured data (ProfessionalService, Person, Service, FAQPage, Article, VideoObject). AI crawlers are allowed on prod; the test environment is noindex and behind basic auth.
- Time zones and availability are not addressed on the site (no time-zone FAQ, no response-time promises); Ron manages call slots in his Proton Calendar booking page.
- No client-location claims in site copy ("Working with clients in…"); target markets live only in structured data.
- Analytics: Umami (self-hosted, cookie-less, prod only) + Google Search Console + Bing Webmaster Tools.
- Email: Proton Mail on `contactme@ronsystemsai.com`. The site only links to it and sends no mail itself. See docs/08-open-decisions.md.

## Brand Commitments

- Brand: **Ron Systems AI** · domain **ronsystemsai.com** · handle `@ronsystemsai` on Facebook, YouTube, and LinkedIn. The About page and structured data name the person as Rolando "Ron" Tactay.
- Voice: plain, honest, calm, and specific. No jargon, no hype, no hard sell. "I'll tell you honestly whether I can help."
- Commitments stated to clients: vendor-neutral (no commissions), client owns all code, documentation, and access, and everything is scoped and quoted before work starts.

## Evidence on Hand

- Resume: `docs/about-ron/ron-resume.pdf` (private, gitignored; includes a phone number).
- Anonymized project proof from the resume: custom CRM (leads, payments, scheduling, SMS, analytics, catalog, promo codes); Python + n8n pipelines into replicated PostgreSQL; GPT agent integrated with a project-management platform; self-hosted business stack on Proxmox/TrueNAS; OCR/RAG/local-LLM document processing.
- Initial design prototype with drafted copy: `docs/site-initial-design/`.
- **Absent, never fabricate:** testimonials, client names or logos, and quantified results.
- **Brand mascot:** a cauldron character (navy and red), used as the business logo in structured data (`app/static/img/logo.jpg`, 512×512). The visible site keeps the RON wordmark.

## Product Principles

1. Outcome first, tools second: every message is about the visitor's business, not the tech.
2. Honesty is the differentiator: no invented claims, and advise against buying when that's the right answer.
3. Built to be quoted: answer-first, specific, dated, and authored content that search and AI can cite.
4. Ownership and reliability: everything handed over and documented, with the 24/7 production mindset applied to small businesses.
5. One experienced person, not a faceless agency.

## Accessibility & Inclusion

Target WCAG 2.2 AA. International, often non-technical audience, so use plain English.
