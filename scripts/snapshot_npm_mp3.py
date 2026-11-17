"""Capture the bounded npm search and 30-day download counts for the JavaScript plain MP3 pilot."""

from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import quote
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/javascript/mp3/registry-snapshot.json"
QUERIES = ["mp3 parser", "mpeg audio", "mp3 decoder", "mp3 frame", "mp3 duration", "mp3 demuxer"]
WINDOW = "2026-10-17:2026-11-15"
CANDIDATES = ["mediabunny", "music-metadata", "codec-parser", "mpg123-decoder", "audio-decode",
              "@audio/decode-mp3", "@audio/decode", "mp3-duration", "get-mp3-duration", "mp3-parser",
              "is-mp3", "mp3", "js-mp3", "minimp3", "mpeg-frame-parser"]


def fetch(url: str) -> dict:
    result = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
                             "--max-time", "60", url], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main() -> None:
    search = []
    for query in QUERIES:
        url = f"https://registry.npmjs.org/-/v1/search?text={quote(query)}&size=100&from=0"
        data = fetch(url)
        search.append({"query": query, "url": url, "total": data["total"], "hits": [
            {"rank": i + 1, "name": o["package"]["name"], "version": o["package"]["version"],
             "description": o["package"].get("description") or ""}
            for i, o in enumerate(data["objects"])]})
    downloads = {}
    for name in CANDIDATES:
        url = f"https://api.npmjs.org/downloads/point/{WINDOW}/{name}"
        data = fetch(url)
        latest = fetch(f"https://registry.npmjs.org/{quote(name, safe='@')}/latest")
        downloads[name] = {"downloads": data.get("downloads"), "start": data.get("start"),
                           "end": data.get("end"), "url": url, "latest_version": latest.get("version"),
                           "license": latest.get("license")}
    hits = [hit["name"] for entry in search for hit in entry["hits"]]
    OUT.write_text(json.dumps({
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_api_docs": "https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md",
        "downloads_api_docs": "https://github.com/npm/registry/blob/main/docs/download-counts.md",
        "search_limit_per_query": 100, "metric_window": WINDOW,
        "search_hits_recorded": len(hits), "unique_search_hits": len(set(hits)),
        "search": search, "downloads": downloads}, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(hits)} hits, {len(set(hits))} unique; "
          + ", ".join(f"{n}={d['downloads']}" for n, d in downloads.items()))


if __name__ == "__main__":
    main()
