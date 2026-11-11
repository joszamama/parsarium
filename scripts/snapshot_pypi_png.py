"""Capture bounded PyPI name-index leads, pinned releases, and download signals."""

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "png"
INDEX_URL = "https://pypi.org/simple/"
TERMS = ("png", "imread", "imageio", "pillow", "opencv", "vips", "cairo")
LIMIT = 100


def read_json(url: str, accept: str = "application/json"):
    request = Request(url, headers={"Accept": accept, "User-Agent": "Parsarium parser collection research"})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def main() -> None:
    index = read_json(INDEX_URL, "application/vnd.pypi.simple.v1+json")
    projects = [project["name"] for project in index["projects"]]
    search = []
    for term in TERMS:
        matches = sorted((name for name in projects if term in name.lower()), key=str.casefold)
        search.append({"query": f"project name contains {term!r}", "url": INDEX_URL,
                       "total": len(matches), "limit": LIMIT,
                       "ordering": "case-insensitive project-name order; not a popularity order",
                       "hits": [{"rank": i, "name": name} for i, name in enumerate(matches[:LIMIT], 1)]})
    parsers = json.loads((CELL / "parsers.json").read_text())
    releases = {}
    downloads = {}
    for parser in parsers:
        name, version = parser["name"], parser["version"]
        release_url = f"https://pypi.org/pypi/{quote(name)}/{quote(version)}/json"
        release = read_json(release_url)
        info = release["info"]
        releases[name] = {
            "version": version, "url": release_url,
            "license_expression": info.get("license_expression"),
            "license_metadata_excerpt": (info.get("license") or "")[:160],
            "license_classifiers": [item for item in info.get("classifiers", []) if item.startswith("License ::")],
            "files": [{"filename": item["filename"], "sha256": item["digests"]["sha256"]}
                      for item in release["urls"]],
        }
        metric_url = f"https://pypistats.org/api/packages/{quote(name.lower())}/recent?period=month"
        try:
            metric = read_json(metric_url)
            count = metric["data"]["last_month"]
        except Exception as error:
            count = None
            downloads[name] = {"downloads": count, "url": metric_url, "error": str(error)}
        else:
            downloads[name] = {"downloads": count, "url": metric_url}
    captured = datetime.now(timezone.utc).isoformat()
    snapshot = {
        "captured_at_utc": captured,
        "search_surface": "PyPI Simple JSON project-name index, filtered locally; results have no relevance ranking",
        "search_api_docs": "https://docs.pypi.org/api/index-api/",
        "search_index_serial": index["meta"].get("_last-serial"),
        "search_limit_per_query": LIMIT,
        "search": search,
        "releases": releases,
        "download_metric": {
            "name": "PyPI Stats last_month downloads excluding known mirrors",
            "documentation": "https://pypistats.org/api/",
            "captured_at_utc": captured,
            "window": "API-defined last_month rolling period; all requests captured on the same UTC date",
            "packages": downloads,
        },
    }
    (CELL / "registry-snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    print(f"Saved {sum(len(row['hits']) for row in search)} name-index leads and {len(parsers)} pinned releases")


if __name__ == "__main__":
    main()
