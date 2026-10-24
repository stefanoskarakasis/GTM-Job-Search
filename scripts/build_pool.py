#!/usr/bin/env python3
"""Build data/company-universe.json from the plain-text lists in data/sources/. Standard library only.

Edit or add a list in data/sources/, add it to SOURCES below if it is new, then run:
  python3 scripts/build_pool.py
Priority 0 = live listing seen. Wave 1 (default pool, searched first) = priority 0-2.
Wave 2 (wider pool, searched after) = priority 3 and up.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "sources"
OUT = ROOT / "data" / "company-universe.json"

# (file, source tag, priority)
SOURCES = [
    ("marketingengineer-jobs.txt", "marketingengineer.jobs", 0),
    ("gtmjobs-substack.txt", "gtmjobs.substack", 1),
    ("tracker-t1.txt", "tracker:T1", 1),
    ("tracker-t2.txt", "tracker:T2", 2),
    ("tracker-t3.txt", "tracker:T3", 3),
    ("skills-marketing.txt", "skills.marketing", 4),
    ("adamgtm.txt", "adamgtm", 4),
    ("tracker-emea-pmm.txt", "tracker:EMEA-PMM", 5),
    ("tracker-fintech.txt", "tracker:FinTech", 5),
    ("trueup-marketing-growth-top20.txt", "trueup:marketing-growth-top20", 5),
]
WAVE1_MAX_PRIORITY = 2


def key(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def load_aliases():
    out = {}
    path = SRC / "aliases.txt"
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if "=" in line:
                a, b = (x.strip() for x in line.split("=", 1))
                out[key(a)] = b
    return out


def main():
    aliases = load_aliases()
    pool = {}
    for fname, tag, prio in SOURCES:
        path = SRC / fname
        if not path.exists():
            print(f"missing source list: {fname}", file=sys.stderr)
            continue
        for raw in path.read_text().splitlines():
            line = raw.split(" #", 1)[0].strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            name = parts[0]
            unconfirmed = name.endswith("?")
            name = name.rstrip("?").strip()
            name = aliases.get(key(name), name)
            c = pool.setdefault(key(name), {"name": name, "sources": [], "priority": prio})
            if tag not in c["sources"]:
                c["sources"].append(tag)
            c["priority"] = min(c["priority"], prio)
            if not unconfirmed:
                c["_confirmed"] = True  # at least one source states the name without a '?'
            if len(parts) > 1 and parts[1]:
                c["size_band"] = parts[1]
            if len(parts) > 2 and parts[2]:
                c["listings_seen"] = [x.strip() for x in parts[2].split(";")]
    rows = list(pool.values())
    for r in rows:
        if not r.pop("_confirmed", False):
            r["verify_name"] = True
        r["wave"] = 1 if r["priority"] <= WAVE1_MAX_PRIORITY else 2
        r["signal_count"] = len(r["sources"])
    rows.sort(key=lambda r: (r["priority"], -r["signal_count"], r["name"].lower()))
    waves = {1: sum(1 for r in rows if r["wave"] == 1), 2: sum(1 for r in rows if r["wave"] == 2)}
    out = {
        "version": 2,
        "about": ("Company pool for GTM Job Search, built by scripts/build_pool.py from data/sources/*.txt. "
                  "Wave 1 is the default pool, searched first; wave 2 is the wider pool, searched after. "
                  "priority 0 = live listing seen on marketingengineer.jobs; signal_count = how many source "
                  "lists name the company. verify_name = name taken from a list and not independently confirmed. "
                  "Careers sites are resolved at first run and cached locally; none are hard-coded here."),
        "waves": {"1": waves[1], "2": waves[2]},
        "companies": rows,
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"{len(rows)} companies: wave 1 = {waves[1]}, wave 2 = {waves[2]} -> {OUT}")


if __name__ == "__main__":
    main()
