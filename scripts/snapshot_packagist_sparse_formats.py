"""Save bounded Packagist leads for PHP Matrix Market and ASCII PLY."""

from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
SEARCHES = {
    "matrix_market": ["matrix market", "matrixmarket", "mtx"],
    "ascii_ply": ["ply", "ascii ply"],
}
LIMIT = 100


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    for format_name, queries in SEARCHES.items():
        search = []
        for query in queries:
            url = "https://packagist.org/search.json?q=" + quote(query) + f"&per_page={LIMIT}"
            item = {"query": query, "url": url, "limit": LIMIT, "captured_at_utc": now()}
            try:
                with urlopen(url, timeout=20) as response:
                    data = json.load(response)
                item.update(total=data["total"], hits=[
                    {"name": hit["name"], "description": hit.get("description", ""),
                     "url": hit.get("url")}
                    for hit in data["results"]])
            except Exception as error:
                item.update(total=None, hits=[], error=f"{type(error).__name__}: {error}")
            search.append(item)
        target = ROOT / "data/php" / format_name / "registry-snapshot.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({
            "captured_at_utc": now(), "search_surface": "Packagist search API",
            "search_api_docs": "https://packagist.org/apidoc",
            "search_limit_per_query": LIMIT, "search": search,
            "releases": {},
            "download_metric": {
                "name": "Packagist package downloads",
                "documentation": "https://packagist.org/apidoc",
                "scope": "Only verified packages can enter the within-PHP ranking; no metric is claimed for these leads",
                "packages": {},
            },
        }, indent=2) + "\n")
        print(format_name, sum(len(row["hits"]) for row in search), "hits")


if __name__ == "__main__":
    main()
