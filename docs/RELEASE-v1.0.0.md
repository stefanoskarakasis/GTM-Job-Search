Tell Claude which AI GTM role you want. It finds matching open roles on company job sites, checks they are still live, researches the company, and tailors your resume.

## What it does
- **Five-question onboarding:** target role, work you want and want to avoid, seniority with proof, location and work authorization, salary band.
- **Searches company job sites, not job boards:** 289 companies in two waves (120 default, 169 wider), then the open web. You never get an aggregator link.
- **Checks every role is live:** original posting date, pay only when listed, and every "Remote" role vetted for its real region.
- **Company momentum:** funding, headcount growth, open GTM roles, layoffs and news, ending in Rising, Steady, Cooling or Unclear.
- **Tailors your resume** to one posting across 8 role types: GTM Engineering, AI Product Management, Product Marketing, RevOps, Forward-Deployed Engineer, Marketing Engineering, AEO/GEO, AI Transformation. It never invents an achievement.

## Install
- **Claude app:** download both zips below, then Customize, Skills, Upload a skill.
- **Cowork:** Customize, Browse plugins, Personal, add marketplace from GitHub: stefanoskarakasis/GTM-Job-Search
- **Claude Code:** claude plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search

## Known limits
- Tested in Claude Code only. The Claude app and Cowork routes are untested.
- About half the companies cannot be read through public job feeds and are checked by hand, which is slower.
- The 8 tailoring profiles are working hypotheses, not validated with hiring managers.
