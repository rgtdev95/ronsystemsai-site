# 08 — Decisions

## Decided (2026-09-30)

| # | Decision | Choice | Notes |
|---|---|---|---|
| 1 | **Brand name** | **Ron Systems AI** | The About page and structured data say "Rolando 'Ron' Tactay" so search engines and AI tools connect the brand to the person. |
| 2 | **Domain** | **ronsystemsai.com** | Showed no DNS records on 2026-09-30, so it looks unregistered. Confirm with a registrar before buying. Matching handles: `@ronsystemsai`. |
| 3 | **Tech stack** | **Flask (Python) + server-rendered HTML (Jinja2) + plain CSS and JavaScript** | No frontend framework, no build step. Server-rendered pages suit search and AI crawlers. See [09-architecture-and-deployment.md](09-architecture-and-deployment.md). |
| 4 | **Hosting** | **Own VPS, Docker containers** | One environment for now: **prod** (the test site was dropped, decision 17). See [09-architecture-and-deployment.md](09-architecture-and-deployment.md). |
| 5 | **Git workflow** | **Simple git flow**: `main` → prod, `develop` collects work (CI only), short-lived feature branches | See [10-git-workflow.md](10-git-workflow.md). |
| 6 | **Pricing on the site** | **Not shown** | Services use "scoped and quoted before work starts" wording. No price figures anywhere on the site. |
| 7 | **Language** | **English**, US spelling | Matches the existing copy ("prioritized"). One variant site-wide. |
| 8 | **Individuals offer** | **Skipped for now** | Site targets small and medium businesses. Revisit later. |
| 9 | **Social channels** | **Facebook, YouTube, LinkedIn** | Same name, one-liner, photo, and link on all three. |
| 10 | **Time zones and availability** | **Not on the site** | No time-zone FAQ and no response-time promise for support. Call slots are managed manually in the Proton Calendar booking page. |
| 11 | **Client-location claims** | **Not on the site** | No "Working with clients in AU/NZ/EU/Asia" or "Available to clients in…" lines in the site copy. Target markets stay in hidden metadata only (structured data `areaServed`). |
| 12 | **Analytics** | **Umami (self-hosted on the VPS) + Google Search Console + Bing Webmaster Tools** | Umami: visits, pages, referrers (incl. AI assistants), countries, devices, and events (Book-a-call clicks, booking-page opens, email and LinkedIn clicks). Cookie-less, so no consent banner. Search Console and Bing show the search queries. Enabled on prod only. |
| 13 | **Reverse proxy** | **Caddy** | Runs as a container; automatic HTTPS for `ronsystemsai.com`, `www` (redirect), and `stats.`. Also sets security headers and compression. See [09-architecture-and-deployment.md](09-architecture-and-deployment.md). |
| 14 | **Email provider** | **Proton Mail**, custom domain `contactme@ronsystemsai.com` | Needs a paid plan that supports custom domains. The site only links to this address; it sends no mail itself, so no SMTP token is needed (the contact form was dropped, decision 16). DNS: Proton's verification TXT, MX, SPF, DKIM (3 CNAMEs), and DMARC records. |

All decisions made as of 2026-09-30.

## Decided (2026-11-08)

| # | Decision | Choice | Notes |
|---|---|---|---|
| 15 | **Booking tool** | **Proton Calendar booking page** (for now), linked from `/book/` | Included with the paid Proton plan already needed for email (decision 14), reads Ron's Proton calendar directly; booking details are encrypted. The discovery call is a 30-minute phone call (changed from a 20-minute video call on 2026-11-08); the booking form doesn't collect phone numbers, so Ron follows up each booking by email (template and a possible automation in [12-booking-follow-up.md](12-booking-follow-up.md)). The site links out in a new tab (no embed), so there are no third-party scripts or cookies. Set via `BOOKING_URL`; any other tool's link works the same way. Limits: one booking page on Mail plans, name and email only (no intake questions), and no completed-booking events for analytics. Calendly and Cal.com were the alternatives. |
| 16 | **Contact form** | **Dropped.** `/contact/` redirects to `/book/` | Booking and the contact form did the same job. Visitors book a call, email `contactme@ronsystemsai.com`, or message on LinkedIn (`/book/` lists LinkedIn and Facebook when their URLs are set). Removes SMTP sending, the site's only cookie (so the site sets no cookies at all), CSRF and rate limiting, and three dependencies. Trade-off: someone who won't book a call and won't open their email app has no form to fill in. Revisit if inquiries are low. |
| 17 | **Settings and deployment** | **One `.env` file, one compose file (`deploy/compose.yml`), live site only** | Replaces `.env.local` / `.env.prod` / `.env.test` / `.env.proxy` and four compose files. `.env` holds the values that are the same everywhere; `APP_ENV` (and from it `SITE_URL`) comes from where the site runs, so the file can be copied to the server unchanged. Locally, `flask run` loads `.env` automatically (python-dotenv). The test site (`test.ronsystemsai.com`) is dropped for now: check changes locally, and only `main` deploys. Bring it back as a second service in the same compose file if needed. |
