"""Recheck xmldoc's XmlDocument path: both valid controls against the expat
oracle, V8 coverage per source file, and stable, differential AFL++ feedback
confined to xmldoc and its underlying sax.

xmldoc runs sax without namespace processing, so outputs are raw qualified
names. The receipt stays candidate-scoped and does not touch the shared XML
cell files.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from verify_javascript_xml_feedback import probe, run, sandbox
from run_case import ROOT


PROJECT = ROOT / "projects/xml/javascript/xmldoc"
OVERLAY = ROOT / "fuzzing/afl-native/xml/javascript/xmldoc"
REPORT = ROOT / "data/javascript/xml/xmldoc-feedback-differential.json"
MODULES = "/work/node_modules/"
PARSER_FILE = MODULES + "xmldoc/dist/index.js"
PACKAGES = {"xmldoc", "sax"}


def package_of(feature: str) -> str:
    return feature[len(MODULES):].split("/", 1)[0]


def by_file(features: set) -> dict:
    counts: dict = {}
    for feature in features:
        name = feature[len(MODULES):].rsplit(":", 1)[0]
        counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items()))


def by_package(features: set) -> dict:
    counts: dict = {}
    for feature in features:
        counts[package_of(feature)] = counts.get(package_of(feature), 0) + 1
    return dict(sorted(counts.items()))


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}:
        raise SystemExit("usage: verify_javascript_xml_xmldoc.py --write|--check")
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    base = json.loads((PROJECT / "verification.json").read_text())
    receipt = json.loads((OVERLAY / "verification.json").read_text())
    if receipt["base_image_id"] != base["image_id"]:
        raise ValueError("overlay was built from a different project image")
    if receipt["base_project_receipt_sha256"] != sha256((PROJECT / "verification.json").read_bytes()).hexdigest():
        raise ValueError("overlay receipt does not pin the current project receipt")
    if manifest["afl_coverage_subject_prefix"] != MODULES:
        raise ValueError("unexpected AFL++ subject prefix")
    oracle = json.loads(subprocess.run([sys.executable, "-I", str(PROJECT / "oracle.py")],
                                       check=True, capture_output=True, text=True).stdout)
    control, differential = ROOT / manifest["control"], ROOT / manifest["differential_control"]
    for path, digest, expected in (
            (control, manifest["control_sha256"], manifest["expected_output"]),
            (differential, manifest["differential_control_sha256"], manifest["differential_expected_output"])):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")
        if oracle[manifest["control" if path == control else "differential_control"]] != expected:
            raise RuntimeError(f"manifest output differs from expat oracle: {path}")
    with tempfile.TemporaryDirectory(prefix="parsarium-xmldoc-") as temporary:
        work = Path(temporary)
        replayed = {}
        for key, path in (("control", control), ("differential", differential)):
            replayed[key] = json.loads(run([*sandbox(manifest, path, work), "--entrypoint", "node",
                                            base["image_id"], "/work/replay.js", "/input/case"]))
        if replayed["control"] != manifest["expected_output"]:
            raise RuntimeError(f"first control output differs: {replayed['control']}")
        if replayed["differential"] != manifest["differential_expected_output"]:
            raise RuntimeError(f"second control output differs: {replayed['differential']}")
        coverage_dir = work / "coverage"
        coverage_dir.mkdir()
        run(["docker", "run", "--rm", "--platform", manifest["platform"], "--network", "none",
             "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
             "--user", f"{os.getuid()}:{os.getgid()}",
             "--tmpfs", "/tmp:rw,nosuid,size=64m",
             "-v", f"{control}:/input/control:ro", "-v", f"{coverage_dir}:/coverage",
             base["image_id"]])
        lines = json.loads((coverage_dir / "summary.json").read_text())["lines_covered_by_file"]
        first = probe(manifest, receipt["image_id"], control, work, "first")
        repeat = probe(manifest, receipt["image_id"], control, work, "repeat")
        other = probe(manifest, receipt["image_id"], differential, work, "other")
        other_repeat = probe(manifest, receipt["image_id"], differential, work, "other-repeat")
    if first != repeat or other != other_repeat:
        raise RuntimeError("repeated probe changed parser features or AFL++ map")
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError("control probe differs from overlay receipt")
    changed = first[0] ^ other[0]
    if not changed or not first[1] ^ other[1]:
        raise RuntimeError("second control did not change parser feedback")
    # Only xmldoc and sax may contribute feedback, and xmldoc's own tree builder
    # must change between the controls, not just the sax tokenizer underneath.
    outside = {package_of(feature) for feature in first[0] | other[0]} - PACKAGES
    if outside:
        raise RuntimeError(f"feedback outside xmldoc/sax: {sorted(outside)}")
    if not any(feature.startswith(PARSER_FILE + ":") for feature in changed):
        raise RuntimeError("second control did not change xmldoc dist/index.js ranges")
    result = {
        "project": "xml/javascript/xmldoc", "pass": True,
        "feedback_kind": receipt["feedback_kind"],
        "namespace_resolution": False,
        "compared_fields": sorted(manifest["expected_output"]),
        "oracle": "projects/xml/javascript/xmldoc/oracle.py (expat, non-namespace mode, root-element scope)",
        "overlay_receipt_sha256": sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"], "overlay_image_id": receipt["image_id"],
        "release_tarball_sha256": manifest["source_sha256"],
        "underlying_tarball_sha256": manifest["underlying_source_sha256"],
        "control": manifest["control"], "control_sha256": manifest["control_sha256"],
        "control_output_matches_oracle": True,
        "differential": manifest["differential_control"],
        "differential_sha256": manifest["differential_control_sha256"],
        "differential_output_matches_oracle": True,
        "control_lines_covered_by_file": {name[len(MODULES):]: count for name, count in lines.items()},
        "repeated_control_identical": True, "repeated_differential_identical": True,
        "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
        "control_features_by_package": by_package(first[0]),
        "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
        "parser_feature_difference": len(changed), "afl_tuple_difference": len(first[1] ^ other[1]),
        "control_only_features_by_file": by_file(first[0] - other[0]),
        "differential_only_features_by_file": by_file(other[0] - first[0]),
        "differential_features_by_package": by_package(changed),
    }
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if sys.argv[1] == "--write":
        REPORT.write_text(output)
    elif REPORT.read_text() != output:
        raise SystemExit("xmldoc feedback receipt changed")
    print(f"verified xmldoc: {result['parser_feature_difference']} parser ranges, "
          f"{result['afl_tuple_difference']} AFL++ tuples differ")


if __name__ == "__main__":
    main()
