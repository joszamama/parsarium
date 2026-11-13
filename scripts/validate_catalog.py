"""Check cross-file consistency of accepted cells and their recorded evidence."""

from pathlib import Path
import json
import re
import tomllib
import xml.etree.ElementTree as ET

from audit_popularity_coverage import build_report


ROOT = Path(__file__).resolve().parents[1]


def read(path: str):
    return json.loads((ROOT / path).read_text())


def main() -> None:
    matrix = read("data/cells.json")["cells"]
    assert len(matrix) == 88
    assert len({(c["ecosystem"], c["format"]) for c in matrix}) == 88
    lock = read("package-lock.json")["packages"][""]["dependencies"]
    for cell in matrix:
        assert cell["working_target"] == 20 and cell["ceiling"] == 30
        if cell["status"] == "not_started":
            assert cell["verified_third_party_count"] == 0
            assert cell["search_hits_recorded"] == 0
            continue
        key = f"data/{cell['ecosystem']}/{cell['format']}"
        parsers = read(f"{key}/parsers.json")
        snapshot = read(f"{key}/registry-snapshot.json")
        assert len(parsers) == cell["verified_third_party_count"]
        assert len(parsers) <= cell["ceiling"]
        assert len({p["name"] for p in parsers}) == len(parsers)
        if "verified_document_input_count" in cell:
            assert sum(p["input_variant"] == "svg_document" for p in parsers) == cell["verified_document_input_count"]
            assert sum(p["input_variant"] == "svg_path_data" for p in parsers) == cell["verified_path_data_only_count"]
            assert cell["verified_document_input_count"] + cell["verified_path_data_only_count"] == len(parsers)
        assert sum(len(s["hits"]) for s in snapshot["search"]) == cell["search_hits_recorded"]
        assert snapshot["search_limit_per_query"] == cell["search_limit_per_query"]
        hit_key = "packagePath" if cell["ecosystem"] == "go" else "name"
        assert len({hit[hit_key] for search in snapshot["search"] for hit in search["hits"]}) == cell["unique_search_hits"]
        assert len(snapshot["search"]) == len(cell["search_queries"])
        leads = read(f"{key}/leads.json")
        assert sum(lead["status"] == "unresolved" for lead in leads) == cell["unresolved_documentation_leads"]
        assert not ({lead["name"] for lead in leads} & {p["name"] for p in parsers})
        for parser in parsers:
            name = parser["name"]
            if cell["ecosystem"] in ("c", "cpp"):
                primary_sources = read(cell.get("source_lock", f"{key}/source-lock.json"))
                if name in primary_sources:
                    source = primary_sources[name]
                else:
                    extra_sources = read(cell["extra_source_lock"])
                    if cell.get("additional_source_lock"):
                        extra_sources.update(read(cell["additional_source_lock"]))
                    source = extra_sources[name]
                release = snapshot["releases"][name]
                assert parser["version"] == source["release"] == release["version"]
                assert parser["license"] == release["license"]
                if source.get("source_kind") == "subversion":
                    assert release["source_kind"] == "subversion"
                    assert source["svn_revision"] == release["svn_revision"]
                    assert source["version_file_sha256"] == release["version_file_sha256"]
                    assert len(source["version_file_sha256"]) == 64
                elif source.get("source_kind") == "official_binary_distribution":
                    assert release["source_kind"] == "official_binary_distribution"
                    assert source["distribution_sha256"] == release["distribution_sha256"]
                    assert source["source_commit"] == release["source_commit"]
                    assert len(source["distribution_sha256"]) == 64
                    assert len(source["source_commit"]) == 40
                elif source.get("source_kind") == "gitiles_blobs":
                    assert release["source_kind"] == "gitiles_blobs"
                    assert source["release_commit"] == release["release_commit"]
                    assert source["files"] == release["files"]
                    assert len(source["release_commit"]) == 40
                else:
                    assert source["source_sha256"] == release["source_sha256"]
                    assert len(source["source_sha256"]) == 64
                assert all(len(file["sha256"]) == 64 for file in source.get("files", []))
                assert (ROOT / parser["adapter"]).exists()
                assert (ROOT / parser["control"]).exists()
                metric_key = ("install_on_request_365d" if snapshot["popularity_metric"].get("metric")
                              == "Homebrew install-on-request count over 365 days" else "stars")
                count = snapshot["popularity_metric"]["packages"][name][metric_key]
                assert count is None or isinstance(count, int)
            elif cell["ecosystem"] == "go":
                go_mod = (ROOT / "adapters" / "go" / cell["format"] / "go.mod").read_text()
                go_versions = dict(re.findall(r"^\s*(\S+)\s+(v\S+)", go_mod, re.MULTILINE))
                assert parser["version"] == go_versions[parser["module"]]
                count = snapshot["popularity_metric"]["packages"][name]["imported_by_packages"]
                assert count is None or isinstance(count, int)
                assert parser["license"] == snapshot["releases"][name]["license"]
            elif cell["ecosystem"] == "python":
                requirements_dir = ROOT / "adapters" / "python" / cell["format"]
                requirements = "\n".join(path.read_text() for path in requirements_dir.glob("requirements*.in"))
                python_versions = dict(re.findall(r"^([A-Za-z0-9_.-]+)(?:\[[^]]+\])?==([^\s]+)$",
                                                  requirements, re.MULTILINE))
                assert parser["version"] == python_versions[name]
                count = snapshot["download_metric"]["packages"][name]["downloads"]
                assert count is None or isinstance(count, int)
                assert (ROOT / parser["control"]).exists()
            elif cell["ecosystem"] == "rust":
                adapter = ROOT / parser.get("adapter_manifest_dir", f"adapters/rust/{cell['format']}")
                manifest = tomllib.loads((adapter / "Cargo.toml").read_text())
                dependency = manifest["dependencies"][parser.get("manifest_dependency", name)]
                requirement = dependency if isinstance(dependency, str) else dependency["version"]
                if isinstance(dependency, dict) and "package" in dependency:
                    assert dependency["package"] == name
                assert requirement == "=" + parser["version"]
                locked = tomllib.loads((adapter / "Cargo.lock").read_text())
                match = [package for package in locked["package"]
                         if package["name"] == name and package["version"] == parser["version"]]
                assert len(match) == 1
                assert match[0]["checksum"] == snapshot["releases"][name]["checksum"]
                assert parser["license"] == snapshot["releases"][name]["license"]
                count = snapshot["popularity_metric"]["packages"][name]["recent_downloads"]
                assert count is None or isinstance(count, int)
                assert (ROOT / parser["control"]).exists()
            elif cell["ecosystem"] == "java":
                if parser.get("group") is None:
                    release = snapshot["non_maven_release"][name]
                    assert release["version"] == parser["version"]
                    assert release["license"] == parser["license"]
                    if parser.get("source_kind") == "source_build":
                        source = read(parser["source_lock"])[name]
                        assert source["release"] == parser["version"]
                        assert source["license"] == parser["license"]
                        assert source["source_sha256"] == release["source_sha256"]
                        assert len(source["source_sha256"]) == 64
                        assert (ROOT / parser["adapter"]).exists()
                        assert snapshot["popularity_metric"]["packages"][name]["direct_dependent_count"] is None
                    elif parser.get("source_kind") == "official_binary_distribution":
                        source = read(parser["source_lock"])[name]
                        assert source["release"] == parser["version"]
                        assert source["license"] == parser["license"]
                        assert source["source_sha256"] == release["source_sha256"]
                        assert source["jar_sha256"] == release["distribution_sha256"]
                        assert source["tag_commit"] == release["source_commit"]
                        assert len(source["jar_sha256"]) == 64
                        assert (ROOT / parser["adapter"]).exists()
                        assert snapshot["popularity_metric"]["packages"][name]["direct_dependent_count"] is None
                    else:
                        assert cell["format"] == "pdf" and name == "pdfclown"
                        assert len(release["archive_sha256"]) == 64 and len(release["jar_sha256"]) == 64
                        assert release["popularity_metric"] is None
                else:
                    adapter_module = parser.get("adapter_module", "main")
                    adapter_dir = ROOT / "adapters" / "java" / cell["format"]
                    pom_path = adapter_dir / (adapter_module if adapter_module != "main" else "") / "pom.xml"
                    pom = ET.parse(pom_path).getroot()
                    ns = {"m": "http://maven.apache.org/POM/4.0.0"}
                    dependencies = {
                        (entry.findtext("m:groupId", namespaces=ns),
                         entry.findtext("m:artifactId", namespaces=ns)):
                        entry.findtext("m:version", namespaces=ns)
                        for entry in pom.findall("m:dependencies/m:dependency", ns)
                    }
                    assert dependencies[(parser["group"], parser["artifact"])] == parser["version"]
                    release = snapshot["releases"][name]
                    assert (release["group"], release["artifact"], release["version"]) == (
                        parser["group"], parser["artifact"], parser["version"])
                    assert parser["license"] == release["license"]
                    count = snapshot["popularity_metric"]["packages"][name]["direct_dependent_count"]
                    assert count is None or isinstance(count, int)
                    assert len(release["jar_sha256"]) == 64 and len(release["pom_sha256"]) == 64
                assert (ROOT / parser["control"]).exists()
            elif cell["ecosystem"] == "php":
                release = snapshot["releases"][name]
                if parser.get("source_kind") == "pecl":
                    source = read(parser["source_lock"])
                    assert parser["version"] == release["version"] == source["release"]
                    assert source["source_sha256"] == release["source_sha256"]
                    assert len(source["source_sha256"]) == 64
                else:
                    lock_path = ROOT / parser["composer_lock"]
                    locked = {package["name"]: package
                              for package in json.loads(lock_path.read_text())["packages"]}
                    assert name in locked
                    assert parser["version"] == release["version"] == locked[name]["version"]
                    assert locked[name]["source"]["reference"] == release["source_reference"]
                assert parser["license"] == release["license"]
                assert parser["license_evidence"] == release["license_evidence"]
                assert (ROOT / parser["adapter"]).exists()
                assert (ROOT / parser["control"]).exists()
                count = snapshot["download_metric"]["packages"][name]["downloads"]
                assert count is None or isinstance(count, int)
            else:
                assert parser["version"] == lock[name]
                assert isinstance(snapshot["download_metric"]["packages"][name]["downloads"], int)
            if not (cell["ecosystem"] == "java" and parser.get("group", "present") is None):
                assert parser["version"] == snapshot["releases"][name]["version"]
            assert parser["license"] and parser["documentation"] and parser["family"] and parser["input_api"]
        results = read(f"{key}/verification.json")
        browser_png = cell["ecosystem"] == "javascript" and cell["format"] == "png"
        runs = results["results"] if browser_png else results["third_party"]
        assert {r["package"] for r in runs} == {p["name"] for p in parsers}
        assert all(r["pass"] for r in runs)
        if cell["ecosystem"] in ("c", "cpp"):
            expected = {parser["name"]: parser for parser in parsers}
            assert all(row["version"] == expected[row["package"]]["version"]
                       and row["control"] == expected[row["package"]]["control"]
                       and row["output"] == expected[row["package"]]["expected_output"]
                       for row in runs)
        elif cell["ecosystem"] == "rust":
            expected = {parser["name"]: parser for parser in parsers}
            assert all(row["version"] == expected[row["package"]]["version"]
                       and row["control"] == expected[row["package"]]["control"]
                       and row["output"] == expected[row["package"]]["expected_output"]
                       for row in runs)
        elif cell["ecosystem"] in ("java", "php"):
            expected = {parser["name"]: parser for parser in parsers}
            assert all(row["version"] == expected[row["package"]]["version"]
                       and row["control"] == expected[row["package"]]["control"]
                       and row["output"] == expected[row["package"]]["expected_output"]
                       for row in runs)
        if browser_png:
            assert read(f"{key}/browser-verification.json")["pass"]
        elif cell["verified_standard_or_runtime_count"]:
            runtime_results = results["runtime"]
            if isinstance(runtime_results, list):
                assert len(runtime_results) == cell["verified_standard_or_runtime_count"]
                assert all(row["pass"] for row in runtime_results)
                if cell["ecosystem"] == "php":
                    standard = read(f"{key}/standard.json")
                    expected_runtime = {api["name"]: api for api in standard["verified_apis"]}
                    assert {row["name"] for row in runtime_results} == set(expected_runtime)
                    assert all(row["control"] == expected_runtime[row["name"]]["control"]
                               and row["output"] == expected_runtime[row["name"]]["expected_output"]
                               for row in runtime_results)
            else:
                assert runtime_results["pass"]
        assert cell["verified_standard_or_runtime_count"] == len(read(f"{key}/standard.json")["verified_apis"])
    assert read("data/popularity-coverage.json") == build_report()
    print(f"Validated {len(matrix)} cells, {sum(c['status'] != 'not_started' for c in matrix)} with recorded evidence")


if __name__ == "__main__":
    main()
