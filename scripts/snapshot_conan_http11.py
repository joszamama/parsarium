"""Snapshot bounded Conan recipe-name leads and C HTTP parser adoption signals."""

from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
import json
from render_c_http11_ranking import render


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/http11"
INDEX = "https://api.github.com/repos/conan-io/conan-center-index/git/trees/master?recursive=1"
REPOS = {"llhttp": "nodejs/llhttp", "http-parser": "nodejs/http-parser",
         "picohttpparser": "h2o/picohttpparser", "mongoose": "cesanta/mongoose",
         "httpp": "cebem1nt/httpp", "HTTPParserC": "Building42/HTTPParserC",
         "libmicrohttpd": None, "libevhtp": "ellzey/libevhtp", "libhtp": "OISF/libhtp",
         "libwebsockets": "warmcat/libwebsockets", "libonion": "davidmoreno/onion",
         "libsoup": None, "serf": None, "facil-cstl": "facil-io/cstl",
         "facil-legacy": "boazsegev/facil.io"}
NO_GITHUB_REASON = {
    "libmicrohttpd": "Official upstream is git.gnunet.org, not a primary GitHub repository",
    "libsoup": "Primary upstream is GNOME GitLab; no comparable primary GitHub star count",
    "serf": "Primary upstream is Apache Subversion; no comparable primary GitHub star count",
}


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
        if repo is None:
            metrics[name] = {"stars": None, "url": None,
                             "reason": NO_GITHUB_REASON[name]}
        else:
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
    (DATA / "ranking.md").write_text(render(parsers, snapshot))
    print(f"Saved {sum(len(row['hits']) for row in searches)} recipe hits; {len(metrics)} upstream metrics")


if __name__ == "__main__":
    main()
