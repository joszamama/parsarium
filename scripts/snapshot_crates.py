"""Capture bounded crates.io discovery hits for a Rust format cell."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
QUERIES = {
    "png": ["png", "png decoder", "png reader", "png image", "png metadata", "libpng", "png chunk"],
    "zip": ["zip", "zip archive", "zip reader", "zip extract", "unzip", "libzip", "pkzip"],
    "wav": ["wav", "wave file", "wav reader", "wav decoder", "riff wave", "pcm wav", "waveform audio"],
    "mp3_id3v2": ["mp3", "id3v2", "id3", "mp3 decoder", "mpeg audio", "mp3 parser", "audio metadata"],
    "mp4": ["mp4", "mp4 parser", "isobmff", "mp4 reader", "mpeg4 container", "quicktime mov", "mp4 metadata"],
    "pdf": ["pdf", "pdf parser", "pdf reader", "pdf extract", "pdf render", "pdf document", "pdf text"],
    "svg": ["svg", "svg parser", "svg reader", "svg render", "svg image", "svg path", "svg xml"],
}


def fetch(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "Parsarium format parser research (https://github.com/joszamama/parsarium)"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> None:
    cell = sys.argv[1] if len(sys.argv) > 1 else ""
    if cell not in QUERIES:
        raise SystemExit("usage: python3 scripts/snapshot_crates.py png|zip|mp4|wav|pdf|svg|mp3_id3v2")
    search = []
    for query in QUERIES[cell]:
        url = "https://crates.io/api/v1/crates?" + urlencode({"q": query, "per_page": 100, "page": 1})
        data = fetch(url)
        search.append({
            "query": query, "url": url, "total": data["meta"]["total"], "limit": 100,
            "hits": [{
                "rank": rank, "name": crate["id"], "version": crate["max_version"],
                "description": crate.get("description") or "",
                "url": f"https://crates.io/crates/{crate['id']}",
                "recent_downloads": crate.get("recent_downloads"),
            } for rank, crate in enumerate(data["crates"], 1)],
        })
        print(f"{query}: {len(data['crates'])} of {data['meta']['total']}")
    directory = ROOT / "data" / "rust" / cell
    directory.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "crates.io API first page, default registry order",
        "search_api_docs": "https://crates.io/api/",
        "search_limit_per_query": 100,
        "search": search,
        "releases": {},
        "popularity_metric": {
            "name": "crates.io recent downloads (90 days)",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "packages": {},
        },
    }
    (directory / "registry-snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")


if __name__ == "__main__":
    main()
