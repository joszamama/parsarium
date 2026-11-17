"""Capture the bounded Maven Central search and deps.dev metric for the Java XML pilot."""

from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/java/xml/registry-snapshot.json"
QUERIES = ["xml", "xml parser", "dom4j", "jdom", "xerces", "stax"]
LIMIT = 100
# Coordinates looked up directly after the search; the search surface ranks by
# text relevance, not adoption, so widely used parsers need targeted lookups.
LEADS = [
    "org.dom4j:dom4j",
    "dom4j:dom4j",
    "xerces:xercesImpl",
    "org.jdom:jdom2",
    "org.jdom:jdom",
    "com.fasterxml.woodstox:woodstox-core",
    "org.codehaus.woodstox:woodstox-core-asl",
    "com.fasterxml.jackson.dataformat:jackson-dataformat-xml",
    "com.thoughtworks.xstream:xstream",
    "xom:xom",
    "org.codehaus.woodstox:stax2-api",
    "com.sun.xml.fastinfoset:FastInfoset",
    "org.jsoup:jsoup",
    "net.sf.kxml:kxml2",
    "xpp3:xpp3",
    "com.ximpleware:vtd-xml",
    "org.apache.xmlbeans:xmlbeans",
    "com.fasterxml:aalto-xml",
]
SELECTED = {"xerces:xercesImpl": "2.12.2"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def deps_dev(coordinate: str) -> dict:
    """Sum and maximum of version-level direct dependents over every release."""
    name = urllib.parse.quote(coordinate, safe="")
    base = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{name}"
    versions = json.loads(get(base))["versions"]
    default, = [item["versionKey"]["version"] for item in versions if item.get("isDefault")]

    def count(version: str) -> tuple[str, int]:
        url = f"{base}/versions/{urllib.parse.quote(version, safe='')}:dependents"
        return version, json.loads(get(url))["directDependentCount"]

    with ThreadPoolExecutor(16) as pool:
        counts = dict(pool.map(count, [item["versionKey"]["version"] for item in versions]))
    peak = max(counts, key=counts.get)
    return {"default_version": default, "releases": len(counts),
            "summed_direct_dependent_count": sum(counts.values()),
            "max_release": peak, "max_release_direct_dependent_count": counts[peak],
            "default_release_direct_dependent_count": counts[default],
            "url": base, "captured_at_utc": now()}


def main() -> None:
    snapshot = {
        "captured_at_utc": now(),
        "search_surface": "Maven Central Solr artifact search; targeted deps.dev and Maven Central release lookups",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": LIMIT,
        "search": [],
    }
    for query in QUERIES:
        url = f"https://search.maven.org/solrsearch/select?q={urllib.parse.quote(query)}&rows={LIMIT}&wt=json"
        body = json.loads(get(url))["response"]
        snapshot["search"].append({
            "query": query, "url": url, "limit": LIMIT, "captured_at_utc": now(),
            "total": body["numFound"],
            "hits": [{"rank": rank, "name": doc["id"], "latest_version": doc.get("latestVersion")}
                     for rank, doc in enumerate(body["docs"], 1)],
        })
    snapshot["popularity_metric"] = {
        "name": "deps.dev directDependentCount summed over all releases",
        "documentation": "https://docs.deps.dev/api/v3alpha/",
        "scope": "Sum over every Maven release of deps.dev version-level directDependentCount; a dependent package is counted once per release it depends on. Incomplete public coverage. The single-release maximum and the default-release count are recorded beside it; the default-release count alone favours old single-release packages such as json-simple 1.1.1",
        "captured_at_utc": now(),
        "packages": {coordinate: deps_dev(coordinate) for coordinate in LEADS},
    }
    releases = {}
    for coordinate, version in SELECTED.items():
        group, artifact = coordinate.split(":")
        prefix = f"https://repo.maven.apache.org/maven2/{group.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}"
        releases[coordinate] = {"version": version}
        for kind, suffix in (("jar", ".jar"), ("sources", "-sources.jar"), ("pom", ".pom")):
            releases[coordinate][f"{kind}_url"] = prefix + suffix
            releases[coordinate][f"{kind}_sha256"] = sha256(get(prefix + suffix)).hexdigest()
    snapshot["releases"] = releases
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    hits = [hit["name"] for entry in snapshot["search"] for hit in entry["hits"]]
    print(len(hits), len(set(hits)))
    for coordinate, item in sorted(snapshot["popularity_metric"]["packages"].items(),
                                   key=lambda pair: -pair[1]["summed_direct_dependent_count"]):
        print(item["summed_direct_dependent_count"], item["max_release_direct_dependent_count"],
              item["default_release_direct_dependent_count"], coordinate, item["default_version"])


if __name__ == "__main__":
    main()
