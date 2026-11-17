"""Audit container harnesses against third-party and standard API inventories."""

import argparse
from functools import cache
from hashlib import sha256
import json
from pathlib import Path
import re
from binary_feedback import check_binary_feedback


ROOT = Path(__file__).resolve().parents[1]


def browser_control_verified(path: Path, manifest: dict) -> bool:
    """Validate a staged browser control without treating adapter coverage as parser feedback."""
    if (manifest.get("coverage_kind") != "browser_control_only"
            or manifest.get("native_decoder_source_coverage") != "unavailable"
            or manifest.get("parser_feedback_available") is not False
            or "fuzz_engine" in manifest or "fuzz_engine_sha256" in manifest):
        return False
    receipt = path.parent / "control-verification.json"
    if not receipt.is_file():
        return False
    observed = json.loads(receipt.read_text())
    current_files = {
        str(file.relative_to(path.parent)): sha256(file.read_bytes()).hexdigest()
        for file in sorted(path.parent.rglob("*"))
        if file.is_file() and file.name not in {"control-verification.json", "README.md"}
        and "target" not in file.relative_to(path.parent).parts
        and "__pycache__" not in file.relative_to(path.parent).parts
    }
    return (
        observed.get("status") == "verified_control_only"
        and observed.get("api") == manifest["api"]
        and observed.get("runtime") == manifest["runtime"]
        and observed.get("base_image") == manifest["base_image"]
        and observed.get("browser_binary_sha256") == manifest["source_sha256"]
        and observed.get("image_id", "").startswith("sha256:")
        and observed.get("output") == manifest["expected_output"]
        and observed.get("control_sha256") == manifest["control_sha256"]
        and sha256((ROOT / manifest["control"]).read_bytes()).hexdigest() == manifest["control_sha256"]
        and observed.get("adapter_js_functions_covered", 0) > 0
        and observed.get("adapter_coverage_scope") == "browser-harness.js only"
        and observed.get("native_decoder_source_coverage") == "unavailable"
        and observed.get("parser_feedback_available") is False
        and observed.get("project_file_sha256") == current_files
    )


def native_source_control_verified(path: Path, manifest: dict) -> bool:
    """Validate a staged native parser source control without AFL feedback."""
    kind = manifest.get("coverage_kind")
    if (kind not in {"native_source_control_only", "native_source_afl_feedback"}
            or manifest.get("parser_feedback_available") is not
                (kind == "native_source_afl_feedback")
            or (kind == "native_source_control_only" and
                ("fuzz_engine" in manifest or "fuzz_engine_sha256" in manifest))):
        return False
    receipt = path.parent / "control-verification.json"
    if not receipt.is_file():
        return False
    observed = json.loads(receipt.read_text())
    current_files = {
        str(file.relative_to(path.parent)): sha256(file.read_bytes()).hexdigest()
        for file in sorted(path.parent.rglob("*"))
        if file.is_file() and file.name not in {"control-verification.json", "README.md"}
        and "target" not in file.relative_to(path.parent).parts
        and "__pycache__" not in file.relative_to(path.parent).parts
    }
    return (
        observed.get("status") == "verified_control_only"
        and observed.get("api") == manifest["api"]
        and observed.get("runtime") == manifest["runtime"]
        and observed.get("base_image") == manifest["base_image"]
        and observed.get("source_sha256") == manifest["source_sha256"]
        and observed.get("python_source_sha256") == manifest["python_source_sha256"]
        and observed.get("png_reader_source_sha256") == manifest["png_reader_source_sha256"]
        and observed.get("image_id", "").startswith("sha256:")
        and observed.get("output") == manifest["expected_output"]
        and observed.get("control_sha256") == manifest["control_sha256"]
        and sha256((ROOT / manifest["control"]).read_bytes()).hexdigest() == manifest["control_sha256"]
        and observed.get("parser_source_file") == "tkImgPNG.c"
        and observed.get("parser_source_lines_covered", 0) > 0
        and observed.get("parser_feedback_available") is False
        and observed.get("project_file_sha256") == current_files
    )


def native_source_feedback_verified(path: Path, manifest: dict) -> bool:
    """Bind Tk's source-covered control to decoder-scoped, differential AFL feedback."""
    if (manifest.get("coverage_kind") != "native_source_afl_feedback"
            or manifest.get("kind") != "standard"
            or manifest.get("parser_feedback_available") is not True
            or manifest.get("fuzz_engine") != "AFL++"
            or not native_source_control_verified(path, manifest)):
        return False
    project = path.parent.relative_to(ROOT / "projects")
    overlay_dir = ROOT / "fuzzing/afl-native" / project
    receipt_path = overlay_dir / "verification.json"
    if not receipt_path.is_file():
        return False
    receipt = json.loads(receipt_path.read_text())
    base_path = path.parent / "control-verification.json"
    base = json.loads(base_path.read_text())
    variant = ROOT / manifest.get("control_variant", "")
    if not variant.is_file():
        return False
    current_files = {
        str(file.relative_to(overlay_dir)): sha256(file.read_bytes()).hexdigest()
        for file in sorted(overlay_dir.rglob("*"))
        if file.is_file() and file.name not in {"verification.json", "README.md"}
        and "target" not in file.relative_to(overlay_dir).parts
        and "__pycache__" not in file.relative_to(overlay_dir).parts
    }
    docker_text = (overlay_dir / "Dockerfile").read_text()
    return (
        receipt.get("pass") is True
        and receipt.get("project") == str(project)
        and receipt.get("base_control_receipt_sha256") == sha256(base_path.read_bytes()).hexdigest()
        and receipt.get("base_image_id") == base["image_id"]
        and receipt.get("image_id", "").startswith("sha256:")
        and receipt.get("platform") == manifest["platform"]
        and receipt.get("afl_package") == manifest["afl_package"]
        and receipt.get("source_sha256") == manifest["source_sha256"]
        and receipt.get("png_reader_source_sha256") == manifest["png_reader_source_sha256"]
        and receipt.get("control_sha256") == manifest["control_sha256"]
        and receipt.get("variant_sha256") == manifest["control_variant_sha256"]
        and sha256(variant.read_bytes()).hexdigest() == manifest["control_variant_sha256"]
        and receipt.get("output") == manifest["expected_output"]
        and receipt.get("decoder_source_file") == "tkImgPNG.c"
        and receipt.get("decoder_source_lines_covered", 0) > 0
        and receipt.get("feedback_scope") == "AFL++ LLVM source allowlist: tkImgPNG.c"
        and receipt.get("afl_map_size", 0) > 0
        and receipt.get("unparsed_baseline_edges") == 0
        and receipt.get("control_edges", 0) >= 2
        and receipt.get("variant_edges", 0) >= 2
        and receipt.get("afl_edge_id_difference", 0) > 0
        and receipt.get("stable_identical_replays") is True
        and receipt.get("overlay_file_sha256") == current_files
        and manifest["source_sha256"] in docker_text
        and manifest["png_reader_source_sha256"] in docker_text
        and manifest["afl_package"] in docker_text
        and "src:tkImgPNG.c" in docker_text
    )


def standard_feedback_smoke_verified(path: Path, manifest: dict) -> bool:
    """Check the saved one-input and AFL plan preflight for a standard feedback path."""
    if not native_source_feedback_verified(path, manifest):
        return False
    receipt_path = ROOT / "data/standard-feedback-smoke.json"
    if not receipt_path.is_file():
        return False
    receipt = json.loads(receipt_path.read_text())
    project = path.parent.relative_to(ROOT / "projects")
    base_path = path.parent / "control-verification.json"
    overlay_path = ROOT / "fuzzing/afl-native" / project / "verification.json"
    files = ("parsarium.py", "scripts/run_case.py", "scripts/prepare_afl_run.py",
             "scripts/run_prepared_afl.py", "scripts/replay_corpus.py",
             "scripts/run_corpus_batch.py", "scripts/verify_standard_feedback.py")
    current_files = {name: sha256((ROOT / name).read_bytes()).hexdigest() for name in files}
    base = json.loads(base_path.read_text())
    overlay = json.loads(overlay_path.read_text())
    return (
        receipt.get("project") == str(project)
        and receipt.get("status") == "verified"
        and receipt.get("control_sha256") == manifest["control_sha256"]
        and receipt.get("variant_sha256") == manifest["control_variant_sha256"]
        and receipt.get("base_receipt_sha256") == sha256(base_path.read_bytes()).hexdigest()
        and receipt.get("overlay_receipt_sha256") == sha256(overlay_path.read_bytes()).hexdigest()
        and receipt.get("base_image_id") == base["image_id"]
        and receipt.get("overlay_image_id") == overlay["image_id"]
        and receipt.get("control_output") == manifest["expected_output"]
        and receipt.get("variant_output") == manifest["expected_output"]
        and receipt.get("afl_plan_status") == "ready"
        and receipt.get("replay_status") == "ok"
        and receipt.get("replay_unique_inputs") == 2
        and receipt.get("afl_target") == ["/work/afl-python", "/work/replay.py", "@@"]
        and receipt.get("cli_file_sha256") == current_files
    )


def third_party_control_verified(path: Path, manifest: dict) -> bool:
    """Validate a staged third-party Docker control without promoting parser feedback."""
    if (manifest.get("coverage_kind") != "control_only"
            or manifest.get("parser_feedback_available") is not False
            or manifest.get("native_parser_source_coverage") != "unavailable"):
        return False
    receipt = path.parent / "control-verification.json"
    if not receipt.is_file():
        return False
    observed = json.loads(receipt.read_text())
    parser_binary_pins = {
        key: value for key, value in manifest.items()
        if key.endswith(("_module_sha256", "_plugin_sha256"))
    }
    current_files = {
        str(file.relative_to(path.parent)): sha256(file.read_bytes()).hexdigest()
        for file in sorted(path.parent.rglob("*"))
        if file.is_file() and file.name not in {"control-verification.json", "README.md"}
        and "target" not in file.relative_to(path.parent).parts
        and "__pycache__" not in file.relative_to(path.parent).parts
    }
    return (
        observed.get("status") == "verified_control_only"
        and observed.get("platform") == manifest["platform"]
        and observed.get("base_image") == manifest["base_image"]
        and observed.get("release") == manifest["release"]
        and observed.get("source_sha256") == manifest["source_sha256"]
        and observed.get("image_id", "").startswith("sha256:")
        and observed.get("control_sha256") == manifest["control_sha256"]
        and observed.get("output") == manifest["expected_output"]
        and sha256((ROOT / manifest["control"]).read_bytes()).hexdigest() == manifest["control_sha256"]
        and observed.get("variant_sha256") == manifest.get("control_variant_sha256")
        and sha256((ROOT / manifest["control_variant"]).read_bytes()).hexdigest()
            == manifest["control_variant_sha256"]
        and observed.get("variant_output") != observed.get("output")
        and bool(parser_binary_pins)
        and all(re.fullmatch(r"[0-9a-f]{64}", value) is not None
                and observed.get(key) == value
                for key, value in parser_binary_pins.items())
        and observed.get("parser_source_lines_covered") is None
        and observed.get("parser_feedback_available") is False
        and observed.get("afl_feedback_edges") is None
        and observed.get("project_file_sha256") == current_files
    )


def macos_host_control_verified(path: Path, manifest: dict) -> bool:
    """Validate the pinned macOS control, separately from Docker and AFL paths."""
    if (manifest.get("kind") != "standard"
            or manifest.get("coverage_kind") != "macos_host_control_only"
            or manifest.get("execution") != "macos_host"
            or manifest.get("parser_feedback_available") is not False):
        return False
    receipt = path.parent / "control-verification.json"
    if not receipt.is_file():
        return False
    observed = json.loads(receipt.read_text())
    current_files = {
        str(file.relative_to(path.parent)): sha256(file.read_bytes()).hexdigest()
        for file in sorted(path.parent.rglob("*"))
        if file.is_file() and file.name not in {"control-verification.json", "README.md"}
        and "target" not in file.relative_to(path.parent).parts
        and "__pycache__" not in file.relative_to(path.parent).parts
    }
    adapter = ROOT / manifest["evidence_adapter"]
    return (
        observed.get("status") == "verified_control_only"
        and observed.get("api") == manifest["api"]
        and observed.get("runtime") == manifest["runtime"]
        and observed.get("execution") == "macos_host"
        and observed.get("toolchain") == manifest["toolchain"]
        and re.fullmatch(r"[0-9a-f]{64}", observed.get("replay_binary_sha256", "")) is not None
        and observed.get("evidence_adapter_sha256") == manifest["evidence_adapter_sha256"]
        and observed.get("evidence_adapter_output") == manifest["expected_output"]
        and sha256(adapter.read_bytes()).hexdigest() == manifest["evidence_adapter_sha256"]
        and observed.get("control_sha256") == manifest["control_sha256"]
        and sha256((ROOT / manifest["control"]).read_bytes()).hexdigest() == manifest["control_sha256"]
        and observed.get("output") == manifest["expected_output"]
        and observed.get("container") == "unavailable"
        and observed.get("parser_source_coverage") == "unavailable"
        and observed.get("parser_feedback_available") is False
        and observed.get("afl_feedback") == "unavailable"
        and observed.get("project_file_sha256") == current_files
    )


@cache
def smoke_rows(filename: str) -> dict[str, dict]:
    report = json.loads((ROOT / "data" / filename).read_text())
    return {item["project"]: item for item in report["results"]}


def lwjgl_assimp_native_feedback_verified(path: Path, manifest: dict,
                                          overlay: dict) -> bool:
    """Require native Assimp PLY features, rather than Java wrapper feedback."""
    project = path.parent.relative_to(ROOT / "projects")
    if str(project) != "ascii_ply/java/lwjgl_assimp":
        return True
    base = json.loads((path.parent / "verification.json").read_text())
    overlay_dir = ROOT / "fuzzing/afl-native" / project
    variant = ROOT / "controls/ascii_ply/triangle-colour.ply"
    expected_files = {"Dockerfile", "afl_trace", "native_trace.py", "build.py"}
    file_hashes = overlay.get("overlay_file_sha256", {})
    feature_count = overlay.get("parser_source_features", 0)
    variant_counts = overlay.get("variant_repeat_feature_counts")
    return (
        manifest.get("underlying_coverage_subject_prefix")
            == "/work/source/code/AssetLib/Ply/"
        and overlay.get("feedback_kind")
            == "java_native_assimp_ply_regions_to_afl_bitmap"
        and overlay.get("feedback_scope")
            == "LLVM source regions in pinned Assimp PLY importer; Java wrapper excluded"
        and overlay.get("base_image_id") == base["image_id"]
        and overlay.get("source_sha256") == manifest["source_sha256"]
        and overlay.get("underlying_source_sha256") == manifest["underlying_source_sha256"]
        and variant.is_file()
        and overlay.get("variant_sha256") == sha256(variant.read_bytes()).hexdigest()
        and overlay.get("afl_package") == "4.09c-1ubuntu3"
        and overlay.get("afl_map_size") == 65536
        and feature_count > 0
        and overlay.get("control_repeat_feature_counts") == [feature_count, feature_count]
        and overlay.get("stable_control_features") == feature_count
        and isinstance(variant_counts, list) and len(variant_counts) == 2
        and variant_counts[0] == variant_counts[1] and variant_counts[0] > 0
        and overlay.get("stable_variant_only_features", 0) > 0
        and overlay.get("variant_feedback_edges", 0) > 1
        and set(file_hashes) == expected_files
        and all((overlay_dir / name).is_file()
                and sha256((overlay_dir / name).read_bytes()).hexdigest() == digest
                for name, digest in file_hashes.items())
        and set(overlay.get("bridge_file_sha256", {})) == {"afl_proxy.c", "JavaCase.java"}
    )


def fltk_native_feedback_verified(path: Path, manifest: dict, overlay: dict) -> bool:
    """Require the native FLTK PNM source to contribute AFL++ feedback."""
    project = path.parent.relative_to(ROOT / "projects")
    if str(project) != "ascii_pnm/rust/fltk":
        return True
    overlay_dir = ROOT / "fuzzing/afl-native" / project
    file_hashes = overlay.get("overlay_file_sha256", {})
    rust_edges = overlay.get("rust_only_feedback_edges", 0)
    native_edges = overlay.get("native_feedback_edges", 0)
    return (
        manifest.get("underlying_format_specific_coverage_file_suffix")
            == "/Fl_PNM_Image.cxx"
        and overlay.get("feedback_kind") == "rust_and_native_fltk_source_edges"
        and overlay.get("parser_source_sha256") == manifest["source_sha256"]
        and overlay.get("underlying_source_sha256") == manifest["underlying_source_sha256"]
        and overlay.get("afl_rust_release") == "0.18.2"
        and overlay.get("afl_package") == "4.33c-1.1ubuntu1"
        and native_edges > 0 and rust_edges > 0
        and native_edges + rust_edges == overlay.get("feedback_edges")
        and overlay.get("afl_map_size", 0) > overlay.get("rust_only_afl_map_size", 0)
        and set(file_hashes)
            == {"Cargo.toml", "Cargo.lock", "afl_fuzzer.rs", "Dockerfile", "build.py"}
        and all((overlay_dir / name).is_file()
                and sha256((overlay_dir / name).read_bytes()).hexdigest() == digest
                for name, digest in file_hashes.items())
    )


def vlc_cpp_mp4_feedback_verified(path: Path, manifest: dict, overlay: dict) -> bool:
    """Bind C++ VLC feedback to its MP4-only instrumented plugin."""
    project = path.parent.relative_to(ROOT / "projects")
    if str(project) != "mp4/cpp/vlc":
        return True
    overlay_dir = ROOT / "fuzzing/afl-native" / project
    variant = path.parent / manifest.get("valid_variant", "")
    file_hashes = overlay.get("overlay_file_sha256", {})
    control_stability = overlay.get("control_stability", {})
    variant_stability = overlay.get("variant_stability", {})
    return (
        overlay.get("feedback_kind") == "vlc_mp4_plugin_pcguard_edges"
        and "modules/demux/mp4" in overlay.get("feedback_scope", "")
        and "harness uninstrumented" in overlay.get("feedback_scope", "")
        and overlay.get("shared_parser_family") == manifest.get("shared_parser_family")
        and overlay.get("shared_parser_family_projects")
            == manifest.get("shared_parser_family_projects")
        and overlay.get("source_sha256") == manifest["source_sha256"]
        and variant.is_file()
        and overlay.get("variant_sha256") == manifest.get("valid_variant_sha256")
            == sha256(variant.read_bytes()).hexdigest()
        and overlay.get("variant_output") == manifest.get("valid_variant_expected_output")
        and overlay.get("repeats", 0) >= 3
        and control_stability.get("all_repeats_identical") is True
        and variant_stability.get("all_repeats_identical") is True
        and control_stability.get("stable_edges") == overlay.get("feedback_edges")
        and variant_stability.get("stable_edges") == overlay.get("variant_feedback_edges")
        and overlay.get("stable_variant_only_edges", 0) > 0
        and set(file_hashes) == {"Dockerfile", "build.py"}
        and all((overlay_dir / name).is_file()
                and sha256((overlay_dir / name).read_bytes()).hexdigest() == digest
                for name, digest in file_hashes.items())
    )


def fully_runnable(path: Path, manifest: dict) -> bool:
    """Require a current base receipt, AFL++ overlay, and replay plans."""
    if manifest.get("coverage_kind") == "native_source_afl_feedback":
        return standard_feedback_smoke_verified(path, manifest)
    if not receipt_verified(path, manifest):
        return False
    project = path.parent.relative_to(ROOT / "projects")
    key = str(project)
    base_sha = sha256((path.parent / "verification.json").read_bytes()).hexdigest()
    overlay_path = ROOT / "fuzzing" / "afl-native" / project / "verification.json"
    if not overlay_path.is_file():
        return False
    overlay = json.loads(overlay_path.read_text())
    if (overlay.get("pass") is not True
            or overlay.get("base_project_receipt_sha256") != base_sha
            or overlay.get("control_sha256") != manifest["control_sha256"]
            or overlay.get("feedback_edges", 0) < 2):
        return False
    if not lwjgl_assimp_native_feedback_verified(path, manifest, overlay):
        return False
    if not fltk_native_feedback_verified(path, manifest, overlay):
        return False
    if not vlc_cpp_mp4_feedback_verified(path, manifest, overlay):
        return False
    for name, digest in overlay.get("bridge_file_sha256", {}).items():
        bridge_file = ROOT / "fuzzing/afl-bridge" / name
        if not bridge_file.is_file() or sha256(bridge_file.read_bytes()).hexdigest() != digest:
            return False
    if manifest.get("coverage_kind") == "native_binary_edges":
        base = json.loads((path.parent / "verification.json").read_text())
        dockerfile = overlay_path.parent / "Dockerfile"
        if (overlay.get("coverage_kind") != "native_binary_edges"
                or overlay.get("feedback_kind") != "underlying_shared_library_binary_edges"
                or overlay.get("source_lines_covered", False) is not None
                or overlay.get("binary_feedback") != base["binary_feedback"]
                or overlay.get("image_id") != base["binary_feedback_image_id"]
                or not dockerfile.is_file()
                or dockerfile.read_bytes() != (path.parent / "binary-feedback/Dockerfile").read_bytes()
                or overlay.get("overlay_file_sha256", {}).get("Dockerfile")
                != sha256(dockerfile.read_bytes()).hexdigest()):
            return False
    native_status = "unsupported" if manifest.get("native_campaign_supported") is False else "ready"
    checks = (("fuzz-case-smoke.json", {"ok"}),
              ("fuzz-batch-smoke.json", {"ok", "per_case_only"}),
              ("native-plan-smoke.json", {native_status}),
              ("afl-plan-smoke.json", {"ready"}))
    for filename, accepted in checks:
        row = smoke_rows(filename).get(key)
        if row is None or row.get("status") not in accepted:
            return False
        if "project_receipt_sha256" in row and row["project_receipt_sha256"] != base_sha:
            return False
        if "overlay_receipt_sha256" in row and row["overlay_receipt_sha256"] != sha256(overlay_path.read_bytes()).hexdigest():
            return False
    return True


def receipt_verified(path: Path, manifest: dict) -> bool:
    verification_path = path.parent / "verification.json"
    if not verification_path.exists():
        return False
    result = json.loads(verification_path.read_text())
    current_files = {str(file.relative_to(path.parent)): sha256(file.read_bytes()).hexdigest()
                     for file in sorted(path.parent.rglob("*"))
                     if file.is_file() and file.name != "verification.json"
                     and file.relative_to(path.parent) != Path("README.md")
                     and "target" not in file.relative_to(path.parent).parts
                     and "vendor" not in file.relative_to(path.parent).parts
                     and "__pycache__" not in file.relative_to(path.parent).parts}
    binary = manifest.get("coverage_kind") == "native_binary_edges"
    if binary:
        try:
            check_binary_feedback(path.parent, ROOT, manifest, result["binary_feedback"])
        except (KeyError, TypeError, ValueError, OSError):
            return False
        coverage_ok = (
            result.get("coverage_kind") == "native_binary_edges"
            and result.get("binary_feedback_scope") == "underlying_shared_library"
            and result.get("binary_feedback_image_id", "").startswith("sha256:")
            and result.get("parser_source_files") is None
            and result.get("parser_source_lines_covered") is None
            and result.get("format_specific_source_lines_covered") is None
            and result.get("underlying_source_files") is None
            and result.get("underlying_source_lines_covered") is None
            and result.get("coverage_output") is None
        )
    else:
        coverage_ok = (
            result.get("parser_source_files", 0) > 0
            and result.get("parser_source_lines_covered", 0) > 0
            and ("format_specific_coverage_file_suffix" not in manifest
                 or (result.get("format_specific_source_lines_covered") or 0) > 0)
            and ("underlying_coverage_subject_prefix" not in manifest
                 or (result.get("underlying_source_lines_covered") or 0) > 0)
        )
    if (result.get("pass") is not True or result.get("fuzz_engine_smoke_pass") is not True
            or result.get("kind", "third_party") != manifest.get("kind", "third_party")
            or (manifest.get("kind") == "standard"
                and (result.get("api") != manifest["api"]
                     or result.get("runtime") != manifest["runtime"]))
            or result.get("manifest") != str(path.relative_to(ROOT))
            or result.get("source_sha256") != manifest["source_sha256"]
            or result.get("platform") != manifest["platform"]
            or not result.get("image_id", "").startswith("sha256:")
            or not result.get("toolchain")
            or result.get("output") != manifest["expected_output"]
            or not coverage_ok
            or result.get("control_sha256") != manifest["control_sha256"]
            or result.get("project_file_sha256") != current_files):
        return False
    return True


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("--write", action="store_true")
    cli.add_argument("--check", action="store_true")
    args = cli.parse_args()
    if args.write and args.check:
        cli.error("choose --write or --check")

    catalog = {}
    for path in sorted((ROOT / "data").glob("*/*/parsers.json")):
        ecosystem, format_name = path.relative_to(ROOT / "data").parts[:2]
        for parser in json.loads(path.read_text()):
            key = (format_name, ecosystem, parser["name"])
            if key in catalog:
                raise ValueError(f"duplicate catalog path: {key}")
            catalog[key] = parser

    standard_by_cell = {}
    standard_catalog = {}
    for path in sorted((ROOT / "data").glob("*/*/standard.json")):
        ecosystem, format_name = path.relative_to(ROOT / "data").parts[:2]
        inventory = json.loads(path.read_text())
        entries = inventory["verified_apis"]
        standard_by_cell[(format_name, ecosystem)] = len(entries)
        for entry in entries:
            identifier = entry.get("api") or entry.get("name") or entry.get("input_api")
            key = (format_name, ecosystem, identifier)
            if key in standard_catalog:
                raise ValueError(f"duplicate standard API path: {key}")
            standard_catalog[key] = {
                **entry,
                "runtime": entry.get("runtime", inventory.get("runtime")),
                "expected": entry.get("expected", entry.get("expected_output",
                            entry.get("result") if isinstance(entry.get("result"), dict) else None)),
            }
    if set(standard_by_cell) != {key[:2] for key in catalog}:
        raise ValueError("standard API inventory does not cover the catalog matrix")

    completed = set()
    staged = set()
    standard_completed = set()
    standard_staged = set()
    for path in sorted((ROOT / "projects").glob("*/*/*/manifest.json")):
        parts = path.relative_to(ROOT / "projects").parts
        manifest = json.loads(path.read_text())
        if manifest.get("kind") == "standard":
            key = (manifest["format"], manifest["ecosystem"], manifest["api"])
            if parts[0:2] != key[0:2] or key not in standard_catalog:
                raise ValueError(f"standard project does not match inventory: {path}")
            if key in standard_completed or key in standard_staged:
                raise ValueError(f"duplicate standard project: {key}")
            entry = standard_catalog[key]
            if (entry["runtime"] != manifest["runtime"]
                    or entry["control"] != manifest["control"]
                    or entry["expected"] != manifest["expected_output"]):
                raise ValueError(f"standard API evidence mismatch: {path}")
            lock = json.loads((path.parent / manifest["runtime_lock"]).read_text())
            if lock != {"runtime": manifest["runtime"],
                        "base_image": manifest["base_image"],
                        "source_sha256": manifest["source_sha256"]}:
                raise ValueError(f"runtime lock mismatch: {path}")
            if sha256((ROOT / manifest["control"]).read_bytes()).hexdigest() != manifest["control_sha256"]:
                raise ValueError(f"standard control hash mismatch: {path}")
            dockerfile = path.parent / "Dockerfile"
            if not dockerfile.is_file() or not (path.parent / manifest["harness"]).is_file():
                raise ValueError(f"missing standard Dockerfile or harness: {path}")
            docker_text = dockerfile.read_text()
            if manifest.get("coverage_kind") == "browser_control_only":
                if not browser_control_verified(path, manifest):
                    raise ValueError(f"browser control receipt mismatch: {path}")
                pinned_fields = ("base_image", "source_sha256")
            elif manifest.get("coverage_kind") in {"native_source_control_only", "native_source_afl_feedback"}:
                if not native_source_control_verified(path, manifest):
                    raise ValueError(f"native source control receipt mismatch: {path}")
                if (manifest["coverage_kind"] == "native_source_afl_feedback"
                        and not standard_feedback_smoke_verified(path, manifest)):
                    raise ValueError(f"native source AFL feedback or execution receipt mismatch: {path}")
                pinned_fields = ("base_image", "source_sha256", "python_source_sha256",
                                 "png_reader_source_sha256")
            else:
                pinned_fields = ("base_image", "source_sha256", "fuzz_engine_sha256")
            if any(manifest[field] not in docker_text for field in pinned_fields):
                raise ValueError(f"standard Dockerfile pin mismatch: {path}")
            (standard_completed if fully_runnable(path, manifest) else standard_staged).add(key)
            continue
        if manifest.get("kind", "third_party") != "third_party":
            raise ValueError(f"unknown project kind: {path}")
        key = (manifest["format"], manifest["ecosystem"], manifest["package"])
        if parts[0:2] != key[0:2] or key not in catalog:
            raise ValueError(f"project does not match catalog: {path}")
        if key in completed or key in staged:
            raise ValueError(f"duplicate project: {key}")
        parser = catalog[key]
        if "expected_output" in parser:
            expected = parser["expected_output"]
        else:
            legacy = json.loads((ROOT / manifest["catalog_parser"]).with_name("verification.json").read_text())
            records = legacy.get("third_party", legacy.get("results", []))
            record, = [item for item in records if item["package"] == manifest["package"]]
            if record["pass"] is not True or record["version"] != manifest["release"]:
                raise ValueError(f"legacy verification mismatch: {path}")
            expected = record["output"]
        if manifest["release"] != parser["version"] or manifest["expected_output"] != expected:
            raise ValueError(f"release or output mismatch: {path}")
        control = ROOT / manifest["control"]
        if sha256(control.read_bytes()).hexdigest() != manifest["control_sha256"]:
            raise ValueError(f"control hash mismatch: {path}")
        lock_path = ROOT / manifest["source_lock"]
        if lock_path.suffix == ".json":
            source = json.loads(lock_path.read_text())[manifest["package"]]
            if source["release"] != manifest["release"] or source["source_sha256"] != manifest["source_sha256"]:
                raise ValueError(f"source lock mismatch: {path}")
            if "go_module_sum" in source and (f"{source.get('go_module', manifest['package'])} {manifest['release']} "
                    f"{source['go_module_sum']}") not in (path.parent / "go.sum").read_text():
                raise ValueError(f"Go module sum mismatch: {path}")
            if "npm_integrity" in source:
                npm_lock = json.loads((path.parent / "package-lock.json").read_text())
                npm_package = npm_lock["packages"][f"node_modules/{manifest['package']}"]
                if (npm_package["version"] != manifest["release"]
                        or npm_package["integrity"] != source["npm_integrity"]):
                    raise ValueError(f"npm integrity mismatch: {path}")
                if (manifest.get("fuzz_engine") == "Jazzer.js"
                        and npm_lock["packages"]["node_modules/@jazzer.js/core"]["version"]
                        != manifest["fuzz_engine_release"]):
                    raise ValueError(f"Jazzer.js release mismatch: {path}")
            if "composer_reference" in source:
                composer_lock = json.loads((path.parent / "composer.lock").read_text())
                composer_package, = [item for item in composer_lock["packages"]
                                     if item["name"] == manifest["package"]]
                if (composer_package["version"] != manifest["release"]
                        or composer_package["source"]["reference"] != source["composer_reference"]):
                    raise ValueError(f"Composer source mismatch: {path}")
                if manifest.get("fuzz_engine") == "nikic/php-fuzzer":
                    engine, = [item for item in composer_lock["packages"]
                               if item["name"] == "nikic/php-fuzzer"]
                    if engine["version"] != manifest["fuzz_engine_release"]:
                        raise ValueError(f"PHP fuzzer release mismatch: {path}")
        else:
            lock = lock_path.read_text()
            normalized = lambda value: re.sub(r"[-_.]+", "-", value).lower()
            versions = {normalized(name): version for name, version in
                        re.findall(r"(?m)^([A-Za-z0-9_.-]+)==([^\s\\]+)", lock)}
            if (versions.get(normalized(manifest["package"])) != manifest["release"]
                    or manifest["source_sha256"] not in lock):
                raise ValueError(f"source lock mismatch: {path}")
        dockerfile = path.parent / "Dockerfile"
        if not dockerfile.is_file() or not (path.parent / manifest["harness"]).is_file():
            raise ValueError(f"missing Dockerfile or harness: {path}")
        docker_text = dockerfile.read_text()
        for field in ("base_image", "source_sha256", "fuzz_engine_sha256", "underlying_runtime_base_image"):
            if field in manifest and manifest[field] not in docker_text:
                raise ValueError(f"Dockerfile does not pin {field}: {path}")
        if "underlying_npm_integrity" in manifest:
            npm_lock = json.loads((path.parent / "package-lock.json").read_text())
            underlying = npm_lock["packages"][f"node_modules/{manifest['underlying_package']}"]
            if (underlying["version"] != manifest["underlying_release"]
                    or underlying["integrity"] != manifest["underlying_npm_integrity"]):
                raise ValueError(f"underlying NPM lock mismatch: {path}")
        for dependency in manifest.get("dependencies", []):
            if (lock_path.suffix == ".json"
                    or f"{dependency['package']}=={dependency['release']}" not in lock
                    or dependency["sha256"] not in lock
                    or dependency["sha256"] not in docker_text):
                raise ValueError(f"dependency pin mismatch: {path}")
        if (manifest.get("coverage_kind") == "control_only"
                and not third_party_control_verified(path, manifest)):
            raise ValueError(f"third-party staged control receipt mismatch: {path}")
        (completed if fully_runnable(path, manifest) else staged).add(key)

    for path in sorted((ROOT / "projects").glob("*/*/*/macos-manifest.json")):
        parts = path.relative_to(ROOT / "projects").parts
        manifest = json.loads(path.read_text())
        key = (manifest["format"], manifest["ecosystem"], manifest["api"])
        if parts[0:2] != key[0:2] or key not in standard_catalog:
            raise ValueError(f"host-only project does not match standard inventory: {path}")
        if key in standard_completed or key in standard_staged:
            raise ValueError(f"duplicate standard project: {key}")
        entry = standard_catalog[key]
        if (entry["runtime"] != manifest["runtime"]
                or entry["control"] != manifest["control"]
                or entry["expected"] != manifest["expected_output"]
                or entry["input_api"] != manifest["input_api"]):
            raise ValueError(f"host-only standard evidence mismatch: {path}")
        if not macos_host_control_verified(path, manifest):
            raise ValueError(f"host-only control receipt mismatch: {path}")
        standard_staged.add(key)

    cells = []
    for format_name, ecosystem in sorted({key[:2] for key in catalog}):
        keys = {key for key in catalog if key[:2] == (format_name, ecosystem)}
        standard_keys = {key for key in standard_catalog if key[:2] == (format_name, ecosystem)}
        standard_count = standard_by_cell[(format_name, ecosystem)]
        cells.append({"format": format_name, "ecosystem": ecosystem,
                      "catalog_paths": len(keys), "containerized_verified": len(keys & completed),
                      "staged": len(keys & staged), "pending": len(keys - completed - staged),
                      "standard_api_paths": standard_count,
                      "standard_containerized_verified": len(standard_keys & standard_completed),
                      "standard_staged": len(standard_keys & standard_staged),
                      "standard_pending": len(standard_keys - standard_completed - standard_staged)})
    standard_total = sum(standard_by_cell.values())
    runnable_cells = sum(cell["containerized_verified"] > 0 for cell in cells)
    report = {"schema_version": 3, "catalog_paths": len(catalog),
              "cells_total": len(cells), "cells_with_verified_project": runnable_cells,
              "cells_pending": len(cells) - runnable_cells,
              "containerized_verified": len(completed), "staged": len(staged),
              "pending": len(catalog) - len(completed) - len(staged),
              "standard_api_paths": standard_total,
              "standard_containerized_verified": len(standard_completed),
              "standard_staged": len(standard_staged),
              "standard_pending": standard_total - len(standard_completed) - len(standard_staged),
              "cells": cells}
    output = ROOT / "data/projects-coverage.json"
    serialized = json.dumps(report, indent=2) + "\n"
    if args.write:
        output.write_text(serialized)
    if args.check and output.read_text() != serialized:
        raise ValueError("data/projects-coverage.json is stale; run --write")
    print(f"{runnable_cells}/{len(cells)} cells runnable; "
          f"{len(completed)}/{len(catalog)} containerized parser paths verified; "
          f"{len(staged)} staged; {report['pending']} pending; "
          f"{len(standard_completed)}/{standard_total} standard API paths covered")


if __name__ == "__main__":
    main()
