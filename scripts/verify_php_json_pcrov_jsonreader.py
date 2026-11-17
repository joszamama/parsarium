"""Recheck pcrov/jsonreader's two valid controls, parser source lines and AFL++ feedback."""

from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from verify_php_json_feedback import probe


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/json/php/pcrov_jsonreader"
OVERLAY = ROOT / "fuzzing/afl-native/json/php/pcrov_jsonreader"
REPORT = ROOT / "data/php/json/pcrov-jsonreader-feedback-differential.json"
PREFIX = "/work/vendor/pcrov/jsonreader/"


def replay(manifest: dict, image: str, control: Path, work: Path) -> dict:
    """Run the Xdebug control runner on one valid control and return its per-file line counts."""
    work.mkdir()
    result = subprocess.run(
        ["docker", "run", "--rm", "--platform", manifest["platform"],
         "--network", "none", "--read-only", "--cap-drop", "ALL",
         "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
         "--tmpfs", "/tmp:rw,nosuid,size=64m",
         "-v", f"{control}:/input/control:ro", "-v", f"{work}:/coverage", image],
        capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    summary = json.loads((work / "summary.json").read_text())
    files = json.loads((work / "coverage.json").read_text())["data"][0]["files"]
    if not summary["control_pass"] or not summary["file_and_stream_api_match"]:
        raise RuntimeError(f"{control.name}: control runner did not pass")
    if any(not item["filename"].startswith(PREFIX) for item in files):
        raise RuntimeError("coverage outside pcrov/jsonreader source")
    return {"output": summary["output"],
            "parser_source_lines_covered": summary["parser_source_lines_covered"],
            "lines_by_file": {item["filename"].removeprefix(PREFIX): item["summary"]["lines"]["covered"]
                              for item in files}}


def by_file(features: set) -> dict:
    return dict(sorted(Counter(item.removeprefix(PREFIX).rsplit(":", 1)[0] for item in features).items()))


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}:
        raise SystemExit("usage: verify_php_json_pcrov_jsonreader.py --write|--check")
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    base = json.loads((PROJECT / "verification.json").read_text())
    overlay = json.loads((OVERLAY / "verification.json").read_text())
    if manifest["coverage_subject_prefix"] != PREFIX:
        raise RuntimeError("coverage subject is not the pcrov/jsonreader package source")
    if f"ENV PARSARIUM_SUBJECT_PREFIX={PREFIX}\n" not in (OVERLAY / "Dockerfile").read_text():
        raise RuntimeError("AFL++ bridge is not scoped to the pcrov/jsonreader package source")
    if overlay["base_image_id"] != base["image_id"]:
        raise RuntimeError("AFL++ overlay was not built from the verified project image")
    control = ROOT / manifest["control"]
    differential = ROOT / manifest["differential_control"]
    for path, digest in ((control, manifest["control_sha256"]),
                         (differential, manifest["differential_control_sha256"])):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"{path.name}: control bytes changed")
    with tempfile.TemporaryDirectory(prefix="parsarium-pcrov-jsonreader-") as temporary:
        work = Path(temporary)
        lines = replay(manifest, base["image_id"], control, work / "control-lines")
        other_lines = replay(manifest, base["image_id"], differential, work / "differential-lines")
        image = overlay["image_id"]
        first = probe(manifest, image, control, work, "first", True)
        repeat = probe(manifest, image, control, work, "repeat", True)
        other = probe(manifest, image, differential, work, "other", True)
        other_repeat = probe(manifest, image, differential, work, "other-repeat", True)
    if lines["output"] != manifest["expected_output"]:
        raise RuntimeError("nested-object tree differs from manifest")
    if other_lines["output"] != manifest["differential_expected_output"]:
        raise RuntimeError("nested-array tree differs from manifest")
    if first != repeat or other != other_repeat:
        raise RuntimeError("repeated probe changed parser features or AFL++ map")
    if len(first[0]) != overlay["parser_source_features"] or len(first[1]) != overlay["feedback_edges"]:
        raise RuntimeError("control probe differs from overlay receipt")
    if len(first[0]) != lines["parser_source_lines_covered"]:
        raise RuntimeError("AFL++ bridge features differ from Xdebug control lines")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len({item.split(":", 1)[0] for item in first[1]} ^
                           {item.split(":", 1)[0] for item in other[1]})
    if not feature_difference or not tuple_difference:
        raise RuntimeError("differential control did not change parser feedback")
    result = {
        "project": "json/php/pcrov_jsonreader", "pass": True,
        "feedback_kind": overlay["feedback_kind"],
        "overlay_receipt_sha256": sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"], "overlay_image_id": image,
        "release_source_sha256": manifest["source_sha256"],
        "parser_source_prefix": PREFIX,
        "control": manifest["control"], "control_sha256": manifest["control_sha256"],
        "differential": manifest["differential_control"],
        "differential_sha256": manifest["differential_control_sha256"],
        "control_output_matches_oracle": True, "differential_output_matches_oracle": True,
        "file_and_stream_api_match": True,
        "control_source_lines_by_file": lines["lines_by_file"],
        "differential_source_lines_by_file": other_lines["lines_by_file"],
        "repeated_control_identical": True, "repeated_differential_identical": True,
        "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
        "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
        "parser_feature_difference": feature_difference,
        "afl_tuple_difference": tuple_difference,
        "control_only_features_by_file": by_file(first[0] - other[0]),
        "differential_only_features_by_file": by_file(other[0] - first[0]),
    }
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if sys.argv[1] == "--write":
        REPORT.write_text(output)
    elif REPORT.read_text() != output:
        raise SystemExit("pcrov/jsonreader feedback receipt changed")
    print(f"verified pcrov/jsonreader: {feature_difference} parser lines, "
          f"{tuple_difference} AFL++ tuples differ")


if __name__ == "__main__":
    main()
