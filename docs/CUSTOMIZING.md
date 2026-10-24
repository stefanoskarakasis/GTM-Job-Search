# Customizing GTM Job Search

Everything here is a plain text or small Python file. After you change a file in the repo, bump `version` in `plugins/gtm-job-search/.claude-plugin/plugin.json` and commit; users get it with `claude plugin update gtm-job-search@stefanos-gtm`. To change only your own copy, edit the files in the installed plugin folder or fork the repo and install your fork.

## 1. Customize the scoring (how roles are ranked)

Ranking is written in plain language in `plugins/gtm-job-search/skills/find-my-job/SKILL.md`, Step 3 ("Filter and rank"). Claude follows it as instructions, so changing the words changes the behavior.

| What you want to change | Where | How |
|---|---|---|
| Hard filters (location, level, salary) | SKILL.md, Step 3, "Hard filters" | Edit the rules. Example: allow two levels above target for everyone, or never drop a role for salary. |
| What counts most in fit | SKILL.md, Step 3, "Fit, in order of weight" | Reorder or add a factor. Default order: position-type match, skills and evidence against the posting's must-haves, level fit, salary fit. |
| Labels | SKILL.md, Step 3 | Default is ⭐ Strong, 🟢 Good, 🟡 Stretch, with rules for each. There are no percentage scores on purpose. |
| Proof cap | SKILL.md, Step 3, "Proof cap", and Step 1, "Proof check" | A Thin proof grade caps verdicts at 🟡 and Partial at 🟢. Edit the grades or the caps. |
| Shortlist card layout and emoji | SKILL.md, Step 5 | Fixed field order and a closed emoji set. If you add or change an emoji, update the closed-set line so each emoji keeps one meaning. |
| How many cards in chat | SKILL.md, Step 5, "How many" | Default is 5 full cards plus a table of every role; the saved file holds all cards. Change the 5, or the table cap of 10. |
| What the tailor receives | SKILL.md, Step 7, and `skills/gtm-resume-tailor/SKILL.md`, Inputs | The hand-off packet: profile card with proof grade, resume, full posting text, verdict, gap and flags. `tests/check_handoff.py` fails if the two skills drift apart. |
| Remote vetting | SKILL.md, Step 4, "Remote vetting" | Edit which phrases and scopes it looks for. |
| Which titles are scanned per target role | SKILL.md, Step 2, the per-role keyword list | Each entry is a regex passed to `fetch_ats.py scan --keywords`. Add or remove title words. |
| What each position type is, and what proof it needs | `skills/gtm-resume-tailor/references/position-types.md` | Edit signal words, hiring lens, lead metrics and red flags per type. |
| Which responsibilities people can pick in onboarding | `skills/find-my-job/references/responsibilities.md` | Edit the want/avoid menus. |
| What the company momentum verdict is based on | `skills/find-my-job/references/company-research.md` | Edit the variables, sources and the Rising / Steady / Cooling / Unclear rules. |

Keep the honesty rules in SKILL.md (no invented facts, no estimated salary, no guessed links). Everything else is yours to tune. After changing keywords, test with:

```bash
python3 plugins/gtm-job-search/scripts/fetch_ats.py scan \
  --universe plugins/gtm-job-search/data/company-universe.json \
  --wave 1 --keywords "your|regex|here" --out /tmp/test.json
```

## 2. Add a job board for one company

If a company's job board was not found automatically, tell the scanner where it is. Create or edit `~/.gtm-job-search/overrides.json` on your machine:

```json
{ "Company Name": { "ats": "greenhouse", "token": "board-name" } }
```

- `ats` is `greenhouse`, `lever` or `ashby`.
- `token` is the board name in the company's job-board address, for example `jobs.ashbyhq.com/<token>`, `boards.greenhouse.io/<token>` or `jobs.lever.co/<token>`.
- Test it: `python3 plugins/gtm-job-search/scripts/fetch_ats.py resolve "Company Name"`.

To ship the fix to everyone, ask for the mapping to be added to the repo instead of each person's `overrides.json`.

## 3. Add companies to the pool

1. Open `plugins/gtm-job-search/data/sources/` and edit one of the lists, or add a new `.txt` file. One company per line, `#` starts a comment, a trailing `?` means the name is not confirmed, and `Name | size band | listings` is optional.
2. For a new list file, add one line to `SOURCES` in `plugins/gtm-job-search/scripts/build_pool.py`: file name, a source tag, and a priority. Priority 0-2 puts a company in the default pool (searched first). Priority 3 and up puts it in the wider pool.
3. If two lists spell a company differently, add `Alias = Canonical Name` to `data/sources/aliases.txt`.
4. Rebuild: `python3 plugins/gtm-job-search/scripts/build_pool.py`. Commit the updated `company-universe.json` together with your list.
5. Run `bash tests/run_checks.sh`.

## 4. Add a job-board system the scanner does not read yet

The scanner reads Greenhouse, Lever and Ashby. To add another system that publishes a public JSON feed:

1. Add a `fetch_<system>(token)` function in `plugins/gtm-job-search/scripts/fetch_ats.py` that returns a list of `{id, title, location, url, posted, updated}`, or `None` if the board does not exist.
2. Register it in the `FETCHERS` dictionary and add the system name to the `choices` of the `detail --ats` option, with a matching branch in `cmd_detail`.
3. Test it live on three companies before trusting it. Workable, SmartRecruiters and Recruitee were tried and not added because their public feeds did not return reliable results.

For systems with no public feed (Workday, custom career pages), no code is needed. The assistant reads those pages through web search and the page itself.

## 5. Add an open-web search source

The third search wave uses site-restricted web searches. To add one, edit the "Wave 3" item in SKILL.md, Step 2, and add a line such as `site:jobs.workable.com "<target title>"`. Results found this way are always labelled "outside the pool", and the assistant still has to reach the company's own posting before showing a link. Aggregators stay leads, never the link.
