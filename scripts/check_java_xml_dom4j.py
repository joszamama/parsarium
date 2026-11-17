"""Recheck the dom4j Java XML pilot's release hashes, adoption metric, and JAXP delegation.

Downloads the pinned org.dom4j:dom4j 2.2.0 jar, sources jar, and POM from Maven
Central, compares their SHA-256 with source-lock.json and the registry snapshot,
reads the cited SAXReader/SAXHelper/JAXPHelper lines from the sources jar, and
re-sums deps.dev direct dependents over every release. With --write, the recheck
is recorded beside the release pin in data/java/xml/registry-snapshot.json.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
from pathlib import Path
import urllib.parse
import urllib.request
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data/java/xml/registry-snapshot.json"
LOCK = ROOT / "projects/xml/java/dom4j/source-lock.json"
COORDINATE = "org.dom4j:dom4j"
VERSION = "2.2.0"
PREFIX = f"https://repo.maven.apache.org/maven2/org/dom4j/dom4j/{VERSION}/dom4j-{VERSION}"
# (file in sources jar, first line, text that line must contain)
CITATIONS = [
    ("org/dom4j/io/SAXReader.java", 152, "public static SAXReader createDefault()"),
    ("org/dom4j/io/SAXReader.java", 386, "public Document read(InputStream in)"),
    ("org/dom4j/io/SAXReader.java", 462, "public Document read(InputSource in)"),
    ("org/dom4j/io/SAXReader.java", 494, "reader.parse(in);"),
    ("org/dom4j/io/SAXReader.java", 896, "SAXHelper.createXMLReader(isValidating())"),
    ("org/dom4j/io/SAXHelper.java", 87, "createXMLReaderViaJAXP(validating, true)"),
    ("org/dom4j/io/JAXPHelper.java", 46, "SAXParserFactory.newInstance()"),
    ("org/dom4j/io/JAXPHelper.java", 48, "factory.setNamespaceAware(namespaceAware)"),
]


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "parsarium-pilot"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except (TimeoutError, OSError):
            if attempt == 3:
                raise
    raise AssertionError


def deps_dev() -> dict:
    name = urllib.parse.quote(COORDINATE, safe="")
    base = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{name}"
    versions = [item["versionKey"]["version"] for item in json.loads(get(base))["versions"]]

    def count(version: str) -> tuple[str, int]:
        url = f"{base}/versions/{urllib.parse.quote(version, safe='')}:dependents"
        return version, json.loads(get(url))["directDependentCount"]

    with ThreadPoolExecutor(8) as pool:
        counts = dict(pool.map(count, versions))
    peak = max(counts, key=counts.get)
    return {"releases": len(counts), "summed_direct_dependent_count": sum(counts.values()),
            "max_release": peak, "max_release_direct_dependent_count": counts[peak]}


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--write", action="store_true", help="record the recheck in the registry snapshot")
    args = cli.parse_args()
    lock = json.loads(LOCK.read_text())["dom4j"]
    snapshot = json.loads(SNAPSHOT.read_text())
    recorded = snapshot["popularity_metric"]["packages"][COORDINATE]
    artifacts = {kind: get(PREFIX + suffix)
                 for kind, suffix in (("jar", ".jar"), ("sources", "-sources.jar"), ("pom", ".pom"))}
    digests = {kind: sha256(body).hexdigest() for kind, body in artifacts.items()}
    expected = {"jar": lock["jar_sha256"], "sources": lock["source_sha256"], "pom": lock["pom_sha256"]}
    if digests != expected:
        raise SystemExit(f"release hashes changed: {digests}")
    pinned = snapshot.get("releases", {}).get(COORDINATE)
    if pinned and any(pinned[f"{kind}_sha256"] != digest for kind, digest in digests.items()):
        raise SystemExit("registry snapshot release pin differs from Maven Central")
    with zipfile.ZipFile(io.BytesIO(artifacts["sources"])) as sources:
        for name, line, text in CITATIONS:
            lines = sources.read(name).decode("utf-8").splitlines()
            if text not in lines[line - 1]:
                raise SystemExit(f"{name}:{line} no longer contains {text!r}")
    if b"<optional>true</optional>" not in artifacts["pom"] or b"BSD 3-clause" not in artifacts["pom"]:
        raise SystemExit("POM license or optional-dependency evidence changed")
    live = deps_dev()
    unchanged = all(live[key] == recorded[key] for key in live)
    print(json.dumps({"hashes": digests, "citations_checked": len(CITATIONS),
                      "recorded": {key: recorded[key] for key in live}, "live": live,
                      "metric_unchanged": unchanged}, indent=2))
    if args.write:
        snapshot.setdefault("releases", {})[COORDINATE] = {
            "version": VERSION,
            **{f"{kind}_url": PREFIX + suffix for kind, suffix in
               (("jar", ".jar"), ("sources", "-sources.jar"), ("pom", ".pom"))},
            **{f"{kind}_sha256": digest for kind, digest in digests.items()},
            "metric_rechecked_at_utc": datetime.now(timezone.utc).isoformat(),
            "metric_recheck": live,
            "metric_recheck_unchanged": unchanged,
        }
        SNAPSHOT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
