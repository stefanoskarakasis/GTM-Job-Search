---
name: find-my-job
version: 1.0.0
description: Finds GTM and marketing-engineering jobs matched to you from company job sites, checks they are live, researches the companies, and tailors your resume. Use for job search in this category.
metadata:
  author: Stefanos Karakasis
  context: claude
  quality_gate: false
last_updated: 2026-10-19
---

# Find My Job

One conversation: onboard → find roles → check they are live → rank → research companies → tailor the resume. Everything that touches the user's profile stays on their machine.

**Voice:** plain, direct, kind. No hype. "No good match" is an acceptable answer; never stretch a fit to look useful.

---

## Trigger

- **When:** the user wants to find, compare, research or apply for GTM / marketing-engineering roles, or says "start".
- **Not for:** cover letters, interview coaching, applying on the user's behalf. Never submit anything or contact anyone.

---

## Inputs and files

- **Where the files are.** `data/` and `scripts/` sit inside this skill's own folder when it was uploaded as a standalone skill (Claude app), or two folders above it when installed as a plugin (Claude Code, Cowork marketplace). Check this skill's folder first, then two levels up. Below, `data/...` and `scripts/...` mean wherever you found them. If neither exists, say so and use Mode B (see Pre-flight).
- `data/company-universe.json`: the company pool. `wave` 1 = default pool (searched first: live listings on marketingengineer.jobs, companies in GTM Jobs issues, tracker tiers 1-2); `wave` 2 = wider pool (tracker tier 3, skills.marketing, adamgtm.com GTM Index, EMEA/FinTech lists, TrueUp marketing-and-growth top companies). Each company lists its `sources`; `verify_name: true` means the name was taken from a list and not independently confirmed.
- `references/responsibilities.md`: responsibility menus per role. `references/company-research.md`: momentum scorecard.
- `scripts/fetch_ats.py`: reads public job feeds (Greenhouse, Lever, Ashby). Standard library Python, no install, no keys.
- **User state:** `~/.gtm-job-search/profile.md` (their profile card), `company-cache.json` (which job site each company uses), `overrides.json` (manual fixes). Create the folder if missing. In the Claude app the files may not survive between chats; see Pre-flight.
- Resume or profile: optional at the start. A file path or pasted text.

---

## Pre-flight

Claude runs this skill in different places: Claude Code, the Claude desktop app or claude.ai with code execution, or a chat without code execution. Settle two things before onboarding.

**1. Saved profile.**
- If `~/.gtm-job-search/profile.md` exists, say "Welcome back. I have your profile: [one-line card]. Use it, or change something?" and skip onboarding unless they change something.
- If there is no saved profile, or the session cannot keep files between chats (common in the Claude app), tell the person once: at the end you will give them their profile card as text to paste at the start of a future chat, so they do not repeat onboarding. If they paste a card, use it as the saved profile.

**2. Which mode can run.** Test with one quick scan: `python3 scripts/fetch_ats.py scan --universe data/company-universe.json --only "Stripe" --out /tmp/preflight.json`.
- **Mode A (scanner works).** Use the scripts as written in the steps below.
- **Mode B (no shell, no Python, or the network check fails).** Do not stop. Use the web tools you have (web search and fetch, or a browser). Read `data/company-universe.json` with your file tools if it is available, and work wave 1 first. For each company, fetch its public job feed directly: `https://api.ashbyhq.com/posting-api/job-board/<slug>`, `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs`, `https://api.lever.co/v0/postings/<slug>?mode=json`, or read its careers page. Large boards come back truncated, so also run targeted searches such as `site:jobs.ashbyhq.com "<target title>"`. Cover the strongest wave 1 companies for the person's target role and the open-web search; do not pretend to have scanned the whole pool. Say plainly what you covered and what you did not.
- If no web tools are available either, say so and give the person the pool file and the keywords to search themselves, then offer the research and tailoring steps, which need only their input.

Tell them once, before searching: "I check the default pool first, then a wider pool. About half of these companies' job sites can be read directly through public feeds; the rest I check by hand, which is slower."

---

## Steps

### Step 1: Onboard (tight: five questions, then a confirmation)

Goal: get hyper-focused on the role and the work before any search. Ask one at a time. Use an in-chat question tool with options where one exists (for example AskUserQuestion in Claude Code) (the person can always type their own answer); otherwise ask in plain text. If they answer several at once, parse it and do not re-ask. A resume or profile, if the person has one handy, prefills the answers; ask them to correct it. Never infer target role or seniority silently.

1. **Target role.** "Which of these are you going for?" Options (pick one primary, optionally one secondary): GTM Engineering / AI Product Management / Product Marketing / RevOps / Forward-Deployed Engineer / Marketing Engineering / AEO-GEO / AI Transformation. If unsure, ask what they build or do best and propose one, then ask them to confirm. Full definitions: `gtm-resume-tailor/references/position-types.md`.
2. **Responsibilities.** Read `references/responsibilities.md`, show the menu for their target role(s), and have them pick up to 4 they want to do and up to 3 they want to avoid. Titles lie; this is what postings get matched on.
3. **Seniority and proof.** Options: just starting (0-2 years) / mid (3-5) / senior (6-9) / lead or director (10+); VP and above by typing. Then: "Name 2-3 things you built, shipped or ran, with a number if you have one. Coursework and side projects count." Set the mode:
   - **Beginner** (0-2 years): explain role names in one plain line, no unexplained jargon, include a few stretch roles with a gap plan.
   - **Standard** (3-9 years): normal detail.
   - **Veteran** (10+ or director and above): terse; ask for scale (ARR influenced, team size, systems owned).
   Level scale for matching: Entry and mid-level / Senior / Senior++ / Director / VP / SVP-CXO (product marketing: PMM / Senior PMM / PMM Lead / Principal / Director / VP).
4. **Location and work authorization.** City and country; remote / hybrid / onsite; whether they would relocate; work-authorization limits for places they would work.
5. **Salary band.** Minimum and target with currency, or "not sure, show me posted ranges first." Never push; skipping is fine.

Skills are inferred from the answers to 1-3 and the resume if given; when stated skills and evidence disagree, say so and ask which is right.

**Confirm, never assume.** Show a profile card (target role, wants, avoids, level, proof, location, authorization, salary, mode) and ask "Right?" Save it to `~/.gtm-job-search/profile.md`.

### Step 2: Find roles (default pool, wider pool, then open web)

Always search in this order and keep the waves labelled in the output.

1. **Wave 1, default pool.** Company's own hiring site first, whatever the system (Ashby, Greenhouse, Lever, Workday, a custom page):
   `python3 scripts/fetch_ats.py scan --universe data/company-universe.json --wave 1 --out ~/.gtm-job-search/last-scan-w1.json`
   (Mode A. In Mode B follow the Pre-flight instructions instead, still wave 1 first.)
   Always pass `--keywords` built from the confirmed target role so the shortlist is not drowned in other role types (the default regex covers all eight and returns hundreds of unrelated titles):
   - GTM Engineering: `gtm engineer|go-to-market engineer|revenue engineer|growth engineer|gtm systems|gtm architect`
   - AI Product Management: `ai product (manager|lead)|product manager.{0,20}(ai|ml|agent|llm)`
   - Product Marketing: `product marketing`
   - RevOps: `revenue operations|\brevops\b|sales operations|gtm operations|marketing operations`
   - Forward-Deployed Engineer: `forward[- ]deployed|deployment engineer|implementation engineer|solutions engineer`
   - Marketing Engineering: `marketing engineer|marketing technolog|marketing automation|growth engineer|growth platform`
   - AEO/GEO: `\baeo\b|\bgeo\b|answer engine|generative engine|ai search|ai discoverability|seo`
   - AI Transformation: `ai transformation|transformation lead|ai enablement|ai adoption`
   Use the union for a secondary target role. The scanner reads Greenhouse, Lever and Ashby feeds; it prints a summary and lists companies it could not read.
2. **Unresolved wave 1 companies.** Find the careers page with WebSearch ("[company] careers"), read it with WebFetch or a browser if available, and search it for the target role. When you learn a company's system and board name, record it in `~/.gtm-job-search/overrides.json` as `{"Company": {"ats": "greenhouse", "token": "board-name"}}` so the next run reads the feed directly. Companies with `verify_name: true` that cannot be resolved: confirm the company exists and is the right one before spending time.
3. **Wave 2, wider pool.** Run the same scan with `--wave 2`. Do not hand-check every unresolved wave 2 company; offer: "I can also dig through the other N by hand. Want that?"
4. **Wave 3, open web.** Then cast a wider net outside the pool: WebSearch sweeps such as `site:jobs.ashbyhq.com "<target title>"`, `site:boards.greenhouse.io "<target title>"`, `site:jobs.lever.co "<target title>"`. Roles found this way are marked **outside the pool** and get the research step in full, since the company is unknown to us.
5. Every role's link must be unique to that posting on the company's own site or job system. Aggregators (LinkedIn, Indeed, TrueUp, marketingengineer.jobs and the like) are leads only, never the link. If a lead exists only on an aggregator, find the company's own posting or drop it.
6. Roles whose match came from a guessed feed (name unchecked) are confirmed by the live check in Step 4 before they are shown.

### Step 3: Filter and rank

- **Hard filters:** location and work arrangement (**vet every "Remote" role**, see Step 4); level (within one level of their target, two for beginners going up); salary where a pay range is posted (exclude if the top of the range is below their minimum, and count how many you excluded so you can mention it).
- **Fit, in order of weight:** position-type match → skills and evidence versus the posting's must-haves → level fit → salary fit.
- For roles that pass the filters, run `fetch_ats.py detail --ats <ats> --token <board> --id <id>` to get the full description, original publish date and pay. Read the descriptions; do not rank on titles alone.
- Label each match **Strong**, **Good** or **Stretch**. Do not invent percentage scores.

### Step 4: Check they are live

The `detail` call reads the company's own job system at that moment, so a closed or removed role returns "not found": drop it. For any role the person picks to research or tailor for, also open the posting link (WebFetch, or a browser if available) and confirm the title and company match and applications are open. If a check fails, drop the role and say so. Never guess a corrected link.

**Remote vetting (every role that says remote, hybrid-remote or anywhere).** "Remote" is not a location. Read the posting description and location text and record the scope: remote anywhere / remote within a country or region / remote within a time zone / remote but must live near an office or hub / hybrid with office days. Look for phrases like "must be located in", "authorized to work in", "US only", "EMEA", "within X hours of", and payroll or entity limits. Compare to the person's location and work authorization. Show the verified scope on the card (for example "Remote (US only)"). If the posting does not say, show ⚠️ Remote scope not stated and do not rank it as a fit for someone outside the likely region. A role that fails the person's region is dropped and counted.

### Step 5: Show the shortlist

Up to 10 roles, best first, plus (beginners) up to 3 labelled **Stretch**. Format:

```
1. [Title] @ [Company] →
   [link]
   [Location, with verified remote scope] | [Level] | [Salary as posted, or ⚠️ Salary not listed] | [N days since posted, or ⚠️ Posted date not found]
   Fit: Strong. Why: [one sentence tied to their evidence]. Gap: [the main thing missing, or "none seen"]
```

- Salary only as posted; never estimate it. Days posted from the original publish date, not a renewed date.
- Single ⚠️ flag for anything missing or uncertain.
- Save the full list to `gtm-jobs-YYYY-MM-DD.md` in the current folder and say where it is.
- If fewer than three roles pass, say so plainly, show the nearest few, and name the one constraint that most limited the results (usually location or level). Ask which to relax. Do not pad.
- Then ask which up to three to research.

### Step 6: Research the companies they pick

Follow `references/company-research.md`: a momentum scorecard using TrueUp's variables (trajectory, valuation, funding, last round, headcount growth, open jobs and GTM trend, layoffs) plus every public source (newsroom, SEC filings for public companies, news, layoffs trackers). Every claim linked, "not found" where nothing is found, and one label: Momentum Rising / Steady / Cooling / Unclear, with evidence.

Then ask which single role to tailor the resume for.

### Step 7: Tailor the resume

Load the `gtm-resume-tailor` skill and pass it: the profile card, the resume, and the verified posting text from `detail`. It classifies the role, maps their real evidence, flags gaps, and rebuilds the resume; it builds the final file only after they confirm.

**No resume yet (common for beginners):** ask 6 short questions (roles or projects, tools used, one result with a number, education or courses, links, what they want to be hired as) and draft a plain baseline resume using only what they said. Show it, let them correct it, then tailor. Never add a fact they did not give.

### Step 8: Wrap up

Say what was produced and where the files are, in two sentences. Offer one next step. Update `~/.gtm-job-search/profile.md` with the date of this run. If files do not persist here, end with the profile card as a short text block and tell them to paste it next time.

---

## Honesty rules

- No invented facts: not on the resume, not in a dossier, not in a fit judgement.
- No guessed links, salaries, dates or headcounts. Missing means ⚠️ and a plain note.
- Say how fresh the data is: the company pool was built 2026-10-19; role data is read live on each run.
- Never submit applications, send messages, or enter personal data into any site.
- If asked to forget them, delete `~/.gtm-job-search/profile.md` and confirm.

---

## Outputs

- `~/.gtm-job-search/profile.md`, `company-cache.json`, `overrides.json`, `last-scan-w1.json`, `last-scan-w2.json` (local state).
- `gtm-jobs-YYYY-MM-DD.md` (the shortlist) in the working folder.
- A tailored resume file (.docx or .pdf) after confirmation, produced by `gtm-resume-tailor`. In a chat without file creation, the resume text is shown in the reply.

---

## Verification

- Onboarding covered all five questions, and the target role and responsibilities were confirmed with the user.
- Wave 1 was searched before wave 2, and wave 3 results are labelled outside the pool.
- Every shown role was read from the company's own job system in this run and its link is a unique company-hosted posting.
- Salary, dates and company figures are as sourced or flagged ⚠️.
- Roles below the stated salary minimum were excluded, not shown.
- Mode (beginner / standard / veteran) matched the stated seniority.

---

## Do Not Use For

- Roles outside GTM and marketing engineering (for example software engineering or finance).
- Applying, outreach, or interview coaching.
- Searching outside GTM and marketing engineering. Companies outside the pool are fine (wave 3) but must be labelled.
