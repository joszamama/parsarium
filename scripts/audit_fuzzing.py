"""Check that committed one-input and AFL++ smoke receipts are current."""

from hashlib import sha256
import json
import tomllib

from build_afl_native import OVERLAYS, derived_dockerfile
from build_afl_rust import AFL_RUST_RELEASE, dockerfile as rust_dockerfile, overlay_manifest, overlay_target
from run_case import ROOT, project_for


def main() -> None:
    manifests = sorted((ROOT / "projects").glob("*/*/*/manifest.json"))
    case_report = json.loads((ROOT / "data/fuzz-case-smoke.json").read_text())
    case_records = {item["project"]: item for item in case_report["results"]}
    assert len(case_records) == len(manifests) == case_report["projects_total"]
    for path in manifests:
        relative = path.parent.relative_to(ROOT / "projects")
        project, manifest = project_for(*relative.parts)
        verification = json.loads((project / "verification.json").read_text())
        assert verification["fuzz_engine_smoke_pass"]
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
        assert entry["status"] == ("per_case_only" if manifest["ecosystem"] == "php" else "ok")
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
        assert entry["status"] == "ready" and entry["unique_seeds"] == 1
        assert entry["control_sha256"] == manifest["control_sha256"]
        assert entry["project_receipt_sha256"] == sha256((project / "verification.json").read_bytes()).hexdigest()
        assert entry["image_id"] == json.loads((project / "verification.json").read_text())["image_id"]
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
        assert dockerfile == derived_dockerfile(project).encode()
        assert receipt["overlay_dockerfile_sha256"] == sha256(dockerfile).hexdigest()
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
                    "Dockerfile": rust_dockerfile(relative)}
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
    print(f"{len(manifests)}/{len(manifests)} one-input projects and native plans, "
          f"{batch_report['batch_passing']} batch replay projects, and "
          f"{len(native) + len(rust)}/{len(native) + len(rust)} AFL++ native overlays current")


if __name__ == "__main__":
    main()
