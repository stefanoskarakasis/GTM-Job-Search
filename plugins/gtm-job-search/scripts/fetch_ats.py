#!/usr/bin/env python3
"""Scan company job feeds (Greenhouse, Lever, Ashby) for open roles. Standard library only.

Usage:
  fetch_ats.py scan --universe PATH [--wave 1|2] [--keywords REGEX] [--only "A,B"] [--out FILE] [--threads N]
  fetch_ats.py resolve "Company Name"
  fetch_ats.py detail --ats greenhouse|ashby|lever --token BOARD --id JOB_ID
      (full description text, original publish date where the feed has one, pay if listed)

State lives in ~/.gtm-job-search/ (company-cache.json, overrides.json). Nothing is sent anywhere
except plain GET requests to the companies' public job-board feeds.
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

STATE = Path(os.path.expanduser("~")) / ".gtm-job-search"
CACHE = STATE / "company-cache.json"
OVERRIDES = STATE / "overrides.json"
UA = "gtm-job-search/1.1 (job-seeker tool; public GET only)"
UNKNOWN_RETRY_DAYS = 30

DEFAULT_KEYWORDS = (
    r"marketing engineer|gtm engineer|go-to-market engineer|revenue engineer|growth engineer|"
    r"forward[- ]deployed|deployment engineer|implementation engineer|product marketing|"
    r"revenue operations|\brevops\b|sales operations|gtm operations|marketing operations|"
    r"\baeo\b|\bgeo\b|answer engine|generative engine|ai search|ai discoverability|"
    r"ai product (manager|lead)|ai transformation|transformation lead|"
    r"marketing technolog|marketing automation|gtm systems|gtm architect|growth platform"
)

# Names too generic to resolve by guessing a board slug; resolve these by hand via overrides.json.
GENERIC = {"default", "light", "ben", "rover", "attention", "upside", "agency", "block", "primer",
           "vector", "momentum", "monaco", "cargo", "octave", "volt", "tem", "gecko", "loom",
           "endgame", "cleo", "sift"}


def get_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                time.sleep(2)
                continue
            return None
        except (urllib.error.URLError, TimeoutError, ValueError):
            if attempt == 1:
                time.sleep(1)
                continue
            return None
    return None


def slug_candidates(name):
    base = re.sub(r"\(.*?\)", "", name).strip().lower()
    no_tld = re.sub(r"\.(ai|io|com|co)$", "", base)
    out = []
    for s in (re.sub(r"[^a-z0-9]", "", base),
              re.sub(r"[^a-z0-9]+", "-", base).strip("-"),
              re.sub(r"[^a-z0-9]", "", no_tld),
              re.sub(r"[^a-z0-9]+", "-", no_tld).strip("-")):
        if s and s not in out:
            out.append(s)
    return out


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def fetch_greenhouse(token):
    d = get_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs")
    if not isinstance(d, dict) or "jobs" not in d:
        return None
    return [{"id": str(j.get("id")), "title": j.get("title", ""),
             "location": (j.get("location") or {}).get("name", ""),
             "url": j.get("absolute_url", ""), "posted": None,
             "updated": (j.get("updated_at") or "")[:10] or None} for j in d["jobs"]]


def fetch_lever(site):
    for host in ("api.lever.co", "api.eu.lever.co"):
        d = get_json(f"https://{host}/v0/postings/{site}?mode=json")
        if isinstance(d, list):
            out = []
            for j in d:
                ts = j.get("createdAt")
                posted = time.strftime("%Y-%m-%d", time.gmtime(ts / 1000)) if isinstance(ts, (int, float)) else None
                out.append({"id": j.get("id"), "title": j.get("text", ""),
                            "location": (j.get("categories") or {}).get("location", ""),
                            "url": j.get("hostedUrl", ""), "posted": posted, "updated": None})
            return out
    return None


def fetch_ashby(name):
    d = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{name}")
    if not isinstance(d, dict) or "jobs" not in d:
        return None
    out = []
    for j in d["jobs"]:
        if j.get("isListed") is False:
            continue
        pub = j.get("publishedAt") or j.get("publishedDate") or ""
        out.append({"id": j.get("id"), "title": j.get("title", ""),
                    "location": j.get("location", "") if isinstance(j.get("location"), str) else "",
                    "url": j.get("jobUrl", "") or j.get("applyUrl", ""),
                    "posted": str(pub)[:10] or None, "updated": None})
    return out


FETCHERS = {"greenhouse": fetch_greenhouse, "lever": fetch_lever, "ashby": fetch_ashby}


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return default


def save_json(path, data):
    STATE.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=1, ensure_ascii=False))


def mentions_company(ats, slug, company, sample=10):
    """Ashby/Lever feeds carry no company name, so check the posting text mentions it."""
    c = norm(re.sub(r"\(.*?\)", "", company))
    if ats == "ashby":
        d = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
        jobs = (d or {}).get("jobs", []) if isinstance(d, dict) else []
        texts = [(j.get("descriptionPlain") or "") + " " + (j.get("title") or "") for j in jobs[:sample]]
    elif ats == "lever":
        texts = []
        for host in ("api.lever.co", "api.eu.lever.co"):
            d = get_json(f"https://{host}/v0/postings/{slug}?mode=json")
            if isinstance(d, list):
                texts = [(j.get("descriptionPlain") or "") for j in d[:sample]]
                break
    else:
        return False
    return any(c and c in norm(t) for t in texts)


def gh_board_name_ok(token, company):
    d = get_json(f"https://boards-api.greenhouse.io/v1/boards/{token}")
    n = norm((d or {}).get("name", ""))
    c = norm(company)
    return bool(n) and (c in n or n in c)


def resolve(name, cache, overrides):
    """Return {'ats','token','name_checked'} or {'ats':'unknown'}. Uses overrides, then cache, then probes."""
    if name in overrides:
        return {**overrides[name], "name_checked": True}
    hit = cache.get(name)
    if hit:
        if hit.get("ats") != "unknown":
            return hit
        if time.time() - hit.get("checked", 0) < UNKNOWN_RETRY_DAYS * 86400:
            return hit
    if norm(name) in GENERIC:
        return {"ats": "unknown", "reason": "generic name; add to overrides.json", "checked": time.time()}
    for slug in slug_candidates(name):
        for ats, fn in FETCHERS.items():
            jobs = fn(slug)
            if jobs is None:
                continue
            if ats == "greenhouse":
                if not gh_board_name_ok(slug, name):
                    continue
                return {"ats": ats, "token": slug, "name_checked": True, "checked": time.time()}
            # Lever/Ashby feeds carry no company name: accept only if non-empty, flag as unchecked.
            if jobs:
                return {"ats": ats, "token": slug, "name_checked": mentions_company(ats, slug, name),
                        "checked": time.time()}
    # Second pass: common board-name suffixes/prefixes. Greenhouse is verified by board name;
    # Ashby and Lever are accepted only if the posting text mentions the company.
    for slug in slug_candidates(name)[:1]:
        for variant in [slug + x for x in ("hq", "ai", "labs", "io", "inc", "app", "co")] + ["get" + slug, "join" + slug, "use" + slug]:
            if fetch_greenhouse(variant) is not None and gh_board_name_ok(variant, name):
                return {"ats": "greenhouse", "token": variant, "name_checked": True, "checked": time.time()}
            for ats in ("ashby", "lever"):
                jobs = FETCHERS[ats](variant)
                if jobs and mentions_company(ats, variant, name):
                    return {"ats": ats, "token": variant, "name_checked": True, "checked": time.time()}
    return {"ats": "unknown", "checked": time.time()}


def scan_one(company, cache, overrides, rx):
    name = company["name"]
    res = resolve(name, cache, overrides)
    cache[name] = res
    if res.get("ats") == "unknown":
        return name, res, None, []
    jobs = FETCHERS[res["ats"]](res["token"])
    if jobs is None:
        return name, res, False, []
    matched = [dict(j, company=name, ats=res["ats"], board=res["token"],
                    name_checked=res.get("name_checked", False),
                    size_band=company.get("size_band"), priority=company.get("priority"),
                    wave=company.get("wave"), sources=company.get("sources"))
               for j in jobs if rx.search(j["title"])]
    return name, res, True, matched


def cmd_scan(a):
    uni = load_json(a.universe, None)
    if not uni:
        sys.exit(f"cannot read universe file: {a.universe}")
    companies = uni["companies"]
    if a.wave:
        companies = [c for c in companies if str(c.get("wave")) == a.wave]
    if a.only:
        wanted = {norm(x) for x in a.only.split(",")}
        companies = [c for c in companies if norm(c["name"]) in wanted]
    try:
        rx = re.compile(a.keywords, re.I)
    except re.error as e:
        sys.exit(f"invalid --keywords regex: {e}")
    if get_json("https://boards-api.greenhouse.io/v1/boards/stripe/jobs") is None:
        sys.exit("network check failed: cannot reach public job feeds from here. "
                 "No scan was run and nothing was cached. Check the connection and retry.")
    cache = load_json(CACHE, {})
    overrides = load_json(OVERRIDES, {})
    if OVERRIDES.exists() and not overrides:
        print(f"warning: {OVERRIDES} is empty or not valid JSON; ignoring it", file=sys.stderr)
    roles, unknown, failed, resolved, total_jobs = [], [], [], 0, 0
    with ThreadPoolExecutor(max_workers=a.threads) as ex:
        results = list(ex.map(lambda c: scan_one(c, cache, overrides, rx), companies))
    for name, res, ok, matched in results:
        if res.get("ats") == "unknown":
            unknown.append(name)
            continue
        resolved += 1
        if ok is False:
            failed.append(name)
        roles.extend(matched)
    save_json(CACHE, cache)
    roles.sort(key=lambda r: (r.get("priority", 9), r["company"].lower(), r["title"].lower()))
    out = {"scanned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "summary": {"companies_in_scope": len(companies), "resolved_to_feed": resolved,
                       "feed_failed": failed, "unresolved": unknown, "roles_matched": len(roles)},
           "roles": roles}
    text = json.dumps(out, indent=1, ensure_ascii=False)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text)
        print(f"{len(roles)} matching roles at {resolved}/{len(companies)} companies "
              f"({len(unknown)} unresolved) -> {a.out}", file=sys.stderr)
    else:
        print(text)


def cmd_resolve(a):
    cache = load_json(CACHE, {})
    res = resolve(a.name, cache, load_json(OVERRIDES, {}))
    cache[a.name] = res
    save_json(CACHE, cache)
    print(json.dumps(res, indent=1))


def strip_html(s):
    s = s or ""
    if re.search(r"&lt;/?[a-z]", s):  # Greenhouse sends its HTML entity-escaped
        s = html.unescape(s)
    s = re.sub(r"<(script|style).*?</\1>", " ", s or "", flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    for a, b in (("&amp;", "&"), ("&nbsp;", " "), ("&lt;", "<"), ("&gt;", ">"), ("&#39;", "'"), ("&quot;", '"')):
        s = s.replace(a, b)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", s)).strip()


PAY_RX = re.compile(r"[$€£]\s?\d[\d,.]*\s?[kK]?\s*(?:[-–—]|to)\s*[$€£]?\s?\d[\d,.]*\s?[kK]?(?:\s*(?:USD|EUR|GBP))?")


def pay_in_text(text):
    """Pay ranges written into the description. Greenhouse often leaves its pay field empty and puts the range
    in the text, so 'no structured pay' must never be read as 'salary not listed'."""
    seen = []
    for m in PAY_RX.finditer(text or ""):
        t = " ".join(m.group(0).split()).rstrip(".,;")
        if t not in seen:
            seen.append(t)
    return seen[:5]


def cmd_detail(a):
    """Full posting for one role: description text, original publish date where the feed has one, pay if listed."""
    if a.ats == "greenhouse":
        d = get_json(f"https://boards-api.greenhouse.io/v1/boards/{a.token}/jobs/{a.id}?pay_transparency=true")
        if not isinstance(d, dict):
            sys.exit("job not found (it may be closed)")
        out = {"ats": a.ats, "id": d.get("id"), "title": d.get("title"), "company": d.get("company_name"),
               "location": (d.get("location") or {}).get("name"), "url": d.get("absolute_url"),
               "first_published": d.get("first_published"), "updated": d.get("updated_at"),
               "pay_ranges": d.get("pay_input_ranges"),
               "description": strip_html(d.get("content"))}
    elif a.ats == "ashby":
        d = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{a.token}?includeCompensation=true")
        job = next((j for j in (d or {}).get("jobs", []) if j.get("id") == a.id), None)
        if not job:
            sys.exit("job not found (it may be closed)")
        out = {"ats": a.ats, "id": job.get("id"), "title": job.get("title"), "location": job.get("location"),
               "url": job.get("jobUrl"), "first_published": job.get("publishedAt"),
               "workplace": job.get("workplaceType"), "pay": job.get("compensation"),
               "description": job.get("descriptionPlain") or strip_html(job.get("descriptionHtml"))}
    else:
        d = get_json(f"https://api.lever.co/v0/postings/{a.token}/{a.id}?mode=json")
        if not isinstance(d, dict):
            sys.exit("job not found (it may be closed)")
        ts = d.get("createdAt")
        # Lever keeps requirements and responsibilities in "lists" and the arrangement in "workplaceType";
        # reading only descriptionPlain would miss the must-haves a fit judgement depends on.
        parts = [d.get("descriptionPlain") or strip_html(d.get("description"))]
        for lst in d.get("lists") or []:
            parts.append((lst.get("text") or "").strip() + ":\n" + strip_html(lst.get("content")))
        if d.get("additionalPlain"):
            parts.append(d["additionalPlain"])
        out = {"ats": a.ats, "id": d.get("id"), "title": d.get("text"),
               "location": (d.get("categories") or {}).get("location"), "url": d.get("hostedUrl"),
               "first_published": time.strftime("%Y-%m-%d", time.gmtime(ts / 1000)) if isinstance(ts, (int, float)) else None,
               "workplace": d.get("workplaceType"), "pay": d.get("salaryRange"), "pay_text": d.get("salaryDescriptionPlain"),
               "description": "\n\n".join(p for p in parts if p)}
    out["pay_in_text"] = pay_in_text(out.get("description"))
    print(json.dumps(out, indent=1, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan")
    s.add_argument("--universe", required=True)
    s.add_argument("--keywords", default=DEFAULT_KEYWORDS)
    s.add_argument("--wave", choices=["1", "2"], help="1 = default pool, 2 = wider pool; omit for both")
    s.add_argument("--only")
    s.add_argument("--out")
    s.add_argument("--threads", type=int, default=10)
    s.set_defaults(fn=cmd_scan)
    r = sub.add_parser("resolve")
    r.add_argument("name")
    r.set_defaults(fn=cmd_resolve)
    d = sub.add_parser("detail")
    d.add_argument("--ats", required=True, choices=["greenhouse", "ashby", "lever"])
    d.add_argument("--token", required=True)
    d.add_argument("--id", required=True)
    d.set_defaults(fn=cmd_detail)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
