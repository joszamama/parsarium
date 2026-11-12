"""Save bounded Maven leads, pinned HTTP/1.1 releases, and Java adoption signals.

Search hits are leads only. parsers.json and verify_java_http11.py carry the
independent format-aware parsing decision and control result.
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
DEST = ROOT / "data/java/http11/registry-snapshot.json"
COORDS = {
    "netty": ("io.netty", "netty", "3.10.6.Final"),
    "netty5-codec-http": ("io.netty", "netty5-codec-http", "5.0.0.Alpha5"),
    "netty-codec-http": ("io.netty", "netty-codec-http", "4.2.20.Final"),
    "http1_1-parser": ("org.webpieces.http", "http1_1-parser", "2.1.109"),
    "httpcore5": ("org.apache.httpcomponents.core5", "httpcore5", "5.4.4"),
    "httpcore": ("org.apache.httpcomponents", "httpcore", "4.4.16"),
    "jetty-http": ("org.eclipse.jetty", "jetty-http", "12.1.15"),
    "jodd-http": ("org.jodd", "jodd-http", "6.3.0"),
    "rawhttp-core": ("com.athaydes.rawhttp", "rawhttp-core", "2.6.0"),
    "nanohttpd": ("org.nanohttpd", "nanohttpd", "2.3.1"),
    "jwarc": ("org.netpreserve", "jwarc", "0.37.0"),
    "webarchive-commons": ("org.netpreserve.commons", "webarchive-commons", "3.0.5"),
    "jwat-common": ("org.jwat", "jwat-common", "1.2.1"),
    "sentinel-transport-simple-http": ("com.alibaba.csp", "sentinel-transport-simple-http", "1.8.10"),
    "httpcore-nio": ("org.apache.httpcomponents", "httpcore-nio", "4.4.16"),
    "mina-http": ("org.apache.mina", "mina-http", "2.2.10"),
}
LICENSES = {
    "netty": ("Apache-2.0", "https://github.com/netty/netty/blob/netty-3.10.6.Final/LICENSE.txt"),
    "netty5-codec-http": ("Apache-2.0", "https://github.com/netty/netty/blob/netty-5.0.0.Alpha5/LICENSE.txt"),
    "netty-codec-http": ("Apache-2.0", "https://github.com/netty/netty/blob/netty-4.2.20.Final/LICENSE.txt"),
    "http1_1-parser": ("Apache-2.0", "Maven release POM licenses"),
    "httpcore5": ("Apache-2.0", "Maven release JAR META-INF/LICENSE"),
    "httpcore": ("Apache-2.0", "Maven release JAR META-INF/LICENSE"),
    "jetty-http": ("EPL-2.0 OR Apache-2.0", "https://github.com/jetty/jetty.project/blob/jetty-12.1.15/LICENSE"),
    "jodd-http": ("BSD-2-Clause", "https://central.sonatype.com/artifact/org.jodd/jodd-http/6.3.0"),
    "rawhttp-core": ("Apache-2.0", "https://repo.maven.apache.org/maven2/com/athaydes/rawhttp/rawhttp-core/2.6.0/rawhttp-core-2.6.0.pom"),
    "nanohttpd": ("BSD-3-Clause", "https://github.com/NanoHttpd/nanohttpd/blob/nanohttpd-project-2.3.1/LICENSE.md"),
    "jwarc": ("Apache-2.0", "https://repo.maven.apache.org/maven2/org/netpreserve/jwarc/0.37.0/jwarc-0.37.0.pom"),
    "webarchive-commons": ("Apache-2.0", "https://github.com/iipc/webarchive-commons/blob/webarchive-commons-3.0.5/LICENSE"),
    "jwat-common": ("Apache-2.0", "https://repo.maven.apache.org/maven2/org/jwat/jwat/1.2.1/jwat-1.2.1.pom"),
    "sentinel-transport-simple-http": ("Apache-2.0", "https://github.com/alibaba/Sentinel/blob/1.8.10/LICENSE"),
    "httpcore-nio": ("Apache-2.0", "https://repo.maven.apache.org/maven2/org/apache/httpcomponents/httpcore-nio/4.4.16/httpcore-nio-4.4.16.pom"),
    "mina-http": ("Apache-2.0", "https://repo.maven.apache.org/maven2/org/apache/mina/mina-http/2.2.10/mina-http-2.2.10.pom"),
}
QUERIES = ["http parser", "http request parser", "http1", "http codec", "HTTP/1.1"]


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
        "group": group, "artifact": artifact, "version": version,
        "jar_url": jar_url, "jar_sha256": sha256(jar).hexdigest(),
        "pom_url": pom_url, "pom_sha256": sha256(pom).hexdigest(),
        "license": license_id, "license_evidence": license_evidence,
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
    captured = datetime.now(timezone.utc).isoformat()
    try:
        response = json.loads(get(url, timeout=20))
        payload = response["response"]
        hits = [{"rank": index, "name": item["id"],
                 "latest_version": item.get("latestVersion")}
                for index, item in enumerate(payload["docs"], 1)]
        return {"query": query, "url": url, "limit": 100,
                "captured_at_utc": captured, "total": payload["numFound"], "hits": hits}
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
        return {"query": query, "url": url, "limit": 100,
                "captured_at_utc": captured, "total": None, "hits": [],
                "error": f"{type(exc).__name__}: {exc}"}


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
                    "latest_refresh_error": item["error"],
                    "latest_refresh_at_utc": item["captured_at_utc"],
                }
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "Maven Central Solr bounded artifact queries plus targeted official Maven releases",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": 100,
        "search": searches,
        "targeted_documentation_leads": ["https://http.jodd.org/connection",
                                         "https://github.com/renatoathaydes/rawhttp",
                                         "https://javadoc.io/static/org.nanohttpd/nanohttpd/2.3.1/fi/iki/elonen/NanoHTTPD.HTTPSession.html",
                                         "https://github.com/iipc/jwarc/blob/v0.37.0/src/org/netpreserve/jwarc/HttpRequest.java",
                                         "https://github.com/iipc/webarchive-commons/blob/webarchive-commons-3.0.5/src/main/java/org/archive/format/http/HttpRequestParser.java",
                                         "https://github.com/netarchivesuite/jwat/blob/jwat-1.2.1/jwat-common/src/main/java/org/jwat/common/HttpHeader.java",
                                         "https://github.com/alibaba/Sentinel/blob/1.8.10/sentinel-transport/sentinel-transport-simple-http/src/main/java/com/alibaba/csp/sentinel/transport/heartbeat/client/SimpleHttpResponseParser.java",
                                         "https://hc.apache.org/httpcomponents-core-4.4.x/current/httpcore-nio/apidocs/org/apache/http/nio/NHttpMessageParser.html",
                                         "https://nightlies.apache.org/mina/mina/2.2.10/apidocs/org/apache/mina/http/HttpServerDecoder.html"],
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
    print(f"Maven HTTP/1.1 snapshot: {sum(len(s['hits']) for s in searches)} search hits; "
          f"{len(releases)} pinned releases")


if __name__ == "__main__":
    main()
