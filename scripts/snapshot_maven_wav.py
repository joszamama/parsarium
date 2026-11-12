"""Capture bounded Java WAV discovery, pinned Maven releases, and adoption proxies.

Search results stay separate from accepted parsers. Run after Maven resolves the
adapter classpath. Existing successful search windows survive a transient refresh
failure, with the failed refresh recorded explicitly.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha1, sha256
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen
from zipfile import ZipFile
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/java/wav"
PARSERS = json.loads((DATA / "parsers.json").read_text())
QUERIES = ["wav", "wav parser", "wav reader", "Java WAV", "audio wav"]


def get(url: str, timeout: int = 12) -> bytes:
    with urlopen(url, timeout=timeout) as response:
        return response.read()


def release(parser: dict) -> tuple[str, dict]:
    name, group, artifact, version = (parser[k] for k in ("name", "group", "artifact", "version"))
    repository_url = parser.get("repository_url", "https://repo.maven.apache.org/maven2")
    base = f"{repository_url}/{group.replace('.', '/')}/{artifact}/{version}/"
    stem = f"{artifact}-{version}"
    local = Path.home() / ".m2/repository" / group.replace(".", "/") / artifact / version
    jar = (local / f"{stem}.jar").read_bytes()
    pom = (local / f"{stem}.pom").read_bytes()
    if sha1(jar).hexdigest() != get(base + stem + ".jar.sha1").decode().split()[0]:
        raise ValueError(f"Maven Central JAR SHA-1 mismatch: {name}")
    if sha1(pom).hexdigest() != get(base + stem + ".pom.sha1").decode().split()[0]:
        raise ValueError(f"Maven Central POM SHA-1 mismatch: {name}")
    ET.fromstring(pom)
    if parser.get("documentation_archive_entry"):
        with ZipFile(BytesIO(get(parser["documentation"]))) as docs:
            if parser["documentation_archive_entry"] not in docs.namelist():
                raise ValueError(f"Documented API missing from pinned Javadoc: {name}")
    return name, {
        "group": group, "artifact": artifact, "version": version,
        "repository_url": repository_url,
        "jar_url": base + stem + ".jar", "jar_sha256": sha256(jar).hexdigest(),
        "pom_url": base + stem + ".pom", "pom_sha256": sha256(pom).hexdigest(),
        "license": parser["license"], "license_evidence": parser["license_evidence"],
    }


def native_release(name: str, group: str, artifact: str, version: str,
                   classifier: str) -> tuple[str, dict]:
    base = f"https://repo.maven.apache.org/maven2/{group.replace('.', '/')}/{artifact}/{version}/"
    stem = f"{artifact}-{version}-{classifier}"
    local = Path.home() / ".m2/repository" / group.replace(".", "/") / artifact / version
    jar = (local / f"{stem}.jar").read_bytes()
    pom = (local / f"{artifact}-{version}.pom").read_bytes()
    if sha1(jar).hexdigest() != get(base + stem + ".jar.sha1").decode().split()[0]:
        raise ValueError(f"Maven Central native JAR SHA-1 mismatch: {name}")
    if sha1(pom).hexdigest() != get(base + f"{artifact}-{version}.pom.sha1").decode().split()[0]:
        raise ValueError(f"Maven Central native POM SHA-1 mismatch: {name}")
    return name, {
        "group": group, "artifact": artifact, "version": version,
        "classifier": classifier, "jar_url": base + stem + ".jar",
        "jar_sha256": sha256(jar).hexdigest(),
        "pom_url": base + f"{artifact}-{version}.pom",
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
    with ThreadPoolExecutor(max_workers=7) as pool:
        releases = dict(pool.map(release, PARSERS))
        metrics = dict(pool.map(metric, PARSERS))
        natives = dict(pool.map(lambda spec: native_release(*spec), [
            ("ffmpeg-macosx-arm64", "org.bytedeco", "ffmpeg", "8.1.2-1.5.14", "macosx-arm64"),
            ("javacpp-macosx-arm64", "org.bytedeco", "javacpp", "1.5.14", "macosx-arm64"),
        ]))
    with ThreadPoolExecutor(max_workers=5) as pool:
        searches = list(pool.map(search, QUERIES))
    dest = DATA / "registry-snapshot.json"
    if dest.exists():
        prior = {s["query"]: s for s in json.loads(dest.read_text())["search"]}
        for index, item in enumerate(searches):
            old = prior.get(item["query"])
            if not item["hits"] and old and old["hits"]:
                searches[index] = {**old,
                                   "latest_refresh_result": item.get("error", "zero hits"),
                                   "latest_refresh_at_utc": item["captured_at_utc"]}
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "Maven Central Solr bounded artifact queries; targeted official Maven Central releases and project docs",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": 100,
        "search": searches, "releases": releases,
        "native_releases": natives,
        "popularity_metric": {
            "name": "deps.dev exact-version directDependentCount",
            "documentation": "https://docs.deps.dev/api/v3alpha/",
            "scope": "Known public direct dependents of pinned Maven releases; incomplete coverage and release-age bias",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "packages": metrics,
        },
    }
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Java WAV snapshot: {sum(len(s['hits']) for s in searches)} search hits; "
          f"{len(releases)} pinned releases; {len(natives)} native artifacts")


if __name__ == "__main__":
    main()
