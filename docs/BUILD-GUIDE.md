# Build guide: the GTM-Job-Search repo

This guide gets you from the files in this folder to a public repo that anyone installs with one command. Nothing here is run for you; you run each command.

## 1. What you are building

One repo, one marketplace, one plugin:

```
GTM-Job-Search/
  README.md
  .claude-plugin/marketplace.json        # marketplace "stefanos-gtm", lists the plugin
  docs/BUILD-GUIDE.md
  plugins/gtm-job-search/
    .claude-plugin/plugin.json           # name, version, description
    agents/gtm-job-search.md             # dedicated assistant; loads the find-my-job skill
    skills/
      find-my-job/
        SKILL.md                         # onboarding, search waves, rank, research, hand-off
        references/responsibilities.md   # per-role responsibility menus
        references/company-research.md   # momentum scorecard
      gtm-resume-tailor/
        SKILL.md
        references/position-types.md     # eight role profiles
    scripts/
      fetch_ats.py                       # reads Greenhouse / Lever / Ashby feeds (stdlib only)
      build_pool.py                      # builds the company pool from data/sources
    data/
      company-universe.json              # generated; do not hand-edit
      sources/*.txt                      # edit these
```

Skills, agents and the manifest are discovered by folder name; there is no registration step.

## 2. Prerequisites

- Claude Code v2.1.292+ (`claude --version`).
- Python 3 (scripts use the standard library only).
- `git`, and `gh` (GitHub CLI) if you want to create the repo from the terminal.

## 3. Validate locally

One command runs every pre-release check (manifests, scripts, pool freshness and sanity, skill size limits, stale names, a live scan of three companies, bad-input handling):

```bash
bash tests/run_checks.sh
```

All lines must say PASS. The manual steps:

From the repo root:

```bash
claude plugin validate ./plugins/gtm-job-search
claude plugin validate .
```

Both must pass. Then test an install from the local folder before publishing:

```bash
claude plugin install gtm-job-search --marketplace /absolute/path/to/GTM-Job-Search
```

Open Claude Code and run `/gtm-job-search:find-my-job`. Check that onboarding asks the five questions, wave 1 scans run, and a link you are shown opens on the company's own site.

## 4. Create the repo and publish

```bash
cd GTM-Job-Search
git init
git add .
git commit -m "Initial release"
gh repo create stefanoskarakasis/GTM-Job-Search --public --source . --push \
  --description "$(cat docs/REPO-DESCRIPTION.txt)"
```

Without `gh`: create an empty public repo named `GTM-Job-Search` on github.com/stefanoskarakasis, then `git remote add origin https://github.com/stefanoskarakasis/GTM-Job-Search.git` and `git push -u origin main`.

Verify from a clean machine or another user:

```bash
claude plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search
```

Repo description (GitHub "About", 350 characters max) is in `docs/REPO-DESCRIPTION.txt`. If you create the repo in the browser, paste it into the About box. Suggested topics: `claude-code`, `claude-code-plugin`, `job-search`, `gtm`, `marketing-engineering`, `resume`.

## 5. Refresh the company pool

1. Edit or add a list in `plugins/gtm-job-search/data/sources/` (one company per line, `#` comments, a trailing `?` = name not confirmed, optional `Name | size band | listings`).
2. New list files must also be added to `SOURCES` in `scripts/build_pool.py` with a source tag and priority. Priority 0-2 = wave 1 (default), 3+ = wave 2 (wider).
3. Rename duplicates in `aliases.txt` (for example `Apollo = Apollo.io`).
4. Run `python3 plugins/gtm-job-search/scripts/build_pool.py`.
5. Test: `python3 plugins/gtm-job-search/scripts/fetch_ats.py scan --universe plugins/gtm-job-search/data/company-universe.json --wave 1`.

Sources worth re-reading regularly: marketingengineer.jobs (live listings, priority 0), each new GTM Jobs issue, the adamgtm.com GTM Index, skills.marketing, and TrueUp's company pages.

## 6. Release and update

1. Bump `version` in `plugins/gtm-job-search/.claude-plugin/plugin.json` (and in the skill front matter if you changed a skill). Without a bump, users may not receive updates.
2. Commit and push.
3. Tag: `git tag v1.1.0 && git push --tags`.
4. Users update with `claude plugin update gtm-job-search@stefanos-gtm`.

## 7. Maintenance checklist (monthly)

- Rebuild the pool and re-run a wave 1 scan; note how many companies resolve.
- Spot-check five returned links against the company's own site.
- Re-check the ATS endpoints in `fetch_ats.py` still return 200 (feeds change).
- Re-read the eight position-type profiles against fresh postings.

## 8. Known limits (state these; do not hide them)

- About half the pool cannot be read through direct feeds (Workday, custom sites, unusual board names). The agent checks those by hand through search and the careers page.
- Some Ashby and Lever matches come from guessed board names. The live check confirms the company before a role is shown.
- TrueUp cannot be filtered by marketing-engineering title; its list here is broad and low relevance, so it sits in wave 2.
- The eight tailoring profiles are hypotheses from general hiring practice, not validated with hiring managers. Test each on 3+ real postings and 2+ real resumes.
- The pool lists contain names not independently confirmed (`verify_name`), and GTM Jobs issues #01 and #02 plus most of the adamgtm.com directory were not read when the pool was built.
- Stress test on 2026-10-19 found and fixed: an offline scan silently reported "no matches" and cached every company as unresolved (now stops with a network error and caches nothing); a bad `--keywords` regex crashed (now a clean error); Clay and similar companies with suffixed board names (`claylabs`) were missed (suffix pass now covers Ashby and Lever, accepted only when the posting text names the company). Remaining: Rippling, Glean and about 90 others still unresolved; the default keyword set returned 550 roles across both waves of which most were not the target type, so the skill now passes per-role keywords.
- Two simulated runs (beginner Marketing Engineering in Europe; veteran PMM director in the US) were done against real scan data, not with real people. The beginner case returned 3 candidate roles, one a poor fit (a US-remote events role) — which is why the skill now checks the region behind "Remote".
- No end-to-end user run has been recorded yet. Do one beginner and one 10+ year run before announcing.

## 9. License

No license file is included. Choose one (for example MIT) before making the repo public; without one, others have no right to reuse the code.

## 10. Privacy

Local state only, in `~/.gtm-job-search/`. No analytics, no connectors, no keys. The plugin never applies or contacts anyone.
