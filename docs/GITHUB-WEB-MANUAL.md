# Roll out GTM-Job-Search on GitHub, by hand (v2)

For someone who has never used GitHub. No terminal and no Git until the final test. About 30 minutes. At the end, anyone can install your plugin with one command.

**What you need:** a free GitHub account (github.com/signup), the 32 repo files (as `GTM-Job-Search.zip` or the single files), and Chrome, Edge, Firefox or Safari.

**Words you will see.** Repository (repo): a project folder on GitHub. Commit: save a change. Public: anyone can see it. It must be public or the install command fails for everyone else.

## The whole job in 7 lines

1. Unzip. Turn on hidden files.
2. Create an empty public repo named `GTM-Job-Search`.
3. Drag all 32 files in (hidden folders included).
4. Commit.
5. Check the file list against the table below.
6. Add the description and topics.
7. Test the install.

## Part 1. Get the files ready (5 min)

1. Find `GTM-Job-Search.zip` (usually Downloads) and unzip it. Mac: double-click. Windows: right-click, Extract All. You get a folder `GTM-Job-Search`.
2. **Show hidden files.** Two folders are named `.claude-plugin`. Names that start with a dot are hidden by default.
   - Mac: open the folder in Finder, press **Cmd + Shift + .** (period). Hidden items appear greyed.
   - Windows: in File Explorer click **View**, then **Show**, then **Hidden items**.
3. Open `GTM-Job-Search`. You should see: `.claude-plugin`, `README.md`, `docs`, `plugins`, `spec`, `tests`. If `.claude-plugin` is missing, redo step 2.
4. Open `plugins`, then `gtm-job-search`. You should see another `.claude-plugin`, plus `agents`, `data`, `scripts`, `skills`.
5. Ignore any `__MACOSX` folder or `.DS_Store` file. Never upload those.

## Part 2. Create the empty repo (3 min)

1. Sign in at github.com. Click the **+** at the top right, then **New repository**.
2. **Repository name:** type exactly `GTM-Job-Search`.
3. **Description:** paste this (237 characters):

```
Claude skills that find roles matched to you, confirm they're live and truly open where you live, research each company's momentum, and tailor your resume to the one you pick. Works in the Claude app, Cowork and Claude Code. No API keys.
```

4. Choose **Public**.
5. Leave every checkbox unticked: no README, no .gitignore, no license.
6. Click **Create repository**.
7. On the next page click the small link **uploading an existing file**. If you cannot find it, click **Add file**, then **Upload files**.

## Part 3. Upload everything (8 min)

1. Open the unzipped `GTM-Job-Search` folder (with hidden files shown) next to the GitHub page.
2. Select everything inside it: Cmd+A (Mac) or Ctrl+A (Windows). That is 6 items: `.claude-plugin`, `README.md`, `docs`, `plugins`, `spec`, `tests`.
3. Drag the selection onto the box that says "Drag files here". Folders keep their structure.
4. Wait for every progress bar to finish. GitHub shows the list of files it will add. **Count them: 32.** If you see 30, the two hidden `.claude-plugin` files were skipped; add them in Part 4.
5. In **Commit changes**, type `Add plugin files`. Leave "Commit directly to the main branch" selected.
6. Click **Commit changes**.

If dragging folders does not work (some Safari versions): use **choose your files** and upload `README.md`, then go folder by folder. Or use the paste method in Part 4 for any file that is missing.

## Part 4. Only if the two hidden files are missing (5 min)

Check first: on your repo page, can you see `.claude-plugin/marketplace.json` and `plugins/gtm-job-search/.claude-plugin/plugin.json`? If yes, skip this part.

### Create `.claude-plugin/marketplace.json`

1. **Add file**, **Create new file**.
2. In the name box type `.claude-plugin/marketplace.json`. When you type the `/`, GitHub turns `.claude-plugin` into a folder.
3. Paste exactly:

```json
{
  "name": "stefanos-gtm",
  "description": "GTM and marketing-engineering career tools",
  "owner": {
    "name": "Stefanos Karakasis"
  },
  "plugins": [
    {
      "name": "gtm-job-search",
      "source": "./plugins/gtm-job-search",
      "description": "Find GTM and marketing-engineering jobs matched to you, check they are live, research the companies, and tailor your resume."
    }
  ]
}
```

4. Click **Commit changes...**, then **Commit changes**.

### Create `plugins/gtm-job-search/.claude-plugin/plugin.json`

1. **Add file**, **Create new file**.
2. Name box: `plugins/gtm-job-search/.claude-plugin/plugin.json`
3. Paste exactly:

```json
{
  "name": "gtm-job-search",
  "version": "1.0.0",
  "description": "Find GTM and marketing-engineering jobs matched to you, check they are live, research the companies, and tailor your resume. Works for beginners and 10+ year veterans.",
  "author": {
    "name": "Stefanos Karakasis"
  },
  "keywords": ["jobs", "gtm", "marketing-engineering", "resume", "careers"]
}
```

4. Commit the same way.

Paste, do not retype. Straight quotes only. A red mark in the editor means a comma or bracket changed; paste again.

## Part 5. Check the file list (5 min)

Open each folder on GitHub and match it to this table. All 32 must exist.

| Path | What it is |
|---|---|
| `.claude-plugin/marketplace.json` | Tells Claude Code this repo is a plugin marketplace |
| `README.md` | The front page people see |
| `docs/BUILD-GUIDE.md` | Maintainer guide |
| `docs/CUSTOMIZING.md` | Customizing scoring, job boards, companies |
| `docs/GITHUB-WEB-MANUAL.md` | This manual |
| `docs/REPO-DESCRIPTION.txt` | The About text |
| `plugins/gtm-job-search/.claude-plugin/plugin.json` | The plugin's name and version |
| `plugins/gtm-job-search/agents/gtm-job-search.md` | The dedicated assistant |
| `plugins/gtm-job-search/data/company-universe.json` | The generated company pool |
| `plugins/gtm-job-search/data/sources/*.txt` (11 files) | The lists the pool is built from |
| `plugins/gtm-job-search/scripts/build_pool.py` | Rebuilds the pool |
| `plugins/gtm-job-search/scripts/fetch_ats.py` | Reads company job feeds |
| `plugins/gtm-job-search/skills/find-my-job/SKILL.md` | The main flow |
| `plugins/gtm-job-search/skills/find-my-job/references/company-research.md` | Company scorecard |
| `plugins/gtm-job-search/skills/find-my-job/references/responsibilities.md` | Responsibility menus |
| `plugins/gtm-job-search/skills/gtm-resume-tailor/SKILL.md` | Resume tailoring |
| `plugins/gtm-job-search/skills/gtm-resume-tailor/references/position-types.md` | Eight role profiles |
| `spec/gtm-job-search-spec-v0.5.md` | Design spec |
| `tests/run_checks.sh` | Pre-release checks |
| `tests/build_dist.sh` | Builds the two upload zips |
| `dist/find-my-job.zip` | Skill upload for the Claude app, linked from the README |
| `dist/gtm-resume-tailor.zip` | Skill upload for the Claude app, linked from the README |

**Fix a missing file:** open its folder on GitHub, **Add file**, **Upload files**, drag it in, commit. If the folder does not exist, use **Create new file**, type the full path, paste the file's contents.

**Fix a file in the wrong place:** open it, click the trash icon, commit, then re-add it at the right path.

## Part 6. Polish the page (3 min)

1. On the main page, click the gear next to **About**.
2. Confirm the description is there. Add topics: `claude-code`, `claude-code-plugin`, `job-search`, `gtm`, `marketing-engineering`, `resume`. Save.
3. Optional but recommended: **Add file**, **Create new file**, name it `LICENSE`. GitHub shows **Choose a license template**; pick one (MIT is common), add your name, commit. Without a license nobody else has the legal right to reuse your code. This is your choice.

## Part 7. Test the install like a stranger (5 min)

This is the only step that needs a terminal. Claude Code must be installed, version 2.1.292 or later (`claude --version`).

1. Open Terminal (Mac: Cmd+Space, type Terminal) or PowerShell (Windows).
2. Run:

```
claude plugin install gtm-job-search --marketplace stefanoskarakasis/GTM-Job-Search
```

3. You should see "Successfully added marketplace" and "Successfully installed plugin".
4. Start `claude` and type `/gtm-job-search:find-my-job`. The first question asks which role you are going for.

### If it fails

| What you see | Cause | Fix |
|---|---|---|
| Marketplace not found or 404 | Repo is private, or the name is spelled differently | Repo Settings, Danger Zone, Change visibility to Public. Name must be exactly `GTM-Job-Search` |
| Marketplace file invalid | `.claude-plugin/marketplace.json` missing or mistyped | Compare with Part 4, fix with the pencil icon, commit |
| Plugin not found | `plugins/gtm-job-search/.claude-plugin/plugin.json` missing, or a folder misspelled | Check Part 5 paths |
| `/gtm-job-search:find-my-job` not listed | Install unfinished or needs restart | Quit and reopen `claude`, run `/plugin` to see what is installed |
| `claude: command not found` | Claude Code is not installed | Install it from docs.claude.com |

## Part 8. Change things later, by hand

- **Edit a file:** open it on GitHub, click the pencil, change, **Commit changes**.
- **Add a company:** edit the right `.txt` in `plugins/gtm-job-search/data/sources/`. `company-universe.json` is generated by a script (needs Python, see `docs/BUILD-GUIDE.md` section 5), so new names are not searched until you rebuild it.
- **Release an update:** change `"version": "1.0.0"` to `"1.1.0"` in `plugin.json` and commit. Users update with `claude plugin update gtm-job-search@stefanos-gtm`.

## Before you announce it

- Run one onboarding conversation yourself from a clean install.
- Have one beginner and one experienced marketing engineer run it too.
- Decide on a license.
