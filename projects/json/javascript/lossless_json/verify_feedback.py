"""Replay only two valid JSON controls through lossless-json's AFL++ bridge."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from oracle import summarize


PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parents[3]
MANIFEST = json.loads((PROJECT / "manifest.json").read_text())
BASE = json.loads((PROJECT / "verification.json").read_text())
OVERLAY = ROOT / "fuzzing/afl-native/json/javascript/lossless_json"
BRIDGE = json.loads((OVERLAY / "verification.json").read_text())
RECEIPT = ROOT / "data/javascript/json/lossless-json-feedback.json"
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
        raise ValueError("AFL feedback absent or outside lossless-json's parse.js")
    return features, edges


def main() -> None:
    if BRIDGE["base_image_id"] != BASE["image_id"]:
        raise ValueError("AFL overlay is not built from the verified control image")
    cases = [(ROOT / MANIFEST[key], MANIFEST[hash_key], expected)
             for key, hash_key, expected in
             (("control", "control_sha256", "expected_output"),
              ("differential_control", "differential_control_sha256",
               "differential_expected_output"))]
    with tempfile.TemporaryDirectory(prefix="parsarium-lossless-json-feedback-") as temporary:
        work = Path(temporary)
        results = []
        for index, (path, digest, output_key) in enumerate(cases):
            data = path.read_bytes()
            if sha256(data).hexdigest() != digest:
                raise ValueError(f"control hash changed: {path}")
            independent = summarize(data)
            if independent != MANIFEST[output_key]:
                raise ValueError(f"pinned result differs from Python JSON numeric-lexeme oracle: {path}")
            observed = json.loads(run([*sandbox(path, work), "--entrypoint", "node",
                                       BASE["image_id"], "/work/replay.js", "/input/case"]))
            if observed != independent:
                raise ValueError(f"lossless-json output differs from independent oracle: {path}")
            repeats = [probe(path, work, f"case{index}-repeat{repeat}")
                       for repeat in range(3)]
            if any(item != repeats[0] for item in repeats[1:]):
                raise ValueError(f"AFL features or tuples varied across repeats: {path}")
            results.append(repeats[0])
    first, second = results
    if len(first[0]) != BRIDGE["parser_source_features"] or len(first[1]) != BRIDGE["feedback_edges"]:
        raise ValueError("first control differs from AFL overlay receipt")
    feature_difference = first[0] ^ second[0]
    edge_difference = first[1] ^ second[1]
    if not feature_difference or not edge_difference:
        raise ValueError("the two valid controls did not change parser-source feedback")
    receipt = {
        "schema_version": 1, "pass": True,
        "feedback_kind": BRIDGE["feedback_kind"],
        "scope": "lossless-json 4.3.3 ESM parse.js V8 source ranges; valid controls only",
        "base_image_id": BASE["image_id"], "overlay_image_id": BRIDGE["image_id"],
        "overlay_receipt_sha256": sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
        "control_sha256": cases[0][1], "differential_sha256": cases[1][1],
        "repeats_per_control": 3,
        "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
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
