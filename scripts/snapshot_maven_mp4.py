"""Capture bounded Java MP4 registry leads and pinned-release evidence.

Search hits are discovery leads, separate from parser verification. Successful
search windows survive a transient refresh failure, which remains visible.
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
DATA = ROOT / "data/java/mp4"
PARSERS = json.loads((DATA / "parsers.json").read_text())
QUERIES = ["mp4", "mp4 parser", "isoparser", "Java MP4", "ISO base media"]
NATIVE_ARTIFACTS = [("ffmpeg-macosx-arm64", "ffmpeg", "8.1.2-1.5.14"),
                    ("javacpp-macosx-arm64", "javacpp", "1.5.14")]
AUXILIARY_ARTIFACTS = [("jave-nativebin-osxm1", "ws.schild", "jave-nativebin-osxm1", "4.2.0")]


def get(url: str, timeout: int = 12) -> bytes:
    with urlopen(url, timeout=timeout) as response:
        return response.read()


def release(parser: dict) -> tuple[str, dict]:
    name, group, artifact, version = (parser[k] for k in ("name", "group", "artifact", "version"))
    base = f"https://repo.maven.apache.org/maven2/{group.replace('.', '/')}/{artifact}/{version}/"
    stem = f"{artifact}-{version}"
    local = Path.home() / ".m2/repository" / group.replace(".", "/") / artifact / version
    jar, pom = (local / f"{stem}.jar").read_bytes(), (local / f"{stem}.pom").read_bytes()
    assert sha1(jar).hexdigest() == get(base + stem + ".jar.sha1").decode().split()[0], name
    assert sha1(pom).hexdigest() == get(base + stem + ".pom.sha1").decode().split()[0], name
    ET.fromstring(pom)
    with ZipFile(BytesIO(get(parser["documentation"]))) as docs:
        assert parser["documentation_archive_entry"] in docs.namelist(), name
    return name, {
        "group": group, "artifact": artifact, "version": version,
        "jar_url": base + stem + ".jar", "jar_sha256": sha256(jar).hexdigest(),
        "pom_url": base + stem + ".pom", "pom_sha256": sha256(pom).hexdigest(),
        "license": parser["license"], "license_evidence": parser["license_evidence"],
    }


def native_release(item: tuple[str, str, str]) -> tuple[str, dict]:
    name, artifact, version = item
    group, classifier = "org.bytedeco", "macosx-arm64"
    base = f"https://repo.maven.apache.org/maven2/org/bytedeco/{artifact}/{version}/"
    stem = f"{artifact}-{version}"
    local = Path.home() / ".m2/repository/org/bytedeco" / artifact / version
    jar = (local / f"{stem}-{classifier}.jar").read_bytes()
    pom = (local / f"{stem}.pom").read_bytes()
    assert sha1(jar).hexdigest() == get(base + f"{stem}-{classifier}.jar.sha1").decode().split()[0]
    assert sha1(pom).hexdigest() == get(base + stem + ".pom.sha1").decode().split()[0]
    return name, {"group": group, "artifact": artifact, "version": version,
                  "classifier": classifier, "jar_url": base + f"{stem}-{classifier}.jar",
                  "jar_sha256": sha256(jar).hexdigest(), "pom_url": base + stem + ".pom",
                  "pom_sha256": sha256(pom).hexdigest()}


def auxiliary_release(item: tuple[str, str, str, str]) -> tuple[str, dict]:
    name, group, artifact, version = item
    base = f"https://repo.maven.apache.org/maven2/{group.replace('.', '/')}/{artifact}/{version}/"
    stem = f"{artifact}-{version}"
    local = Path.home() / ".m2/repository" / group.replace(".", "/") / artifact / version
    jar, pom = (local / f"{stem}.jar").read_bytes(), (local / f"{stem}.pom").read_bytes()
    assert sha1(jar).hexdigest() == get(base + stem + ".jar.sha1").decode().split()[0]
    assert sha1(pom).hexdigest() == get(base + stem + ".pom.sha1").decode().split()[0]
    ET.fromstring(pom)
    return name, {"group": group, "artifact": artifact, "version": version,
                  "jar_url": base + stem + ".jar", "jar_sha256": sha256(jar).hexdigest(),
                  "pom_url": base + stem + ".pom", "pom_sha256": sha256(pom).hexdigest(),
                  "license": "GPL-3.0-only", "license_evidence": "Maven POM licenses"}


def metric(parser: dict) -> tuple[str, dict]:
    name, group, artifact, version = (parser[k] for k in ("name", "group", "artifact", "version"))
    url = ("https://api.deps.dev/v3alpha/systems/MAVEN/packages/"
           + quote(f"{group}:{artifact}", safe="") + f"/versions/{version}:dependents")
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
    with ThreadPoolExecutor(max_workers=6) as pool:
        releases = dict(pool.map(release, PARSERS))
        native_releases = dict(pool.map(native_release, NATIVE_ARTIFACTS))
        auxiliary_releases = dict(pool.map(auxiliary_release, AUXILIARY_ARTIFACTS))
        metrics = dict(pool.map(metric, PARSERS))
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
        "search_surface": "Maven Central Solr bounded artifact queries; targeted official Maven releases and project docs",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": 100,
        "search": searches, "releases": releases,
        "native_releases": native_releases,
        "auxiliary_releases": auxiliary_releases,
        "external_tools": {"ffprobe": json.loads((ROOT / "data/java/wav/registry-snapshot.json").read_text())["external_tools"]["ffprobe"]},
        "popularity_metric": {
            "name": "deps.dev exact-version directDependentCount",
            "documentation": "https://docs.deps.dev/api/v3alpha/",
            "scope": "Known public direct dependents of pinned Maven releases; incomplete coverage and release-age bias",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "packages": metrics,
        },
    }
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Java MP4 snapshot: {sum(len(s['hits']) for s in searches)} search hits; {len(releases)} pinned releases")


if __name__ == "__main__":
    main()
