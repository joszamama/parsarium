"""Save bounded Maven leads, pinned MP3 releases, and Java adoption signals.

Search hits are only leads. Local MP3/ID3v2 parsing is decided by the control
adapter and verify_java_mp3_tagged.py.
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
DEST = ROOT / "data/java/mp3/registry-snapshot.json"
COORDS = {
    "jaudiotagger": ("net.jthink", "jaudiotagger", "3.0.1"),
    "mp3agic": ("com.mpatric", "mp3agic", "0.9.1"),
    "tika-audiovideo": ("org.apache.tika", "tika-parser-audiovideo-module", "4.2.0"),
    "jlayer": ("javazoom", "jlayer", "1.0.1"),
    "jave-core": ("ws.schild", "jave-core", "4.2.0"),
    "jaffree": ("com.github.kokorin.jaffree", "jaffree", "2024.08.29"),
    "mp3spi": ("com.googlecode.soundlibs", "mp3spi", "1.9.5.4"),
    "javacv": ("org.bytedeco", "javacv", "1.5.14"),
    "bytedeco-ffmpeg": ("org.bytedeco", "ffmpeg", "8.1.2-1.5.14"),
    "jcodec": ("org.jcodec", "jcodec", "0.2.5"),
    "codecmedia": ("me.tamkungz.codecmedia", "codecmedia", "1.2.2"),
    "jid3lib": ("net.sf.javamusictag", "jid3lib", "0.5.4"),
    "taglib-java": ("cz.skyba", "taglib", "1.0.0"),
    "javamp3": ("fr.delthas", "javamp3", "1.0.1"),
    "tianscar-mp3spi": ("com.tianscar.javasound", "javasound-mp3", "1.9.8"),
    "bramp-ffmpeg": ("net.bramp.ffmpeg", "ffmpeg", "0.9.2"),
    "imagic-ffmpeg-java": ("ch.imagic", "ffmpeg-java", "0.1.2"),
    "v47-jaffree": ("io.v47.jaffree", "jaffree", "2.1.0"),
    "vlcj-info": ("uk.co.caprica", "vlcj-info", "2.0.3"),
    "mediainfo-jna-wrapper": ("com.amilesend", "mediainfo-jna-wrapper", "2.1.9"),
}
LICENSES = {
    "jaudiotagger": ("LGPL-2.1-or-later", "https://repo.maven.apache.org/maven2/net/jthink/jaudiotagger/3.0.1/jaudiotagger-3.0.1.pom"),
    "mp3agic": ("MIT", "https://repo.maven.apache.org/maven2/com/mpatric/mp3agic/0.9.1/mp3agic-0.9.1.pom"),
    "tika-audiovideo": ("Apache-2.0", "https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0.pom"),
    "jlayer": ("LGPL-2.1-or-later", "https://repo.maven.apache.org/maven2/javazoom/jlayer/1.0.1/jlayer-1.0.1.pom"),
    "jave-core": ("GPL-3.0-only", "https://repo.maven.apache.org/maven2/ws/schild/jave-core/4.2.0/jave-core-4.2.0.pom"),
    "jaffree": ("Apache-2.0", "https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29.pom"),
    "mp3spi": ("LGPL-2.0-or-later", "https://repo.maven.apache.org/maven2/com/googlecode/soundlibs/mp3spi/1.9.5.4/mp3spi-1.9.5.4-sources.jar"),
    "javacv": ("Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception", "https://repo.maven.apache.org/maven2/org/bytedeco/javacv/1.5.14/javacv-1.5.14.pom"),
    "bytedeco-ffmpeg": ("Apache-2.0 OR GPL-2.0-or-later OR GPL-2.0-with-classpath-exception", "https://repo.maven.apache.org/maven2/org/bytedeco/ffmpeg/8.1.2-1.5.14/ffmpeg-8.1.2-1.5.14.pom"),
    "jcodec": ("BSD-2-Clause", "https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5.pom"),
    "codecmedia": ("Apache-2.0", "https://repo.maven.apache.org/maven2/me/tamkungz/codecmedia/codecmedia/1.2.2/codecmedia-1.2.2.pom"),
    "jid3lib": ("LGPL-2.1", "https://github.com/ericfarng/jid3lib/blob/master/LGPL.html"),
    "taglib-java": ("LGPL-2.1 OR MPL-2.0", "https://repo.maven.apache.org/maven2/cz/skyba/taglib/1.0.0/taglib-1.0.0.pom"),
    "javamp3": ("MIT", "https://repo.maven.apache.org/maven2/fr/delthas/javamp3/1.0.1/javamp3-1.0.1.pom"),
    "tianscar-mp3spi": ("LGPL-2.0-only", "https://repo.maven.apache.org/maven2/com/tianscar/javasound/javasound-mp3/1.9.8/javasound-mp3-1.9.8.pom"),
    "bramp-ffmpeg": ("BSD-2-Clause", "https://repo.maven.apache.org/maven2/net/bramp/ffmpeg/ffmpeg/0.9.2/ffmpeg-0.9.2.pom"),
    "imagic-ffmpeg-java": ("BSD-2-Clause", "https://repo.maven.apache.org/maven2/ch/imagic/ffmpeg-java/0.1.2/ffmpeg-java-0.1.2.pom"),
    "v47-jaffree": ("GPL-3.0-only", "https://repo.maven.apache.org/maven2/io/v47/jaffree/jaffree/2.1.0/jaffree-2.1.0.pom"),
    "vlcj-info": ("GPL-3.0-or-later", "https://repo.maven.apache.org/maven2/uk/co/caprica/vlcj-info/2.0.3/vlcj-info-2.0.3.pom"),
    "mediainfo-jna-wrapper": ("MIT + MediaInfoLib Binary License", "https://repo.maven.apache.org/maven2/com/amilesend/mediainfo-jna-wrapper/2.1.9/mediainfo-jna-wrapper-2.1.9.pom"),
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
    native_dir = Path(os.environ.get("PARSARIUM_LIBMEDIAINFO_DIR", "/opt/homebrew/lib"))
    native_tools = {}
    for name in ("libmediainfo", "libzen"):
        path = native_dir / f"{name}.dylib"
        installed = subprocess.run(["brew", "list", "--versions", name], text=True,
                                   capture_output=True, check=True).stdout.strip()
        native_tools[name] = {"path": str(path), "filename": path.name,
                              "version": installed.removeprefix(f"{name} "),
                              "sha256": sha256(path.read_bytes()).hexdigest()}
    snapshot = {
        "captured_at_utc": now,
        "search_surface": "Maven Central Solr bounded artifact queries plus targeted Sonatype/Maven release and project documentation leads",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": 100,
        "search": searches,
        "targeted_registry_leads": [
            {"name": "codecmedia", "url": "https://central.sonatype.com/artifact/me.tamkungz.codecmedia/codecmedia/1.2.2"},
            {"name": "jid3lib", "url": "https://central.sonatype.com/artifact/net.sf.javamusictag/jid3lib/0.5.4"},
            {"name": "taglib-java", "url": "https://central.sonatype.com/artifact/cz.skyba/taglib/1.0.0"},
            {"name": "javasound-mp3", "url": "https://central.sonatype.com/artifact/com.tianscar.javasound/javasound-mp3/1.9.8"},
            {"name": "groupdocs-metadata", "url": "https://central.sonatype.com/artifact/com.groupdocs/groupdocs-metadata/18.4"},
            {"name": "javamp3", "url": "https://central.sonatype.com/artifact/fr.delthas/javamp3/1.0.1"}
        ],
        "targeted_registry_lead_rule": "A package page supplied only a lead; eligibility came from the pinned local control adapter and license evidence.",
        "targeted_documentation_leads": [
            "https://www.jthink.net/jaudiotagger/examples_id3.jsp",
            "https://github.com/mpatric/mp3agic/blob/master/readme.md",
            "https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-sources.jar",
            "https://repo.maven.apache.org/maven2/javazoom/jlayer/1.0.1/jlayer-1.0.1-javadoc.jar",
            "https://github.com/pdudits/soundlibs/blob/master/README.adoc",
            "https://central.sonatype.com/artifact/me.tamkungz.codecmedia/codecmedia/1.2.2",
            "https://central.sonatype.com/artifact/net.sf.javamusictag/jid3lib/0.5.4",
            "https://central.sonatype.com/artifact/cz.skyba/taglib/1.0.0",
        ],
        "releases": releases,
        "external_tools": {
            "ffprobe": {"path": str(ffprobe), "version": ffprobe_version,
                        "sha256": sha256(ffprobe.read_bytes()).hexdigest()},
            **native_tools,
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
