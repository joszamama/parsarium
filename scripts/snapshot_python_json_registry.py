#!/usr/bin/env python3
"""Capture the bounded PyPI search and download metrics for the Python JSON pilot cell.

Search hits and the top-package discovery aid are leads only; nothing here verifies a parser.
Writes data/python/json/registry-snapshot.json.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/python/json/registry-snapshot.json"
UA = "parsarium-research (python json registry snapshot)"
LIMIT = 100
SIMPLE = "https://pypi.org/simple/"
TOP = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"
QUERIES = ["json", "json5", "simdjson", "rapidjson", "yajl", "jiter"]
# Every package named in data/python/json/leads.json, selected or not.
PACKAGES = [
    "pydantic", "jiter", "orjson", "simplejson", "ijson", "msgspec", "ujson", "python-rapidjson",
    "pysimdjson", "json5", "pydantic-core", "pandas", "pyarrow", "polars", "json-repair", "srsly",
    "partial-json-parser", "dirtyjson", "hjson", "pyjson5", "commentjson", "json-stream",
    "json-stream-rs-tokenizer", "jsonnet", "demjson3", "jsonslicer", "json-five", "yapic-json",
    "cysimdjson", "yyjson", "hyperjson",
]
# Pinned releases of promoted paths and of leads whose package source was inspected.
RELEASES = {"json5": "0.17.3", "json-repair": "0.64.9", "dirtyjson": "1.0.8", "hjson": "3.1.0"}


def get(url: str, accept: str | None = None) -> bytes:
    headers = {"User-Agent": UA, **({"Accept": accept} if accept else {})}
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    raise RuntimeError(url)


def capture_releases() -> dict:
    releases = {}
    for package, version in RELEASES.items():
        url = f"https://pypi.org/pypi/{package}/{version}/json"
        info = json.loads(get(url))
        releases[package] = {"version": version, "url": url,
                             "license_expression": info["info"].get("license_expression"),
                             "license": info["info"].get("license") or None,
                             "requires_dist": info["info"].get("requires_dist") or [],
                             "files": [{"filename": item["filename"], "sha256": item["digests"]["sha256"]}
                                       for item in info["urls"]]}
    return releases


def main() -> None:
    if sys.argv[1:] == ["--releases-only"]:
        # Refresh pinned release records without re-capturing searches or download counts.
        snapshot = json.loads(OUT.read_text())
        snapshot["releases"] = capture_releases()
        snapshot["releases_captured_at_utc"] = datetime.now(timezone.utc).isoformat()
        OUT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(sorted(snapshot["releases"]), indent=2))
        return
    captured = datetime.now(timezone.utc).isoformat()
    index = json.loads(get(SIMPLE, "application/vnd.pypi.simple.v1+json"))
    names = sorted((project["name"] for project in index["projects"]), key=str.lower)
    search = []
    for query in QUERIES:
        matches = [name for name in names if query in name.lower()]
        search.append({"query": f"project name contains '{query}'", "url": SIMPLE, "total": len(matches),
                       "limit": LIMIT, "ordering": "case-insensitive project-name order; not a popularity order",
                       "hits": [{"rank": rank, "name": name} for rank, name in enumerate(matches[:LIMIT], 1)]})
    top = json.loads(get(TOP))
    top_hits = [{"rank": rank, "name": row["project"], "download_count": row["download_count"]}
                for rank, row in enumerate(top["rows"], 1) if "json" in row["project"].lower()]
    packages = {}
    for package in PACKAGES:
        url = f"https://pypistats.org/api/packages/{package}/recent?period=month"
        packages[package] = {"downloads": json.loads(get(url))["data"]["last_month"], "url": url}
        time.sleep(1.2)
    releases = capture_releases()
    snapshot = {
        "captured_at_utc": captured,
        "search_surface": "PyPI Simple JSON project-name index, filtered locally; results have no relevance ranking",
        "search_api_docs": "https://docs.pypi.org/api/index-api/",
        "search_index_serial": index.get("meta", {}).get("_last-serial"),
        "search_limit_per_query": LIMIT,
        "search": search,
        "discovery_aid": {
            "name": "top-pypi-packages 30-day list (hugovk), filtered for project names containing 'json'",
            "url": TOP, "source": top.get("source"), "last_update": top.get("last_update"),
            "rows": len(top["rows"]), "matches": len(top_hits), "hits": top_hits[:LIMIT],
            "use": "Only used to pick plausible high-adoption leads beyond the alphabetical name search; "
                   "its download counts are not the cell metric and do not rank anything. Leads whose names "
                   "do not contain 'json' (pydantic-core, pandas, pyarrow, polars, srsly and the native "
                   "binding names) come from package documentation of JSON loading APIs.",
        },
        "download_metric": {
            "name": "PyPI Stats last_month downloads excluding known mirrors",
            "documentation": "https://pypistats.org/api/", "captured_at_utc": captured,
            "window": "API-defined last_month rolling period; the nine earlier values in leads.json were captured "
                      "on the same UTC date, and the simplejson value is identical in both captures",
            "packages": packages,
        },
        "releases": releases,
    }
    OUT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({query["query"]: query["total"] for query in search}, indent=2))
    print(json.dumps({name: item["downloads"] for name, item in packages.items()}, indent=2))


if __name__ == "__main__":
    main()
