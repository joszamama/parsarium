#!/usr/bin/env python3
"""Verify two valid go-faster/jx controls and repeatable AFL++ feedback."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_go_json_feedback import CONTROL, DIFFERENTIAL, check, probe  # noqa: E402

SLUG = "github_com_go_faster_jx"
PROJECT = ROOT / "projects/json/go" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/json/go" / SLUG


def oracle(path: Path) -> dict:
    """Summarize a control with Python's json module, independent of the Go harness."""
    root = json.loads(path.read_bytes())
    counts = {"objects": 0, "arrays": 0, "booleans": 0, "nulls": 0}
    strings, numbers, depth = [], [], 0

    def walk(value, level):
        nonlocal depth
        if isinstance(value, dict):
            counts["objects"] += 1
            depth = max(depth, level + 1)
            for child in value.values():
                walk(child, level + 1)
        elif isinstance(value, list):
            counts["arrays"] += 1
            depth = max(depth, level + 1)
            for child in value:
                walk(child, level + 1)
        elif isinstance(value, bool):
            counts["booleans"] += 1
        elif value is None:
            counts["nulls"] += 1
        elif isinstance(value, str):
            strings.append(value)
        else:
            numbers.append(float(value))

    walk(root, 0)
    result = {**counts, "strings": sorted(strings), "numbers": sorted(numbers), "max_depth": depth}
    if isinstance(root, dict):
        result |= {"root": "object", "top_level_keys": sorted(root)}
    elif isinstance(root, list):
        result |= {"root": "array", "top_level_items": len(root)}
    else:
        result["root"] = "scalar"
    return result


def main() -> None:
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    harness = (PROJECT / "harness_test.go").read_text()
    constants = dict(re.findall(r"const (expected\w*JSON) = `([^`]*)`", harness))
    if json.loads(constants["expectedJSON"]) != oracle(ROOT / CONTROL):
        raise RuntimeError("object control constant disagrees with the Python oracle")
    if json.loads(constants["expectedDifferentialJSON"]) != oracle(ROOT / DIFFERENTIAL):
        raise RuntimeError("array control constant disagrees with the Python oracle")
    if manifest["expected_output"] != oracle(ROOT / CONTROL):
        raise RuntimeError("manifest expected_output disagrees with the Python oracle")
    subprocess.run(
        ["docker", "run", "--rm", "--platform", manifest["platform"],
         "--network", "none", "--read-only", "--cap-drop", "ALL",
         "--security-opt", "no-new-privileges",
         "--user", f"{os.getuid()}:{os.getgid()}",
         "--tmpfs", "/tmp:rw,nosuid,size=64m",
         "-v", f"{ROOT / DIFFERENTIAL}:/input/differential:ro",
         "--entrypoint", "/work/harness.test", f"parsarium/json-go-{SLUG}:local",
         "-test.run=^TestDifferential$", "-test.v"],
        check=True, capture_output=True, text=True, timeout=120,
    )
    result = check(SLUG)
    image = json.loads((OVERLAY / "verification.json").read_text())["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-jx-feedback-") as temporary:
        work = Path(temporary)
        first = probe(manifest, image, ROOT / DIFFERENTIAL, work, "second-first")
        repeated = probe(manifest, image, ROOT / DIFFERENTIAL, work, "second-repeated")
    if first != repeated:
        raise RuntimeError("second valid control changed parser features or AFL++ map")
    if len(first[0]) != result["differential_parser_features"] or len(first[1]) != result["differential_afl_tuples"]:
        raise RuntimeError("second valid control disagrees with differential receipt")
    result["repeated_differential_identical"] = True
    result["differential_control_pass"] = True
    result["independent_oracle"] = "Python json module summary of both controls equals harness constants"
    result["feedback_scope"] = "go-faster/jx Go package blocks (coverpkg github.com/go-faster/jx)"
    (OVERLAY / "differential.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
