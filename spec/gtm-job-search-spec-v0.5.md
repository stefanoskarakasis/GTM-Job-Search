# GTM Job Search: Spec v0.5 (draft)

Date: 2026-10-19. Supersedes v0.4. Repo: github.com/stefanoskarakasis/GTM-Job-Search (build steps in docs/BUILD-GUIDE.md).

## What changed in v0.5
- Renamed: plugin `gtm-job-search`, marketplace `stefanos-gtm`, command `/gtm-job-search:find-my-job`, local state `~/.gtm-job-search/`.
- Company pool rebuilt from plain-text lists (`data/sources/*.txt`) by `scripts/build_pool.py`: 289 companies, wave 1 (default) = 120, wave 2 (wider) = 169. Sources: marketingengineer.jobs, GTM Jobs substack issues #03-#05, gtm-jobs-tracker tiers and lists, skills.marketing, adamgtm.com (partial), TrueUp marketing-and-growth top 20.
- Search order: wave 1, wave 2, then wave 3 open-web `site:` sweeps (Ashby, Greenhouse, Lever), labelled outside the pool. Company's own hiring site always first.
- Onboarding: five questions (target role, responsibilities, seniority and proof, location and authorization, salary band).
- Company research: momentum scorecard from TrueUp variables plus public sources, one label (Rising/Steady/Cooling/Unclear).
- Still no connectors.

## Measured 2026-10-19
Wave 1: 400 matching roles at 79 of 120 companies (41 unresolved). Wave 2: 143 roles at 71 of 169 (98 unresolved). The default keywords are broad (for example "Senior Sales Operations Lead" matched); ranking must read descriptions, and the keyword set should be tightened per target role.

## Open
- D2 token cost owner for a web app. D3 persist weekly verified roles. Free tailor vs paid hs-pmm-resume overlap.
- Seven tailoring profiles unvalidated. No end-to-end onboarding transcript run yet.
- GTM Jobs #01/#02 unreadable; adamgtm directory partially read (~110 of 868); TrueUp cannot isolate marketing-engineering titles; 10 names unconfirmed (verify_name).
