"""Capture bounded Java ASCII PLY leads and adoption at exact Maven versions."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/java/ascii_ply/registry-snapshot.json"
QUERIES = ["ply", "ascii ply", "jply", "meshio"]
RELEASES = [("jply", "org.smurn", "jply", "0.2.0", "Apache-2.0"),
            ("meshio", "com.ripplargames", "meshio", "2.1.2", "MIT"),
            ("mesh-ply", "hu.kazocsaba.geom3d", "mesh-ply", "1.1.0", "MIT"),
            ("pcutil", "cn.jimmiez", "pcutil", "0.3.0", "MIT"),
            ("lwjgl-assimp", "org.lwjgl", "lwjgl-assimp", "3.4.3", "BSD-3-Clause"),
            ("MonkeyWrench", "com.github.stephengold", "MonkeyWrench", "1.0.1", "BSD-3-Clause")]
DEPENDENCIES = [("hu.kazocsaba.geom3d", "mesh", "1.0.1"),
                ("hu.kazocsaba.math", "matrix", "1.1.0"),
                ("org.lwjgl", "lwjgl", "3.4.3")]
NATIVE_ARTIFACTS = [("org.lwjgl", "lwjgl", "3.4.3", "natives-macos-arm64"),
                    ("org.lwjgl", "lwjgl-assimp", "3.4.3", "natives-macos-arm64")]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get(url: str) -> bytes:
    with urlopen(url, timeout=15) as response:
        return response.read()


def main() -> None:
    previous_search = {}
    if OUT.exists():
        previous_search = {item["query"]: item for item in json.loads(OUT.read_text())["search"]}
    search = []
    for query in QUERIES:
        url = "https://search.maven.org/solrsearch/select?q=" + quote(query) + "&rows=100&wt=json"
        item = {"query": query, "url": url, "limit": 100, "captured_at_utc": now()}
        try:
            response = json.loads(get(url))["response"]
            item.update(total=response["numFound"], hits=[
                {"name": f"{doc['g']}:{doc['a']}", "group": doc['g'],
                 "artifact": doc['a'], "latestVersion": doc.get("latestVersion")}
                for doc in response["docs"]])
        except Exception as error:
            if query in previous_search and previous_search[query].get("total") is not None:
                item = previous_search[query].copy()
                item["retained_after_failed_refresh_at_utc"] = now()
                item["refresh_error"] = f"{type(error).__name__}: {error}"
            else:
                item.update(total=None, hits=[], error=f"{type(error).__name__}: {error}")
        search.append(item)

    releases = {}
    popularity = {}
    for name, group, artifact, version, license_name in RELEASES:
        prefix = ("https://repo.maven.apache.org/maven2/" + group.replace(".", "/")
                  + f"/{artifact}/{version}/{artifact}-{version}")
        release = {"group": group, "artifact": artifact,
                   "version": version, "license": license_name}
        for kind in ("jar", "pom"):
            url = f"{prefix}.{kind}"
            release[f"{kind}_url"] = url
            release[f"{kind}_sha256"] = sha256(get(url)).hexdigest()
        releases[name] = release
        dep_url = ("https://api.deps.dev/v3alpha/systems/MAVEN/packages/"
                   + quote(f"{group}:{artifact}", safe="")
                   + f"/versions/{version}:dependents")
        metric = {"url": dep_url}
        try:
            metric["direct_dependent_count"] = json.loads(get(dep_url))["directDependentCount"]
        except Exception as error:
            metric.update(direct_dependent_count=None,
                          error=f"{type(error).__name__}: {error}")
        popularity[name] = metric

    dependencies = []
    for group, artifact, version in DEPENDENCIES:
        prefix = ("https://repo.maven.apache.org/maven2/" + group.replace(".", "/")
                  + f"/{artifact}/{version}/{artifact}-{version}")
        item = {"group": group, "artifact": artifact, "version": version}
        for kind in ("jar", "pom"):
            url = f"{prefix}.{kind}"
            item[f"{kind}_url"] = url
            item[f"{kind}_sha256"] = sha256(get(url)).hexdigest()
        dependencies.append(item)

    natives = []
    for group, artifact, version, classifier in NATIVE_ARTIFACTS:
        url = ("https://repo.maven.apache.org/maven2/" + group.replace(".", "/")
               + f"/{artifact}/{version}/{artifact}-{version}-{classifier}.jar")
        natives.append({"group": group, "artifact": artifact, "version": version,
                        "classifier": classifier, "jar_url": url,
                        "jar_sha256": sha256(get(url)).hexdigest()})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "captured_at_utc": now(), "search_surface": "Maven Central Solr artifact search",
        "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/",
        "search_limit_per_query": 100, "search": search, "releases": releases,
        "dependencies": dependencies, "native_artifacts": natives,
        "popularity_metric": {
            "name": "deps.dev version-level directDependentCount",
            "documentation": "https://docs.deps.dev/api/v3alpha/",
            "scope": "Known public exact-release direct dependents; incomplete coverage and version-age bias",
            "captured_at_utc": now(), "packages": popularity,
        },
    }, indent=2) + "\n")
    print(f"Recorded {sum(len(item['hits']) for item in search)} Maven hits")


if __name__ == "__main__":
    main()
