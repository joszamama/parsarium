"""Check that committed one-input and AFL++ smoke receipts are current."""

from hashlib import sha256
import json
import tomllib

from build_afl_native import OVERLAYS, derived_dockerfile
from build_afl_rust import AFL_RUST_RELEASE, dockerfile as rust_dockerfile, overlay_manifest, overlay_target
from audit_projects import receipt_verified
from run_case import ROOT, project_for


def main() -> None:
    manifests = [path for path in sorted((ROOT / "projects").glob("*/*/*/manifest.json"))
                 if receipt_verified(path, json.loads(path.read_text()))]
    case_report = json.loads((ROOT / "data/fuzz-case-smoke.json").read_text())
    case_records = {item["project"]: item for item in case_report["results"]}
    assert len(case_records) == len(manifests) == case_report["projects_total"]
    for path in manifests:
        relative = path.parent.relative_to(ROOT / "projects")
        project, manifest = project_for(*relative.parts)
        verification = json.loads((project / "verification.json").read_text())
        assert verification["fuzz_engine_smoke_pass"]
        if manifest.get("coverage_kind") == "native_binary_edges":
            assert verification["coverage_kind"] == "native_binary_edges"
            assert verification["parser_source_lines_covered"] is None
            assert verification["underlying_source_lines_covered"] is None
            assert verification["binary_feedback_scope"] == "underlying_shared_library"
        else:
            assert verification["parser_source_lines_covered"] > 0
            if "format_specific_coverage_file_suffix" in manifest:
                assert verification["format_specific_source_lines_covered"] > 0
        entry = case_records[str(relative)]
        assert entry["status"] == "ok"
        assert entry["control"] == manifest["control"]
        assert entry["case_sha256"] == entry["control_sha256"] == manifest["control_sha256"]
        assert entry["project_receipt_sha256"] == sha256((project / "verification.json").read_bytes()).hexdigest()
        assert entry["image_id"]
    batch_report = json.loads((ROOT / "data/fuzz-batch-smoke.json").read_text())
    batch_records = {item["project"]: item for item in batch_report["results"]}
    assert len(batch_records) == len(manifests) == batch_report["projects_total"]
    for path in manifests:
        relative = path.parent.relative_to(ROOT / "projects")
        project, manifest = project_for(*relative.parts)
        entry = batch_records[str(relative)]
        per_case = (manifest["ecosystem"] == "php"
                    or manifest.get("native_campaign_supported") is False)
        assert entry["status"] == ("per_case_only" if per_case else "ok")
        assert entry["control_sha256"] == manifest["control_sha256"]
        assert entry["project_receipt_sha256"] == sha256((project / "verification.json").read_bytes()).hexdigest()
        if entry["status"] == "ok":
            assert entry["image_id"]
    native_plans = json.loads((ROOT / "data/native-plan-smoke.json").read_text())
    plan_records = {item["project"]: item for item in native_plans["results"]}
    assert len(plan_records) == len(manifests) == native_plans["projects_total"]
    for path in manifests:
        relative = path.parent.relative_to(ROOT / "projects")
        project, manifest = project_for(*relative.parts)
        entry = plan_records[str(relative)]
        if manifest.get("native_campaign_supported") is False:
            assert entry["status"] == "unsupported"
            assert entry["engine"] == "in-process native campaign"
        else:
            assert entry["status"] == "ready" and entry["unique_seeds"] == 1
        assert entry["control_sha256"] == manifest["control_sha256"]
        assert entry["project_receipt_sha256"] == sha256((project / "verification.json").read_bytes()).hexdigest()
        native_override = (manifest["ecosystem"] == "php" and
                           (manifest.get("kind") == "standard" or manifest.get("afl_entrypoint")))
        expected_image = (json.loads((OVERLAYS / relative / "verification.json").read_text())["image_id"]
                          if native_override else json.loads((project / "verification.json").read_text())["image_id"])
        assert entry["image_id"] == expected_image
    native = [path for path in manifests if path.parent.parent.name in {"c", "cpp"}]
    afl_report = json.loads((ROOT / "data/afl-native-smoke.json").read_text())
    afl_records = {item["project"]: item for item in afl_report["results"]}
    assert len(afl_records) == len(native) == afl_report["projects_total"]
    for path in native:
        relative = path.parent.relative_to(ROOT / "projects")
        project, manifest = project_for(*relative.parts)
        overlay = OVERLAYS / relative
        receipt = json.loads((overlay / "verification.json").read_text())
        record = afl_records[str(relative)]
        assert record["status"] == "verified" and receipt["pass"]
        assert record["feedback_edges"] == receipt["feedback_edges"] > 0
        assert record["image_id"] == receipt["image_id"]
        assert receipt["afl_map_size"] > 0
        assert receipt["control_sha256"] == manifest["control_sha256"]
        assert receipt["base_project_receipt_sha256"] == sha256((project / "verification.json").read_bytes()).hexdigest()
        dockerfile = (overlay / "Dockerfile").read_bytes()
        # These SVG paths use path-local builders to instrument librsvg's Rust
        # parser; the generic C overlay cannot build that parser.
        custom_rust_svg = str(relative) in {"svg/c/gdk_pixbuf", "svg/c/librsvg"}
        if manifest["package"] not in {"gstreamer", "netpbm", "sail"} and not custom_rust_svg:
            assert dockerfile == derived_dockerfile(project).encode()
        if custom_rust_svg:
            assert (overlay / "build.py").is_file()
            assert "build.py" in receipt.get("overlay_file_sha256", {})
        for name, digest in receipt.get("overlay_file_sha256", {}).items():
            assert sha256((overlay / name).read_bytes()).hexdigest() == digest
        expected_dockerfile_hash = (receipt.get("overlay_dockerfile_sha256") or
                                    receipt.get("overlay_file_sha256", {}).get("Dockerfile"))
        assert expected_dockerfile_hash == sha256(dockerfile).hexdigest()
    rust = [path for path in manifests if path.parent.parent.name == "rust"]
    rust_report = json.loads((ROOT / "data/afl-rust-smoke.json").read_text())
    rust_records = {item["project"]: item for item in rust_report["results"]}
    assert len(rust_records) == len(rust) == rust_report["projects_total"]
    for path in rust:
        relative = path.parent.relative_to(ROOT / "projects")
        project, manifest = project_for(*relative.parts)
        overlay = OVERLAYS / relative
        receipt = json.loads((overlay / "verification.json").read_text())
        record = rust_records[str(relative)]
        assert record["status"] == "verified" and receipt["pass"]
        assert record["feedback_edges"] == receipt["feedback_edges"] > 0
        assert record["image_id"] == receipt["image_id"]
        assert receipt["afl_map_size"] > 0
        assert receipt["control_sha256"] == manifest["control_sha256"]
        assert receipt["parser_source_sha256"] == manifest["source_sha256"]
        assert receipt["base_project_receipt_sha256"] == sha256((project / "verification.json").read_bytes()).hexdigest()
        expected = {"Cargo.toml": overlay_manifest(project),
                    "afl_fuzzer.rs": overlay_target(project),
                    "Dockerfile": rust_dockerfile(relative, manifest, receipt["afl_package"])}
        for name, text in expected.items():
            assert (overlay / name).read_text() == text
        lock = tomllib.loads((overlay / "Cargo.lock").read_text())
        parser = [item for item in lock["package"] if item["name"] == manifest["package"]
                  and item["version"] == manifest["release"]]
        assert len(parser) == 1 and parser[0]["checksum"] == manifest["source_sha256"]
        afl = [item for item in lock["package"] if item["name"] == "afl"
               and item["version"] == AFL_RUST_RELEASE]
        assert len(afl) == 1 and afl[0]["checksum"] == receipt["afl_rust_checksum"]
        for name, digest in receipt["overlay_file_sha256"].items():
            assert sha256((overlay / name).read_bytes()).hexdigest() == digest
    managed = [path for path in manifests if path.parent.parent.name in
               {"go", "java", "javascript", "python", "php"}]
    managed_report = json.loads((ROOT / "data/ecosystem-feedback-smoke.json").read_text())
    managed_records = {item["project"]: item for item in managed_report["results"]}
    assert len(managed_records) == len(managed) == managed_report["projects_total"]
    for path in managed:
        relative = path.parent.relative_to(ROOT / "projects")
        project, manifest = project_for(*relative.parts)
        record = managed_records[str(relative)]
        assert record["status"] == "verified" and record["ecosystem"] == manifest["ecosystem"]
        assert record["control_sha256"] == manifest["control_sha256"]
        assert record["project_receipt_sha256"] == sha256((project / "verification.json").read_bytes()).hexdigest()
        if manifest.get("coverage_kind") == "native_binary_edges":
            assert record["parser_source_lines_covered"] is None
            assert record["feedback_evidence"]["kind"] == "underlying_shared_library_binary_edges"
        else:
            assert record["parser_source_lines_covered"] > 0
        assert record["feedback_evidence"]["value"] > 0
    python_report = json.loads((ROOT / "data/afl-python-smoke.json").read_text())
    bridge_report = json.loads((ROOT / "data/afl-bridge-smoke.json").read_text())
    bridge_records = {item["project"]: item for report in (python_report, bridge_report)
                      for item in report["results"]}
    assert python_report["projects_verified"] == python_report["projects_total"] == len(
        [path for path in managed if path.parent.parent.name == "python"])
    assert bridge_report["projects_verified"] == bridge_report["projects_total"] == len(
        [path for path in managed if path.parent.parent.name != "python"])
    assert len(bridge_records) == len(managed)
    for path in managed:
        relative = path.parent.relative_to(ROOT / "projects")
        project, manifest = project_for(*relative.parts)
        overlay = OVERLAYS / relative
        receipt = json.loads((overlay / "verification.json").read_text())
        record = bridge_records[str(relative)]
        assert receipt == record and receipt["pass"]
        if manifest.get("coverage_kind") == "native_binary_edges":
            assert receipt["feedback_edges"] > 0
            assert receipt["source_lines_covered"] is None
            assert receipt["feedback_kind"] == "underlying_shared_library_binary_edges"
        elif manifest.get("kind") == "standard" and manifest["ecosystem"] == "php":
            assert receipt["feedback_edges"] > 0
            assert receipt["feedback_kind"] in {"native_php_runtime_source_edges",
                                                "native_php_http_parser_source_edges"}
        else:
            assert receipt["feedback_edges"] > 0 and receipt["parser_source_features"] > 0
        assert receipt["afl_map_size"] == 65536
        assert receipt["control_sha256"] == manifest["control_sha256"]
        assert receipt["base_project_receipt_sha256"] == sha256(
            (project / "verification.json").read_bytes()).hexdigest()
        for name, digest in receipt["overlay_file_sha256"].items():
            assert sha256((overlay / name).read_bytes()).hexdigest() == digest
        for name, digest in receipt.get("bridge_file_sha256", {}).items():
            assert sha256((ROOT / "fuzzing/afl-bridge" / name).read_bytes()).hexdigest() == digest
    for report_name in ("afl-feedback-differential.json", "afl-campaign-smoke.json"):
        report = json.loads((ROOT / "data" / report_name).read_text())
        assert report["projects_total"] == report["projects_passed"] == 5
        assert {item["project"].split("/")[1] for item in report["results"]} == {
            "go", "java", "javascript", "python", "php"}
        for item in report["results"]:
            overlay = OVERLAYS / item["project"]
            assert item["pass"]
            assert item["overlay_receipt_sha256"] == sha256(
                (overlay / "verification.json").read_bytes()).hexdigest()
            if report_name == "afl-feedback-differential.json":
                assert item["parser_feature_difference"] > 0
                assert item["afl_tuple_difference"] > 0
            else:
                assert item["executions"] > 0 and item["edges_found"] > 0
                assert item["queue_items"] > 0
    afl_plans = json.loads((ROOT / "data/afl-plan-smoke.json").read_text())
    assert afl_plans["projects_ready"] == afl_plans["projects_total"] == len(manifests)
    for item in afl_plans["results"]:
        assert item["status"] == "ready"
        receipt = OVERLAYS / item["project"] / "verification.json"
        assert item["overlay_receipt_sha256"] == sha256(receipt.read_bytes()).hexdigest()
    print(f"{len(manifests)}/{len(manifests)} one-input projects; "
          f"{native_plans['projects_ready']} in-process native plans ready, "
          f"{batch_report['batch_passing']} batch replay projects, and "
          f"{len(native) + len(rust) + len(managed)}/{len(manifests)} AFL++ overlays plus "
          f"{len(managed)}/{len(managed)} ecosystem feedback checks current")


if __name__ == "__main__":
    main()
