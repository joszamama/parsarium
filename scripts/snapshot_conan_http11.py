"""Snapshot bounded Conan recipe-name leads and C HTTP parser adoption signals."""

from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
import json


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/http11"
INDEX = "https://api.github.com/repos/conan-io/conan-center-index/git/trees/master?recursive=1"
REPOS = {"llhttp": "nodejs/llhttp", "http-parser": "nodejs/http-parser",
         "picohttpparser": "h2o/picohttpparser", "mongoose": "cesanta/mongoose",
         "httpp": "cebem1nt/httpp"}


def get(url: str) -> dict:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium C HTTP/1.1 catalog"}), timeout=30) as response:
        return json.load(response)


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    lock = json.loads((DATA / "source-lock.json").read_text())
    tree = get(INDEX)["tree"]
    names = sorted({item["path"].split("/")[1] for item in tree
                    if item["path"].startswith("recipes/") and len(item["path"].split("/")) >= 2})
    searches = []
    for query in ("http", "llhttp", "pico", "parser"):
        matches = [name for name in names if query in name.lower()]
        searches.append({"query": query,
                         "url": "https://github.com/conan-io/conan-center-index/tree/master/recipes",
                         "method": "literal case-insensitive recipe-name substring; alphabetic, not usage ranked",
                         "total": len(matches), "limit": 100,
                         "hits": [{"rank": index, "name": name,
                                   "url": f"https://conan.io/center/recipes/{name}"}
                                  for index, name in enumerate(matches[:100], 1)]})
    metrics = {}
    for name, repo in REPOS.items():
        url = f"https://api.github.com/repos/{repo}"
        metrics[name] = {"stars": get(url)["stargazers_count"], "url": url}
    snapshot = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "Conan Center Index recipe tree; exact GitHub API response, with upstream docs for targeted leads",
        "search_index_api": INDEX, "search_limit_per_query": 100, "search": searches,
        "releases": {p["name"]: {"version": p["version"], "license": p["license"],
                                  "source_url": lock[p["name"]]["source_url"],
                                  "source_sha256": lock[p["name"]]["source_sha256"],
                                  "license_evidence": p["license_evidence"]} for p in parsers},
        "popularity_metric": {
            "name": "GitHub stargazers_count of primary upstream repository",
            "scope": "Project-level interest proxy within C only; not downloads, package installs or independent parser use",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(), "packages": metrics}}
    (DATA / "registry-snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    ranked = sorted(parsers, key=lambda parser: (-metrics[parser["name"]]["stars"], parser["name"]))
    lines = ["# C × HTTP/1.1: verified parser ranking", "",
             f"{len(ranked)} verified package paths; working goal 20, original ceiling 30. "
             "GitHub stars are project-level interest signals captured at "
             f"{snapshot['popularity_metric']['captured_at_utc']}; they are compared only within C. "
             "They are not downloads or a measure of actual parser use.", "",
             "Search hits, unresolved leads, and C standard APIs are separate from this ranking. "
             "See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.", "",
             "| Rank | Package | Pinned release | Stars | Scope | Underlying family |",
             "| ---: | --- | --- | ---: | --- | --- |"]
    for index, parser in enumerate(ranked, 1):
        lines.append(f"| {index} | [{parser['name']}]({parser['documentation']}) | "
                     f"{parser['version']} | {metrics[parser['name']]['stars']:,} | "
                     f"{parser['scope']} | {parser['family']} |")
    (DATA / "ranking.md").write_text("\n".join(lines) + "\n")
    print(f"Saved {sum(len(row['hits']) for row in searches)} recipe hits; {len(metrics)} upstream metrics")


if __name__ == "__main__":
    main()
