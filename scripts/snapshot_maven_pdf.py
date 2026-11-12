"""Save bounded Java PDF discovery, exact Maven releases, and adoption proxies.

The Maven Solr hits are leads only. Parsed packages are selected in parsers.json
after API documentation and a control run. Maven's SHA-1 is checked before the
stronger local SHA-256 is saved. Run after resolving the adapter modules.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha1, sha256
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/java/pdf"
PARSERS = json.loads((DATA / "parsers.json").read_text())
MAVEN_PARSERS = [p for p in PARSERS if p["group"] is not None]
QUERIES = ["pdf", "pdf parser", "pdf reader", "Java PDF", "pdfium"]


def get(url: str, timeout: int = 12) -> bytes:
    with urlopen(url, timeout=timeout) as response:
        return response.read()


def release(name: str, group: str, artifact: str, version: str,
            classifier: str | None = None) -> tuple[str, dict]:
    stem = f"{artifact}-{version}" + (f"-{classifier}" if classifier else "")
    base = f"https://repo.maven.apache.org/maven2/{group.replace('.', '/')}/{artifact}/{version}/"
    local = Path.home() / ".m2/repository" / group.replace(".", "/") / artifact / version
    jar = (local / f"{stem}.jar").read_bytes()
    pom = (local / f"{artifact}-{version}.pom").read_bytes()
    jar_url, pom_url = base + f"{stem}.jar", base + f"{artifact}-{version}.pom"
    if sha1(jar).hexdigest() != get(jar_url + ".sha1").decode().split()[0]:
        raise ValueError(f"Maven Central JAR SHA-1 mismatch: {name}")
    if sha1(pom).hexdigest() != get(pom_url + ".sha1").decode().split()[0]:
        raise ValueError(f"Maven Central POM SHA-1 mismatch: {name}")
    ET.fromstring(pom)
    return name, {
        "group": group, "artifact": artifact, "version": version,
        "classifier": classifier, "jar_url": jar_url,
        "jar_sha256": sha256(jar).hexdigest(), "pom_url": pom_url,
        "pom_sha256": sha256(pom).hexdigest(),
    }


def metric(parser: dict) -> tuple[str, dict]:
    name, group, artifact, version = (parser[k] for k in ("name", "group", "artifact", "version"))
    package = quote(f"{group}:{artifact}", safe="")
    url = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{package}/versions/{version}:dependents"
    try:
        value = json.loads(get(url, timeout=20)).get("directDependentCount")
        if not isinstance(value, int):
            raise ValueError("missing directDependentCount")
        return name, {"direct_dependent_count": value, "url": url}
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        return name, {"direct_dependent_count": None, "url": url,
                      "error": f"{type(exc).__name__}: {exc}"}


def search(query: str) -> dict:
    url = "https://search.maven.org/solrsearch/select?" + urlencode({
        "q": query, "rows": 100, "wt": "json",
    })
    captured = datetime.now(timezone.utc).isoformat()
    try:
        response = json.loads(get(url, timeout=8))["response"]
        hits = [{"rank": index, "name": item["id"],
                 "latest_version": item.get("latestVersion")}
                for index, item in enumerate(response["docs"], 1)]
        return {"query": query, "url": url, "limit": 100,
                "captured_at_utc": captured, "total": response["numFound"], "hits": hits}
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
        return {"query": query, "url": url, "limit": 100,
                "captured_at_utc": captured, "total": None, "hits": [],
                "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    with ThreadPoolExecutor(max_workers=8) as pool:
        releases = dict(pool.map(lambda p: release(p["name"], p["group"], p["artifact"], p["version"]),
                                 MAVEN_PARSERS))
        for parser in MAVEN_PARSERS:
            releases[parser["name"]]["license"] = parser["license"]
            releases[parser["name"]]["license_evidence"] = parser["license_evidence"]
        metrics = dict(pool.map(metric, MAVEN_PARSERS))
        natives = dict(pool.map(lambda a: release(*a), [
            ("pdfium4j-darwin-arm64", "org.grimmory", "pdfium4j", "1.3.0", "natives-darwin-arm64"),
            ("jpdfium-darwin-arm64", "com.stirling", "jpdfium-natives-darwin-arm64", "1.3.1", None),
        ]))
    searches = [search(query) for query in QUERIES]
    dest = DATA / "registry-snapshot.json"
    if dest.exists():
        previous = json.loads(dest.read_text())
        prior = {item["query"]: item for item in previous["search"]}
        for index, item in enumerate(searches):
            old = prior.get(item["query"])
            if not item["hits"] and old and old["hits"]:
                searches[index] = {**old,
                                   "latest_refresh_result": item.get("error", "zero hits"),
                                   "latest_refresh_at_utc": item["captured_at_utc"]}
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "Maven Central Solr bounded artifact queries; targeted Maven Central release lookups; PDF Clown official SourceForge release",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": 100,
        "search": searches,
        "releases": releases,
        "native_releases": natives,
        "non_maven_release": {
            "pdfclown": {
                "version": "0.1.2-Beta",
                "license": "LGPL-3.0",
                "url": "https://downloads.sourceforge.net/project/clown/PDFClown-devel/0.1.2%20Beta/PDFClown-0.1.2-Beta.zip",
                "archive_sha256": "3f6606ae17e66f6b1bdf39c15edc5f3fa6754365277c14a46affb9a1ce5750c2",
                "jar_entry": "PDFClown/java/pdfclown.lib/build/package/pdfclown.jar",
                "jar_sha256": "7d31b0c4fe4c188cd390c8f0137955f50d7c6d71ab673fcb39bee4285d4d9046",
                "version_evidence": "https://pdfclown.org/downloads/",
                "popularity_metric": None,
                "metric_limit": "No comparable deps.dev exact-version Maven direct-dependent count for this non-Maven release",
            }
        },
        "popularity_metric": {
            "name": "deps.dev version-level directDependentCount",
            "documentation": "https://docs.deps.dev/api/v3alpha/",
            "scope": "Known public direct dependents of exact Maven releases; incomplete coverage and version age bias",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "packages": metrics,
        },
    }
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Maven PDF snapshot: {sum(len(s['hits']) for s in searches)} search hits; "
          f"{len(releases)} Maven releases; {len(natives)} native artifacts")


if __name__ == "__main__":
    main()
