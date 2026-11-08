# 04 — Site structure and pages

The current design (`docs/site-initial-design/`) is a single long page. That works for converting visitors but is weak for search: **one page can only rank for one topic.** Keep the homepage as the persuasive overview, and give each service, case study, and common question its own page.

## Sitemap

```
/                               Home: problem → services → process → proof → FAQ → book
/services/                      Overview of all services
  /services/tech-roadmap/
  /services/workflow-automation/
  /services/ai-assistants-and-agents/
  /services/software-selection/
  /services/systems-setup/
  /services/custom-business-tools/
  /services/ongoing-support/
/work/                          Case studies (anonymized)
  /work/<case-study-slug>/
/process/                       How we work together (8 stages)
/ways-to-start/                 Engagement models (no prices)
/about/                         Rolando: story, background, credentials, photo
/resources/                     Articles and guides (the AEO/GEO engine)
  /resources/<article-slug>/
/videos/                        YouTube videos, each embedded with a summary and transcript
  /videos/<video-slug>/
/faq/                           All common questions (answer-first format)
/book/                          Booking (Proton Calendar booking page) + email alternative
/contact/                       Redirects to /book/ (no contact form; email and LinkedIn instead)
/privacy/                       Privacy policy (GDPR-ready)
/terms/                         Terms of service
```

Later, only with genuinely different content per market:

```
/australia/  /new-zealand/  /singapore/  /uk/  /us/
```

## Template for a service page

1. **H1 = the outcome** ("Automate the repetitive work in your business")
2. **Answer-first paragraph** (40–60 words): what it is, who it's for, and what you get. AI tools quote this part.
3. Signs you need this (bullets)
4. What I do (steps)
5. Example / case study link
6. Tools, as one or two sentences, not a list: I work with what you already use or prefer; if you're starting fresh, I'll recommend what fits; then a few examples, names spelled out for search
7. Format (how the work is scoped; no prices)
8. FAQ for this service (3–5 real questions)
9. Call to action: book a free call

## Template for a resource article

- Title phrased as the question people actually ask ("n8n vs Zapier vs Make: which should a small business use?")
- A one-paragraph direct answer at the top
- A "Key takeaways" list
- Body with clear H2/H3 questions
- A comparison table where relevant
- Author box (Rolando, with a link to /about) plus published and updated dates
- Related service + call to action

## Starter content backlog

Written for the questions SMB owners type into Google and ask ChatGPT:

1. What can a small business automate first? (10 examples)
2. n8n vs Zapier vs Make for small businesses: cost, limits, and when to switch
3. What is an AI agent, and is it useful for a small business?
4. How to tell if an AI tool is worth paying for
5. Self-hosting vs SaaS: when running your own tools saves money
6. What a tech audit includes and how to prepare for one
7. Signs your business has outgrown spreadsheets
8. How to stop one person being the only one who knows how everything works
9. Microsoft 365 setup checklist for a small team
10. Hiring a freelance IT/automation consultant: questions to ask

Each article can double as a YouTube video script (see [06-social-and-content.md](06-social-and-content.md)).

## Reuse from the initial design

Content already written in `docs/site-initial-design/Rolando Tactay.dc.html` that carries over:
hero, "Signs it's time" list, 6 services, 8-stage process, 3 engagement models, 3 case studies, "Why work with me", tools list, 6 FAQs, and the booking section. The "Today vs With a plan" tool-tangle diagram is a strong explainer; keep that idea.
