---
title: "How I chose the tools my business runs on"
description: "A look at the tools behind Ron Systems AI and the questions I ask before adding another one."
published: 2026-11-15
---

When I started putting the systems for Ron Systems AI together, I wasn't looking for the biggest collection of apps. I wanted a setup I could understand, maintain, and explain. Some tools run on a small server I rent; others are online services. Each one has a reason to be there.

You don't need a server to apply the same thinking. Whether your business uses Microsoft 365, Google Workspace, or a mix of apps, it helps to know what each tool does, who can reach it, and what happens if something breaks.

## What does my business run on?

The short answer is a handful of online services and one rented server. The server runs this website and several tools I use for my work. I chose online services for jobs such as email and domain management, where I prefer to rely on a provider that specializes in them.

Here's the setup:

| Job | Tool | Where it runs |
|---|---|---|
| Email and discovery call bookings | :logo-protonmail: Proton Mail and :logo-protoncalendar: Proton Calendar | Online service |
| Domain and DNS, which directs people to the right online services | :logo-cloudflare: Cloudflare | Online service |
| Website code and setup guides | :logo-github: GitHub | Online service |
| Automation between apps | :logo-n8n: n8n | My server |
| Website visitor statistics | :logo-umami: Umami | My server |
| Client wiki and private project notes | :logo-outline: Outline | My server |
| My passwords | :logo-vaultwarden: Vaultwarden, with Bitwarden apps | My server |
| App data | :logo-postgresql: PostgreSQL | My server |
| Passwords and keys used by apps | :logo-infisical: Infisical | Online service |
| Emails sent by apps, such as invitations | :logo-resend: Resend | Online service |
| Directing public traffic and managing HTTPS | :logo-caddy: Caddy | My server |
| Private access to admin tools | :logo-pangolin: Pangolin | My server and its online service |
| This website | :logo-flask: Flask | My server |

The server is an OVHcloud virtual private server, or VPS. It has two processor cores, 4 GB of memory, and 35 GB of storage. That's enough for my current setup, but it's small enough that I pay attention to what each new tool needs.

I run the server tools in containers. Think of a container as a separate package for an app and the things it needs to run. That makes it easier to manage each app without treating the whole setup as one big, tangled system.

## Why use a private server at all?

I like having control over where my data lives and how my tools are set up. Many of the tools I run are open source, and the server bill doesn't automatically rise each time I add a person in the way a per-user subscription might.

That doesn't make a private server free of costs or responsibilities. Someone still has to maintain it, install updates, and make sure backups can be restored. The server and any paid services also have their own costs. If nobody has the time or skills to look after it, a managed online service may be the better choice.

That's why I don't try to host everything myself. Proton handles my email, for example, and Cloudflare handles my domain. I make the same distinction when helping clients: start with what they already use, then choose the option that makes sense for the job.

## What is each tool actually doing?

Some tools have an obvious day-to-day role. Proton handles email and the calendar page for my free 30-minute discovery calls. n8n runs workflows that move information between apps. Umami shows me how people find and use this website without using cookies. Outline gives me a place to share project information with clients and keep separate private notes. Vaultwarden holds my own passwords.

Others work quietly in the background. PostgreSQL stores app data. Infisical holds the passwords and keys the apps need. Resend sends messages such as sign-in links and invitations. Caddy directs incoming traffic to the right place and takes care of HTTPS certificates. Pangolin gives me a private connection to tools I don't need to expose publicly.

Writing the list out makes overlaps easier to spot. In a small business, that overlap might look like tasks tracked in both a spreadsheet and a project app, or two chat tools that split the same conversation. The problem isn't just the extra software. It's the time spent wondering which version is current.

I haven't settled on a project management tool yet. Kaneo and Worklenz are both on my list to try before I choose one.

## Does every tool need to be public?

No. My website needs to be available to visitors, and my client wiki needs to be reachable by clients who sign in. My automation tool also needs to receive messages from other services. The part of Umami that counts visits has to be reachable by visitors' browsers.

My password manager, the Umami dashboard, the database, and admin screens have a different job. I access them through a private connection from my signed-in devices. They don't need a public entrance just because they run on a server.

The public tools still need protection. My automation tool has its own login and two-factor sign-in. Clients sign in to the wiki with a passkey or a one-time email link. Caddy handles HTTPS for public traffic.

For your own business, the useful question is: *who needs to reach this?* Take a look at old admin pages, remote access, and folders shared with anyone who has a link. Close access that no longer serves a purpose, and use two-factor sign-in wherever it's available.

## Where do the passwords go?

I keep my own logins in Vaultwarden, which I use through the Bitwarden apps on my devices. The passwords and keys my apps need live separately in Infisical. My setup files can name the secrets an app needs without containing the secret values themselves.

The apps also use separate database logins with access limited to their own data. My password manager doesn't depend on the shared database, and the Bitwarden apps keep an offline copy of my vault.

For a team, a practical first step is moving shared logins out of spreadsheets, email, and group chats and into a password manager made for sharing access. That gives everyone a clearer place to find what they need and makes access easier to manage when someone leaves.

## Could the setup be simpler?

This is the question I keep coming back to. A tool can look great on a feature list and still create more work than it saves. On a small server, every extra component also takes some of the memory I have available.

I compared AppFlowy and Outline for the wiki. AppFlowy needed nine containers and roughly 0.6–1.2 GB of memory in the setup I reviewed. Outline needed one container, a small cache, and the database I was already running. For my server, Outline was the more practical fit.

I also chose Resend over Brevo for app emails because I found its settings simpler. The apps currently share one sending key. That's convenient to manage, but it comes with a trade-off: if I cancel that key, email stops for all of them. I've written that down so it isn't a surprise later.

Before adding another tool, I estimate its memory use and add it to a budget. Once it's running, I check the real numbers. I'm also researching security tools such as CrowdSec, but each addition needs to earn its place.

## Is it written down?

I keep setup guides and a decision log in a private repository. They cover how the server is secured, the order things are installed, and why I made particular choices. The point is to make the setup understandable to someone following the documentation, including me when I return to it months later.

I also keep a list of things I haven't tested yet. A backup is reassuring, but until you've tried restoring it, you don't know for sure that it will get you back to work. I'm setting up a test machine at home so I can try new tools before putting them on the server.

This matters just as much in a business that doesn't run its own server. If the person who set up an important system left tomorrow, would someone else know how to get in, what depends on it, and where to find help? A short, current guide is a useful place to start.

## What's next?

I'm still choosing between Kaneo and Worklenz for project management. I also want to add uptime alerts and a server health dashboard, including a check from outside the server. A monitor on the server can't alert me if the server itself goes down.

Security monitoring is on the list too. I'll try it on the home test machine first and update this post as the setup changes.

## What can you take from this?

You don't need to copy my tools. The better place to start is with a few questions about your own: What does each one do? Who needs access? Where are the passwords? Is there an easier way to do the same job? And could someone else understand the setup if they needed to?

The answers can reveal a lot without requiring a complete overhaul. I work with the tools a business already uses and recommend options when a change would help or when it's starting fresh. If you'd like a second opinion, a [tech check-up](/services/tech-roadmap/) is a place to start.
