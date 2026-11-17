"""Snapshot a bounded Packagist search for PHP plain MP3 (untagged MPEG Layer III) parser candidates."""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import urllib.parse


ROOT = Path(__file__).resolve().parents[1]
QUERIES = ("mp3", "mpeg audio", "mp3 duration", "mp3 bitrate", "mp3 info", "getid3", "audio duration")
LIMIT = 50
OUT = ROOT / "data/php/mp3/registry-snapshot.json"


def fetch(query: str) -> dict:
    url = "https://packagist.org/search.json?" + urllib.parse.urlencode({"q": query, "per_page": LIMIT})
    result = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
                             "--user-agent", "parsarium", url], capture_output=True, text=True, check=True, timeout=60)
    return json.loads(result.stdout)


def main() -> None:
    search = []
    for query in QUERIES:
        data = fetch(query)
        hits = [{"name": item["name"], "description": item.get("description", ""),
                 "downloads": item["downloads"], "favers": item["favers"], "url": item["url"]}
                for item in data["results"][:LIMIT]]
        search.append({"query": query, "total": data["total"], "hits": hits})
    unique = {hit["name"] for entry in search for hit in entry["hits"]}
    OUT.write_text(json.dumps({
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "https://packagist.org/search.json",
        "search_limit_per_query": LIMIT,
        "download_metric": "Packagist total downloads from the search response",
        "search": search,
        "search_hits_recorded": sum(len(entry["hits"]) for entry in search),
        "unique_search_hits": len(unique),
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
