"""Save bounded pkg.go.dev discovery results; hits are not verified parsers."""

import json
import sys
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from bs4 import BeautifulSoup

QUERIES = {
    "zip": ["zip", "zip reader", "archive zip", "unzip", "zip parser"],
    "png": ["png", "png decoder", "png reader", "image png", "png parser"],
}
ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    cell = sys.argv[1] if len(sys.argv) > 1 else ""
    if cell not in QUERIES:
        raise SystemExit("usage: python3 scripts/snapshot_go.py zip|png")
    search = []
    for query in QUERIES[cell]:
        url = "https://pkg.go.dev/search?" + urlencode({"q": query, "limit": 100, "m": "package"})
        with urlopen(url, timeout=20) as response:
            page = BeautifulSoup(response.read(), "html.parser")
        hits = []
        for index, snippet in enumerate(page.select(".SearchSnippet"), start=1):
            link = snippet.select_one('a[data-clicked-package]')
            if link is None:
                continue
            synopsis = snippet.select_one(".SearchSnippet-synopsis")
            imported = snippet.select_one('a[href*="tab=importedby"] strong')
            license_element = snippet.select_one('[data-test-id="snippet-license"]')
            version_match = re.search(r"\bv\d+\.\d+\.\d+(?:[-+][\w.-]+)?\b", snippet.get_text(" ", strip=True))
            hits.append({
                "rank": index,
                "packagePath": link.get("data-clicked-package"),
                "url": "https://pkg.go.dev" + link.get("href", ""),
                "version": version_match.group(0) if version_match else None,
                "synopsis": synopsis.get_text(" ", strip=True) if synopsis else "",
                "license": license_element.get_text(" ", strip=True) if license_element else None,
                "importedByPackages": int(imported.get_text(strip=True).replace(",", "")) if imported else None,
            })
        search.append({
            "query": query,
            "url": url,
            "total": None,
            "limit": 100,
            "hits": hits,
        })
    out = ROOT / "data" / "go" / cell / "registry-snapshot.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "pkg.go.dev public HTML package search (the documented v1 JSON API returned HTTP 429 during this capture)",
        "search_api_docs": "https://pkg.go.dev/v1/api",
        "search_limit_per_query": 100,
        "search": search,
        "ranking_metric": "pkg.go.dev Imported by package count",
        "ranking_metric_definition": "Number of packages importing the given package, as displayed in pkg.go.dev search results. Missing counts remain null. Used only within Go, never compared with npm downloads.",
    }, indent=2) + "\n")
    print(f"Saved {sum(len(row['hits']) for row in search)} Go package search hits to {out}")


if __name__ == "__main__":
    main()
