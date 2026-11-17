"""Check repeatable, differing source and AFL++ feedback for a C++ pilot.

The base project image replays both valid controls against their pinned
expected outputs and records covered parser source lines (LLVM lcov export).
Defaults to the JSON JsonCpp pilot; --format xml --slug xerces_c checks the
XML Xerces-C++ pilot, and --format yaml --slug yaml-cpp --repeats 3 the YAML
yaml-cpp pilot.
The AFL++ overlay image traces each control twice with afl-showmap. Covered
lines and AFL++ tuples must repeat exactly per control and differ between the
two controls. No malformed inputs are run.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


REPEATS = 2
LINES = r"""
set -eu
LLVM_PROFILE_FILE=/tmp/case.profraw /work/replay /input/case > /coverage/$1.observed.json
llvm-profdata merge -sparse /tmp/case.profraw -o /tmp/case.profdata
llvm-cov export -format=lcov /work/replay -instr-profile=/tmp/case.profdata > /tmp/case.lcov
awk -F'[:,]' '/^SF:/{f=$2} /^DA:/{if ($3 > 0 && index(f, "/work/source/") == 1) print f ":" $2}' /tmp/case.lcov > /coverage/$1.lines
"""


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(platform: str, mounts: list[str]) -> list[str]:
    return ["docker", "run", "--rm", "--platform", platform,
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", *mounts]


def typed_tree(text: str) -> object:
    """Order-preserving, kind-aware view: 1 and 1.0 or reordered keys differ."""
    def canon(value: object) -> object:
        if isinstance(value, tuple): return ("object", [(k, canon(v)) for k, v in value[1]])
        if isinstance(value, list): return ("array", [canon(v) for v in value])
        return (type(value).__name__, value)
    return canon(json.loads(text, object_pairs_hook=lambda pairs: ("object", pairs)))


def summarize_tree(tree: object) -> dict:
    counts = {"arrays": 0, "objects": 0, "booleans": 0, "nulls": 0,
              "max_depth": 0}
    numbers: list[int | float] = []
    strings: list[str] = []

    def walk(value: object, depth: int) -> None:
        if isinstance(value, dict):
            counts["objects"] += 1
            counts["max_depth"] = max(counts["max_depth"], depth)
            for child in value.values(): walk(child, depth + 1)
        elif isinstance(value, list):
            counts["arrays"] += 1
            counts["max_depth"] = max(counts["max_depth"], depth)
            for child in value: walk(child, depth + 1)
        elif value is None: counts["nulls"] += 1
        elif isinstance(value, bool): counts["booleans"] += 1
        elif isinstance(value, (int, float)): numbers.append(value)
        elif isinstance(value, str): strings.append(value)

    walk(tree, 1)
    result = {"arrays": counts["arrays"], "booleans": counts["booleans"],
              "max_depth": counts["max_depth"], "nulls": counts["nulls"],
              "numbers": sorted(numbers), "objects": counts["objects"],
              "root": "object" if isinstance(tree, dict) else "array",
              "strings": sorted(strings)}
    if isinstance(tree, dict): result["top_level_keys"] = sorted(tree)
    else: result["top_level_items"] = len(tree)
    return result


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--format", default="json")
    cli.add_argument("--slug", default="jsoncpp")
    cli.add_argument("--repeats", type=int, default=REPEATS,
                     help="identical replays required per control (default 2)")
    args = cli.parse_args()
    if args.repeats < 2:
        cli.error("--repeats must be at least 2")
    project, manifest = project_for(args.format, "cpp", args.slug)
    relative = Path(args.format) / "cpp" / args.slug
    overlay = ROOT / "fuzzing/afl-native" / relative
    base_receipt = json.loads((project / "verification.json").read_text())
    overlay_receipt = json.loads((overlay / "verification.json").read_text())
    if overlay_receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise ValueError("AFL++ overlay receipt does not match the project receipt")
    base_image = base_receipt["image_id"]
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    digests = [manifest["control_sha256"], manifest["differential_control_sha256"]]
    expected = [manifest["expected_output"], manifest["differential_expected_output"]]
    for path, digest in zip(controls, digests):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")
    platform = manifest["platform"]
    lines: list[set[str]] = []
    maps: list[set[str]] = []
    with tempfile.TemporaryDirectory(prefix=f"parsarium-cpp-{args.format}-") as temporary:
        work = Path(temporary)
        for index, control in enumerate(controls):
            run_lines, run_maps = [], []
            for attempt in range(args.repeats):
                name = f"{index}-{attempt}"
                common = sandbox(platform, ["-v", f"{control}:/input/case:ro", "-v", f"{work}:/coverage"])
                run([*common, "--entrypoint", "/bin/sh", base_image, "-c", LINES, "lines", name])
                observed = json.loads((work / f"{name}.observed.json").read_text())
                if args.slug == "boost-json" and (typed_tree((work / f"{name}.observed.json").read_text())
                                                  != typed_tree(control.read_text())):
                    raise RuntimeError(f"{control.name}: parsed DOM order or number kinds differ")
                if args.slug in {"simdjson", "boost-json"}:  # replay prints the full parsed DOM
                    if observed != json.loads(control.read_text()):
                        raise RuntimeError(f"{control.name}: parsed DOM differs from valid control")
                    observed = summarize_tree(observed)
                if observed != expected[index]:
                    raise RuntimeError(f"{control.name}: output mismatch {observed}")
                run_lines.append(set((work / f"{name}.lines").read_text().splitlines()) - {""})
                run([*common, "-e", f"AFL_MAP_SIZE={overlay_receipt['afl_map_size']}",
                     "--workdir", "/tmp", "--entrypoint", "afl-showmap", overlay_receipt["image_id"],
                     "-m", "none", "-t", "10000", "-o", f"/coverage/{name}.map", "--",
                     "/work/fuzzer", "/input/case"])
                run_maps.append({line.split(":", 1)[0] for line in
                                 (work / f"{name}.map").read_text().splitlines() if line})
            if any(item != run_lines[0] for item in run_lines):
                raise RuntimeError(f"{control.name}: covered lines differ between repeats")
            if any(item != run_maps[0] for item in run_maps):
                raise RuntimeError(f"{control.name}: AFL++ tuples differ between repeats")
            if not run_lines[0] or not run_maps[0]:
                raise RuntimeError(f"{control.name}: no source lines or AFL++ tuples")
            lines.append(run_lines[0])
            maps.append(run_maps[0])
    line_difference = len(lines[0] ^ lines[1])
    map_difference = len(maps[0] ^ maps[1])
    if not line_difference or not map_difference:
        raise RuntimeError("source lines or AFL++ map did not differ between valid controls")
    prefix = manifest["coverage_subject_prefix"]

    def by_file(items: set[str]) -> dict:
        return dict(sorted(Counter(item.rsplit(":", 1)[0].removeprefix(prefix) for item in items).items()))

    record = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(relative), "pass": True,
        "feedback_kind": "native_afl_clang_fast_edges_with_llvm_source_lines",
        "base_project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base_image,
        "overlay_image_id": overlay_receipt["image_id"],
        "afl_package": overlay_receipt["afl_package"],
        "repeats_per_control": args.repeats,
        "first_control": manifest["control"],
        "first_sha256": digests[0],
        "second_control": manifest["differential_control"],
        "second_sha256": digests[1],
        "second_control_output": expected[1],
        "first_source_lines": len(lines[0]),
        "second_source_lines": len(lines[1]),
        "source_line_difference": line_difference,
        "first_only_lines_by_file": by_file(lines[0] - lines[1]),
        "second_only_lines_by_file": by_file(lines[1] - lines[0]),
        "first_afl_tuples": len(maps[0]),
        "second_afl_tuples": len(maps[1]),
        "afl_tuple_difference": map_difference,
        "second_case_kind": "valid_control",
    }
    if args.slug == "boost-json":
        record["dom_oracle"] = "python_json_loads_order_and_number_kind_preserving"
    (overlay / "differential.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"{relative}: {line_difference} source lines, {map_difference} AFL++ tuples differ; "
          f"{args.repeats} repeats per control identical", flush=True)


if __name__ == "__main__":
    main()
