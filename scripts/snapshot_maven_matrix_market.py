"""Refresh bounded Maven discovery and exact-release EJML adoption evidence."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/java/matrix_market/registry-snapshot.json"
QUERIES = ["matrix market", "matrix-market", "MatrixMarket", "ejml"]
LIMIT = 100
GROUP, ARTIFACT, VERSION = "org.ejml", "ejml-core", "0.46.1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get(url: str) -> bytes:
    with urlopen(url, timeout=15) as response:
        return response.read()


def main() -> None:
    search = []
    for query in QUERIES:
        url = "https://search.maven.org/solrsearch/select?q=" + quote(query) + f"&rows={LIMIT}&wt=json"
        item = {"query": query, "url": url, "limit": LIMIT, "captured_at_utc": now()}
        try:
            response = json.loads(get(url))['response']
            item.update(total=response['numFound'], hits=[
                {"name": f"{doc['g']}:{doc['a']}", "group": doc['g'],
                 "artifact": doc['a'], "latestVersion": doc.get('latestVersion')}
                for doc in response['docs']])
        except Exception as error:
            item.update(total=None, hits=[], error=f"{type(error).__name__}: {error}")
        search.append(item)

    prefix = f"https://repo.maven.apache.org/maven2/org/ejml/{ARTIFACT}/{VERSION}/{ARTIFACT}-{VERSION}"
    release = {"group": GROUP, "artifact": ARTIFACT, "version": VERSION, "license": "Apache-2.0"}
    for kind in ("jar", "pom"):
        url = f"{prefix}.{kind}"
        release[f"{kind}_url"] = url
        release[f"{kind}_sha256"] = sha256(get(url)).hexdigest()

    dependency_url = (
        "https://api.deps.dev/v3alpha/systems/MAVEN/packages/"
        "org.ejml%3Aejml-core/versions/0.46.1:dependents"
    )
    try:
        count = json.loads(get(dependency_url))["directDependentCount"]
        metric_error = None
    except Exception as error:
        count = None
        metric_error = f"{type(error).__name__}: {error}"
    metric = {"direct_dependent_count": count, "url": dependency_url}
    if metric_error:
        metric["error"] = metric_error

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "captured_at_utc": now(),
        "search_surface": "Maven Central Solr artifact search",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": LIMIT,
        "search": search,
        "releases": {"ejml-core": release},
        "popularity_metric": {
            "name": "deps.dev version-level directDependentCount",
            "documentation": "https://docs.deps.dev/api/v3alpha/",
            "scope": "Known public direct dependents of this exact Maven release; incomplete coverage and version-age bias",
            "captured_at_utc": now(),
            "packages": {"ejml-core": metric},
        },
    }, indent=2) + "\n")
    print(f"Recorded {sum(len(item['hits']) for item in search)} Maven hits; direct dependents: {count}")


if __name__ == "__main__":
    main()
