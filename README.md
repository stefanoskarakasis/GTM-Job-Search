# AT GTM Job Search

A job-search assistant for AT GTM roles that runs inside Claude Code. It reads open roles straight from companies' own job sites, checks they are still live, researches the companies, and tailors your resume to one posting.

It is built for two kinds of people: someone starting out who does not know what a "GTM Engineer" is yet, and a marketing engineer with ten-plus years who wants a terse shortlist and nothing else.

No accounts. No API keys. No connectors. Your profile stays on your machine.

---

## What it does

- **Asks five questions first**, so it knows the exact role and the exact work you want before it searches anything: target role, responsibilities you want and want to avoid, seniority and proof, location and work authorization, salary band.
- **Searches in three waves.** The default pool of forward-looking companies first, a wider pool second, then the open web for companies it does not know.
- **Goes to the company's own job site first**, whatever system it runs on (Ashby, Greenhouse, Lever, Workday, a custom page). LinkedIn, Indeed, TrueUp and other aggregators are leads only. You never get an aggregator link.
- **Checks every role is live** and shows the original posting date and the salary only if the posting lists one. It never estimates pay.
- **Ranks by fit** with a plain reason and the main gap for each role. "No good match" is a valid answer.
- **Researches the companies you pick** with a momentum scorecard: funding, last round, valuation, headcount growth, open GTM roles, layoffs, news. It ends in one label (Rising, Steady, Cooling, Unclear) with the evidence.
- **Tailors your resume** to one posting across eight position types. It never invents an achievement; gaps are reported, not filled.

### The eight position types

GTM Engineering · AI Product Management · Product Marketing · RevOps · Forward-Deployed Engineer · Marketing Engineering · AEO/GEO · AI Transformation

---

## Demo

A sample session, with an invented person. The roles are real ones read from company job feeds on 2026-10-19; they will have changed by the time you run it.

```text
> /gtm-job-search:find-my-job

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

Searching the default pool (120 companies)...  80 job sites read, 40 checked by hand.
Searching the wider pool (169 companies)...
Searching the open web for the title...

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

## Requirements

- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) v2.1.292 or later (`claude --version`)
- Python 3 (standard library only; already on most machines)
- Internet access

---

## Setup

One command, in your terminal:

```bash
claude plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search
```

Or inside a Claude Code session (v2.1.275 or later):

```text
/plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search
```

Choose "Install for you" when asked. That is the whole setup. The first run is the onboarding.

---

## Daily usage

| You say | What happens |
|---|---|
| `/gtm-job-search:find-my-job` | Full flow: onboard (or welcome back), search, rank, research, tailor |
| "find me a marketing engineering job" | Same, without the slash command |
| "tailor my resume to this posting" + a link or text | Skips to tailoring; asks only for what is missing |
| "research Granola and Assured" | Momentum scorecard for those companies |
| "show the wider pool" | Runs wave 2 again with your saved profile |
| "change my salary / location" | Updates the profile card and re-ranks |
| "forget me" | Deletes your saved profile |

You can also pick the `gtm-job-search` assistant from `/agents` for a dedicated session. It starts the same flow.

---

## How the search works

| Wave | What it covers | How |
|---|---|---|
| 1. Default pool (120) | Companies with live listings on marketingengineer.jobs, companies featured in GTM Jobs issues, and the top tiers of the gtm-jobs-tracker lists | Company job feeds via `scripts/fetch_ats.py`; hand-check of the rest |
| 2. Wider pool (169) | The rest of the tracker lists, skills.marketing, the adamgtm.com GTM Index, and TrueUp's top marketing-and-growth companies | Same; the unreadable ones are offered, not dug through automatically |
| 3. Open web | Companies outside the pool | `site:jobs.ashbyhq.com`, `site:boards.greenhouse.io` and `site:jobs.lever.co` searches for your target title. Results are labelled "outside the pool" |

**Reading job sites.** Greenhouse, Lever and Ashby publish their job boards as public data. The scanner reads those directly, works out which one a company uses, and remembers it. For Workday and custom careers pages the assistant uses web search and the page itself.

**Filtering.** Hard filters first (location with every "remote" role vetted for its real region, level, posted salary), then fit: position type, then skills and evidence against the posting's must-haves, then level, then salary. Roles are labelled Strong, Good or Stretch. There are no percentage scores.

**Live check.** The full posting is re-read from the company's own system before it is shown. A closed role is dropped.

### Company research scorecard

Modelled on what TrueUp tracks, plus every public source: company newsroom, SEC filings for public companies, news, layoffs trackers.

| Variable | Notes |
|---|---|
| Trajectory, rank, valuation | TrueUp company page if it loads, else web search |
| Funding, last round (type, amount, date, lead) | One source per figure, never added up by the assistant |
| Headcount and 12-month growth | A size band if no exact number is public |
| Open roles, GTM share, trend | From the scan; trend only if a previous scan exists |
| Layoffs and leadership changes | TrueUp layoffs page, layoffs trackers, WARN notices, news |
| Last 90 days | Raises, launches, layoffs, departures, acquisitions |

Verdict: **Momentum: Rising / Steady / Cooling / Unclear**. A last raise older than three years gets a ⚠️. Anything not found says "not found."

---

## Folder structure

```text
GTM-Job-Search/
├── README.md
├── .claude-plugin/marketplace.json          marketplace "stefanos-gtm"
├── docs/BUILD-GUIDE.md                      build, publish, maintain
├── spec/                                    design spec
├── tests/run_checks.sh                      pre-release checks
└── plugins/gtm-job-search/
    ├── .claude-plugin/plugin.json
    ├── agents/gtm-job-search.md
    ├── skills/
    │   ├── find-my-job/
    │   │   ├── SKILL.md                     the whole flow
    │   │   └── references/
    │   │       ├── responsibilities.md      per-role responsibility menus
    │   │       └── company-research.md      momentum scorecard
    │   └── gtm-resume-tailor/
    │       ├── SKILL.md
    │       └── references/position-types.md eight position-type profiles
    ├── scripts/
    │   ├── fetch_ats.py                     scan, resolve, detail
    │   └── build_pool.py                    builds the pool from data/sources
    └── data/
        ├── company-universe.json            generated
        └── sources/*.txt                    edit these
```

On your machine, local only:

```text
~/.gtm-job-search/
├── profile.md          your confirmed profile card
├── company-cache.json  which job system each company uses
├── overrides.json      manual fixes
└── last-scan-*.json    last scan results
```

---

## Customising

**Add a company's job board by hand** in `~/.gtm-job-search/overrides.json`:

```json
{ "Company Name": { "ats": "greenhouse", "token": "board-name" } }
```

`ats` is `greenhouse`, `lever` or `ashby`.

**Change the company pool.** Edit or add a plain-text list in `plugins/gtm-job-search/data/sources/` (one company per line, `#` for comments, a trailing `?` if the name is unconfirmed), then run `python3 plugins/gtm-job-search/scripts/build_pool.py`. Priority 0-2 is the default pool, 3 and up the wider pool. Details in [docs/BUILD-GUIDE.md](docs/BUILD-GUIDE.md).

**Adapt it to another field.** The flow, the scanner and the research scorecard are not specific to GTM. Replace the position types in `skills/gtm-resume-tailor/references/position-types.md`, the menus in `skills/find-my-job/references/responsibilities.md`, the per-role keywords in `find-my-job/SKILL.md`, and the company lists.

---

## What it does not do

- It does not apply, message anyone, or fill in forms.
- It does not read every job site directly. About half the pool uses systems with no public feed (Workday, custom sites) or board names it cannot guess; those are checked by hand through search, which is slower and can miss roles.
- It cannot see marketing-engineering roles that no company posts. The pool is dominated by US companies, so outside the US the honest answer is often a short list.
- It does not estimate salaries, posting dates or headcounts. Missing data is flagged ⚠️.
- The eight tailoring profiles are working hypotheses from general hiring practice, not data from hiring managers. Treat the output as a strong first draft and read it as a recruiter would.
- Company lists carry names that are not independently confirmed; they are flagged in the data and checked before use.

---

## Privacy

Your profile and settings live in `~/.gtm-job-search/`. The scanner sends only plain GET requests to companies' public job feeds. Your resume goes to Claude the way any file you share in a Claude Code session does. Say "forget me" and the saved profile is deleted.

## Update

```bash
claude plugin update gtm-job-search@stefanos-gtm
```

---

Built by [Stefanos Karakasis](https://github.com/stefanoskarakasis). Company lists draw on marketingengineer.jobs, GTM Jobs, skills.marketing, the adamgtm.com GTM Index and TrueUp; none of them is affiliated with this project.
