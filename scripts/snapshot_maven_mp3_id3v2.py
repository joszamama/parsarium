"""Save bounded Maven leads, pinned MP3 releases, and Java adoption signals.

Search hits are only leads. Local MP3/ID3v2 parsing is decided by the control
adapter and verify_java_mp3_id3v2.py.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import os
import subprocess
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen
import json
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data/java/mp3_id3v2/registry-snapshot.json"
COORDS = {
    "jaudiotagger": ("net.jthink", "jaudiotagger", "3.0.1"),
    "mp3agic": ("com.mpatric", "mp3agic", "0.9.1"),
    "tika-audiovideo": ("org.apache.tika", "tika-parser-audiovideo-module", "4.2.0"),
    "jlayer": ("javazoom", "jlayer", "1.0.1"),
    "jave-core": ("ws.schild", "jave-core", "4.2.0"),
    "jaffree": ("com.github.kokorin.jaffree", "jaffree", "2024.08.29"),
    "mp3spi": ("com.googlecode.soundlibs", "mp3spi", "1.9.5.4"),
}
LICENSES = {
    "jaudiotagger": ("LGPL-2.1-or-later", "https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1.pom"),
    "mp3agic": ("MIT", "https://repo.maven.apache.org/maven2/com/mpatric/mp3agic/0.9.1/mp3agic-0.9.1.pom"),
    "tika-audiovideo": ("Apache-2.0", "https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0.pom"),
    "jlayer": ("LGPL-2.1-or-later", "https://repo.maven.apache.org/maven2/javazoom/jlayer/1.0.1/jlayer-1.0.1.pom"),
    "jave-core": ("GPL-3.0-only", "https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0.pom"),
    "jaffree": ("Apache-2.0", "https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29.pom"),
    "mp3spi": ("LGPL-2.0-or-later", "https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4-sources.jar"),
}
QUERIES = ["mp3", "id3", "mp3 parser", "audio tag", "mpeg audio"]


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
        value = json.loads(get(url)).get("directDependentCount")
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
        payload = json.loads(get(url, timeout=20))["response"]
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
    with ThreadPoolExecutor(max_workers=7) as pool:
        releases = dict(pool.map(release, COORDS.items()))
        metrics = dict(pool.map(metric, COORDS.items()))
        searches = list(pool.map(search, QUERIES))
    now = datetime.now(timezone.utc).isoformat()
    ffprobe = Path(os.environ.get("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin")) / "ffprobe"
    ffprobe_version = subprocess.run([str(ffprobe), "-version"], text=True,
                                     capture_output=True, check=True).stdout.splitlines()[0]
    snapshot = {
        "captured_at_utc": now,
        "search_surface": "Maven Central Solr bounded artifact queries plus targeted official Maven releases",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": 100,
        "search": searches,
        "targeted_documentation_leads": [
            "https://www.jthink.net/jaudiotagger/examples_id3.jsp",
            "https://github.com/mpatric/mp3agic/blob/master/readme.md",
            "https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-sources.jar",
            "https://repo.maven.apache.org/maven2/javazoom/jlayer/1.0.1/jlayer-1.0.1-javadoc.jar",
            "https://github.com/pdudits/soundlibs/blob/master/README.adoc",
        ],
        "releases": releases,
        "external_tools": {
            "ffprobe": {"path": str(ffprobe), "version": ffprobe_version,
                        "sha256": sha256(ffprobe.read_bytes()).hexdigest()}
        },
        "popularity_metric": {
            "name": "deps.dev version-level directDependentCount",
            "documentation": "https://docs.deps.dev/api/v3alpha/",
            "scope": "Known public direct dependents of the exact Maven release; incomplete coverage and version-level bias",
            "captured_at_utc": now,
            "packages": metrics,
        },
    }
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(snapshot, indent=2) + "\n")
    print(f"Maven MP3/ID3v2 snapshot: {sum(len(s['hits']) for s in searches)} "
          f"search hits; {len(releases)} pinned releases")


if __name__ == "__main__":
    main()
