#!/usr/bin/env python3
"""Capture the bounded PyPI search and download metrics for the Python XML pilot cell.

Search hits and the top-package discovery aid are leads only; nothing here verifies a parser.
Writes data/python/xml/registry-snapshot.json.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/python/xml/registry-snapshot.json"
UA = "parsarium-research (python xml registry snapshot)"
LIMIT = 100
SIMPLE = "https://pypi.org/simple/"
TOP = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"
QUERIES = ["xml", "expat", "etree", "sax", "xpath", "pugixml", "rapidxml"]
TOP_TERMS = ("xml", "expat", "etree", "sax", "xpath", "soup", "pyquery", "parsel", "scrapy", "untangle", "xsdata")
# Every package named in data/python/xml/leads.json, selected or not.
PACKAGES = [
    "lxml", "beautifulsoup4", "defusedxml", "xmltodict", "xmlschema", "scrapy", "parsel", "xsdata", "untangle",
    "et-xmlfile", "elementpath", "selectolax", "pydantic-xml", "saxonche", "tree-sitter-xml", "pyquery",
    "cmeel-tinyxml2", "xmljson", "alibabacloud-tea-xml", "xmltojson", "djangorestframework-xml", "xmldiff",
    "pandas-read-xml", "mwxml", "xml-python", "pyaxmlparser", "jxmlease", "beautifulsoup", "pygixml", "rapidxml",
]


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


def downloads(package: str):
    url = f"https://pypistats.org/api/packages/{package}/recent?period=month"
    try:
        return {"downloads": json.loads(get(url))["data"]["last_month"], "url": url}
    except urllib.error.HTTPError as error:
        return {"downloads": None, "url": url, "error": f"HTTP {error.code}"}


def main() -> None:
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
                for rank, row in enumerate(top["rows"], 1) if any(term in row["project"].lower() for term in TOP_TERMS)]
    packages = {}
    for package in PACKAGES:
        packages[package] = downloads(package)
        time.sleep(1.2)
    snapshot = {
        "captured_at_utc": captured,
        "search_surface": "PyPI Simple JSON project-name index, filtered locally; results have no relevance ranking",
        "search_api_docs": "https://docs.pypi.org/api/index-api/",
        "search_index_serial": index.get("meta", {}).get("_last-serial"),
        "search_limit_per_query": LIMIT,
        "search": search,
        "discovery_aid": {
            "name": "top-pypi-packages 30-day list (hugovk), filtered for project names containing " + ", ".join(repr(t) for t in TOP_TERMS),
            "url": TOP, "source": top.get("source"), "last_update": top.get("last_update"),
            "rows": len(top["rows"]), "matches": len(top_hits), "hits": top_hits[:LIMIT],
            "use": "Only used to pick plausible high-adoption leads beyond the alphabetical name search; its download "
                   "counts are not the cell metric and do not rank anything. The earlier nine leads came from targeted "
                   "PyPI project pages and project documentation.",
        },
        "download_metric": {
            "name": "PyPI Stats last_month downloads excluding known mirrors",
            "documentation": "https://pypistats.org/api/", "captured_at_utc": captured,
            "window": "API-defined last_month rolling period; the nine earlier values in leads.json were captured on the "
                      "same UTC date and stay the ranking values for those packages",
            "packages": packages,
        },
    }
    OUT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({query["query"]: query["total"] for query in search}, indent=2))
    print(json.dumps({name: item["downloads"] for name, item in packages.items()}, indent=2))


if __name__ == "__main__":
    main()
