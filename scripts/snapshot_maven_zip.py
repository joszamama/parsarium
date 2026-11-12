"""Capture pinned Maven Central release evidence and deps.dev Java adoption signals.

The Maven Central Solr search endpoint is attempted separately from targeted
artifact lookups. A failed search records no hits and never implies that no
packages exist. This script intentionally does not promote a search hit into a
verified parser; see parsers.json and verify_java_zip.py for that decision.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen
import json
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data/java/zip/registry-snapshot.json"
COORDS = {
    "commons-compress": ("org.apache.commons", "commons-compress", "1.28.0"),
    "zip4j": ("net.lingala.zip4j", "zip4j", "2.11.6"),
    "zt-zip": ("org.zeroturnaround", "zt-zip", "1.18.2"),
    "lljzip": ("software.coley", "lljzip", "2.1.0"),
    "ant": ("org.apache.ant", "ant", "1.10.18"),
    "commons-vfs2": ("org.apache.commons", "commons-vfs2", "2.10.0"),
    "zip4jvm": ("ru.oleg-cherednik.zip4jvm", "zip4jvm", "1.13"),
    "quarkus-fs-util": ("io.quarkus", "quarkus-fs-util", "1.4.2"),
    "plexus-archiver": ("org.codehaus.plexus", "plexus-archiver", "4.15.0"),
    "jarchivelib": ("org.rauschig", "jarchivelib", "1.2.0"),
    "compress4j": ("com.hominux", "compress4j", "5.1.0"),
    "arcana": ("io.github.realburst", "arcana", "1.1.0"),
    "tika-parser-pkg-module": ("org.apache.tika", "tika-parser-pkg-module", "4.2.0"),
    "truezip-driver-zip": ("de.schlichtherle.truezip", "truezip-driver-zip", "7.7.10"),
    "commons-archive": ("io.github.deepakdaneva.commons", "commons-archive", "1.1.0"),
    "truezip-utils": ("org.codehaus.mojo", "truezip-utils", "1.2"),
    "simplezip": ("com.j256.simplezip", "simplezip", "2.2"),
    "tinyzip-core": ("io.github.bitstorm", "tinyzip-core", "1.0.0"),
    "sevenzipjbinding": ("net.sf.sevenzipjbinding", "sevenzipjbinding", "23.01-2.2"),
    "truevfs-driver-zip": ("net.java.truevfs", "truevfs-driver-zip", "0.14.0"),
}
LICENSES = {
    "commons-compress": ("Apache-2.0", "Maven release JAR META-INF/LICENSE.txt"),
    "zip4j": ("Apache-2.0", "Maven release POM licenses"),
    "zt-zip": ("Apache-2.0", "Maven release POM licenses"),
    "lljzip": ("MIT", "Maven release POM licenses"),
    "ant": ("Apache-2.0", "Maven release JAR META-INF/LICENSE.txt"),
    "commons-vfs2": ("Apache-2.0", "Maven release JAR META-INF/LICENSE.txt"),
    "zip4jvm": ("Apache-2.0", "Maven release POM licenses"),
    "quarkus-fs-util": ("Apache-2.0", "Maven release POM licenses"),
    "plexus-archiver": ("Apache-2.0", "https://github.com/codehaus-plexus/plexus-archiver"),
    "jarchivelib": ("Apache-2.0", "https://github.com/thrau/jarchivelib/blob/master/LICENSE"),
    "compress4j": ("Apache-2.0", "Maven release POM licenses"),
    "arcana": ("Apache-2.0", "Maven release POM licenses"),
    "tika-parser-pkg-module": ("Apache-2.0", "Maven release JAR META-INF/LICENSE"),
    "truezip-driver-zip": ("EPL-1.0", "https://christian-schlichtherle.bitbucket.io/truezip/"),
    "commons-archive": ("Apache-2.0", "Maven release JAR META-INF/LICENSE"),
    "truezip-utils": ("Apache-2.0", "https://www.mojohaus.org/truezip/truezip-maven-plugin/dependencies.html"),
    "simplezip": ("ISC", "Maven release POM licenses"),
    "tinyzip-core": ("Apache-2.0", "Maven release POM licenses"),
    "sevenzipjbinding": ("LGPL-2.1", "Maven release POM licenses; unRAR restriction also declared"),
    "truevfs-driver-zip": ("Apache-2.0", "Maven release POM licenses"),
}
QUERIES = ["zip parser", "zip archive", "zip reader", "Java ZIP"]


def get(url: str, timeout: int = 15) -> bytes:
    with urlopen(url, timeout=timeout) as response:
        return response.read()


def release(item: tuple[str, tuple[str, str, str]]) -> tuple[str, dict]:
    name, (group, artifact, version) = item
    base = f"https://repo.maven.apache.org/maven2/{group.replace('.', '/')}/{artifact}/{version}/"
    jar_url = f"{base}{artifact}-{version}.jar"
    pom_url = f"{base}{artifact}-{version}.pom"
    jar = get(jar_url)
    pom = get(pom_url)
    ET.fromstring(pom)
    license_id, license_evidence = LICENSES[name]
    return name, {
        "group": group,
        "artifact": artifact,
        "version": version,
        "jar_url": jar_url,
        "jar_sha256": sha256(jar).hexdigest(),
        "pom_url": pom_url,
        "pom_sha256": sha256(pom).hexdigest(),
        "license": license_id,
        "license_evidence": license_evidence,
    }


def metric(item: tuple[str, tuple[str, str, str]]) -> tuple[str, dict]:
    name, (group, artifact, version) = item
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
    try:
        response = json.loads(get(url, timeout=8))
        payload = response["response"]
        hits = [{"rank": index, "name": item["id"],
                 "latest_version": item.get("latestVersion")}
                for index, item in enumerate(payload["docs"], 1)]
        return {"query": query, "url": url, "limit": 100,
                "captured_at_utc": datetime.now(timezone.utc).isoformat(),
                "total": payload["numFound"], "hits": hits}
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
        return {"query": query, "url": url, "limit": 100,
                "captured_at_utc": datetime.now(timezone.utc).isoformat(), "total": None,
                "hits": [], "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    with ThreadPoolExecutor(max_workers=8) as pool:
        releases = dict(pool.map(release, COORDS.items()))
        metrics = dict(pool.map(metric, COORDS.items()))
        searches = list(pool.map(search, QUERIES))
    if DEST.exists():
        previous = json.loads(DEST.read_text())
        prior_searches = {item["query"]: item for item in previous["search"]}
        for index, item in enumerate(searches):
            prior = prior_searches.get(item["query"])
            if item.get("error") and prior and prior["hits"]:
                searches[index] = {
                    **prior,
                    "captured_at_utc": prior.get("captured_at_utc", previous["captured_at_utc"]),
                    "latest_refresh_error": item["error"],
                    "latest_refresh_at_utc": item["captured_at_utc"],
                }
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "Maven Central Solr artifact search; targeted Maven Central release lookups when search is unavailable",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": 100,
        "search": searches,
        "releases": releases,
        "popularity_metric": {
            "name": "deps.dev version-level directDependentCount",
            "documentation": "https://docs.deps.dev/api/v3alpha/",
            "scope": "Known public direct dependents of the exact Maven release; incomplete coverage and version-level bias",
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "packages": metrics,
        },
    }
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Maven ZIP snapshot: {sum(len(s['hits']) for s in searches)} saved search hits; "
          f"{len(releases)} pinned release lookups")


if __name__ == "__main__":
    main()
