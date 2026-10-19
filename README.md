# AI GTM Job Search

> Find your next role in **AI GTM**. Claude skills that match you to roles at companies hiring now, check they are live, research each company's momentum, and tailor your resume to the one you pick.
>
> Built for **Claude**: the Claude app, Cowork and Claude Code. **No API keys, no accounts, no connectors.**

AI GTM is where go-to-market meets AI: agents that run outbound, answer engines that replace search, engineers embedded with customers, marketers who ship code. Job titles vary widely from one company to the next, so this tool searches by the **work you want to do**, not just by title.

## Why AI GTM Job Search?

Job boards give you listings. This gives you a **short list you can trust**: links straight from the company's own job site, roles checked live, "Remote" vetted for your region, and a resume rewritten for one posting without inventing anything.

**The result:** fewer, better applications.

## Who it is for

- **Starting out:** you have seen "GTM Engineer" or "AI Transformation Lead" and do not know which role is yours. It explains the titles in plain language and adds a few stretch roles.
- **10+ years in:** marketing engineer, PMM, RevOps or product leader. You get a terse shortlist and questions about scale, not basics.
- **Switching in** from sales, marketing, product, data or engineering.

## How it works

1. **Onboard in five questions.** Target role, work you want and want to avoid, seniority with proof, location and work authorization, salary band. **Add your resume and it fills the answers for you.** You confirm a profile card before anything is searched.
2. **Search the source.** Company job sites first, from a curated pool drawn from weekly AI GTM job trackers and live listings, including Anthropic, OpenAI, Clay and Harvey. LinkedIn, Indeed and TrueUp are leads only, so you **never get an aggregator link**. A wider pool and the open web follow, and every role is labelled with where it came from.
3. **Check every role.** Each posting is re-read live: original posting date, pay **only when the posting lists it**, and every "Remote" role vetted for its real region.
4. **See momentum before you apply.** Pick up to 3 companies and get **Rising, Steady, Cooling or Unclear**, with the funding, headcount, layoffs and news behind it.
5. **Tailor your resume** to one posting across 8 role types. **Gaps are reported, never filled.**

**Get the best results:** bring your resume, name 2-3 things you built with a number, say what work to avoid, and state your location and work authorization up front. Paste your profile card next time to skip onboarding.

## Installation

Every route installs the same two skills: **`find-my-job`** and **`gtm-resume-tailor`**.

### Claude app (claude.ai and desktop)

1. Download [find-my-job.zip](https://github.com/stefanoskarakasis/GTM-Job-Search/raw/main/dist/find-my-job.zip) and [gtm-resume-tailor.zip](https://github.com/stefanoskarakasis/GTM-Job-Search/raw/main/dist/gtm-resume-tailor.zip). **Do not unzip them.**
2. Turn on **code execution** and **web search**: Settings, Capabilities. On Team and Enterprise plans an owner may need to enable code execution and Skills first.
3. Open the **Skills** section (Settings, Capabilities, scroll to Skills, or Customize, Skills), click **Upload skill**, and select each zip.
4. Switch both skills on, start a new chat, and say **"Find me a marketing engineering job."**

If a button is labelled differently, look for the option to add or upload a skill. Anthropic changes these menus often.

Claude may not keep files between chats. At the end it gives you your profile as text. **Paste it next time** to skip the onboarding.

### Claude Cowork

1. Open **Customize** in the sidebar, then **Plugins**.
2. Click **Add marketplace** and enter `stefanoskarakasis/GTM-Job-Search`.
3. Install **gtm-job-search** and say **"Find me a marketing engineering job."**

On Team and Enterprise plans an owner may need to allow the repository first. If the skills do not appear, use the Claude app route above.

### Claude Code

```bash
claude plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search
```

Then run `/gtm-job-search:find-my-job` or just say **"Find me a marketing engineering job."** Needs a recent Claude Code (tested on **v2.1.303**).

## Start Here

| You want to | Say |
|---|---|
| **Find roles** | "Find me a marketing engineering job." |
| **Tailor your resume** | "Tailor my resume to this posting" + a link or text |
| **Research a company** | "Research Granola and Assured" |
| **Widen the search** | "Show the wider pool" |
| **Change your profile** | "Change my location" |
| **Delete your profile** | "Forget me" |

---

## The AI GTM job category

A fast-moving category at the seam of revenue, marketing, product and AI. The tool covers **8 position types**. Titles vary, so onboarding asks about the work.

| Position type | The work | Titles you will see |
|---|---|---|
| **GTM Engineering** | Build the revenue systems: enrichment, routing, scoring, outbound automation, internal agents | GTM Engineer, Revenue Engineer, GTM Architect |
| **AI Product Management** | Own an AI product's quality, cost and adoption | AI Product Manager, AI Product Lead |
| **Product Marketing** | Own positioning, launches, enablement, competitive work | Product Marketing Manager, PMM |
| **RevOps** | Make the revenue engine measurable and predictable | Revenue Operations, Sales Operations, GTM Operations |
| **Forward-Deployed Engineer** | Get the product working inside a real customer's environment | Forward-Deployed Engineer, Deployment Engineer |
| **Marketing Engineering** | Ship the tooling behind marketing and tie it to pipeline | Marketing Engineer, Technical PMM |
| **AEO / GEO** | Improve a brand's presence in AI answers and AI search | AEO, GEO, AI Search roles |
| **AI Transformation** | Change how a team works with AI, and measure it | AI Transformation Lead, Head of AI Transformation |

### A sample session

An invented person. The role is a real one read from a company job feed on 2026-10-19 and will have changed by the time you run it.

```text
> Find me a marketing engineering job.

Which role? 1 GTM Eng  2 AI PM  3 PMM  4 RevOps  5 FDE  6 Marketing Eng  7 AEO/GEO  8 AI Transformation
> 6
What do you want to do all day? (pick up to 4)  > infrastructure, automation, internal tools
Anything to avoid?                               > copywriting, paid media
Level and 2-3 things you built or ran?           > 3 years. Lead router, GA4 rebuild, Webflow migration.
Location?                                        > London, remote or hybrid, UK work rights
Salary?                                          > Show me posted ranges first.

Profile: Marketing Engineering | mid | London / remote UK. Right?  > yes

1. Growth Engineer @ Granola →
   https://jobs.ashbyhq.com/granola/494fe9a6-0144-4ebd-89a8-b8a187f93ff1
   London | mid | ⚠️ Salary not listed | 34 days since posted
   Fit: Good. Why: you built the lead router and the GA4 rebuild. Gap: no product-led growth experience.

Only one role passed your filters. The limit was location: most roles in the pool are US-based.
Relax location, or widen the title search?
```

---

## Customizing

Change how roles are scored, add a company's job board, or add companies to the pool: see **[docs/CUSTOMIZING.md](docs/CUSTOMIZING.md)**. Build and publish your own copy: **[docs/BUILD-GUIDE.md](docs/BUILD-GUIDE.md)**.

## Adapting it to your field

Nothing in the flow is specific to GTM. The assistant, the scanner and the company scorecard work for **any job category** with a list of target companies. To adapt it, replace:

1. **Position types:** `plugins/gtm-job-search/skills/gtm-resume-tailor/references/position-types.md`
2. **Responsibility menus:** `plugins/gtm-job-search/skills/find-my-job/references/responsibilities.md`
3. **Title keywords:** `plugins/gtm-job-search/skills/find-my-job/SKILL.md` (Step 2)
4. **Company lists:** `plugins/gtm-job-search/data/sources/`, then run `python3 plugins/gtm-job-search/scripts/build_pool.py`

## Contributing

Contributions are welcome. The most useful ones:

- **Company lists:** add or correct companies in `data/sources/`. Say where the name comes from.
- **Job boards:** report a company whose job board is not found, with its board name.
- **Position types:** sharpen a profile using **real postings and resumes**.
- **Bugs:** open an issue with what you asked, what you got, and which Claude surface you used.

Before opening a pull request, run `bash tests/run_checks.sh`. **Keep the honesty rules:** no invented facts, no estimated salaries, no aggregator links. See the [changelog](CHANGELOG.md) for what has shipped.

## Privacy

**Nothing is sent anywhere except plain requests to companies' public job feeds.** Where Claude can save files (Claude Code), your profile lives in `~/.gtm-job-search/` on your machine. In the Claude app you keep your profile card as text. Your resume goes to Claude the way any file you share in a chat does. Say **"forget me"** and a saved profile is deleted.

## License

MIT — see [LICENSE](https://github.com/stefanoskarakasis/GTM-Job-Search/blob/main/LICENSE).
