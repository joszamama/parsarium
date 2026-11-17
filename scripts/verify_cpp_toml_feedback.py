"""Check repeatable, differing parser source and AFL++ feedback for a C++ TOML pilot.

Adapted from scripts/verify_cpp_json_feedback.py and the jsoncons parser-probe
audit. The base project image replays both valid TOML controls and requires
the printed typed tree to equal the hand-written expected tree. Its
coverage-instrumented parser probe (parse call only, no tree walk) records
covered library lines (LLVM lcov export, restricted to the manifest's
coverage_subject_prefix). The AFL++ overlay image traces the same probe with
afl-showmap; the probe was compiled with the project's afl-allowlist.txt, so
only the library's parser functions carry AFL++ instrumentation. Each control
runs three times: lines and tuples must repeat exactly and differ between the
two controls. No malformed inputs and no campaign are run.
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


REPEATS = 3
REPORT = ROOT / "data/cpp/toml/afl-feedback.json"
LINES = r"""
set -eu
LLVM_PROFILE_FILE=/tmp/replay.profraw /work/replay /input/case > /coverage/$1.tree.json
LLVM_PROFILE_FILE=/tmp/case.profraw /work/parser-probe /input/case
llvm-profdata merge -sparse /tmp/case.profraw -o /tmp/case.profdata
llvm-cov export -format=lcov /work/parser-probe -instr-profile=/tmp/case.profdata > /tmp/case.lcov
awk -F'[:,]' -v prefix="$2" '/^SF:/{f=$2} /^DA:/{if ($3 > 0 && index(f, prefix) == 1) print f ":" $2}' /tmp/case.lcov > /coverage/$1.lines
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


def update_report(relative: Path, manifest: dict, overlay: Path, record: dict) -> None:
    """Refresh this path's row in data/cpp/toml/afl-feedback.json."""
    report = json.loads(REPORT.read_text()) if REPORT.is_file() else {"results": []}
    row = {
        "project": str(relative), "pass": True,
        "feedback_kind": record["feedback_kind"],
        "overlay_receipt_sha256": record["overlay_receipt_sha256"],
        "differential_receipt_sha256": sha256((overlay / "differential.json").read_bytes()).hexdigest(),
        "control": manifest["control"], "control_sha256": manifest["control_sha256"],
        "differential": manifest["differential_control"],
        "differential_sha256": manifest["differential_control_sha256"],
        "repeats_per_control": record["repeats_per_control"],
        "repeated_control_identical": True,
        "control_source_lines": record["first_source_lines"],
        "control_afl_tuples": record["first_afl_tuples"],
        "differential_source_lines": record["second_source_lines"],
        "differential_afl_tuples": record["second_afl_tuples"],
        "source_line_difference": record["source_line_difference"],
        "afl_tuple_difference": record["afl_tuple_difference"],
    }
    results = [item for item in report.get("results", []) if item["project"] != row["project"]]
    results.append(row)
    results.sort(key=lambda item: item["project"])
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": record["checked_at_utc"],
        "projects_total": len(results),
        "projects_passed": sum(item["pass"] is True for item in results),
        "differential_kind": "two fixed valid TOML controls (service-config, typed-scalars); parser-only probes with allowlisted AFL++ instrumentation and exact typed-tree checks",
        "command": "python3 scripts/verify_cpp_toml_feedback.py --slug <slug>",
        "results": results,
    }, indent=2) + "\n")


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--slug", required=True)
    args = cli.parse_args()
    project, manifest = project_for("toml", "cpp", args.slug)
    relative = Path("toml") / "cpp" / args.slug
    overlay = ROOT / "fuzzing/afl-native" / relative
    base_receipt = json.loads((project / "verification.json").read_text())
    overlay_receipt = json.loads((overlay / "verification.json").read_text())
    base_sha = sha256((project / "verification.json").read_bytes()).hexdigest()
    if overlay_receipt["base_project_receipt_sha256"] != base_sha:
        raise ValueError("AFL++ overlay receipt does not match the project receipt")
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    digests = [manifest["control_sha256"], manifest["differential_control_sha256"]]
    expected = [manifest["expected_output"], manifest["differential_expected_output"]]
    for path, digest in zip(controls, digests):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")
    platform = manifest["platform"]
    prefix = manifest["coverage_subject_prefix"]
    entrypoint = manifest["afl_entrypoint"]
    lines: list[set[str]] = []
    maps: list[set[str]] = []
    with tempfile.TemporaryDirectory(prefix=f"parsarium-cpp-toml-{args.slug}-") as temporary:
        work = Path(temporary)
        for index, control in enumerate(controls):
            run_lines, run_maps = [], []
            for attempt in range(REPEATS):
                name = f"{index}-{attempt}"
                common = sandbox(platform, ["-v", f"{control}:/input/case:ro", "-v", f"{work}:/coverage"])
                run([*common, "--entrypoint", "/bin/sh", base_receipt["image_id"], "-c", LINES,
                     "lines", name, prefix])
                observed = json.loads((work / f"{name}.tree.json").read_text(encoding="utf-8"))
                if observed != expected[index]:
                    raise RuntimeError(f"{control.name}: typed tree mismatch {observed}")
                run_lines.append(set((work / f"{name}.lines").read_text().splitlines()) - {""})
                run([*common, "-e", f"AFL_MAP_SIZE={overlay_receipt['afl_map_size']}",
                     "--workdir", "/tmp", "--entrypoint", "afl-showmap", overlay_receipt["image_id"],
                     "-m", "none", "-t", "10000", "-o", f"/coverage/{name}.map", "--",
                     entrypoint, "/input/case"])
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
    if line_difference < 2 or map_difference < 2:
        raise RuntimeError("source lines or AFL++ map did not differ between valid controls")

    def by_file(items: set[str]) -> dict:
        return dict(sorted(Counter(item.rsplit(":", 1)[0].removeprefix(prefix) for item in items).items()))

    allowlist = project / "afl-allowlist.txt"
    record = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(relative), "pass": True,
        "feedback_kind": "afl_clang_fast_allowlisted_parser_edges_with_llvm_source_lines",
        "probe": f"projects/{relative}/parser-probe.cpp",
        "probe_scope": "library parse call only; no tree walk, typed-tree printing, or harness code",
        "typed_tree_outputs_verified": True,
        "base_project_receipt_sha256": base_sha,
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base_receipt["image_id"],
        "overlay_image_id": overlay_receipt["image_id"],
        "afl_package": overlay_receipt["afl_package"],
        "afl_map_size": overlay_receipt["afl_map_size"],
        "allowlist": f"projects/{relative}/afl-allowlist.txt",
        "allowlist_sha256": sha256(allowlist.read_bytes()).hexdigest(),
        "allowlist_entries": [line for line in allowlist.read_text().splitlines() if line],
        "coverage_subject_prefix": prefix,
        "repeats_per_control": REPEATS,
        "repeated_feedback_identical": True,
        "first_control": manifest["control"],
        "first_sha256": digests[0],
        "second_control": manifest["differential_control"],
        "second_sha256": digests[1],
        "first_source_lines": len(lines[0]),
        "second_source_lines": len(lines[1]),
        "first_source_lines_by_file": by_file(lines[0]),
        "second_source_lines_by_file": by_file(lines[1]),
        "source_line_difference": line_difference,
        "first_only_lines_by_file": by_file(lines[0] - lines[1]),
        "second_only_lines_by_file": by_file(lines[1] - lines[0]),
        "first_afl_tuples": len(maps[0]),
        "second_afl_tuples": len(maps[1]),
        "afl_tuple_difference": map_difference,
        "first_only_afl_tuples": len(maps[0] - maps[1]),
        "second_only_afl_tuples": len(maps[1] - maps[0]),
        "second_case_kind": "valid_control",
    }
    (overlay / "differential.json").write_text(json.dumps(record, indent=2) + "\n")
    update_report(relative, manifest, overlay, record)
    print(f"{relative}: {line_difference} source lines, {map_difference} AFL++ tuples differ; "
          f"{REPEATS} repeats per control identical", flush=True)


if __name__ == "__main__":
    main()
