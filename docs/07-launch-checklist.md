# 07 — Launch checklist (including things easy to miss)

## Identity and trust

- [ ] **Register `ronsystemsai.com`** (confirm at the registrar) and claim `@ronsystemsai` on Facebook, YouTube, and LinkedIn
- [ ] **Proton Mail on the domain** (`contactme@ronsystemsai.com`), replacing the Gmail address on the site. Add Proton's DNS records (verification, MX, SPF, DKIM, DMARC)- [ ] Professional photo on the site (the current design has a `showPhoto` option but no photo yet)
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

- [ ] Real links in `.env`: `CONTACT_EMAIL`, `SOCIAL_LINKEDIN`, `SOCIAL_GITHUB` (and `SOCIAL_YOUTUBE` / `SOCIAL_FACEBOOK` once those exist). `/book/` and the footer use them, since there's no contact form
- [ ] Booking follow-up set up: the note on the Proton booking page and the email template saved in Proton Mail, asking for a phone number and a few lines about the business (see [12-booking-follow-up.md](12-booking-follow-up.md))
- [ ] Simple CRM or pipeline for leads. Run it on your own automation, which also makes good content
- [ ] Optional **lead magnet**: e.g. "The small-business automation checklist" PDF in exchange for an email

## Technical launch

- [ ] Everything in [05-search-and-ai-visibility.md](05-search-and-ai-visibility.md) section 1
- [ ] Security headers (CSP, HSTS). Your security background makes it worth getting an A on securityheaders.com
- [ ] `/.well-known/security.txt` (a small touch that fits a security-minded consultant)
- [ ] Uptime monitoring on the site itself
- [ ] Backups: git remote for source; an off-server backup of the VPS `.env` (it holds the Umami database password)
- [ ] Server `.env` in place at `~/ronsystemsai/deploy/.env` before the first deploy from `main` (see [09-architecture-and-deployment.md](09-architecture-and-deployment.md))
