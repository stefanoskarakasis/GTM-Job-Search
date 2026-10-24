A clearer shortlist and an honest reality check, without changing what gets searched.

## What changed
- **Scannable cards:** every role has the same lines in the same order: verdict, apply link, location, level, pay, days since posted, momentum, why it matches, gap, next move. A quick-glance table sits on top when there are 3 or more roles.
- **Verdicts first:** ⭐ Strong, 🟢 Good or 🟡 Stretch, each with a written rule. One closed set of emoji, one meaning each.
- **Proof check in onboarding:** two option questions on what you built (built, ran or inherited it; does it act on data). Verdicts are capped at 🟡 Stretch with thin proof and 🟢 Good with partial proof, and the shortlist says so.
- **Before you apply:** a fixed block with up to 3 Do steps (with time estimates), up to 4 Don'ts and what to ask in the screen. No generic advice.
- **Quick momentum on every card:** a Rising, Steady, Cooling or Unclear read on up to 5 cards, then the full scorecard for the 3 you pick.
- **Stale postings flagged:** anything older than 180 days gets a ⚠️ and a question to ask.
- **Your numbers are respected:** ask for "3 companies" and you get 3 cards, one per company. The shortlist ends on one question.
- **Honest levels:** level, pay and dates are shown only as posted. "Level not stated" replaces a guess.
- **Five cards in chat, everything in the file:** you get the top 5 as full cards plus a quick-glance table of every role (up to 10). The saved `gtm-jobs-YYYY-MM-DD.md` holds every card. Ask for a number and you get exactly that many.
- **Ordered by verdict, then momentum, then newer posting.** Momentum is read for the top 5 first, so the order is never circular.
- **Cleaner hand-off to the resume tailor:** the tailor now receives your proof grade, the full posting text, the card's gap and flags. It no longer asks what you already answered, never labels a side project "Shipped", never pads must-haves the posting does not state, and shows the posting's level as stated or "not stated". `gtm-resume-tailor` is 1.1.0.
- **Fixes found on live postings:** Lever postings lost their requirement lists and workplace type; an impossible pay line ("$120/year to $250/year") is now quoted with a "looks like a typo" flag and a question to ask; an unstated work arrangement shows as a flag instead of a blank.
- **Fixes found by running it end to end on a real resume:** Greenhouse postings keep their pay range in the description, so roles with a posted range were shown as "Salary not listed" (the scan now returns `pay_in_text`); Greenhouse text arrived HTML-escaped; roles in the same verdict were ordered by recency alone, which put the far-off roles first (must-haves with evidence now break the tie); proof named in chat that is not on the resume stays unconfirmed until you say where it appears; the tailor no longer invents months for year-only dates, flags claims it cannot check, and says plainly when a core must-have has no evidence.

## Upgrading
Saved v1.0 profile cards have no proof grade. The skill asks the two proof questions once, then continues.
