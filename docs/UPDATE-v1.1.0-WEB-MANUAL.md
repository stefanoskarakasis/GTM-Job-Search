# Update the repo to v1.1.0, using only the GitHub website

For someone who has never used GitHub. No terminal, no Git, no installs. About 25 minutes. You upload 15 ready-made files in one go, change one line by hand, check the result, and publish.

**What you need:** your GitHub login, a browser (Chrome, Edge or Firefox; avoid Safari for uploads), and the file `gtm-job-search-v1.1.0-update.zip`.

**Words you will see.** Repo: the project on GitHub. Commit: save a change. Branch: a safe copy of the project where you try the change first. `main` is the live version. Pull request (PR): GitHub's "review this change before it goes live" page. Merge: make the change live. Release: the page where people download the two Claude app zips.

## The plan in 8 lines

1. Check nothing changed on GitHub since this bundle was made.
2. Unzip the bundle.
3. Upload all 15 files to a new branch in one drag.
4. Open a pull request.
5. Change one line in `plugin.json`.
6. Check the pull request shows 16 changed files.
7. Merge.
8. Publish a Release with the two zips attached. (Skip this and the Claude app download links keep serving the old version.)

Nothing you do before step 7 touches the live version. You can stop at any point and nothing is lost.

---

## Part 1. Safety check (2 min)

1. Open `https://github.com/stefanoskarakasis/gtm-job-search`.
2. Look at the latest commit line above the file list (just under the branch button). It should say **Update CHANGELOG.md**. Click the clock icon with a number (for example "12 Commits") and check that the top commit ends in `914591b`.
3. If the top commit is different, **stop**. Someone, possibly you, changed the repo after the bundle was made, and uploading would overwrite those changes. Send the new commit name to Claude and ask for a fresh bundle.

## Part 2. Get the files ready (3 min)

1. Find `gtm-job-search-v1.1.0-update.zip` (usually in Downloads) and unzip it. Mac: double-click it. Windows: right-click, **Extract All**, **Extract**.
2. Open the new folder `gtm-job-search-v1.1.0-update`. You should see exactly 6 items:
   `CHANGELOG.md`, `README.md`, `dist`, `docs`, `plugins`, `tests`
3. Open `dist`. You should see two **zip files**: `find-my-job.zip` and `gtm-resume-tailor.zip`. **Do not unzip these two.** They upload as zips.
4. Ignore any `__MACOSX` folder or `.DS_Store` file. Never upload those.

## Part 3. Upload all 15 files in one go (5 min)

1. On the repo page click **Add file**, then **Upload files**.
2. Open the unzipped folder `gtm-job-search-v1.1.0-update` in a window next to the browser.
3. **Open the folder first**, then select the 6 items **inside** it (Cmd+A on Mac, Ctrl+A on Windows). Do not drag the folder itself.
4. Drag the selection onto the box that says **Drag files here to add them to your repository**.
5. Wait until every progress bar is finished. GitHub lists the files it will add.
6. **Check the list.** You should see 15 files, and every path should start with `CHANGELOG.md`, `README.md`, `dist/`, `docs/`, `plugins/` or `tests/`.
   - If the paths start with `gtm-job-search-v1.1.0-update/`, you dragged the folder instead of its contents. Reload the page and redo step 3 from the inside.
   - If you see more than 15 files, remove the extras with the small **x** next to them.
   - If you see fewer than 15, use the table in Part 8 to find which are missing and add them by dragging them in.
7. Scroll to **Commit changes**.
   - Commit message: `Update to v1.1.0`
   - Select **Create a new branch for this commit and start a pull request**.
   - Branch name: type exactly `v1.1.0`
8. Click **Propose changes**.
9. On the next page ("Open a pull request") leave the title as it is and click **Create pull request**.

## Part 4. Change the one line you cannot upload (3 min)

`plugin.json` sits in a hidden folder (`.claude-plugin`), so you edit it by hand instead of uploading it.

1. On your pull request page, find the line "stefanoskarakasis wants to merge 1 commit into **main** from **v1.1.0**". Click the blue **v1.1.0**. This opens the project as it looks on your new branch.
2. Click into `plugins`, then `gtm-job-search`, then `.claude-plugin`, then `plugin.json`.
3. Click the **pencil** icon at the top right of the file.
4. Line 3 says `"version": "1.0.0",`. Change **only** `1.0.0` to `1.1.0`. It must read exactly: `"version": "1.1.0",`. Keep the quote marks and the comma.
5. Click **Commit changes...** at the top right. In the box, keep **Commit directly to the v1.1.0 branch** selected. Click **Commit changes**.

## Part 5. Check the pull request (4 min)

1. Go back to the pull request (the **Pull requests** tab, then click it).
2. Click **Files changed**. The top should say **16 files changed**.
3. Open the table in Part 8. The list must match: every path in it appears, and nothing else.
4. Click the file `plugins/gtm-job-search/.claude-plugin/plugin.json` in the list. You should see one red line (`1.0.0`) and one green line (`1.1.0`) and nothing else.
5. If the number is not 16, go to Part 9.

## Part 6. Merge (1 min)

1. Back on the **Conversation** tab, scroll down and click **Merge pull request**, then **Confirm merge**.
2. Click **Delete branch** if GitHub offers it. That is safe.
3. Go to the repo's main page. Read the top of the README. It should say the shortlist shows the top 5 as full cards. If you still see the old text, wait a minute and press Ctrl+F5 (Cmd+Shift+R on Mac).

## Part 7. Publish the Release (5 min)

The README download links point at the latest Release. Until you do this, the Claude app users get the old zips.

1. On the repo page click **Releases** (right side), then **Draft a new release**.
2. Click **Choose a tag**, type `v1.1.0`, and click **Create new tag: v1.1.0 on publish**. Leave **Target** on `main`.
3. **Release title:** `v1.1.0: Easier to scan, harder to fool yourself`
4. **Description:** open `docs/RELEASE-v1.1.0.md` in another tab, click the **Copy raw file** icon (two squares, top right of the file), and paste into the description box.
5. Drag the two zip files from the `dist` folder on your computer into the box that says **Attach binaries by dropping them here**: `find-my-job.zip` and `gtm-resume-tailor.zip`. Wait for both to finish.
6. Make sure **Set as the latest release** is ticked.
7. Click **Publish release**.
8. Test the links. Open these two addresses in the browser. Each should download a zip: `https://github.com/stefanoskarakasis/GTM-Job-Search/releases/latest/download/find-my-job.zip` (about 32 KB) and `.../gtm-resume-tailor.zip` (about 10 KB).

## Part 8. What should now be in the repo

These 16 files are the only ones that change. Open any of them on GitHub and look for the check in the right column.

| File | Check |
|---|---|
| `CHANGELOG.md` | First heading is `v1.1.0 (2026-10-24): Easier to scan, harder to fool yourself` |
| `README.md` | Contains the sentence "the top 5 as full cards in chat" |
| `dist/find-my-job.zip` | About 32 KB |
| `dist/gtm-resume-tailor.zip` | About 10 KB |
| `docs/BUILD-GUIDE.md` | Mentions "the proof check" |
| `docs/CUSTOMIZING.md` | Has a row "How many cards in chat" |
| `docs/RELEASE-v1.1.0.md` | New file: the release text |
| `docs/UPDATE-v1.1.0-WEB-MANUAL.md` | New file: this manual |
| `plugins/gtm-job-search/.claude-plugin/plugin.json` | Line 3 reads `"version": "1.1.0",` (the one you edited) |
| `plugins/gtm-job-search/agents/gtm-job-search.md` | Mentions "then the proof check" |
| `plugins/gtm-job-search/scripts/fetch_ats.py` | Use Ctrl+F in the file for `pay_in_text`: it is found |
| `plugins/gtm-job-search/skills/find-my-job/SKILL.md` | Line 3 reads `version: 1.1.0` |
| `plugins/gtm-job-search/skills/find-my-job/references/company-research.md` | Contains "today's count only" |
| `plugins/gtm-job-search/skills/gtm-resume-tailor/SKILL.md` | Line 3 reads `version: 1.1.0` |
| `tests/run_checks.sh` | Contains "hand-off contract" |
| `tests/check_handoff.py` | New file |

## Part 9. If something looks wrong

| What you see | What it means | Fix |
|---|---|---|
| Paths in the upload list start with `gtm-job-search-v1.1.0-update/` | You dragged the folder, not what is inside | Reload the page, redo Part 3 from step 3 |
| Pull request says more than 16 files | An extra file got in (often `.DS_Store`) | In **Files changed**, open the extra file, click the **...** menu, **Delete file**, commit to branch `v1.1.0` |
| Pull request says fewer than 16 files | A file was skipped | Switch to branch `v1.1.0` (branch button), **Add file**, **Upload files**, drag only the missing file with its folder, commit to branch `v1.1.0` |
| Red message "This branch has conflicts" | The repo changed after the bundle was made | Do not merge. Send a screenshot to Claude and ask for a fresh bundle |
| Red mark in the editor on `plugin.json` | A quote or comma got deleted | Press Esc, **Cancel changes**, and redo Part 4 |
| Merged by mistake, or the result looks wrong | Your old version is still saved | Open the merged pull request, click **Revert**, then **Create pull request**, then merge that. Everything returns to the old version |
| Release download is 404 | The release was not published, or the tag is wrong | Open **Releases**; if it says Draft, click **Edit**, then **Publish release** |
| Upload box does not accept folders | Your browser blocks folder drops (some Safari versions) | Switch to Chrome, Edge or Firefox |

## Part 10. After you are done

- Tell Claude "merged and released". It can then re-read the live repo and confirm the 16 files match.
- Optional: users who installed with Claude Code update with `claude plugin update gtm-job-search@stefanos-gtm`.
- Optional housekeeping: `docs/GITHUB-WEB-MANUAL.md` is the original first-time setup guide and still says 32 files. It is not wrong for a fresh install, just old.

## What this release changes

- The shortlist shows the top 5 as full cards, a table of every role, and a saved file with all of them.
- Verdicts are capped by a proof check, and the Before you apply block carries the honest message when no role is a Strong or Good match.
- Pay posted in the description is no longer shown as "Salary not listed".
- The resume tailor receives your proof grade and the posting text, and never invents months, tools or numbers.
- Momentum shows funding, layoffs and headcount only. There is no open-role trend.
