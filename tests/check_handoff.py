#!/usr/bin/env python3
"""Hand-off contract check: what find-my-job passes to gtm-resume-tailor must be what the tailor needs.
Run from the repo root: python3 tests/check_handoff.py"""
import re, sys
P = "plugins/gtm-job-search/skills/"
fm = open(P + "find-my-job/SKILL.md").read()
tl = open(P + "gtm-resume-tailor/SKILL.md").read()
step7 = fm[fm.index("### Step 7"):fm.index("### Step 8")]
fields = {  # field passed in Step 7 -> phrase the tailor must consume
    "proof check answers and the proof grade": "proof check",
    "full text from `detail`": "full text of one verified-live posting",
    "verdict, the 🚧 Gap": "verdict, main gap, and flags",
    "stale posting, level not stated, pay problem": "stale, level not stated, pay problem",
}
rules = {  # behaviour the tailor must state
    "evidence capped by proof": r"side project only or inherited, nothing is Shipped",
    "posting level never inferred": r"Never infer it from the title",
    "no padded must-haves": r"do not pad",
    "stale posting stops and asks": r"older than 180 days",
    "unreadable posting stops": r"stop if it still cannot be read",
    "no duplicate gap questions": r"not asked again",
    "table-only role is live-checked first": r"only in the table",
    "never invent a month": r"never invent a month",
    "unverifiable claims flagged": r"flagged and left out until the person confirms",
    "unprovable core must-have said plainly": r"does not prove \[must-have\]",
    "unconfirmed proof does not count": r"stays \*\*unconfirmed\*\*",
}
bad = []
for a, b in fields.items():
    if a not in step7: bad.append(f"find-my-job Step 7 does not pass: {a}")
    if b not in tl: bad.append(f"tailor does not consume: {b}")
for name, rx in rules.items():
    if not re.search(rx, tl + fm): bad.append(f"missing rule: {name}")
if "GTM Job Finder" in tl: bad.append("stale product name in tailor")
m = re.search(r"^version: (\S+)", tl, re.M)
print("tailor version", m.group(1) if m else "?")
for x in bad: print("FAIL ", x)
print("PASS hand-off contract" if not bad else f"{len(bad)} problems")
sys.exit(1 if bad else 0)
