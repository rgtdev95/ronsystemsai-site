# 07 — Launch checklist (including things easy to miss)

## Next session: what's waiting (as of 2026-11-11)

The site work is done and in `dev` (PR #3). The first two articles and the move onto the VPS's shared Caddy and Umami (decision 21) are on `feature/release-v1`. Deploys are manual: a version tag on `main`, an image built and pushed by hand while GitHub Actions is blocked, and `sudo ./deploy.sh` on the VPS (decision 18). These are the open items, roughly in order.

### First: branches, the first release and the server

- [x] **Tidy the branches and push the work** (done by 2026-11-17: stray branches gone, `main` matches GitHub, the work merged into `dev`):

  ```bash
  git branch -f main origin/main                  # local main back to GitHub's version
  git branch -d checkout list                     # two stray branches
  git push origin --delete feature/initial-site   # old branch, already merged
  git push origin origin/main:dev                 # bring dev up to date with main
  git add -A
  git commit -m "feat: launch prep: branding, docker folder, manual releases"
  git push -u origin feature/launch-prep
  ```

- [ ] **Clear the GitHub billing lock.** No GitHub Actions job can run until it's cleared: CI is paused and the Release workflow is blocked (decision 19). Check GitHub → Settings → Billing and licensing; if nothing is owed there, contact GitHub Support. Then uncomment the `pull_request` trigger in `.github/workflows/ci.yml` and add the `checks` status to the ruleset. On the next release, confirm that publishing it on GitHub starts **Actions → Release** (decision 23; this couldn't be tried while Actions was blocked)
- [ ] **First release and server setup:** follow [13-releasing.md](13-releasing.md), "First release (one time)", steps 1–12. Step 9 checks the VPS for leftovers from the old auto-deploy (the `ec8754a` push to `main` on 2026-11-08 most likely failed at the server step). Where it stands on 2026-11-27: the release PR (#4) is merged and the `v1.0.0` tag is pushed. There's no GitHub release yet, and the image can't be downloaded publicly yet. Still to do in step 2: **Default branch** is still `main`. In step 4, pick the existing `v1.0.0` tag rather than creating one
- [ ] **Merge `main` back into `dev` before the next release PR** (found 2026-11-27): the v1.0.0 release PR (#4) was squash-merged, so a `dev` → `main` PR now shows conflicts in 7 files. Follow [Fix: a squash-merged release PR](13-releasing.md#fix-a-squash-merged-release-pr). `main` still matches `dev` as of `29c09b2`, so the check there passes

### Proton

- [x] Create the **`contactme@ronsystemsai.com`** address (or alias). The site links to it everywhere
- [ ] **Booking page:** set the length to **30 minutes**, add the note from [12-booking-follow-up.md](12-booking-follow-up.md), and turn off the automatic Proton Meet link (the call is by phone)
- [ ] Save the **follow-up email template** from [12-booking-follow-up.md](12-booking-follow-up.md) in Proton Mail

### Content (biggest effect on search and AI visibility)

- [ ] **Articles:** write the first 2–3 from the backlog in [04-site-structure.md](04-site-structure.md). AI assistants mostly cite pages that answer real questions
- [ ] **Case studies (on hold, decision 20):** details for the three drafts (type and size of business, what it was like before, key decisions, any measured results), so they can get full pages ([11-case-studies.md](11-case-studies.md))
- [x] **A real photo of you.** On the About page and in the Person structured data (`app/static/img/ron-profile.webp`, 560 px; original in `docs/brand/`)
- [ ] Optional: what you did in manufacturing, at the MSP and at the startup, if you want more than the one-line mention on the About page and homepage

### Settings in `.env`

- [ ] `INDEXNOW_KEY` (optional): generate with `python -c "import secrets; print(secrets.token_hex(16))"`. The site serves it and each deploy then submits all pages to Bing and others
- [ ] `UMAMI_WEBSITE_ID`: visitor stats don't record until it's set. Add the website in the VPS's shared Umami first ([13-releasing.md](13-releasing.md), step 7)

### After launch (needs the live site)

- [ ] Verify in **Google Search Console** and **Bing Webmaster Tools**, and submit `https://ronsystemsai.com/sitemap.xml`
- [ ] Run **Google's Rich Results Test** and **PageSpeed Insights** on the live pages
- [ ] **LinkedIn:** link to the site and use the same one-line description as `llms.txt`
- [ ] Start the monthly **AI visibility check** ([05-search-and-ai-visibility.md](05-search-and-ai-visibility.md), section 6)

### Small, optional

- [ ] Refresh the social share image (`app/static/img/og-card.png`) to match the new logo mark
- [ ] Add a line under "Choose a time" on `/book/`: "After you book, I'll email you to ask for the best number to call"
- [ ] "Why I do this" on the About page still mentions "support desks"; reword if you'd rather not

## Identity and trust

- [ ] **Register `ronsystemsai.com`** (confirm at the registrar) and claim `@ronsystemsai` on Facebook, YouTube, and LinkedIn
- [x] **Proton Mail on the domain** (`contactme@ronsystemsai.com`), replacing the Gmail address on the site. Add Proton's DNS records (verification, MX, SPF, DKIM, DMARC)
- [x] Professional photo on the About page
- [ ] **Proton Calendar booking page** created (30-minute discovery call by phone; the notes ask for the best number to call) and its link set as `BOOKING_URL` in `.env`. Until then, `/book/` offers email only
- [ ] LinkedIn headline and about section rewritten from job-seeker to consultant
- [x] `docs/about-ron/` (resume with phone number) is in `.gitignore`

## Proof

- [ ] 3–5 anonymized case studies written up in problem → what I built → result form
- [ ] Ask current and past clients for a short testimonial (with permission to publish name, role, and country)
- [ ] Start measuring results on every project (hours saved per week, errors reduced, response time) so later case studies have real numbers
- [ ] Certifications worth listing, if any (AWS, Microsoft, n8n, etc.)

## Business and legal (for working with overseas clients)

- [ ] **Business registration and tax** in the Philippines as a freelancer or sole proprietor (DTI + BIR). Check with an accountant
- [ ] **Getting paid internationally:** Wise, Payoneer, Stripe, or PayPal. Invoice in USD and/or the client's currency
- [ ] **Contract templates:** a services agreement plus a statement of work (scope, deliverables, change requests, payment terms, IP ownership, and liability limit)
- [ ] **Confidentiality / NDA** template
- [ ] **Data Processing Agreement (DPA)**: EU/UK clients will need one because you'll handle their data (GDPR). Australian clients expect Privacy Act awareness
- [ ] Access and credentials handling policy (how you store and return client passwords and keys, e.g. a shared Vaultwarden/Bitwarden vault they own)
- [ ] Consider **professional indemnity insurance** once projects grow

## Website legal pages

- [ ] Privacy policy (GDPR-, UK GDPR-, AU Privacy Act-, and CCPA-aware; cover what emails, analytics, and the Proton Calendar booking page collect)
- [ ] Terms of service: plain-English draft at `/terms/` (website use only; client work runs on the signed agreement). Confirm the governing law and have a lawyer review before launch
- [ ] No cookie banner needed: Umami is cookie-less, and the site sets no cookies of its own (stated on `/privacy/`, checked by a test). Recheck if any cookie-setting script is added later (booking opens Proton Calendar in a new tab, so it sets no cookies on this site)
- [ ] Accessibility statement (optional; WCAG 2.2 AA target)

## Lead handling

- [x] Real links in `.env`: `CONTACT_EMAIL`, `SOCIAL_LINKEDIN`, `SOCIAL_GITHUB` (add `SOCIAL_YOUTUBE` / `SOCIAL_FACEBOOK` once those exist). `/book/` and the footer use them, since there's no contact form
- [ ] Booking follow-up set up: the note on the Proton booking page and the email template saved in Proton Mail, asking for a phone number and a few lines about the business (see [12-booking-follow-up.md](12-booking-follow-up.md))
- [ ] Simple CRM or pipeline for leads. Run it on your own automation, which also makes good content
- [ ] Optional **lead magnet**: e.g. "The small-business automation checklist" PDF in exchange for an email

## Technical launch

- [ ] Everything in [05-search-and-ai-visibility.md](05-search-and-ai-visibility.md) section 1
- [ ] Security headers (CSP, HSTS). Your security background makes it worth getting an A on securityheaders.com
- [ ] `/.well-known/security.txt` (a small touch that fits a security-minded consultant)
- [ ] Uptime monitoring on the site itself
- [ ] Backups: git remote for source; an off-server backup of the VPS `.env` (it holds `SECRET_KEY`)
- [ ] Server `.env` in place at `/opt/apps/website/docker/.env` (root-only) before the first `sudo ./deploy.sh` (see [09-architecture-and-deployment.md](09-architecture-and-deployment.md#the-server))
