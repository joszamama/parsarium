"""Save bounded Packagist discovery hits for PHP HTTP/1.1 parsers."""

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json


ROOT = Path(__file__).resolve().parents[1]
QUERIES = [
    "http parser", "http message parser", "raw http", "http request parser",
    "http response parser", "http message", "http protocol", "psr7 parser",
]


def main() -> None:
    searches = []
    for query in QUERIES:
        url = "https://packagist.org/search.json?" + urlencode({"q": query, "per_page": 100})
        request = Request(url, headers={"User-Agent": "Parsarium format-parser research"})
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
        hits = [{"rank": rank, "name": item["name"], "downloads": item.get("downloads"),
                 "url": item["url"]} for rank, item in enumerate(result["results"][:100], 1)]
        searches.append({"query": query, "url": url, "total": result["total"], "hits": hits})
        print(f"{query}: {len(hits)}/{result['total']} hits")
    output = {"captured_at_utc": datetime.now(timezone.utc).isoformat(),
              "search_surface": "Packagist public search JSON API",
              "search_limit_per_query": 100, "search": searches,
              "releases": {}, "download_metric": {}}
    path = ROOT / "data/php/http11/registry-snapshot.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"{sum(len(item['hits']) for item in searches)} hits, "
          f"{len({hit['name'] for item in searches for hit in item['hits']})} unique names")


if __name__ == "__main__":
    main()
