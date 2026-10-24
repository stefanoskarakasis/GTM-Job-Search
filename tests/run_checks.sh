#!/usr/bin/env bash
# Pre-release checks. Run from the repo root: bash tests/run_checks.sh
# Needs: claude CLI, python3, network (the last check reads three public job feeds).
set -u
fail=0
ok(){ echo "PASS  $1"; }
bad(){ echo "FAIL  $1"; fail=1; }
P=plugins/gtm-job-search

claude plugin validate ./$P >/dev/null 2>&1 && ok "plugin manifest validates" || bad "plugin manifest validates"
[ -f $P/.claude-plugin/plugin.json ] && ok "plugin.json is at $P/.claude-plugin/plugin.json" || bad "plugin.json missing at $P/.claude-plugin/plugin.json"
[ -e $P/plugins ] && bad "nested folder $P/plugins found (a folder was uploaded one level too deep)" || ok "no nested plugins folder"
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

! grep -rnE "history\.json|fetch_ats\.py (snapshot|trend)|Seen:|too early to read|first read" $P/skills $P/scripts $P/agents >/dev/null && ok "no trend or history leftovers in skill, scripts or agent" || bad "trend or history text still present"
python3 - <<PY && ok "lever detail returns requirement lists and workplace (regression: live Fours posting)" || bad "lever detail drops lists or workplace"
import importlib.util,io,json,contextlib
spec=importlib.util.spec_from_file_location("f","$P/scripts/fetch_ats.py"); f=importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
f.get_json=lambda url,timeout=15:{"id":"x","text":"GTM Engineer","descriptionPlain":"Intro.","workplaceType":"hybrid","createdAt":1757376000000,
  "categories":{"location":"San Francisco, CA"},"hostedUrl":"https://jobs.lever.co/acme/x",
  "lists":[{"text":"We're Looking For","content":"<li>2-5 years in data engineering</li><li>Python and SQL</li>"}],"additionalPlain":"Salary: 120-180k"}
class A: ats="lever"; token="acme"; id="x"
buf=io.StringIO()
with contextlib.redirect_stdout(buf): f.cmd_detail(A)
o=json.loads(buf.getvalue())
assert o["workplace"]=="hybrid" and "2-5 years" in o["description"] and "Python and SQL" in o["description"] and "Salary: 120-180k" in o["description"],o
PY
python3 - <<PY && ok "pay written into the description is found (regression: live Vercel and Together AI postings)" || bad "pay_in_text misses pay in description"
import importlib.util
spec=importlib.util.spec_from_file_location("f","$P/scripts/fetch_ats.py"); f=importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
assert f.pay_in_text("The salary range is \$180,000 - \$295,000. Equity too.")==["\$180,000 - \$295,000"]
assert f.pay_in_text("OTE \$160K-190K plus equity")==["\$160K-190K"]
assert f.pay_in_text("raised \$43M in funding")==[] and f.pay_in_text(None)==[]
PY
python3 - <<PY && ok "greenhouse descriptions arrive entity-escaped and are cleaned (regression: live Together AI posting)" || bad "strip_html leaves escaped tags"
import importlib.util
spec=importlib.util.spec_from_file_location("f","$P/scripts/fetch_ats.py"); f=importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
o=f.strip_html("&lt;ul&gt;&lt;li&gt;3&ndash;5+ years &amp;amp; APIs&lt;/li&gt;&lt;/ul&gt;")
assert "<" not in o and "3–5+ years" in o and "& APIs" in o, o
assert f.strip_html("<p>A &amp; B</p>")=="A & B" and f.strip_html(None)==""
PY
python3 tests/check_handoff.py >/dev/null && ok "hand-off contract: what find-my-job passes is what the tailor consumes" || bad "hand-off contract"
python3 $P/scripts/fetch_ats.py scan --universe $P/data/company-universe.json --keywords "(" 2>&1 | grep -q "invalid --keywords" && ok "bad regex is a clean error" || bad "bad regex handling"
exit $fail
