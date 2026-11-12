"""Capture bounded Maven PNG leads, release hashes, and Java adoption signals.

Search hits never become verified parsers without documented API and control evidence.
The cached Maven artifact bytes are checked against Maven Central's published SHA-1
before their stronger SHA-256 is saved. Run after Maven has resolved the adapter.
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
DATA = ROOT / "data/java/png"
PARSERS = json.loads((DATA / "parsers.json").read_text())
QUERIES = ["png", "png parser", "png decoder", "png image reader", "Java PNG"]


def get(url: str, timeout: int = 12) -> bytes:
    with urlopen(url, timeout=timeout) as response:
        return response.read()


def release(parser: dict) -> tuple[str, dict]:
    name, group, artifact, version = (parser[k] for k in ("name", "group", "artifact", "version"))
    classifier = "mac-aarch64" if name == "javafx-graphics" else None
    stem = f"{artifact}-{version}" + (f"-{classifier}" if classifier else "")
    base = f"https://repo.maven.apache.org/maven2/{group.replace('.', '/')}/{artifact}/{version}/"
    local = Path.home() / ".m2/repository" / group.replace(".", "/") / artifact / version
    jar = (local / f"{stem}.jar").read_bytes()
    pom = (local / f"{artifact}-{version}.pom").read_bytes()
    jar_url = base + f"{stem}.jar"
    pom_url = base + f"{artifact}-{version}.pom"
    if sha1(jar).hexdigest() != get(jar_url + ".sha1").decode().strip():
        raise ValueError(f"Maven Central JAR SHA-1 mismatch: {name}")
    if sha1(pom).hexdigest() != get(pom_url + ".sha1").decode().strip():
        raise ValueError(f"Maven Central POM SHA-1 mismatch: {name}")
    ET.fromstring(pom)
    return name, {
        "group": group, "artifact": artifact, "version": version,
        "classifier": classifier, "jar_url": jar_url, "jar_sha256": sha256(jar).hexdigest(),
        "pom_url": pom_url, "pom_sha256": sha256(pom).hexdigest(),
        "license": parser["license"], "license_evidence": parser["license_evidence"],
    }


def metric(parser: dict) -> tuple[str, dict]:
    name, group, artifact, version = (parser[k] for k in ("name", "group", "artifact", "version"))
    package = quote(f"{group}:{artifact}", safe="")
    url = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{package}/versions/{version}:dependents"
    try:
        response = json.loads(get(url))
        value = response.get("directDependentCount")
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
        return {"query": query, "url": url, "limit": 100, "captured_at_utc": captured,
                "total": response["numFound"], "hits": hits}
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
        return {"query": query, "url": url, "limit": 100, "captured_at_utc": captured,
                "total": None, "hits": [], "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    with ThreadPoolExecutor(max_workers=8) as pool:
        releases = dict(pool.map(release, PARSERS))
        metrics = dict(pool.map(metric, PARSERS))
    # The legacy Solr endpoint intermittently stalls under concurrent requests.
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
        "search_surface": "Maven Central Solr artifact search; targeted Maven Central release lookups",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": 100, "search": searches, "releases": releases,
        "popularity_metric": {
            "name": "deps.dev version-level directDependentCount",
            "documentation": "https://docs.deps.dev/api/v3alpha/",
            "scope": "Known public direct dependents of the exact Maven release; incomplete coverage and version age bias",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(), "packages": metrics,
        },
    }
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Maven PNG snapshot: {sum(len(s['hits']) for s in searches)} saved search hits; "
          f"{len(releases)} pinned release lookups")


if __name__ == "__main__":
    main()
