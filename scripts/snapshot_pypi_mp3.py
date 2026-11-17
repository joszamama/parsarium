"""Capture bounded PyPI plain-MP3 leads and PyPI Stats last-month downloads."""

from datetime import datetime, timezone
import json
from pathlib import Path
import time
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/python/mp3/registry-snapshot.json"
QUERIES = ("mp3", "mpeg", "mpg123", "minimp3", "layer3")
# Packages that the former MP3-with-ID3v2 Python cell already reached through its own
# documented local-file APIs, plus pure-Python leads named in project docs.
CANDIDATES = ("mutagen", "tinytag", "av", "soundfile", "pydub", "audioread",
              "librosa", "pygame", "miniaudio", "eyed3", "pymediainfo",
              "hachoir", "minimp3", "pymp3", "mp3")


def fetch(url: str, accept: str = "application/json") -> dict:
    request = urllib.request.Request(url, headers={"Accept": accept,
                                                   "User-Agent": "parsarium-snapshot"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def main() -> None:
    index = fetch("https://pypi.org/simple/", "application/vnd.pypi.simple.v1+json")
    names = sorted((item["name"] for item in index["projects"]), key=str.lower)
    search = [{"query": f"project name contains '{query}'",
               "total": len(hits := [name for name in names if query in name.lower()]),
               "hits": hits}
              for query in QUERIES]
    packages = {}
    for name in CANDIDATES:
        try:
            meta = fetch(f"https://pypi.org/pypi/{name}/json")
        except Exception as exc:
            packages[name] = {"error": str(exc)}
            continue
        info = meta["info"]
        try:
            downloads = fetch(f"https://pypistats.org/api/packages/{name}/recent?period=month")
            last_month = downloads["data"]["last_month"]
        except Exception as exc:
            last_month = None
            info["stats_error"] = str(exc)
        packages[name] = {
            "version": info["version"],
            "license_expression": info.get("license_expression"),
            "summary": info.get("summary"),
            "requires_dist": info.get("requires_dist"),
            "files": [{"filename": item["filename"], "sha256": item["digests"]["sha256"]}
                      for item in meta["urls"]],
            "downloads_last_month": last_month,
            "stats_url": f"https://pypistats.org/api/packages/{name}/recent?period=month",
            **({"stats_error": info["stats_error"]} if "stats_error" in info else {}),
        }
        time.sleep(1)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "PyPI Simple JSON project-name index, filtered locally by case-insensitive substring; no relevance ranking",
        "search_api_docs": "https://docs.pypi.org/api/index-api/",
        "search_index_serial": index.get("meta", {}).get("_last-serial"),
        "search": search,
        "candidate_basis": "Packages with documented local MP3 APIs already reached in data/python/mp3, plus decoder names from the queries; looked up individually",
        "metric": "PyPI Stats last_month downloads excluding known mirrors",
        "metric_docs": "https://pypistats.org/api/",
        "packages": packages,
    }, indent=2) + "\n")
    print(json.dumps({name: item.get("downloads_last_month") for name, item in packages.items()}))


if __name__ == "__main__":
    main()
