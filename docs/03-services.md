# 03 — Services (in business language)

Rule for all copy: **headline = the outcome, body = what I do, footnote = the tools.** Tool names help credibility and search, but they never lead.

## Jargon → plain-language translation

Use the right-hand column in headlines and body copy. Use the left-hand column in tool lists, FAQs, and articles written for search.

| What it is technically | How to say it to a business |
|---|---|
| Application support, L1/L2, incident management | "When something breaks, I find out why and fix it, and make sure it doesn't happen again." |
| Workflow automation (n8n, Zapier, Make, Power Automate) | "The repetitive copy-paste work your team does every day, done automatically." |
| AI agents (Hermes, OpenClaw, GPT-based agents) | "An AI assistant that doesn't just chat: it actually does tasks in your apps, with limits you control." |
| RAG / knowledge search | "Ask a question and get the answer from your own documents, policies, and past emails." |
| OCR / document processing | "Invoices, forms, and receipts read and entered for you." |
| Systems architecture | "A plan for how all your tools fit together so data is entered once and trusted everywhere." |
| Environments / deployment | "Setting things up properly (test first, then live) so updates don't break your business." |
| App evaluation / tool selection | "Before you pay for new software, I check whether it actually fits how your team works." |
| Self-hosting, Proxmox, Docker, VPS | "Run your own tools on your own server, often cheaper and more private than subscriptions." |
| Monitoring, SLAs, runbooks | "I watch your systems so problems get caught before your customers notice." |
| ETL / data pipelines / replication | "Your business data moves between systems by itself: checked, clean, and backed up." |
| Infrastructure as Code, CI/CD | _(keep out of headlines; mention only in the tools section)_ |

## Service catalogue

Each service needs its own page (`/services/<slug>`) for search. See [04-site-structure.md](04-site-structure.md).

### 1. Tech check-up and roadmap · _start here_
**Outcome:** a clear, prioritized plan: what to fix first, what to leave alone, what it will cost.
I review your tools, workflows, and data, talk to the people who use them, and hand you a written roadmap you can act on with or without me.
**Format:** fixed scope, 1–2 weeks, quoted up front.

### 2. Automate repetitive work
**Outcome:** hours back every week, and fewer copy-paste mistakes.
Connect your apps so data flows between them: new lead → CRM → welcome email → invoice → spreadsheet report, with no one re-typing it.
**Tools:** n8n, Zapier, Make, Microsoft Power Automate, Python, PowerShell.

### 3. AI assistants and agents
**Outcome:** AI that saves real time in your business, not a chatbot demo.
- Assistants that answer from your own documents and knowledge.
- Document processing: invoices, forms, and receipts read and entered automatically.
- AI agents that take actions in your tools (create tasks, update records, draft replies), with approvals and guardrails.
- Private or local AI when your data can't leave your control.
**Tools:** GPT and Claude models, AI agent frameworks such as Hermes and OpenClaw, RAG, OCR, local LLMs.

### 4. Choosing the right software
**Outcome:** stop paying for tools that don't fit or that overlap with each other.
Honest buy / build / self-host advice. I test the options against how your team actually works, then recommend. Vendor-neutral: no commissions.

### 5. Systems setup and architecture
**Outcome:** a setup that's secure, backed up, and ready to grow.
Design how your CRM, finance, email, files, and data fit together. Set up cloud or self-hosted environments, migrate from old systems, and document everything with training for your team.
**Tools:** Microsoft 365, AWS, Proxmox, Linux/Windows Server, Docker, PostgreSQL/SQL Server, VPNs, password managers.

### 6. Custom business tools
**Outcome:** a tool shaped around your daily routine instead of bending your routine around off-the-shelf software.
Internal apps such as a lightweight CRM, booking and payment flows, or dashboards on live data. _(Proof: the CRM case study.)_

### 7. Ongoing support and care
**Outcome:** someone who already knows your setup, there when something needs fixing.
Monitoring, fixes, updates, and steady improvements with a set number of hours each month. Built on years of 24/7 production support.
**Format:** monthly, cancel anytime.

## Ways to buy (engagement models)

| Model | For | How it's priced |
|---|---|---|
| Free discovery call (30 min, by phone) | Everyone | Free |
| Tech check-up and roadmap | Businesses not sure where to start | Fixed scope, quoted up front |
| Implementation project | Anyone with a defined roadmap | Scoped and quoted up front |
| Monthly support | After go-live | Monthly, set hours |

> Decision: no price figures on the site. Use "scoped and quoted before work starts" wording.

## Proof on hand (real, from the resume)

Keep the client names private unless you have permission.

1. **Custom CRM**: lead management, payments, scheduling, SMS, analytics, product catalog, promo codes.
2. **Self-running data pipelines**: Python and n8n pipelines into a replicated PostgreSQL database.
3. **AI agent in project tools**: GPT agent connected to a project-management platform; plain-language work-item management.
4. **Self-hosted business stack**: Wazuh, Plane, RocketChat, Vaultwarden, Forgejo, Woodpecker CI on Proxmox/TrueNAS with VPN.
5. **Document AI**: OCR, RAG, notifications, and local LLMs for document processing and decision support.

**Missing (never invent these):** client testimonials, logos, measured results (hours saved, % fewer errors). Start collecting them from every project; see [07-launch-checklist.md](07-launch-checklist.md).
