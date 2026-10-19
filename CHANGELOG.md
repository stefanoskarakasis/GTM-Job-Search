# Changelog

## v1.0.0 (2026-10-19): AI GTM Job Search

First public release. Find AI GTM roles from company job sites, check they are live, research the company, and tailor your resume. Built for Claude: the Claude app, Cowork and Claude Code.

### Highlights

- **Five-question onboarding.** Target role, the responsibilities you want and want to avoid, seniority with proof, location and work authorization, salary band. Beginner, standard and veteran modes follow from your seniority.
- **Eight AI GTM position types.** GTM Engineering, AI Product Management, Product Marketing, RevOps, Forward-Deployed Engineer, Marketing Engineering, AEO/GEO, AI Transformation.
- **Company sites first.** Roles come from each company's own job site. LinkedIn, Indeed, TrueUp and similar sites are leads only; you never get an aggregator link.
- **Default pool, then a wider net.** 289 companies in two waves (120 default, 169 wider), then an open-web search for companies outside the pool, labelled as such.
- **Roles checked live.** Each posting is re-read before it is shown, with the original posting date. Salary appears only when the posting lists it. Every "Remote" role is vetted for its real region.
- **Company momentum scorecard.** Funding, last round, headcount growth, open GTM roles, layoffs and news, ending in Rising, Steady, Cooling or Unclear with the evidence.
- **Resume tailoring** for one posting across all eight types. It never invents an achievement; gaps are reported, not filled.

### What is included

- Skills: `find-my-job` and `gtm-resume-tailor`, plus the `gtm-job-search` assistant for Claude Code.
- `fetch_ats.py`: reads Greenhouse, Lever and Ashby job feeds, with the Claude app fallback to web search when the script cannot run.
- `build_pool.py` and 11 plain-text company lists you can edit.
- `dist/find-my-job.zip` and `dist/gtm-resume-tailor.zip`: upload-ready skills for the Claude app.
- Docs: [customizing](docs/CUSTOMIZING.md) (scoring and adding job boards) and [build guide](docs/BUILD-GUIDE.md).

### Install

- **Claude app:** download the two zips from `dist/`, then Customize, Skills, Upload a skill.
- **Cowork:** Customize, Browse plugins, Personal, add marketplace from GitHub: `stefanoskarakasis/GTM-Job-Search`.
- **Claude Code:** `claude plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search`

### Known limits

- Tested end to end in Claude Code on Linux. The Claude app and Cowork routes are built to Anthropic's upload rules but have not been tested in the app itself.
- About half the company pool cannot be read through public job feeds (Workday, custom sites, unusual board names). Those are checked by hand through search, which is slower and can miss roles.
- The eight tailoring profiles are working hypotheses from general hiring practice, not validated with hiring managers.
- Company lists draw on public sources. Some names are not independently confirmed and are flagged in the data.
