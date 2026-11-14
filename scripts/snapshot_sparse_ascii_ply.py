"""Save bounded supplementary C and PHP ASCII PLY discovery windows.

Repository and package search hits are leads, never parser verification.
"""

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json


ROOT = Path(__file__).resolve().parents[1]
LIMIT = 100
HEADERS = {"User-Agent": "Parsarium parser discovery"}
QUERIES = {
    "c": [
        ("github", '"PLY" "C library"'),
        ("github", "topic:ply language:C"),
        ("github", '"polygon file format" language:C'),
        ("github", "ply parser language:C"),
    ],
    "php": [
        ("packagist", "assimp"),
        ("packagist", "ply file"),
        ("packagist", "3d mesh"),
        ("github", "ply mesh language:PHP"),
        ("github", '"Stanford PLY" language:PHP'),
        ("github", "assimp language:PHP"),
    ],
}


def fetch(url: str) -> dict:
    with urlopen(Request(url, headers=HEADERS), timeout=30) as response:
        return json.load(response)


def snapshot(ecosystem: str) -> dict:
    searches = []
    for surface, query in QUERIES[ecosystem]:
        if surface == "github":
            url = "https://api.github.com/search/repositories?" + urlencode(
                {"q": query, "sort": "stars", "order": "desc", "per_page": LIMIT}
            )
            response = fetch(url)
            hits = [
                {"name": item["full_name"], "description": item["description"],
                 "url": item["html_url"], "stars_at_search": item["stargazers_count"]}
                for item in response["items"][:LIMIT]
            ]
            total = response["total_count"]
        else:
            url = "https://packagist.org/search.json?" + urlencode(
                {"q": query, "per_page": LIMIT}
            )
            response = fetch(url)
            hits = [
                {"name": item["name"], "description": item.get("description"),
                 "url": item["url"]}
                for item in response["results"][:LIMIT]
            ]
            total = response["total"]
        searches.append({"surface": surface, "query": query, "url": url,
                         "sort": "stars descending" if surface == "github" else "Packagist relevance",
                         "limit": LIMIT, "total": total, "hits": hits})
    return {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Supplementary discovery for below-target ASCII PLY cells; names and descriptions are not parser evidence",
        "search_api_docs": {
            "github": "https://docs.github.com/en/rest/search/search#search-repositories",
            "packagist": "https://packagist.org/apidoc",
        },
        "search": searches,
    }


if __name__ == "__main__":
    for ecosystem in QUERIES:
        result = snapshot(ecosystem)
        path = ROOT / "data" / ecosystem / "ascii_ply" / "supplementary-search.json"
        path.write_text(json.dumps(result, indent=2) + "\n")
        print(f"{ecosystem}: {sum(len(item['hits']) for item in result['search'])} supplementary hits")
