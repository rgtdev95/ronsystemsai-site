# 05 — Search and AI visibility (SEO, AEO, GEO)

- **SEO** (search engine optimization): rank in Google and Bing.
- **AEO** (answer engine optimization): be the answer in featured snippets, Google AI Overviews, and voice assistants.
- **GEO** (generative engine optimization): get cited by ChatGPT, Claude, Perplexity, Gemini, and Copilot.

Mostly the same work. The foundations below cover all three.

## 1. Technical foundations (build these into the site from day one)

- [ ] **Content in the HTML, not rendered by JavaScript.** Most AI crawlers don't run JavaScript. The chosen stack (Flask + Jinja2) renders full HTML on the server. Keep it that way: never load main content with client-side JS.
- [ ] `ronsystemsai.com` with HTTPS via Caddy; `www` and the test site handled correctly (see [09-architecture-and-deployment.md](09-architecture-and-deployment.md))
- [ ] Fast: Core Web Vitals green, images optimized, fonts self-hosted or preloaded
- [ ] Mobile-first and accessible (WCAG 2.2 AA)
- [ ] One `<h1>` per page, logical H2/H3, descriptive `<title>` (≤ 60 chars) and meta description (≤ 155 chars)
- [ ] Clean URLs, canonical tags, `sitemap.xml`, `robots.txt`
- [ ] `lang="en"` on the page. No hreflang needed while every page is in one English variant
- [ ] Open Graph and Twitter/X card tags with a share image (for Facebook and LinkedIn previews)
- [ ] 404 page and redirects plan

### robots.txt: let the AI crawlers in

Allow the crawlers that power AI answers (deliberate choice: we *want* to be cited):

```
User-agent: *
Allow: /

# AI assistants and answer engines: allowed on purpose
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: PerplexityBot
User-agent: Google-Extended
User-agent: Applebot-Extended
Allow: /

Sitemap: https://ronsystemsai.com/sitemap.xml
```

If you ever put a CDN/WAF in front of the VPS (e.g. Cloudflare), turn off its "block AI bots" setting. Anything that isn't the live site (`APP_ENV` other than `production`) serves the opposite: `Disallow: /` for everyone.

### llms.txt

Add `/llms.txt`: a short Markdown summary of who you are, what you offer, and links to the key pages. It's a low-cost, emerging convention some AI tools read.

## 2. Structured data (JSON-LD)

| Page | Schema types |
|---|---|
| Every page | `ProfessionalService` "Ron Systems AI" (url `https://ronsystemsai.com`, logo, `areaServed`, `founder` → Person, `sameAs` → Facebook, YouTube, LinkedIn) + `WebSite` |
| Home / About | `Person` (Rolando Tactay, `alternateName` "Ron Tactay", `jobTitle`, `knowsAbout`, `sameAs`, `worksFor`) |
| Service pages | `Service` (`serviceType`, `provider`, `areaServed`: US, GB, IE, EU, AU, NZ, SG) |
| FAQ sections | `FAQPage` (Google shows fewer FAQ rich results now, but AI systems still parse the Q&A structure well) |
| Articles | `Article` / `BlogPosting` with `author` → Person, `datePublished`, `dateModified` |
| Videos | `VideoObject` (name, description, thumbnail, uploadDate, embedUrl, transcript) |
| Breadcrumbs | `BreadcrumbList` |

Validate with Google's Rich Results Test and validator.schema.org.

## 3. Content that gets quoted

AI answers pull short, self-contained, factual passages. Write for that:

- **Answer first.** Start every page and section with a 40–60-word direct answer, then expand.
- **Question-shaped headings**, using the words customers use ("How much does it cost to automate…").
- **Specific facts and numbers**: time frames, price ranges, tool limits, real steps. Vague marketing copy doesn't get cited.
- **Comparison tables** (n8n vs Zapier vs Make, SaaS vs self-hosted) get extracted often.
- **Original experience**: "What I learned setting up X for a client." This is the E-E-A-T signal (experience, expertise, authoritativeness, trust) that AI can't generate itself.
- **Visible dates**: published and updated dates, and refresh key pages every 6–12 months.
- **An author on everything**: a real person with a photo, credentials, and profile links.

## 4. Entity consistency: be one recognizable "thing" across the web

AI models decide who to cite partly by how consistently an entity shows up across sources.

- Use the **same name, one-line description, photo, and link** everywhere: website, Facebook page, YouTube, LinkedIn, directories.
- Recommended one-liner (use it everywhere):
  _"Ron Systems AI is the IT systems, automation, and AI consultancy of Rolando "Ron" Tactay. He helps small and medium businesses automate manual work, adopt practical AI, and set up reliable systems. Based in Manila, working remotely."_
- Link every profile back to the site, and list every profile in the site's `sameAs`.

## 5. Off-site signals (where citations come from)

- **LinkedIn**: profile and posts. Heavily indexed and heavily trusted for B2B.
- **YouTube**: videos are cited in AI answers and Google results; each video links back to the matching site page.
- **Freelance/directory profiles** (pick 2–3): Upwork, Contra, Clutch, GoodFirms, and the partner/expert directories for n8n, Zapier, and Make if you qualify.
- **Q&A and communities**: Reddit (r/smallbusiness, r/n8n, r/automation), the n8n community forum, Quora. Give genuinely helpful answers with no spam.
- **Guest posts and podcasts** in small-business communities in the target markets.
- **Google Business Profile**: only if you can meet Google's rules for a service-area business; otherwise skip it.

## 6. Tools and measurement

- [ ] Google Search Console (verify domain, submit sitemap)
- [ ] Bing Webmaster Tools. Bing's index feeds ChatGPT search and Copilot, so it's easy to overlook and important. Enable **IndexNow**: set `INDEXNOW_KEY` in the server's `.env` (see `.env.example`); the site serves the key file and every deploy submits the sitemap's pages
- [ ] **Umami** analytics, self-hosted on the VPS (decided). Cookie-less, so no cookie banner is needed in the EU. Set up events: Book-a-call clicks, booking-page opens, email clicks, social-link clicks (Proton doesn't report completed bookings back to the site)
- [ ] Monthly "AI visibility check": ask ChatGPT, Perplexity, Gemini, and Claude 10 fixed questions (e.g. "best automation consultant for small business in Australia") and log whether you're cited
- [ ] Track referral traffic from `chatgpt.com`, `perplexity.ai`, `gemini.google.com`, and `copilot.microsoft.com`

## 7. Market pages: the honest version

Pages like "IT automation consultant for small businesses in Australia" work only if each one has **real, different content**: local tools (Xero/MYOB for AU/NZ, QuickBooks in the US), local rules (GDPR in the EU, the Privacy Act in AU), and local examples. Pages that are copies of each other with the city name swapped get treated as spam. Build them later, one at a time.
