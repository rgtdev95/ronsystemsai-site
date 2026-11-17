---
title: "How AI screens job listings for a client"
description: "How I helped a client's job board screen remote listings, and what we changed when the process became hard to manage."
published: 2026-11-15
---

A client of mine runs a job board for people looking for remote, entry-level work. Finding listings wasn't the biggest problem. The harder part was sorting through them: some weren't really remote, some asked for more experience than the board allowed, and others showed signs of being scams.

We use AI to help read the listings, then apply the client's rules to the information it finds. As the board grew, we also had to fix the process around the AI. Here's how it works and what I learned along the way.

## What was the client looking for?

The board collects listings from seven job sites and online communities. The client wanted to show jobs that met a clear set of requirements: remote positions open nationwide, with no more than three years of experience required, no mandatory degree, coding, or second language, and pay at or above a minimum rate they set. Scams, multi-level marketing, and commission-only opportunities were also out.

Reading every listing by hand wasn't practical. There were too many sources to keep up with, and the work was repetitive enough that it would be easy to miss something.

## Where does AI fit in?

Instead of asking the AI to make one broad decision—“Is this a good job?”—we ask it to look for specific information in each listing. Does the description mention a degree? How much experience does it require? What does it say about pay and location? Are there signs that the opportunity may be a scam or commission-only?

The screening rules then use those answers to decide whether the listing passes. If it doesn't, the reason is recorded. The client can also review a separate list of rejected jobs.

That separation makes the process easier to understand and adjust. If the client changes the minimum pay or experience limit, we can update the rule without rewriting the AI prompt. It also makes it easier to investigate a bad result: we can check both what the AI extracted and how the rules handled it. AI can still misread a listing, so those answers aren't a guarantee that every decision is right.

Looking at real results helped us refine the screening. For example, a job requiring a particular software skill or professional license isn't automatically rejected. It's tagged so someone with that background can find it. We also found that some genuinely remote listings didn't use the word “remote” in the description. The screening now receives the source site's location tags too and assumes a listing is remote unless the listing says otherwise.

## What started to break as the board grew?

The first version worked, but it needed someone to start and watch each step. Adding more sources made that harder to manage.

Screening ran in batches of 25 and only picked up jobs added that day. Each batch needed a click. Catching up on one source's backlog took about 120 clicks, and listings missed by the process weren't screened later.

There were also seven nearly identical workflows, one for each source. A fix in one didn't automatically reach the others. Over time they drifted apart, and one ended up ignoring its own screening verdict.

The verdict itself was stored in two places. If a job changed from a pass to a rejection, it could remain on the public board. We also found that country names weren't consistent, which caused the location filter to miss some jobs.

These weren't problems a better AI prompt would have solved. The surrounding process needed attention.

## What did we change?

We moved the app and screening process to my VPS, a rented server, and kept the listing collectors on a separate server I run at home. The collectors need a desktop browser, so they run in a virtual machine there and send new listings to the VPS after each collection.

The rebuilt process has a few safeguards:

- **Listings are confirmed as saved.** If the VPS is unavailable, a listing isn't treated as sent and can go through on the next run.
- **Screening runs every 15 minutes.** It picks up recent listings that haven't been screened, without someone starting each batch.
- **All seven sources use the same screening workflow.** A change to the shared process reaches every source.
- **The verdict has one home.** Both the public board and the rejected list read from it, so a changed verdict is reflected in the lists.
- **Access is limited by job.** The website can read the finished lists. The automation can add and update listings but can't delete them.
- **Previous verdicts moved with the data.** Listings already screened didn't need to be sent to the AI again during the move.

Before the move, I ran about 120 automated checks covering delivery, screening rules, website queries, and the data migration.

## What tools run it?

The tool names aren't the main lesson, but here's the setup for anyone interested in the details:

| Part of the process | Tools |
|---|---|
| Collecting listings | :logo-python: Python and BrowserOS on the home server, with :logo-uv: uv and scripts to run the collectors. :logo-openai: Codex sets up searches on two sites; one also has an :logo-openai: OpenAI API backup reader. |
| Keeping a local copy | :logo-postgresql: PostgreSQL and pgAdmin in :logo-docker: Docker |
| Sending listings to the VPS | A :logo-python: Python script, run after collection and daily by Windows Task Scheduler or cron |
| Screening | :logo-n8n: n8n and an :logo-openai: OpenAI model |
| Storing listings and verdicts | :logo-postgresql: PostgreSQL on the VPS, with pgAdmin for checks |
| The job board | :logo-react: React, :logo-vite: Vite, :logo-nodedotjs: Node.js, :logo-express: Express, and :logo-nginx: nginx; :logo-oxc: oxlint for checks |
| Hosting and access | :logo-ovh: OVHcloud, :logo-docker: Docker, :logo-github: GitHub, :logo-infisical: Infisical, and a client-managed :logo-cloudflare: Cloudflare Tunnel |
| Testing | :logo-pytest: pytest and PGlite for database checks |
| Building the system | :logo-claude: Claude Code, an AI coding assistant |

These tools fit this particular project. A different business or process could call for a much simpler setup.

## Who manages the system?

I manage the collectors, the app, and its data. The client controls the domain and the Cloudflare Tunnel that connects visitors to the app.

The app has its own database, separate from my own tools. Apart from my admin access, its database is available only through its own logins. The automation uses a login limited to this app's listings, and the client's connection reaches this app rather than the rest of the server.

## Where does the project stand now?

The move is complete. The collectors send new listings to the VPS, the existing listings and verdicts have been moved, and screening runs every 15 minutes. The public board is served from the VPS through the client's domain.

Next, I plan to add alerts for sources that stop delivering listings. The old copies are also due to be removed once the new setup has run cleanly for about two weeks.

## What can another business learn from this?

You don't need a job board to run into the same problems. Any process that pulls information from several places and asks someone to make the same checks over and over can become difficult to maintain.

For this client, the useful change was giving each part a clear job: AI helps read the listings, written rules apply the client's criteria, and a shared workflow keeps the sources consistent. Recording the reason for each decision also gives the client a way to review what happened.

If your team has a repetitive process that needs attention, [workflow automation](/services/workflow-automation/) or an [AI assistant](/services/ai-assistants-and-agents/) may help. I'd start by looking at the work itself and where it gets stuck.
