#!/usr/bin/env python3
"""Capture bounded registry searches and adoption metrics for the TOML pilot.

Writes data/<ecosystem>/toml/registry-snapshot.json for each named ecosystem
(default: all eight). Every query keeps at most the first 100 hits. Each
ecosystem's adoption metric is the one its JSON and XML pilot cells use:

* C, C++: Debian popcon installation counts (source-package sourcemax and
  binary-package tables), searched by package-name substring;
* Go: pkg.go.dev "Imported by" from the search snippets;
* Java: deps.dev directDependentCount summed over all releases (leads only);
* JavaScript: npm downloads over the last month (leads and hits);
* Python: PyPI Stats last_month downloads, mirrors excluded (leads only);
* Rust: crates.io 90-day recent downloads from the search API;
* PHP: Packagist lifetime downloads from the search API.

Search hits and leads are not verified parsers. Network access is required
(the macOS python.org build needs SSL_CERT_FILE=/etc/ssl/cert.pem).
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import gzip
from hashlib import sha256
import html
import json
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
UA = "parsarium-research (toml pilot)"
LIMIT = 100
QUERIES = {
    "go": ["toml", "toml parser", "toml decoder"],
    "java": ["toml", "toml parser"],
    "javascript": ["toml", "toml parser", "toml parse"],
    "rust": ["toml", "toml parser", "toml deserialize"],
    "php": ["toml", "toml parser"],
}
# Named leads whose primary metric is looked up individually.
JAVA_LEADS = ("org.tomlj:tomlj", "com.fasterxml.jackson.dataformat:jackson-dataformat-toml",
              "com.moandjiezana.toml:toml4j", "com.electronwill.night-config:toml",
              "io.hotmoka:toml4j", "cc.ekblad:4koma", "net.peanuuutz.tomlkt:tomlkt",
              "com.akuleshov7:ktoml-core", "io.github.wasabithumb:jtoml")
PYTHON_LEADS = ("tomli", "tomlkit", "toml", "rtoml", "pytomlpp", "qtoml", "tomli-w",
                "toml-rs", "pytoml", "tomlrs", "tomllib")
JS_LEADS = ("smol-toml", "@iarna/toml", "toml", "@ltd/j-toml", "toml-eslint-parser",
            "@taplo/lib", "js-toml", "toml-j0.4", "tomlify-j0.4", "@std/toml", "fast-toml")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get(url: str, accept: str | None = None) -> bytes:
    headers = {"User-Agent": UA, **({"Accept": accept} if accept else {})}
    request = urllib.request.Request(url, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = response.read()
                if response.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz"):
                    try:
                        data = gzip.decompress(data)
                    except OSError:
                        pass
                return data
        except urllib.error.HTTPError as error:
            if error.code in (429, 502, 503) and attempt < 4:
                time.sleep(5 * (attempt + 1))
                continue
            raise
        except (TimeoutError, OSError):
            if attempt == 4:
                raise
            time.sleep(2)
    raise AssertionError


def getj(url: str, accept: str | None = None):
    return json.loads(get(url, accept))


def popcon(table_url: str) -> tuple[list[dict], dict]:
    raw = get(table_url)
    rows = []
    for line in raw.decode("latin-1").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) < 7 or not all(part.isdigit() for part in (parts[0], *parts[2:7])):
            continue
        rows.append({"rank": int(parts[0]), "name": parts[1], "inst": int(parts[2]),
                     "vote": int(parts[3]), "old": int(parts[4]), "recent": int(parts[5]),
                     "no_files": int(parts[6])})
    return rows, {"url": table_url, "sha256": sha256(raw).hexdigest(), "rows": len(rows)}


def debian() -> dict:
    sources, source_meta = popcon("https://popcon.debian.org/sourcemax/by_inst.gz")
    binaries, binary_meta = popcon("https://popcon.debian.org/by_inst.gz")
    conan = getj("https://api.github.com/repos/conan-io/conan-center-index/git/trees/master?recursive=1")
    recipes = sorted({item["path"].split("/")[1] for item in conan["tree"]
                      if item["path"].startswith("recipes/") and item["path"].count("/") >= 1})
    search = []
    for label, rows, meta in (("source", sources, source_meta), ("binary", binaries, binary_meta)):
        hits = [row for row in rows if "toml" in row["name"].lower()]
        search.append({"query": "toml", "method": f"case-insensitive substring 'toml' in Debian {label}-package "
                       "names; ordered by popcon installations", "url": meta["url"],
                       "snapshot_sha256": meta["sha256"], "total": len(hits), "limit": LIMIT,
                       "hits": hits[:LIMIT]})
    matches = [name for name in recipes if "toml" in name.lower()]
    search.append({"query": "toml", "method": "case-insensitive Conan Center recipe-name substring; alphabetic, "
                   "not usage ranked (discovery only)",
                   "url": "https://github.com/conan-io/conan-center-index/tree/master/recipes",
                   "index_tree_sha": conan.get("sha"), "total": len(matches), "limit": LIMIT,
                   "hits": [{"rank": i, "name": name} for i, name in enumerate(matches[:LIMIT], 1)]})
    return {"search_surface": "Debian popcon source (sourcemax) and binary installation tables plus "
            "Conan Center recipe names; shared by the C and C++ cells",
            "adoption_metric": {"name": "Debian popcon installations (sourcemax/by_inst for source packages; "
                                "by_inst for binary packages)", "sources": [source_meta, binary_meta]},
            "search": search}


def gopkg() -> dict:
    search = []
    for query in QUERIES["go"]:
        url = f"https://pkg.go.dev/search?q={urllib.parse.quote(query)}&limit={LIMIT}&m=package"
        page = get(url).decode("utf-8", "replace")
        hits = []
        for block in page.split('class="SearchSnippet"')[1:]:
            match = re.search(r'data-clicked-package="([^"]+)"', block)
            if not match:
                continue
            imported = re.search(r'Imported by[\s\S]*?<strong>([\d,]+)</strong>', block)
            version = re.search(r'data-test-id="snippet-version"[^>]*>\s*([^<\s]+)', block)
            hits.append({"rank": len(hits) + 1, "name": html.unescape(match.group(1)),
                         "version": version.group(1) if version else None,
                         "imported_by": int(imported.group(1).replace(",", "")) if imported else None})
        search.append({"query": query, "url": url, "total": None, "limit": LIMIT,
                       "total_note": "The HTML page does not state a total; null means not displayed.",
                       "captured_at_utc": now(), "hits": hits[:LIMIT]})
        time.sleep(2)
    return {"search_surface": "pkg.go.dev public HTML package search (relevance order)",
            "search_api_docs": "https://pkg.go.dev/search-help", "search": search,
            "adoption_metric": {"name": "pkg.go.dev Imported by package count",
                                "definition": "Importer count shown in the search snippet at capture time"}}


def deps_dev(coordinate: str) -> dict:
    name = urllib.parse.quote(coordinate, safe="")
    base = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{name}"
    try:
        versions = getj(base)["versions"]
    except urllib.error.HTTPError as error:
        return {"error": f"HTTP {error.code}", "url": base, "captured_at_utc": now()}
    default = next((item["versionKey"]["version"] for item in versions if item.get("isDefault")), None)

    def count(version: str) -> tuple[str, int]:
        url = f"{base}/versions/{urllib.parse.quote(version, safe='')}:dependents"
        return version, getj(url).get("directDependentCount", 0)

    with ThreadPoolExecutor(8) as pool:
        counts = dict(pool.map(count, [item["versionKey"]["version"] for item in versions]))
    peak = max(counts, key=counts.get)
    return {"default_version": default, "releases": len(counts),
            "summed_direct_dependent_count": sum(counts.values()),
            "max_release": peak, "max_release_direct_dependent_count": counts[peak],
            "default_release_direct_dependent_count": counts.get(default),
            "url": base, "captured_at_utc": now()}


def maven() -> dict:
    search = []
    for query in QUERIES["java"]:
        url = f"https://search.maven.org/solrsearch/select?q={urllib.parse.quote(query)}&rows={LIMIT}&wt=json"
        try:
            response = getj(url)["response"]
            search.append({"query": query, "url": url, "total": response["numFound"], "limit": LIMIT,
                           "captured_at_utc": now(),
                           "hits": [{"rank": i + 1, "name": f"{doc['g']}:{doc['a']}",
                                     "latest_version": doc.get("latestVersion")}
                                    for i, doc in enumerate(response["docs"])]})
        except Exception as error:  # recorded, not hidden
            search.append({"query": query, "url": url, "error": repr(error)[:300]})
    return {"search_surface": "Maven Central Solr artifact search; targeted deps.dev lookups for named leads",
            "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/", "search": search,
            "popularity_metric": {"name": "deps.dev directDependentCount summed over all releases",
                                  "documentation": "https://docs.deps.dev/api/v3alpha/",
                                  "scope": "Sum over every Maven release of the version-level directDependentCount; "
                                           "the maximum and default-release counts are recorded beside it",
                                  "packages": {coordinate: deps_dev(coordinate) for coordinate in JAVA_LEADS}}}


def npm_downloads(names: list[str]) -> dict:
    out = {}
    for name in names:
        url = f"https://api.npmjs.org/downloads/point/last-month/{urllib.parse.quote(name, safe='@/')}"
        try:
            data = getj(url)
            out[name] = {"downloads": data.get("downloads"), "start": data.get("start"), "end": data.get("end"),
                         "url": url}
        except urllib.error.HTTPError as error:
            out[name] = {"downloads": None, "error": f"HTTP {error.code}", "url": url}
        time.sleep(0.2)
    return out


def npm() -> dict:
    search = []
    names = set(JS_LEADS)
    for query in QUERIES["javascript"]:
        url = f"https://registry.npmjs.org/-/v1/search?text={urllib.parse.quote(query)}&size={LIMIT}&from=0"
        data = getj(url)
        hits = [{"rank": i + 1, "name": item["package"]["name"], "version": item["package"].get("version"),
                 "description": (item["package"].get("description") or "")[:160]}
                for i, item in enumerate(data["objects"])]
        names.update(hit["name"] for hit in hits)
        search.append({"query": query, "url": url, "total": data.get("total"), "limit": LIMIT,
                       "ordering": "npm registry search default relevance order", "captured_at_utc": now(),
                       "hits": hits})
    downloads = npm_downloads(sorted(names))
    for record in search:
        for hit in record["hits"]:
            hit["downloads_last_month"] = downloads[hit["name"]]["downloads"]
    return {"search_surface": "npm registry search API",
            "search_api_docs": "https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md",
            "search": search,
            "adoption_metric": {"name": "npm downloads, last month",
                                "documentation": "https://github.com/npm/registry/blob/main/docs/download-counts.md",
                                "packages": downloads}}


def pypi() -> dict:
    url = "https://pypi.org/simple/"
    index = getj(url, "application/vnd.pypi.simple.v1+json")
    names = sorted((project["name"] for project in index["projects"]), key=str.lower)
    matches = [name for name in names if "toml" in name.lower()]
    metrics = {}
    for name in PYTHON_LEADS:
        source = f"https://pypistats.org/api/packages/{name}/recent"
        try:
            release = getj(f"https://pypi.org/pypi/{name}/json")["info"]["version"]
        except urllib.error.HTTPError as error:
            metrics[name] = {"value": None, "error": f"PyPI HTTP {error.code}"}
            continue
        try:
            value = getj(source)["data"]["last_month"]
            metrics[name] = {"value": value, "latest_release_observed": release, "source": source,
                             "observed_at_utc": now()}
        except urllib.error.HTTPError as error:
            metrics[name] = {"value": None, "latest_release_observed": release, "source": source,
                             "error": f"HTTP {error.code}"}
        time.sleep(1.5)
    return {"search_surface": "PyPI Simple JSON project-name index, filtered locally; no relevance ranking",
            "search_api_docs": "https://docs.pypi.org/api/index-api/",
            "search_index_serial": index.get("meta", {}).get("_last-serial"),
            "search": [{"query": "project name contains 'toml'", "url": url, "total": len(matches),
                        "limit": LIMIT, "ordering": "case-insensitive project-name order; not a popularity order",
                        "captured_at_utc": now(),
                        "hits": [{"rank": i + 1, "name": name} for i, name in enumerate(matches[:LIMIT])]}],
            "adoption_metric": {"name": "PyPI Stats last_month downloads excluding known mirrors",
                                "documentation": "https://pypistats.org/api/", "packages": metrics}}


def crates() -> dict:
    search = []
    for query in QUERIES["rust"]:
        url = f"https://crates.io/api/v1/crates?q={urllib.parse.quote(query)}&per_page={LIMIT}&page=1"
        data = getj(url)
        search.append({"query": query, "url": url, "total": data["meta"]["total"], "limit": LIMIT,
                       "ordering": "crates.io default (relevance) order", "captured_at_utc": now(),
                       "hits": [{"rank": i + 1, "name": crate["name"],
                                 "version": crate.get("max_stable_version") or crate.get("max_version"),
                                 "description": (crate.get("description") or "")[:160],
                                 "recent_downloads": crate.get("recent_downloads"),
                                 "downloads_all_time": crate.get("downloads")}
                                for i, crate in enumerate(data["crates"])]})
        time.sleep(1)
    return {"search_surface": "crates.io API first page, default registry order",
            "search_api_docs": "https://crates.io/data-access", "search": search,
            "adoption_metric": {"name": "crates.io recent downloads (90 days)",
                                "definition": "recent_downloads returned by the search API at capture time"}}


def packagist() -> dict:
    search = []
    for query in QUERIES["php"]:
        url = f"https://packagist.org/search.json?q={urllib.parse.quote(query)}&per_page={LIMIT}"
        data = getj(url)
        search.append({"query": query, "url": url, "total": data.get("total"), "limit": LIMIT,
                       "ordering": "Packagist search default order", "captured_at_utc": now(),
                       "hits": [{"rank": i + 1, "name": item["name"], "description": (item.get("description") or "")[:160],
                                 "downloads_lifetime": item.get("downloads"), "favers": item.get("favers")}
                                for i, item in enumerate(data["results"])]})
    return {"search_surface": "Packagist public search JSON API", "search_api_docs": "https://packagist.org/apidoc",
            "search": search,
            "adoption_metric": {"name": "Packagist total downloads",
                                "definition": "Lifetime downloads of all releases, as returned by search.json"}}


CAPTURES = {"c": debian, "cpp": debian, "go": gopkg, "java": maven, "javascript": npm,
            "python": pypi, "rust": crates, "php": packagist}


def main() -> None:
    shared = {}
    for ecosystem in sys.argv[1:] or CAPTURES:
        started = now()
        capture = CAPTURES[ecosystem]
        if capture is debian and "debian" in shared:
            snapshot = shared["debian"]
        else:
            snapshot = capture()
            if capture is debian:
                shared["debian"] = snapshot
        out = ROOT / "data" / ecosystem / "toml" / "registry-snapshot.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        record = {"ecosystem": ecosystem, "format": "toml", "captured_at_utc": started,
                  "search_limit_per_query": LIMIT,
                  "note": "Search hits and leads are not verified parsers.", **snapshot}
        out.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
        print(ecosystem, [(item.get("query"), item.get("total"), len(item.get("hits", [])), item.get("error"))
                          for item in record["search"]])


if __name__ == "__main__":
    main()
