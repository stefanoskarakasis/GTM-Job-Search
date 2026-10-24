# Adapting it to your field

Nothing in the flow is specific to GTM. The assistant, the scanner and the company scorecard work for **any job category** with a list of target companies. To adapt it, replace:

1. **Position types:** `plugins/gtm-job-search/skills/gtm-resume-tailor/references/position-types.md`
2. **Responsibility menus:** `plugins/gtm-job-search/skills/find-my-job/references/responsibilities.md`
3. **Title keywords:** `plugins/gtm-job-search/skills/find-my-job/SKILL.md` (Step 2)
4. **Company lists:** `plugins/gtm-job-search/data/sources/`, then run `python3 plugins/gtm-job-search/scripts/build_pool.py`
