#!/usr/bin/env bash
# Pre-release checks. Run from the repo root: bash tests/run_checks.sh
# Needs: claude CLI, python3, network (the last check reads three public job feeds).
set -u
fail=0
ok(){ echo "PASS  $1"; }
bad(){ echo "FAIL  $1"; fail=1; }
P=plugins/gtm-job-search

claude plugin validate ./$P >/dev/null 2>&1 && ok "plugin manifest validates" || bad "plugin manifest validates"
claude plugin validate .   >/dev/null 2>&1 && ok "marketplace manifest validates" || bad "marketplace manifest validates"
python3 -m py_compile $P/scripts/fetch_ats.py $P/scripts/build_pool.py && ok "scripts compile" || bad "scripts compile"

before=$(md5sum $P/data/company-universe.json | cut -d' ' -f1)
python3 $P/scripts/build_pool.py >/dev/null
after=$(md5sum $P/data/company-universe.json | cut -d' ' -f1)
[ "$before" = "$after" ] && ok "pool file is up to date with data/sources" || bad "pool file was stale (rebuilt: commit it)"

python3 - <<PY && ok "pool sanity (unique names, both waves present, no empty names)" || bad "pool sanity"
import json,re,sys
c=json.load(open("$P/data/company-universe.json"))["companies"]
keys=[re.sub(r"[^a-z0-9]","",x["name"].lower()) for x in c]
assert len(keys)==len(set(keys)), "duplicate company"
assert all(x["name"].strip() for x in c)
assert {x["wave"] for x in c}=={1,2}
PY

for f in $P/skills/*/SKILL.md; do
  n=$(wc -l < "$f"); [ "$n" -le 500 ] && ok "$f under 500 lines ($n)" || bad "$f over 500 lines"
done
python3 - <<PY && ok "skill descriptions <= 1024 chars" || bad "skill description too long"
import re,glob
for f in glob.glob("$P/skills/*/SKILL.md"):
    m=re.search(r"description:\s*>?\s*\n?(.*?)\n[a-z_]+:",open(f).read(),re.S)
    assert len(re.sub(r"\s+"," ",m.group(1)))<=1024,f
PY

python3 - <<PY && ok "skill descriptions <= 200 chars (Claude app upload limit)" || bad "skill description over 200 chars"
import re,glob
for f in glob.glob("$P/skills/*/SKILL.md"):
    d=re.search(r"description: (.*)\n",open(f).read()).group(1)
    assert len(d)<=200,(f,len(d))
PY

bash tests/build_dist.sh >/dev/null
for z in find-my-job gtm-resume-tailor; do
  unzip -Z1 dist/$z.zip | grep -q "^$z/SKILL.md$" && ok "dist/$z.zip has $z/SKILL.md at its root folder" || bad "dist/$z.zip layout"
done
unzip -Z1 dist/find-my-job.zip | grep -q "^find-my-job/scripts/fetch_ats.py$" && unzip -Z1 dist/find-my-job.zip | grep -q "^find-my-job/data/company-universe.json$" && ok "find-my-job.zip bundles scripts and data" || bad "find-my-job.zip missing scripts or data"

grep -rIn "gtm-job-finder\|\.gtm-job-finder" . --exclude-dir=.git --exclude-dir=tests >/dev/null && bad "stale 'gtm-job-finder' names found" || ok "no stale names"

export HOME=$(mktemp -d)
python3 $P/scripts/fetch_ats.py scan --universe $P/data/company-universe.json --only "Clay,Profound,Stripe" --out $HOME/s.json 2>&1 | tail -1
python3 - <<PY && ok "live smoke scan resolves >=2 of Clay/Profound/Stripe" || bad "live smoke scan"
import json
d=json.load(open("$HOME/s.json"))["summary"]
assert d["resolved_to_feed"]>=2, d
PY
python3 $P/scripts/fetch_ats.py scan --universe $P/data/company-universe.json --keywords "(" 2>&1 | grep -q "invalid --keywords" && ok "bad regex is a clean error" || bad "bad regex handling"
exit $fail
