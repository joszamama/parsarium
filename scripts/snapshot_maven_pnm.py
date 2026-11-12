"""Capture bounded Maven Central PNM leads, without treating names as proof."""

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json


ROOT = Path(__file__).resolve().parents[1]
QUERIES = ["pnm", "ppm", "pgm", "imageio-pnm", "portable anymap", "netpbm"]


def main() -> None:
    searches = []
    for query in QUERIES:
        url = "https://search.maven.org/solrsearch/select?" + urlencode(
            {"q": query, "rows": 100, "wt": "json"})
        captured = datetime.now(timezone.utc).isoformat()
        try:
            request = Request(url, headers={"User-Agent": "Parsarium Java PNM research"})
            with urlopen(request, timeout=12) as response:
                result = json.load(response)["response"]
            hits = [{"rank": index, "name": item["id"],
                     "latest_version": item.get("latestVersion")}
                    for index, item in enumerate(result["docs"][:100], 1)]
            searches.append({"query": query, "url": url, "limit": 100,
                             "captured_at_utc": captured, "total": result["numFound"],
                             "hits": hits})
            print(f"{query}: {len(hits)}/{result['numFound']}")
        except Exception as exc:
            searches.append({"query": query, "url": url, "limit": 100,
                             "captured_at_utc": captured, "total": None, "hits": [],
                             "error": f"{type(exc).__name__}: {exc}"})
            print(f"{query}: {type(exc).__name__}: {exc}")
    output = {"captured_at_utc": datetime.now(timezone.utc).isoformat(),
              "search_surface": "Maven Central Solr artifact search",
              "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
              "search_limit_per_query": 100, "search": searches,
              "releases": {}, "popularity_metric": {}}
    path = ROOT / "data/java/ascii_pnm/registry-snapshot.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"{sum(len(s['hits']) for s in searches)} hits, "
          f"{len({h['name'] for s in searches for h in s['hits']})} unique names")


if __name__ == "__main__":
    main()
