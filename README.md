# AI GTM Job Search

Tell Claude which AI GTM role you want. It reads open roles straight from company job sites, checks they are still live, researches each company's momentum, and tailors your resume to the one you pick. Free, MIT licensed, no API keys.

## The roles it searches

The same job has a different name at every company, so onboarding asks what you want to do all day, not what you want to be called. It searches [eight fields](plugins/gtm-job-search/skills/gtm-resume-tailor/references/position-types.md):

- **GTM Engineering:** build the revenue systems
- **AI Product Management:** own an AI product's quality, cost and adoption
- **Product Marketing:** own positioning, launches and enablement
- **RevOps:** make the revenue engine measurable
- **Forward-Deployed Engineer:** get the product working inside a customer's environment
- **Marketing Engineering:** ship the tooling behind marketing
- **AEO / GEO:** improve a brand's presence in AI answers
- **AI Transformation:** change how a team works with AI

Your resume is tailored to whichever field the posting is actually in.

![A sample shortlist card: verdict, apply link, location, level, pay, days since posted, momentum, why it matches, gap and next move](docs/images/shortlist-card.png)

*Sample output for an invented person.*

## Install in under 2 minutes

**Claude Cowork:** Customize, Plugins, Add marketplace, enter `stefanoskarakasis/GTM-Job-Search`, then install **gtm-job-search**.

**Claude Code:**

```bash
claude plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search
```

<details>
<summary>Claude app (claude.ai and desktop)</summary>

1. Download [find-my-job.zip](https://github.com/stefanoskarakasis/GTM-Job-Search/releases/latest/download/find-my-job.zip) and [gtm-resume-tailor.zip](https://github.com/stefanoskarakasis/GTM-Job-Search/releases/latest/download/gtm-resume-tailor.zip). Do not unzip them.
2. Turn on code execution and web search (Settings, Capabilities).
3. Go to Skills, click Upload skill, and select each zip. Switch both on.

</details>

## Use it three ways

1. **"Find me a GTM engineering job."** Swap in any of the eight fields. Five quick questions (role, the work you want and want to avoid, seniority with proof, location and work authorization, salary), plus a proof check. Add your resume and it fills most answers. You get a ranked shortlist.
2. **"Tailor my resume to this posting"** plus a link or pasted text. It skips straight to tailoring.
3. **"Research" any company you name**, up to three at a time. You get a momentum scorecard for each: funding, layoffs and news, ending in Rising, Steady, Cooling or Unclear.

## Four checks before you apply

1. **Is it live?** Each posting is re-read before you see it, with its original posting date.
2. **Is the pay real?** Pay appears only when the posting lists it. Nothing is estimated.
3. **Is "Remote" really remote for you?** Every remote role is checked for the regions it is open to.
4. **Is the company moving?** Rising, Steady, Cooling or Unclear, backed by funding, layoffs and news.

Gaps between your resume and a role are reported, never filled.

## What's inside

- [`find-my-job`](plugins/gtm-job-search/skills/find-my-job/SKILL.md): onboarding, the live search, the four checks, and a "Before you apply" list.
- [`gtm-resume-tailor`](plugins/gtm-job-search/skills/gtm-resume-tailor/SKILL.md): rewrites your resume for one posting across the eight fields.
- [`position-types.md`](plugins/gtm-job-search/skills/gtm-resume-tailor/references/position-types.md): what each of the eight fields needs from you.
- [`company-universe.json`](plugins/gtm-job-search/data/company-universe.json): the 289 companies it searches, built from [public lists](plugins/gtm-job-search/data/sources/).
- [`fetch_ats.py`](plugins/gtm-job-search/scripts/fetch_ats.py): reads Greenhouse, Lever and Ashby job feeds. Standard library only.
- [`docs/`](docs/): [how it works](docs/HOW-IT-WORKS.md), [an example run](docs/EXAMPLE.md), [the category](docs/AI-GTM-CATEGORY.md), [customizing](docs/CUSTOMIZING.md), [adapting it to another field](docs/ADAPTING.md), [contributing](docs/CONTRIBUTING.md) and [sources](docs/SOURCES.md).

## Want more great AI skills?

I write about AI, product marketing and go-to-market every week, and share the Claude skills I build.

- **[Stefanos's Stack](https://stefanoskarakasis.substack.com/)**: research and resources for product marketing leaders, founders and GTM operators.
- **[GTM Jobs](https://gtmjobs.substack.com/)**: the most impactful go-to-market roles, curated weekly.
- **[Product Marketing Skills](https://github.com/stefanoskarakasis/Product-Marketing-Skills)**: Claude skills for PMMs and GTM teams.

## License

[MIT](LICENSE) — use these however you want.
