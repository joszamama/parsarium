"""Check cross-file consistency of accepted cells and their recorded evidence."""

from pathlib import Path
from datetime import datetime
import json
import re
import tomllib
import xml.etree.ElementTree as ET

from audit_popularity_coverage import build_report
from build_matrix import ECOSYSTEMS, FORMATS
from format_registry import PILOT_FORMATS


ROOT = Path(__file__).resolve().parents[1]


def read(path: str):
    return json.loads((ROOT / path).read_text())


def validate_pilot_cells() -> None:
    """Check pilot evidence without treating an unsearched cell as an empty result."""
    data = read("data/pilot-cells.json")
    expected = {(ecosystem, fmt) for ecosystem in ECOSYSTEMS for fmt in PILOT_FORMATS}
    cells = data.get("cells", [])
    if (data.get("phase") != "pilot" or data.get("complete") is not False or
            len(cells) != len(expected) or
            {(cell["ecosystem"], cell["format"]) for cell in cells} != expected):
        raise ValueError("pilot matrix must list every ecosystem cell once as incomplete")
    for cell in cells:
        eco, fmt = cell["ecosystem"], cell["format"]
        base = ROOT / "data" / eco / fmt
        status = cell.get("status")
        if (cell.get("phase") != "pilot" or cell.get("complete") is not False or
                cell.get("working_target") != 10 or cell.get("ceiling") != 10):
            raise ValueError(f"pilot cell is not explicitly incomplete: {eco}/{fmt}")
        if status == "pilot_not_started":
            if (cell.get("verified_third_party_count") != 0 or
                    cell.get("verified_standard_or_runtime_count") != 0 or
                    any((base / name).exists() for name in
                        ("cell.json", "parsers.json", "standard.json", "verification.json"))):
                raise ValueError(f"unreported pilot evidence or count: {eco}/{fmt}")
            continue
        if (not isinstance(status, str) or not status.startswith("pilot_")
                or status == "pilot_complete"):
            raise ValueError(f"unknown pilot status: {eco}/{fmt}/{status}")
        source = base / "cell.json"
        if not source.is_file():
            raise ValueError(f"pilot cell has no source record: {eco}/{fmt}")
        original = json.loads(source.read_text())
        if cell != {**original, "phase": "pilot", "complete": False}:
            raise ValueError(f"pilot matrix differs from its cell record: {eco}/{fmt}")
        count = cell["verified_third_party_count"]
        standard_count = cell["verified_standard_or_runtime_count"]
        if (not isinstance(count, int) or not 0 <= count <= 10 or
                not isinstance(standard_count, int) or standard_count < 0 or
                not isinstance(cell.get("uncertainty"), str) or not cell["uncertainty"].strip()):
            raise ValueError(f"pilot cell lacks bounded counts or uncertainty: {eco}/{fmt}")
        parsers = read(f"data/{eco}/{fmt}/parsers.json") if (base / "parsers.json").is_file() else []
        if len(parsers) != count or len({item["name"] for item in parsers}) != count:
            raise ValueError(f"pilot parser count or deduplication differs: {eco}/{fmt}")
        standard = read(f"data/{eco}/{fmt}/standard.json") if (base / "standard.json").is_file() else {"verified_apis": []}
        if len(standard["verified_apis"]) != standard_count:
            raise ValueError(f"pilot standard API count differs: {eco}/{fmt}")
        if count or standard_count:
            verification = (read(f"data/{eco}/{fmt}/verification.json")
                            if (base / "verification.json").is_file() else {})
            records = verification.get("third_party", verification.get("results", []))
            if records and (len(records) != count or
                            {item["package"] for item in records} !=
                            {item["name"] for item in parsers} or
                            not all(item.get("pass") is True for item in records)):
                raise ValueError(f"pilot control results differ from parser list: {eco}/{fmt}")
            results = {item["package"]: item for item in records}
            leads_file = base / "leads.json"
            lead_data = read(f"data/{eco}/{fmt}/leads.json") if leads_file.is_file() else []
            leads = lead_data.get("leads", []) if isinstance(lead_data, dict) else lead_data
            lead_by_name = {item.get("name"): item for item in leads}
            for parser in parsers:
                name = parser["name"]
                control = parser.get("control")
                if not control:
                    controls = verification.get("controls", {})
                    if isinstance(controls, dict):
                        control = next((value for value in controls.values()
                                        if isinstance(value, str) and value.startswith("controls/")), None)
                if (not all(parser.get(field) for field in
                            ("version", "license", "documentation", "family", "input_api"))
                        or not control or not (ROOT / control).is_file()):
                    raise ValueError(f"pilot parser lacks release/API/control evidence: {eco}/{fmt}/{name}")
                result = results.get(name)
                if result and (result.get("version") != parser["version"] or
                               result.get("output") != parser.get("expected_output")):
                    raise ValueError(f"pilot parser control result differs: {eco}/{fmt}/{name}")
                receipt = (parser.get("project") or (result or {}).get("project_receipt") or
                           (cell.get("third_party_control_results") if count == 1 else None))
                if isinstance(receipt, str) and receipt.endswith("/verification.json"):
                    receipt_path = ROOT / receipt
                elif isinstance(receipt, str):
                    receipt_path = ROOT / receipt / "verification.json"
                else:
                    receipt_path = None
                if not result and not (receipt_path and receipt_path.is_file()):
                    raise ValueError(f"pilot parser lacks control receipt: {eco}/{fmt}/{name}")
                if receipt_path and receipt_path.is_file():
                    observed = json.loads(receipt_path.read_text())
                    if (observed.get("pass") is not True or
                            observed.get("output") != parser.get("expected_output")):
                        raise ValueError(f"pilot parser receipt differs: {eco}/{fmt}/{name}")
                signals = [parser.get("metric"), parser.get("popularity"),
                           parser.get("adoption_exception"), lead_by_name.get(name)]
                numeric = any(isinstance(value, int) and not isinstance(value, bool) and value > 0
                              for signal in signals if isinstance(signal, dict)
                              for value in signal.values())
                if not numeric:
                    raise ValueError(f"pilot parser lacks a numeric adoption signal: {eco}/{fmt}/{name}")
            for api in standard["verified_apis"]:
                docs = api.get("documentation") or api.get("official_documentation")
                control = api.get("control")
                expected_output = api.get("expected", api.get("expected_output"))
                result = api.get("result")
                verification_result = next((item for item in verification.get("standard", [])
                                            if item.get("api") == api.get("api")), None)
                observed = (read(result) if isinstance(result, str) and
                            (ROOT / result).is_file() else {})
                if (not docs or not control or not (ROOT / control).is_file() or
                        expected_output is None or not result or not (ROOT / result).is_file() or
                        observed.get("pass") is not True or observed.get("output") != expected_output or
                        (verification_result and (verification_result.get("pass") is not True or
                                                  verification_result.get("output") != expected_output))):
                    raise ValueError(f"pilot standard API lacks official docs/control: {eco}/{fmt}")


def main() -> None:
    matrix = read("data/cells.json")["cells"]
    expected_cells = {(ecosystem, format_name)
                      for ecosystem in ECOSYSTEMS for format_name in FORMATS}
    assert len(matrix) == len(expected_cells)
    assert {(c["ecosystem"], c["format"]) for c in matrix} == expected_cells
    lock = read("package-lock.json")["packages"][""]["dependencies"]
    for cell in matrix:
        assert cell["working_target"] == 10 and cell["ceiling"] == 10
        if cell["status"] == "not_started":
            assert cell["verified_third_party_count"] == 0
            assert cell["search_hits_recorded"] == 0
            continue
        key = f"data/{cell['ecosystem']}/{cell['format']}"
        parsers = read(f"{key}/parsers.json")
        snapshot = read(f"{key}/registry-snapshot.json")
        searches = list(snapshot["search"])
        if cell.get("supplementary_search"):
            supplementary = read(cell["supplementary_search"])
            assert all(search["limit"] == cell["search_limit_per_query"]
                       for search in supplementary["search"])
            searches.extend(supplementary["search"])
        assert len(parsers) == cell["verified_third_party_count"]
        assert len(parsers) <= cell["ceiling"]
        assert len({p["name"] for p in parsers}) == len(parsers)
        if "verified_document_input_count" in cell:
            assert sum(p["input_variant"] == "svg_document" for p in parsers) == cell["verified_document_input_count"]
            assert sum(p["input_variant"] == "svg_path_data" for p in parsers) == cell["verified_path_data_only_count"]
            assert cell["verified_document_input_count"] + cell["verified_path_data_only_count"] == len(parsers)
        assert sum(len(s["hits"]) for s in searches) == cell["search_hits_recorded"]
        assert snapshot["search_limit_per_query"] == cell["search_limit_per_query"]
        hit_key = "packagePath" if cell["ecosystem"] == "go" else "name"
        assert len({hit[hit_key] for search in searches for hit in search["hits"]}) == cell["unique_search_hits"]
        assert len(searches) == len(cell["search_queries"])
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
                elif source.get("source_kind") == "tagged_source_files":
                    assert release["source_kind"] == "tagged_source_files"
                    assert source["release_commit"] == release["release_commit"]
                    assert source["tagged_files"] == release["tagged_files"]
                    assert source["source_sha256"] == release["source_sha256"]
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
                adapter_dir = ROOT / parser.get(
                    "adapter_manifest_dir", f"adapters/go/{cell['format']}")
                go_mod = (adapter_dir / "go.mod").read_text()
                go_versions = dict(re.findall(r"^\s*(\S+)\s+(v\S+)", go_mod, re.MULTILINE))
                assert parser["version"] == go_versions[parser["module"]]
                if parser.get("source_lock"):
                    source = read(parser["source_lock"])
                    assert source["package"] == name
                    assert source["module"] == parser["module"]
                    assert source["release"] == parser["version"]
                    assert (ROOT / parser["adapter"]).exists()
                    go_sum = (adapter_dir / "go.sum").read_text()
                    assert f"{parser['module']} {parser['version']} {source['module_sum']}" in go_sum
                    assert f"{parser['module']} {parser['version']}/go.mod {source['go_mod_sum']}" in go_sum
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
                elif parser.get("source_kind") == "tagged_source_module":
                    source = read(parser["source_lock"])[name]
                    assert parser["version"] == release["version"] == source["release"]
                    assert source["release_commit"] == release["source_reference"]
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
                if parser.get("source_kind") == "tagged_source_build":
                    source = read(parser["source_lock"])
                    assert source["package"] == name
                    assert source["release"] == parser["version"]
                    assert source["license"] == parser["license"]
                    assert source["source_sha256"] == snapshot["releases"][name]["source_sha256"]
                    assert len(source["source_sha256"]) == 64
                    assert (ROOT / parser["adapter"]).exists()
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
            if cell["ecosystem"] == "php" and cell["format"] == "ascii_ply":
                assert all(datetime.fromisoformat(row["checked_at_utc"]).tzinfo is not None
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
    validate_pilot_cells()
    print(f"Validated {len(matrix)} active cells and {len(ECOSYSTEMS) * len(PILOT_FORMATS)} "
          "explicitly incomplete pilot cells")


if __name__ == "__main__":
    main()
