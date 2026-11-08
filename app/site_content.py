"""Structured site copy. Plain English first; tool names only as supporting detail.

Every claim here must be backed by Ron's real background (docs/about-ron). No prices,
no time-zone promises, no client-location claims, no invented testimonials or numbers.
"""

HERO = {
    "title": "Stop doing it by hand.",
    "lede": (
        "I'm Ron, an engineer with 11+ years in IT. I find the manual work in your "
        "business and build systems that do it for you."
    ),
}

SIGNS = [
    ("Your data lives in several places.", "Customer, sales and finance information sits in different tools, and none of them agree."),
    ("Your team re-types the same information.", "Copying between spreadsheets, email and apps eats hours every week and causes mistakes."),
    ("Your tools don't talk to each other.", "You pay for software nobody chose on purpose, or that overlaps with something you already have."),
    ("One person knows how it all works.", "When they're away, things slow down or break. Nothing is written down."),
    ("You're not sure where AI actually helps.", "You keep hearing you should use it, but can't tell which uses are real and which are hype."),
]

SERVICES = [
    {
        "slug": "tech-roadmap",
        "name": "Tech check-up and roadmap",
        "seo_title": "Small business tech check-up and roadmap",
        "short": "A review of your tools, workflows and data, and a prioritized plan: what to fix first, what to leave alone, and why.",
        "start_here": True,
        "title": "Know exactly what to fix in your business tech, and in what order",
        "answer": (
            "A tech check-up is a one-to-two-week review of the tools, workflows and data your business "
            "runs on. I talk to the people who use them, map where time and money leak, and hand you a "
            "written, prioritized roadmap you can act on, with me or without me."
        ),
        "signs": [
            "You're about to buy new software and aren't sure it's the right call.",
            "Everyone has a workaround, and nobody has the full picture.",
            "You know things could run better but don't know where to start.",
        ],
        "steps": [
            "A short call to agree on what's in scope.",
            "Interviews with the people who do the work every day.",
            "A review of your apps, data, access and costs.",
            "A written roadmap: priorities, options, trade-offs and next steps.",
            "A walkthrough call so every recommendation makes sense.",
        ],
        "tools": "I review whatever you use today, whether that's Microsoft 365 or Google Workspace, a CRM, or your accounting, booking and support software. Nothing has to change before we start, and the roadmap tells you what to keep, fix or replace.",
        "format": "Fixed scope, usually 1–2 weeks. Quoted before work starts.",
        "faqs": [
            ("Do I have to hire you to do the work afterwards?", "No. The roadmap is yours. It's written so your team or another provider can follow it."),
            ("What do you need from us?", "An hour or two with the people who use the tools, and read access where it helps. I'll send a short checklist first."),
        ],
    },
    {
        "slug": "workflow-automation",
        "name": "Automate repetitive work",
        "short": "Connect your apps so information moves by itself: no copy-paste, fewer mistakes, hours back every week.",
        "title": "Automate the repetitive work in your business",
        "answer": (
            "Workflow automation connects the apps you already use so information moves between them by "
            "itself. A new lead lands in your CRM, gets a welcome email and shows up in your reports, and "
            "nobody re-types it. I build these flows, test them with your team and document how they work."
        ),
        "signs": [
            "Someone spends part of every day copying data between apps.",
            "Mistakes creep in when information is typed twice.",
            "Reports take hours to put together by hand.",
        ],
        "steps": [
            "Map the manual steps and pick the ones worth automating first.",
            "Build the flow with error alerts and a log of what ran.",
            "Test it with real examples alongside your team.",
            "Hand over documentation and a short walkthrough.",
        ],
        "tools": "I build with the automation tool you already have or prefer, for example Power Automate if you're on Microsoft 365. If you don't have one yet, I'll recommend the best fit for your apps and budget, such as n8n, Zapier or Make, or write custom Python when no ready-made tool fits.",
        "format": "Scoped and quoted up front, often as part of an implementation project.",
        "faqs": [
            ("Which automation tool will you use?", "The one that fits your budget, your apps and how much control you need. Sometimes that's Zapier; sometimes a self-hosted n8n saves a lot of money."),
            ("What happens when an automation fails?", "Every flow I build reports its own errors to someone who can act on them, and keeps a log so problems are easy to trace."),
        ],
    },
    {
        "slug": "ai-assistants-and-agents",
        "name": "AI assistants and agents",
        "short": "AI that saves real time: answers from your own documents, invoices read for you, and agents that do tasks in your apps.",
        "title": "Practical AI for your business, only where it saves real time",
        "answer": (
            "I build AI tools that do useful work inside your business: assistants that answer from your "
            "own documents, document processing that reads invoices and forms for you, and AI agents that "
            "take actions in your apps with limits and approvals you control. If AI isn't the right answer, "
            "I'll tell you."
        ),
        "signs": [
            "Your team searches old emails and folders for answers every day.",
            "Invoices, forms or receipts are still typed in by hand.",
            "You want to use AI but can't tell what's useful and what's hype.",
        ],
        "steps": [
            "Find the tasks where AI saves time without adding risk.",
            "Decide what data it can see and what it may do on its own.",
            "Build it, connected to the tools you already use.",
            "Test with real examples and add human approval where it matters.",
            "Document it and train your team.",
        ],
        "tools": "I work with the AI your business already uses or prefers, such as ChatGPT or Claude. If you're starting fresh, I'll recommend a setup based on cost, accuracy and privacy, including private models that run on your own hardware when data can't leave your control.",
        "format": "Scoped and quoted up front.",
        "faqs": [
            ("Is our data safe?", "We decide together what the AI can see. When data can't leave your control, a private model can run on your own server."),
            ("What's an AI agent?", "An AI assistant that doesn't just chat: it can take actions in your apps, like creating a task or updating a record, within limits you set."),
        ],
    },
    {
        "slug": "software-selection",
        "name": "Choosing the right software",
        "seo_title": "Choosing the right business software",
        "short": "Honest advice on what to buy, build or self-host, tested against how your team actually works.",
        "title": "Choose software that fits how your business really works",
        "answer": (
            "Before you commit to new software, I test the options against how your team actually works "
            "and what you already pay for, then recommend what to buy, build or self-host. I earn nothing "
            "from the tools I recommend, and sometimes the answer is to keep what you have."
        ),
        "signs": [
            "You pay for several tools that do similar things.",
            "A sales demo looked great, but you're not sure it fits.",
            "Subscription costs keep growing as your team grows.",
        ],
        "steps": [
            "Write down what the software must actually do.",
            "Shortlist options, including the tools you already own.",
            "Test the shortlist with real tasks and real users.",
            "Recommend one, with costs, risks and a migration plan.",
        ],
        "tools": "Vendor-neutral: I earn nothing from what I recommend. If you already have favorites, we test those. If not, I'll shortlist options, cloud or self-hosted, and recommend the one that fits how your team works.",
        "format": "Fixed scope. Quoted before work starts.",
        "faqs": [
            ("Do you get commissions from vendors?", "No. I don't resell software, so the recommendation is only about what's right for you."),
        ],
    },
    {
        "slug": "systems-setup",
        "name": "Systems setup and architecture",
        "seo_title": "IT systems setup for small business",
        "short": "A plan for how your email, CRM, finance, files and data fit together, then set up securely, backed up and ready to grow.",
        "title": "Set up business systems that are secure, backed up and ready to grow",
        "answer": (
            "I design how your email, CRM, finance, files and data fit together, then set them up properly: "
            "in the cloud or on your own server, with test and live environments, backups, access control "
            "and documentation. Migrations from old systems are planned so work doesn't stop."
        ),
        "signs": [
            "Your setup grew one app at a time and nobody planned it.",
            "You're not sure your backups would actually work.",
            "Former staff may still have access to company systems.",
        ],
        "steps": [
            "Design the target setup and agree on it with you.",
            "Build it in phases, starting with quick wins.",
            "Migrate data and test it before switching over.",
            "Hand over documentation, access and training.",
        ],
        "tools": "I build on the platforms you already use, whether that's Microsoft 365, a cloud provider such as AWS, Azure or Google Cloud, or your own servers. If you're starting fresh or outgrowing what you have, I'll recommend a setup that fits your budget and the people who'll look after it.",
        "format": "Scoped and quoted up front, delivered in phases.",
        "faqs": [
            ("Cloud or our own server?", "Whichever fits your budget, skills and data rules. Self-hosting often costs less than subscriptions, but it needs looking after."),
        ],
    },
    {
        "slug": "custom-business-tools",
        "name": "Custom business tools",
        "short": "When off-the-shelf software doesn't fit, a tool shaped around your daily routine, such as a lightweight CRM or dashboard.",
        "title": "Custom tools shaped around your business, not the other way around",
        "answer": (
            "When off-the-shelf software forces your team into awkward workarounds, I build internal tools "
            "shaped around how you actually work: a lightweight CRM, booking and payment flows, or dashboards "
            "on live data. You own the code and the documentation."
        ),
        "signs": [
            "You've bent your process around software that almost fits.",
            "You juggle several apps to finish one job.",
            "Reports rely on data exported from three places.",
        ],
        "steps": [
            "Agree on the smallest version that solves the real problem.",
            "Build it in short rounds you can try as it grows.",
            "Connect it to the tools you keep.",
            "Hand over code, documentation and access.",
        ],
        "tools": "I connect what I build to the apps you already use. If you have a preferred technology or an in-house developer, I'll build with that. If not, I'll use something widely known, such as Python and PostgreSQL, so anyone can maintain it later.",
        "format": "Scoped and quoted up front.",
        "faqs": [
            ("Will we be locked in to you?", "No. You receive the code, documentation and every login. Another developer can pick it up."),
        ],
    },
    {
        "slug": "ongoing-support",
        "name": "Ongoing support and care",
        "short": "Someone who already knows your setup: monitoring, fixes, updates and steady improvements each month.",
        "title": "Ongoing support from someone who already knows your setup",
        "answer": (
            "After go-live, monthly support keeps your systems healthy: monitoring, fixes, updates, and "
            "steady improvements, with a set number of hours each month. It's built on four years of 24/7 "
            "production support for global financial software."
        ),
        "signs": [
            "Problems are only noticed when a customer complains.",
            "Updates get skipped because nobody has time.",
            "Small improvements pile up on a wish list.",
        ],
        "steps": [
            "Set up monitoring and alerts for what matters.",
            "Fix issues and find their root cause.",
            "Keep software, access and backups up to date.",
            "Work through your improvement list each month.",
        ],
        "tools": "I look after your systems with the monitoring you already have. If there isn't any, I'll recommend and set up something lightweight, such as Grafana, and keep the runbooks and documentation up to date for you.",
        "format": "Monthly, a set number of hours, cancel anytime.",
        "faqs": [
            ("Do we need support to work with you?", "No. It's optional, and many clients start with a project and decide later."),
        ],
    },
]

PROCESS = [
    ("Discovery call", "A 30-minute phone call about your business, what's slowing it down and what you'd like to change. You'll know if I'm a fit, and I'll know if I can help.", True),
    ("Assessment", "I review your current tools, workflows and data, and talk to the people who use them every day.", False),
    ("Roadmap and proposal", "A clear plan with priorities, options, timeline and a fixed quote, so there are no surprises.", False),
    ("Design", "I design the solution and choose the tools with you. Nothing gets built until you approve it.", False),
    ("Build", "I build, configure, migrate and automate in phases, with regular check-ins. Quick wins come first.", False),
    ("Testing and training", "We test everything with your team, and I provide documentation and walkthroughs.", False),
    ("Go-live and handover", "A smooth launch, then a full handover of documentation and access. Everything belongs to you.", False),
    ("Support", "Optional monthly support for monitoring, maintenance and continuous improvement.", False),
]

WAYS_TO_START = [
    {
        "name": "Tech check-up and roadmap",
        "text": "A full review of your setup and a prioritized plan you can act on, with me or without me.",
        "format": "1–2 weeks · fixed scope",
        "featured": True,
    },
    {
        "name": "Implementation project",
        "text": "We build the roadmap in phases: architecture, setup, automation, migration and training.",
        "format": "Scoped and quoted up front",
        "featured": False,
    },
    {
        "name": "Monthly support",
        "text": "Monitoring, maintenance and steady improvements after go-live, with set hours each month.",
        "format": "Monthly · cancel anytime",
        "featured": False,
    },
]

CASES = [
    {
        "slug": "custom-crm",
        "tag": "Custom tool",
        "title": "A CRM built around one business's daily routine",
        "problem": "Leads, payments, scheduling and customer messages lived in separate tools.",
        "built": "A custom CRM covering lead management, payment processing, scheduling, SMS, analytics, a product catalog and promo codes.",
        "result": "The team works from one system instead of switching between several, and reports come from live data.",
    },
    {
        "slug": "data-pipelines",
        "tag": "Automation",
        "title": "Business data that moves by itself",
        "problem": "Data had to be checked and copied between systems by hand.",
        "built": "Python and n8n pipelines that validate, transform and load data into a replicated PostgreSQL database.",
        "result": "Cleaner data, fewer manual steps, and a standby copy ready if the main database fails.",
    },
    {
        "slug": "ai-agent",
        "tag": "AI agent",
        "title": "An AI assistant inside the project tools",
        "problem": "Team members spent time creating, updating and searching work items by hand.",
        "built": "A GPT-based agent connected to a project management platform, with secure sign-in, data mapping, real-time sync and plain-language commands.",
        "result": "Work items can be created and updated by describing them in everyday language.",
    },
]

WHY = [
    ("Enterprise discipline, small-business scale", "11+ years of IT work across finance, healthcare, manufacturing, IT service providers (MSPs) and startups taught me incident management, service levels and runbooks. You get the same care about reliability."),
    ("Plain English", "I explain options and trade-offs without jargon, so you can make the decision yourself."),
    ("You own everything", "Documentation, code and access are handed over. No lock-in, and no dependence on me."),
    ("Honest, vendor-neutral advice", "I earn nothing from the tools I recommend. Sometimes the answer is to use what you already have."),
]

TOOLS = [
    ("Your business apps", "Accounting, CRM, booking and scheduling, online stores, email and messaging, forms and spreadsheets, connected through their APIs, webhooks or exports"),
    ("Automation and AI", "n8n, Zapier, Make, Microsoft Power Automate, Python, PowerShell, GPT and Claude models, AI agents, RAG, OCR, local LLMs"),
    ("Data", "PostgreSQL, Microsoft SQL Server, MySQL, ETL pipelines, database replication, dashboards and reporting on live data"),
    ("Cloud and infrastructure", "AWS, Microsoft Azure, Google Cloud, Proxmox, TrueNAS, Linux, Windows Server, Docker, Kubernetes, Terraform, Ansible"),
    ("Security and operations", "Microsoft 365, Active Directory, single sign-on (SSO) and multi-factor authentication (MFA), VPNs, 1Password, Vaultwarden, secrets management, Wazuh, GitHub Actions, Grafana, Prometheus"),
]

# Marks for the home page tool strip, in display order: (symbol slug in partials/tool-logos.svg, name).
# Tools only, never clients. Every name here also appears in TOOLS above.
TOOL_LOGOS = [
    ("n8n", "n8n"),
    ("zapier", "Zapier"),
    ("make", "Make"),
    ("openai", "GPT"),
    ("claude", "Claude"),
    ("python", "Python"),
    ("postgresql", "PostgreSQL"),
    ("microsoft", "Microsoft 365"),
    ("amazonwebservices", "AWS"),
    ("docker", "Docker"),
    ("proxmox", "Proxmox"),
    ("linux", "Linux"),
    ("kubernetes", "Kubernetes"),
    ("terraform", "Terraform"),
    ("ansible", "Ansible"),
    ("githubactions", "GitHub Actions"),
    ("grafana", "Grafana"),
    ("prometheus", "Prometheus"),
    ("mysql", "MySQL"),
    ("truenas", "TrueNAS"),
    ("powershell", "PowerShell"),
    ("vaultwarden", "Vaultwarden"),
]

FAQS = [
    ("What happens on the free call?", "We talk about how your business runs, what's slowing it down and what you'd like to change. I'll tell you honestly whether I can help and what a sensible first step looks like. There's no obligation."),
    ("Do I need to be technical?", "No. I explain everything in plain language and focus on what the technology does for your business, not how it works inside."),
    ("Can you work with the tools we already use?", "Yes, including tools that aren't listed on this site. Most business apps can be connected through their API, webhooks or exports. If I haven't used yours before, I'll say so and check what it can do before quoting. Often the best result comes from connecting and tidying what you already have."),
    ("How does pricing work?", "Every project is scoped and quoted before work starts, so you know the cost up front. Ongoing support is a monthly arrangement for a set number of hours."),
    ("Will I own what you build?", "Yes. You receive the documentation, code and access for everything I build, so you're never locked in."),
    ("Do you work remotely?", "Yes. Assessments, builds, training and support all run remotely over video calls and secure access."),
]

BOOK_AGENDA = [
    "Your current tools and where they fall short",
    "What you'd like to change or automate",
    "Whether a check-up or a project makes sense",
]


def service_by_slug(slug):
    return next((s for s in SERVICES if s["slug"] == slug), None)
