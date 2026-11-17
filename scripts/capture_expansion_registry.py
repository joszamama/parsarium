#!/usr/bin/env python3
"""Capture bounded registry searches for the JSON/XML/plain-MP3 expansion inventory.

Search hits are leads only. Nothing captured here verifies a parser.
Writes data/expansion/registry/<ecosystem>.json.
"""
import datetime, gzip, html, io, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/expansion/registry"
UA = "parsarium-research (expansion inventory; joszamama)"
LIMIT = 100
QUERIES = {
    "json": ["json"],
    "xml": ["xml"],
    "mp3_plain": ["mp3", "mpeg audio"],
}


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def get(url, accept=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **({"Accept": accept} if accept else {})})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            raise


def getj(url, accept=None):
    return json.loads(get(url, accept))


def npm():
    res = []
    for fmt, qs in QUERIES.items():
        for q in qs:
            url = f"https://registry.npmjs.org/-/v1/search?text={urllib.parse.quote(q)}&size={LIMIT}&from=0"
            d = getj(url)
            res.append({"format": fmt, "query": q, "url": url, "total": d.get("total"), "limit": LIMIT,
                        "ordering": "npm registry search default relevance order",
                        "hits": [{"rank": i + 1, "name": o["package"]["name"], "version": o["package"].get("version")}
                                 for i, o in enumerate(d["objects"])]})
    return {"search_surface": "npm registry search API",
            "search_api_docs": "https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md", "search": res}


def pypi():
    url = "https://pypi.org/simple/"
    d = getj(url, "application/vnd.pypi.simple.v1+json")
    names = sorted((p["name"] for p in d["projects"]), key=str.lower)
    res = []
    for fmt, qs in QUERIES.items():
        for q in qs:
            needle = q.replace(" ", "")
            m = [n for n in names if needle in n.lower()]
            res.append({"format": fmt, "query": f"project name contains '{needle}'", "url": url, "total": len(m),
                        "limit": LIMIT, "ordering": "case-insensitive project-name order; not a popularity order",
                        "hits": [{"rank": i + 1, "name": n} for i, n in enumerate(m[:LIMIT])]})
    return {"search_surface": "PyPI Simple JSON project-name index, filtered locally; no relevance ranking",
            "search_api_docs": "https://docs.pypi.org/api/index-api/",
            "search_index_serial": d.get("meta", {}).get("_last-serial"), "search": res}


def crates():
    res = []
    for fmt, qs in QUERIES.items():
        for q in qs:
            url = f"https://crates.io/api/v1/crates?q={urllib.parse.quote(q)}&per_page={LIMIT}&page=1"
            d = getj(url)
            res.append({"format": fmt, "query": q, "url": url, "total": d["meta"]["total"], "limit": LIMIT,
                        "ordering": "crates.io default (relevance) order",
                        "hits": [{"rank": i + 1, "name": c["name"], "version": c.get("max_stable_version") or c.get("max_version"),
                                  "recent_downloads_90d": c.get("recent_downloads"), "downloads_all_time": c.get("downloads")}
                                 for i, c in enumerate(d["crates"])]})
            time.sleep(1)
    return {"search_surface": "crates.io API first page, default registry order",
            "search_api_docs": "https://crates.io/data-access", "search": res,
            "metric": {"name": "crates.io recent_downloads", "definition": "Crate downloads over the trailing 90 days as returned by the crates.io API at capture time. Compared only within Rust."}}


def packagist():
    res = []
    for fmt, qs in QUERIES.items():
        for q in qs:
            url = f"https://packagist.org/search.json?q={urllib.parse.quote(q)}&per_page={LIMIT}"
            d = getj(url)
            res.append({"format": fmt, "query": q, "url": url, "total": d.get("total"), "limit": LIMIT,
                        "ordering": "Packagist search default order",
                        "hits": [{"rank": i + 1, "name": r["name"], "downloads_lifetime": r.get("downloads"), "favers": r.get("favers")}
                                 for i, r in enumerate(d["results"])]})
    return {"search_surface": "Packagist public search JSON API", "search_api_docs": "https://packagist.org/apidoc",
            "search": res,
            "metric": {"name": "Packagist lifetime package downloads", "definition": "Total downloads of all releases of a Composer package name as returned by search.json. Compared only within PHP."}}


def maven():
    res = []
    for fmt, qs in QUERIES.items():
        for q in qs:
            url = f"https://search.maven.org/solrsearch/select?q={urllib.parse.quote(q)}&rows={LIMIT}&wt=json"
            try:
                d = getj(url)
                r = d["response"]
                res.append({"format": fmt, "query": q, "url": url, "total": r["numFound"], "limit": LIMIT,
                            "ordering": "Maven Central Solr default order",
                            "hits": [{"rank": i + 1, "name": f"{x['g']}:{x['a']}", "version": x.get("latestVersion")}
                                     for i, x in enumerate(r["docs"])]})
            except Exception as e:  # recorded, not hidden
                res.append({"format": fmt, "query": q, "url": url, "error": repr(e)})
    return {"search_surface": "Maven Central Solr artifact search",
            "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/", "search": res}


def gopkg():
    res = []
    for fmt, qs in QUERIES.items():
        for q in qs:
            url = f"https://pkg.go.dev/search?q={urllib.parse.quote(q)}&limit={LIMIT}&m=package"
            try:
                page = get(url).decode("utf-8", "replace")
                total = re.search(r"of\s+([\d,]+)\s*results", page) or re.search(r"([\d,]+)\s+results", page)
                hits = []
                for block in page.split('class="SearchSnippet"')[1:]:
                    m = re.search(r'data-clicked-package="([^"]+)"', block)
                    if not m:
                        continue
                    ib = re.search(r'Imported by[\s\S]*?<strong>([\d,]+)</strong>', block)
                    hits.append({"rank": len(hits) + 1, "name": html.unescape(m.group(1)),
                                 "imported_by": int(ib.group(1).replace(",", "")) if ib else None})
                res.append({"format": fmt, "query": q, "url": url,
                            "total": int(total.group(1).replace(",", "")) if total else None, "limit": LIMIT,
                            "ordering": "pkg.go.dev search relevance order", "total_note": "The HTML page does not state a total result count; null means not displayed.", "hits": hits[:LIMIT]})
            except Exception as e:
                res.append({"format": fmt, "query": q, "url": url, "error": repr(e)})
            time.sleep(2)
    return {"search_surface": "pkg.go.dev public HTML package search", "search_api_docs": "https://pkg.go.dev/search-help",
            "search": res,
            "metric": {"name": "pkg.go.dev Imported by package count", "definition": "Importer count shown in search snippets. Compared only within Go."}}


def homebrew():
    formulae = getj("https://formulae.brew.sh/api/formula.json")
    analytics = getj("https://formulae.brew.sh/api/analytics/install-on-request/365d.json")
    counts = {i["formula"]: int(str(i["count"]).replace(",", "")) for i in analytics["items"]}
    res = []
    for fmt, qs in QUERIES.items():
        for q in qs:
            needle = q.replace(" ", "")
            m = [f for f in formulae if needle in f["name"].lower() or needle in (f.get("desc") or "").lower().replace(" ", "")]
            m.sort(key=lambda f: f["name"])
            res.append({"format": fmt, "query": f"formula name or description contains '{needle}'",
                        "url": "https://formulae.brew.sh/api/formula.json", "total": len(m), "limit": LIMIT,
                        "ordering": "formula-name order; not a popularity order",
                        "hits": [{"rank": i + 1, "name": f["name"], "version": f["versions"]["stable"],
                                  "install_on_request_365d": counts.get(f["name"]), "desc": f.get("desc")}
                                 for i, f in enumerate(m[:LIMIT])]})
    return {"search_surface": "Homebrew formula index (names and descriptions), shared by C and C++",
            "search_api_docs": "https://formulae.brew.sh/docs/api/", "search": res,
            "metric": {"name": "Homebrew install-on-request count over 365 days",
                       "source": "https://formulae.brew.sh/api/analytics/install-on-request/365d.json",
                       "window_start": analytics.get("start_date"), "window_end": analytics.get("end_date"),
                       "definition": "User-requested formula installs on macOS/Linux; not format-specific use. Compared only within one C or C++ cell."}}


CAPTURES = {"javascript": npm, "python": pypi, "rust": crates, "php": packagist, "java": maven, "go": gopkg, "c_cpp": homebrew}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for eco in sys.argv[1:] or CAPTURES:
        started = now()
        try:
            snap = CAPTURES[eco]()
        except Exception as e:
            snap = {"error": repr(e)}
        snap = {"ecosystem": eco, "captured_at_utc": started, "search_limit_per_query": LIMIT,
                "note": "Search hits are leads, not verified parsers.", **snap}
        (OUT / f"{eco}.json").write_text(json.dumps(snap, indent=1, ensure_ascii=False) + "\n")
        print(eco, [(s.get("query"), s.get("total"), len(s.get("hits", [])), s.get("error")) for s in snap.get("search", [])] or snap.get("error"))
