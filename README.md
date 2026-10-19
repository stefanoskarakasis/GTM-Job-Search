# AI GTM Job Search

> Find your next role in AI GTM. Claude skills that match you to roles at companies hiring now, check they are live, research each company's momentum, and tailor your resume to the one you pick.
>
> Built for Claude: upload two skills in the Claude app, add the plugin in Cowork, or install it in Claude Code. No API keys, no accounts, no connectors.

AI GTM is where go-to-market meets AI: agents that run outbound, answer engines that replace search, engineers embedded with customers, marketers who ship code. Job titles vary widely from one company to the next, so this tool searches by the work you want to do, not just by title.

## What it is

AI GTM Job Search is a pair of Claude skills (packaged as a plugin): a guided job-search assistant for the roles where go-to-market meets engineering and AI. You answer five questions about the role and the work you want, and it returns a short, ranked list of open roles with the original posting date, the pay only when the posting lists it, and a plain reason each role fits you.

It then researches the companies you pick, using public data on funding, headcount, layoffs and news, and rewrites your resume for one posting without inventing anything you did not do.

## Who it is for

- **Someone starting out** who has seen "GTM Engineer" or "AI Transformation Lead" on a job board and does not know yet which of these roles is theirs. It explains the role names in plain language, and shows a few stretch roles with a gap plan.
- **A marketing engineer, PMM, RevOps or product leader with 10+ years** who wants a terse shortlist, no explanations, and questions about scale instead of basics.
- **Anyone switching into the category** from sales, marketing, product, data or engineering.

## What you get

- **A tight onboarding.** Target role, the responsibilities you want and want to avoid, seniority with proof, location and work authorization, salary band.
- **Roles from the source.** It reads each company's own job site first, whatever system it runs on. LinkedIn, Indeed, TrueUp and similar sites are only leads, and you never get an aggregator link.
- **A default pool first, then a wider net.** It searches a curated pool of forward-looking companies, then a wider pool, then the open web, and labels where each role came from.
- **Roles checked live.** Each posting is re-read before it is shown. Salary is shown only if the posting lists it, and "Remote" is vetted for the real region.
- **Company momentum.** For roles you pick: funding, last round, headcount growth, open GTM roles, layoffs and news, ending in Rising, Steady, Cooling or Unclear with the evidence.
- **A tailored resume** for one posting, across all eight role types below. Gaps are reported, never filled.

---

## What the AI GTM job category holds

This is a small, fast-moving category at the seam of revenue, marketing, product and AI. The assistant covers eight position types. The titles vary by company; the work is what matters, so onboarding asks you about the work.

| Position type | What the work is | Titles you will see |
|---|---|---|
| **GTM Engineering** | Build the revenue systems: enrichment, routing, scoring, outbound automation, internal agents | GTM Engineer, Revenue Engineer, GTM Systems Engineer, GTM Architect |
| **AI Product Management** | Own an AI product surface and its quality, cost and adoption | AI Product Manager, AI Product Lead |
| **Product Marketing** | Own positioning, launches, sales enablement and competitive work | Product Marketing Manager, PMM, Product Marketer |
| **RevOps** | Make the revenue engine measurable and predictable: CRM, pipeline, forecasting, process | Revenue Operations, Sales Operations, GTM Operations |
| **Forward-Deployed Engineer** | Get the product working inside a real customer's environment | Forward-Deployed Engineer, Deployment Engineer, Implementation Engineer |
| **Marketing Engineering** | Ship the tooling and systems behind marketing and tie them to pipeline | Marketing Engineer, Technical PMM, Growth & Marketing Engineer |
| **AEO / GEO** | Improve a brand's presence in AI-generated answers and AI search | AEO, GEO, AI Search roles |
| **AI Transformation** | Change how a team or company works with AI, and measure the change | AI Transformation Lead, Head of AI Transformation |

---

## Get started

Pick the way you use Claude. Every route gives you the same two skills: `find-my-job` and `gtm-resume-tailor`.

### In the Claude app (claude.ai and the desktop app)

1. Download both files: [find-my-job.zip](https://github.com/stefanoskarakasis/GTM-Job-Search/raw/main/dist/find-my-job.zip) and [gtm-resume-tailor.zip](https://github.com/stefanoskarakasis/GTM-Job-Search/raw/main/dist/gtm-resume-tailor.zip). Do not unzip them.
2. Turn on code execution: **Settings, Capabilities**. Skills need it. On Team and Enterprise plans an owner enables it under Organization settings.
3. Go to **Customize, Skills**, click **+**, then **Create skill**, then **Upload a skill**. Upload each zip, one at a time.
4. Make sure both skills are switched on in the list.
5. Start a new chat and say: **"Find me a marketing engineering job."** Replace the role with the one you want. The first run is the onboarding.

Tips for the Claude app:
- Turn on web search so Claude can read company job sites. Without it the search is much thinner.
- Claude may not keep files between chats. At the end it gives you your profile as a short block of text. Paste it at the start of your next chat to skip the onboarding.
- For a long search, use a Project and keep your resume and profile in the project files.

### In Claude Cowork

1. Open **Customize** at the bottom left.
2. Go to **Browse plugins**, then **Personal**, then **+**.
3. Choose **Add marketplace from GitHub** and enter `stefanoskarakasis/GTM-Job-Search`.
4. Install **gtm-job-search**, then start a chat and say "Find me a marketing engineering job."

If the plugin's skills do not appear after installing, use the Claude app route above; it installs the same two skills.

### In Claude Code (terminal)

```bash
claude plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search
```

Or inside a Claude Code session:

```text
/plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search
```

Then start with `/gtm-job-search:find-my-job` or just say "find me a marketing engineering job." You can also pick the `gtm-job-search` assistant from `/agents`. Needs Claude Code v2.1.292 or later.

### Day-to-day commands

| You say | What happens |
|---|---|
| "find me a marketing engineering job" (or `/gtm-job-search:find-my-job` in Claude Code) | Full flow: onboard (or welcome back), search, rank, research, tailor |
| "tailor my resume to this posting" + a link or text | Skips to tailoring and asks only for what is missing |
| "research Granola and Assured" | Momentum scorecard for those companies |
| "show the wider pool" | Runs the wider search again with your saved profile |
| "change my salary / location" | Updates your profile and re-ranks |
| "forget me" | Deletes your saved profile |

---

## A sample session

An invented person. The two roles are real ones read from company job feeds on 2026-10-19 and will have changed by the time you run it.

```text
> Find me a marketing engineering job.

Which role are you going for?
  1 GTM Engineering   2 AI Product Management   3 Product Marketing   4 RevOps
  5 Forward-Deployed Engineer   6 Marketing Engineering   7 AEO/GEO   8 AI Transformation
> 6

Marketing Engineering. What do you want to spend your days on? (pick up to 4)
  [x] marketing infrastructure and tracking   [x] automation across the martech stack
  [ ] attribution and data pipelines          [x] internal tools for marketers
  ...
Anything you want to avoid? > copywriting, paid media

Level, and 2-3 things you built or ran? > 3 years. Built a Zapier + Sheets lead router,
  rebuilt our GA4 setup, ran a Webflow migration.
Location? > London, remote or hybrid, UK work rights
Salary? > Show me posted ranges first.

Profile: Marketing Engineering | mid | London / remote UK | no salary floor
Want: infrastructure, automation, internal tools | Avoid: copywriting, paid media. Right?
> yes

1. Growth Engineer @ Granola →
   https://jobs.ashbyhq.com/granola/494fe9a6-0144-4ebd-89a8-b8a187f93ff1
   London | mid | ⚠️ Salary not listed | 34 days since posted
   Fit: Good. Why: you built the lead router and the GA4 rebuild. Gap: no product-led growth experience.

2. AI Marketing Engineer @ Assured →
   https://jobs.ashbyhq.com/assured/bc94b141-7a54-4e58-9dec-df3fcb292740
   Remote | mid | ⚠️ Salary not listed | 116 days since posted
   Fit: Good. Why: ...  Gap: ...

Only two roles passed your filters. The limit was location: most marketing-engineering
postings in the pool are US-based. Relax location, or want me to widen the title search?
```

---

## Customizing

Change how roles are scored, add a company's job board, add companies to the pool, or teach the scanner a new job-board system: see [docs/CUSTOMIZING.md](docs/CUSTOMIZING.md). Building and publishing your own copy of the repo: [docs/BUILD-GUIDE.md](docs/BUILD-GUIDE.md).

## Adapting it to your field

Nothing in the flow is specific to GTM. The assistant, the scanner and the company scorecard work for any job category with a list of target companies. To adapt it:

1. Replace the position types in `plugins/gtm-job-search/skills/gtm-resume-tailor/references/position-types.md`.
2. Replace the responsibility menus in `plugins/gtm-job-search/skills/find-my-job/references/responsibilities.md`.
3. Replace the per-role title keywords in `plugins/gtm-job-search/skills/find-my-job/SKILL.md` (Step 2).
4. Replace the company lists in `plugins/gtm-job-search/data/sources/`, then run `python3 plugins/gtm-job-search/scripts/build_pool.py`.

---

## Privacy

Nothing is sent anywhere except plain requests to companies' public job feeds. Where Claude can save files (Claude Code), your profile lives in `~/.gtm-job-search/` on your machine. In the Claude app you keep your profile card yourself as text. Your resume goes to Claude the way any file you share in a chat does. Say "forget me" and a saved profile is deleted.

## Update

- **Claude app:** download the new zips and upload them again over the old ones.
- **What changed:** see the [changelog](CHANGELOG.md) and the [Releases](https://github.com/stefanoskarakasis/GTM-Job-Search/releases) page.

## License

MIT
