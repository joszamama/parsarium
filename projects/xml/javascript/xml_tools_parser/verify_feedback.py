"""Replay only the two valid XML controls through this target's AFL++ bridge."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from oracle import structure


PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parents[3]
RECEIPT = ROOT / "data/javascript/xml/xml-tools-parser-feedback.json"
MANIFEST = json.loads((PROJECT / "manifest.json").read_text())
BASE = json.loads((PROJECT / "verification.json").read_text())
OVERLAY = ROOT / "fuzzing/afl-native/xml/javascript/xml_tools_parser"
BRIDGE = json.loads((OVERLAY / "verification.json").read_text())
PREFIX = MANIFEST["afl_coverage_subject_prefix"]


def run(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, timeout=120, check=False)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1500:])
    return result.stdout


def sandbox(path: Path, work: Path) -> list[str]:
    return ["docker", "run", "--rm", "--platform", MANIFEST["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
            "-v", f"{path}:/input/case:ro", "-v", f"{work}:/coverage"]


def probe(path: Path, work: Path, label: str) -> tuple[set[str], set[str]]:
    image = BRIDGE["image_id"]
    run([*sandbox(path, work), "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{label}.features"])
    run([*sandbox(path, work), "-e", "AFL_MAP_SIZE=65536",
         "--entrypoint", "afl-showmap", image, "-m", "none", "-t", "30000",
         "-o", f"/coverage/{label}.map", "--", "/work/afl_proxy", "/input/case"])
    features = set((work / f"{label}.features").read_text().splitlines()) - {""}
    edges = {line.split(":", 1)[0] for line in
             (work / f"{label}.map").read_text().splitlines() if line}
    if not features or not edges or any(not item.startswith(PREFIX) for item in features):
        raise ValueError("AFL feedback was absent or outside the XML parser source")
    return features, edges


def read_only_features(path: Path, work: Path) -> set[str]:
    work.mkdir()
    # Import the same harness, read and decode the same local bytes, then stop
    # before calling the package's parse(text). This exposes constructor-time
    # Chevrotain grammar self-analysis without conflating it with input parsing.
    script = ("const fs=require('node:fs');"
              "const {TextDecoder}=require('node:util');"
              "require('/work/harness.js');"
              "new TextDecoder('utf-8',{fatal:true}).decode(fs.readFileSync('/input/case'));")
    run([*sandbox(path, work), "-e", "NODE_V8_COVERAGE=/coverage",
         "--entrypoint", "node", BASE["image_id"], "-e", script])
    features = set()
    for path in work.glob("coverage-*.json"):
        raw = json.loads(path.read_text())
        for script in raw["result"]:
            if script["url"] != "file:///work/node_modules/@xml-tools/parser/lib/parser.js":
                continue
            for function in script["functions"]:
                if function["functionName"] != "ALT":
                    continue
                for entry in function["ranges"]:
                    if entry["count"] > 0:
                        features.add(f"/work/node_modules/@xml-tools/parser/lib/parser.js:ALT:"
                                     f"{entry['startOffset']}-{entry['endOffset']}:"
                                     f"hits={min(entry['count'], 255)}")
    return features


def counts(features: set[str]) -> dict[str, int]:
    return {key: int(value) for feature in features
            for key, value in [feature.rsplit(":hits=", 1)]}


def main() -> None:
    if BRIDGE["base_image_id"] != BASE["image_id"]:
        raise ValueError("AFL overlay is not built from the verified control image")
    cases = [(ROOT / MANIFEST[key], MANIFEST[hash_key], expected)
             for key, hash_key, expected in
             (("control", "control_sha256", "expected_output"),
              ("differential_control", "differential_control_sha256",
               "differential_expected_output"))]
    with tempfile.TemporaryDirectory(prefix="parsarium-xml-tools-feedback-") as temporary:
        work = Path(temporary)
        baselines = [read_only_features(ROOT / MANIFEST[key], work / f"baseline{index}")
                     for index, key in enumerate(("control", "differential_control"))]
        if baselines[0] != baselines[1]:
            raise ValueError("read-only package grammar counts changed with control bytes")
        results = []
        for index, (path, digest, expected_key) in enumerate(cases):
            if sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError(f"control hash changed: {path}")
            observed = json.loads(run([*sandbox(path, work), "--entrypoint", "node",
                                       BASE["image_id"], "/work/replay.js", "/input/case"]))
            if observed != MANIFEST[expected_key]:
                raise ValueError(f"CST projection differs: {path}")
            if observed["lex_errors"] or observed["parse_errors"]:
                raise ValueError(f"valid control had XML grammar errors: {path}")

            def raw_names(node: dict) -> dict:
                return {"qname": node["qname"],
                        "attributes": [item["qname"] for item in node["attributes"]],
                        "children": [raw_names(child) for child in node["children"]]}

            if {"tree": raw_names(observed["tree"]),
                "max_depth": observed["max_depth"]} != structure(path.read_bytes()):
                raise ValueError(f"raw QName CST differs from independent Expat oracle: {path}")
            repeats = [probe(path, work, f"case{index}-repeat{repeat}")
                       for repeat in range(3)]
            if any(item != repeats[0] for item in repeats[1:]):
                raise ValueError(f"AFL features or tuples varied across repeats: {path}")
            results.append(repeats[0])
    first, second = results
    baseline_counts = counts(baselines[0])
    first_counts, second_counts = counts(first[0]), counts(second[0])
    if set(baseline_counts) != set(first_counts) or set(baseline_counts) != set(second_counts):
        raise ValueError("parse runs did not execute the expected grammar callback ranges")
    changed_ranges = {key for key in baseline_counts
                      if first_counts[key] != second_counts[key]}
    if not changed_ranges or any(first_counts[key] < baseline_counts[key] or
                                 second_counts[key] < baseline_counts[key]
                                 for key in baseline_counts):
        raise ValueError("grammar hit-count difference is not attributable to parsing")
    feature_difference = first[0] ^ second[0]
    edge_difference = first[1] ^ second[1]
    if not feature_difference or not edge_difference:
        raise ValueError("both valid controls produced the same package-source feedback")
    if len(first[0]) != BRIDGE["parser_source_features"] or len(first[1]) != BRIDGE["feedback_edges"]:
        raise ValueError("first control differs from AFL overlay receipt")
    receipt = {
        "schema_version": 1,
        "pass": True,
        "scope": "@xml-tools/parser XML grammar and lexer source ranges; valid controls only",
        "base_image_id": BASE["image_id"],
        "overlay_image_id": BRIDGE["image_id"],
        "overlay_receipt_sha256": sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
        "control_sha256": cases[0][1],
        "differential_sha256": cases[1][1],
        "repeats_per_control": 3,
        "read_only_baseline_identical_for_both_controls": True,
        "read_only_baseline_grammar_features": len(baselines[0]),
        "read_only_baseline_features": sorted(baselines[0]),
        "input_dependent_hit_count_ranges": len(changed_ranges),
        "control_parser_features": len(first[0]),
        "control_afl_tuples": len(first[1]),
        "differential_parser_features": len(second[0]),
        "differential_afl_tuples": len(second[1]),
        "parser_feature_difference": len(feature_difference),
        "afl_tuple_difference": len(edge_difference),
        "control_only_features": sorted(first[0] - second[0]),
        "differential_only_features": sorted(second[0] - first[0]),
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({key: receipt[key] for key in
                      ("control_parser_features", "differential_parser_features",
                       "parser_feature_difference", "control_afl_tuples",
                       "differential_afl_tuples", "afl_tuple_difference")}))


if __name__ == "__main__":
    main()
