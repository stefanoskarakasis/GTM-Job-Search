# Company research: momentum scorecard

Run for each company the person picks (max 3 per round). Every figure carries a source link and the date it was read. "Not found" is a valid value. One authoritative source per figure; never add rounds together yourself. Round dollar amounts to whole M or B. No logins, no LinkedIn scraping, no paid databases.

## Variables (modelled on what TrueUp tracks)

| Variable | Where to look |
|---|---|
| Trajectory / rank | `trueup.io/co/<slug>` if it loads. Fall back to web search "<company> trueup" if the slug fails. Read only pages for roles the person picked. |
| Valuation | Company or press release; public Crunchbase/PitchBook page; TrueUp |
| Total funding | One source only |
| Last round: type, amount, date, lead investor | Company newsroom, press release, TrueUp |
| Headcount and 12-month employee growth | TrueUp, company page; if only a size band is found, say band |
| Open jobs: total, marketing/growth/GTM count (today's count only) | Our own scan (`fetch_ats.py`) or the company's job feed, plus the careers page. No trend is reported: there is no reliable earlier count to compare against |
| Role open since | Posting's original publish date from `detail` |
| Layoffs | TrueUp layoffs page, layoffs.fyi, WARN notices, news search, "Employee reported" items |
| Leadership changes | News search, company newsroom |
| Public companies | Latest earnings release and SEC filings (10-K, 10-Q) for growth, guidance, restructuring |
| Rankings and culture | Public lists only (e.g. TrueUp rankings), labelled with the source |
| Last 90 days | Raises, launches, layoffs, exec departures, acquisitions |

Plus: competitors and how the company positions itself (company site, one or two competitor pages).

## Verdict
Label exactly one: **Momentum: Rising / Steady / Cooling / Unclear**, followed by two or three evidence bullets that justify it.
- Rising: recent raise or revenue growth, headcount up, no recent layoffs. The open-role count is context, never evidence of direction.
- Steady: stable headcount and funding, nothing alarming.
- Cooling: layoffs, hiring freezes, funding more than 3 years old with no news, leadership churn. Flag ⚠️ if last raise is older than 3 years.
- Unclear: not enough public evidence. Say so; do not guess.

## Output per company
```
[Company]: Momentum: [label]
Stage / total funding / last round (date, lead) / valuation: [values or "not found"]
Headcount (growth 12 mo): [..]
Open roles: [N total, N GTM-type] | This role open since: [date]
Layoffs / leadership: [..]
Last 90 days: [..]
Competitors / positioning: [..]
Three things to know before a first call: 1) .. 2) .. 3) ..
Sources: [links, with date read]
```
Note any variable that conflicts between sources and name both rather than picking one silently.
