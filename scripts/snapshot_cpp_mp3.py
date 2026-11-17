"""Capture the bounded Homebrew search for C++ plain MP3 frame-parser leads.

Each query is matched case-insensitively against formula name and description
in the Homebrew formula API. Every hit records its stable version, license,
source URL and checksum, and its 365-day install-on-request count.
"""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/cpp/mp3/registry-snapshot.json"
FORMULAE = "https://formulae.brew.sh/api/formula.json"
ANALYTICS = "https://formulae.brew.sh/api/analytics/install-on-request/365d.json"
QUERIES = ("mp3", "mpeg audio", "layer iii", "taglib", "mp3splt", "mp3val")
GITHUB = ()


def fetch(url: str):
    result = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
                             "--max-time", "60", "-A", "parsarium-snapshot", url],
                            capture_output=True, check=True)
    return json.loads(result.stdout)


def main() -> None:
    formulae = fetch(FORMULAE)
    analytics = fetch(ANALYTICS)
    counts = {item["formula"]: int(str(item["count"]).replace(",", ""))
              for item in analytics["items"]}
    search = []
    for query in QUERIES:
        hits = [f for f in formulae
                if query in f"{f['name']} {f.get('desc') or ''}".lower()]
        hits.sort(key=lambda f: (-counts.get(f["name"], 0), f["name"]))
        search.append({"query": query, "total": len(hits), "hits": [{
            "name": f["name"], "version": f["versions"]["stable"],
            "description": f.get("desc"), "license": f.get("license"),
            "homepage": f.get("homepage"),
            "source_url": f["urls"]["stable"]["url"],
            "source_sha256": f["urls"]["stable"].get("checksum"),
            "install_on_request_365d": counts.get(f["name"], 0),
        } for f in hits]})
    github = []
    for repo in GITHUB:
        data = fetch(f"https://api.github.com/repos/{repo}")
        github.append({"repository": repo, "stargazers_count": data["stargazers_count"],
                       "forks_count": data["forks_count"], "license": (data.get("license") or {}).get("spdx_id"),
                       "pushed_at": data["pushed_at"], "url": data["html_url"]})
    OUT.write_text(json.dumps({
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "Homebrew formula API, case-insensitive substring match on name and description",
        "search_api_docs": "https://formulae.brew.sh/docs/api/",
        "metric": "Homebrew install-on-request count (365 days)",
        "analytics_url": ANALYTICS,
        "analytics_window": [analytics["start_date"], analytics["end_date"]],
        "search": search,
        "supplemental_github": github,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
