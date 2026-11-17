"""Repeat two valid XML controls through the parser-only native AFL++ probe."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[4]
PROJECT = Path(__file__).resolve().parent
OVERLAY = ROOT / "fuzzing/afl-native/xml/cpp/xerces_c"
MANIFEST = json.loads((PROJECT / "manifest.json").read_text())
BASE = json.loads((PROJECT / "verification.json").read_text())
AFL = json.loads((OVERLAY / "verification.json").read_text())


def run(args: list[str]) -> str:
    process = subprocess.run(args, text=True, capture_output=True, timeout=120)
    if process.returncode:
        raise RuntimeError((process.stdout + process.stderr)[-3000:])
    return process.stdout


def sandbox(control: Path, output: Path) -> list[str]:
    return ["docker", "run", "--rm", "--platform", MANIFEST["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
            "-v", f"{control}:/input/case:ro", "-v", f"{output}:/coverage"]


def covered_lines(path: Path) -> set[str]:
    source = ""
    lines = set()
    for line in path.read_text().splitlines():
        if line.startswith("SF:"):
            source = line[3:]
        elif line.startswith("DA:") and source.endswith(
                ("/xercesc/internal/IGXMLScanner.cpp",
                 "/xercesc/internal/IGXMLScanner2.cpp",
                 "/xercesc/internal/XMLScanner.cpp")):
            number, hits, *_ = line[3:].split(",")
            if int(hits) > 0:
                lines.add(f"{source}:{number}")
    return lines


def main() -> None:
    if AFL["base_project_receipt_sha256"] != sha256((PROJECT / "verification.json").read_bytes()).hexdigest():
        raise ValueError("AFL++ overlay was built from a different project receipt")
    controls = [(MANIFEST["control"], MANIFEST["control_sha256"]),
                (MANIFEST["differential_control"], MANIFEST["differential_control_sha256"])]
    expected = [MANIFEST["expected_output"], MANIFEST["differential_expected_output"]]
    results = []
    with tempfile.TemporaryDirectory(prefix="parsarium-xerces-c-") as temp:
        output = Path(temp)
        for index, (name, digest) in enumerate(controls):
            control = ROOT / name
            if sha256(control.read_bytes()).hexdigest() != digest:
                raise ValueError(f"control changed: {name}")
            observed = json.loads(run([*sandbox(control, output),
                                       "-e", "LLVM_PROFILE_FILE=/tmp/replay.profraw",
                                       "--entrypoint", "/work/replay", BASE["image_id"],
                                       "/input/case"]))
            if observed != expected[index]:
                raise RuntimeError(f"{name}: exact DOM output differs from manifest")
            attempts = []
            for repeat in range(2):
                key = f"{index}-{repeat}"
                base = sandbox(control, output)
                script = ("set -eu; LLVM_PROFILE_FILE=/tmp/case.profraw "
                          "/work/parser-probe /input/case; "
                          "llvm-profdata merge -sparse /tmp/case.profraw -o /tmp/case.profdata; "
                          f"llvm-cov export -format=lcov /work/parser-probe -instr-profile=/tmp/case.profdata > /coverage/{key}.lcov")
                run([*base, "--entrypoint", "/bin/sh", BASE["image_id"], "-c", script])
                lines = covered_lines(output / f"{key}.lcov")
                if not lines:
                    raise RuntimeError("native Xerces-C++ scanner has no covered lines")
                run([*base, "-e", f"AFL_MAP_SIZE={AFL['afl_map_size']}",
                     "-e", "LLVM_PROFILE_FILE=/tmp/showmap.profraw", "--workdir", "/tmp",
                     "--entrypoint", "afl-showmap", AFL["image_id"],
                     "-m", "none", "-t", "10000", "-o", f"/coverage/{key}.map",
                     "--", "/work/parser-probe-afl", "/input/case"])
                tuples = {line.split(":", 1)[0] for line in
                          (output / f"{key}.map").read_text().splitlines() if line}
                if not tuples:
                    raise RuntimeError("parser-only AFL++ feedback is empty")
                attempts.append((lines, tuples))
            if attempts[0][1] != attempts[1][1]:
                raise RuntimeError(f"{name}: AFL tuples changed between identical runs")
            results.append((attempts[0][0] & attempts[1][0],
                            attempts[0][0] | attempts[1][0], attempts[0][1],
                            len(attempts[0][0] ^ attempts[1][0])))
    # Count only scanner lines present in both replays of one control and absent
    # from both replays of the other control as the reproducible line difference.
    line_difference = len((results[0][0] - results[1][1]) |
                          (results[1][0] - results[0][1]))
    tuple_difference = len(results[0][2] ^ results[1][2])
    if not line_difference or not tuple_difference:
        raise RuntimeError("valid controls did not produce distinct native parser feedback")
    record = {
        "schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": "xml/cpp/xerces_c", "pass": True,
        "feedback_kind": "native_afl_clang_fast_parser_only_edges_with_xerces_scanner_source_lines",
        "probe": "projects/xml/cpp/xerces_c/parser-probe.cpp",
        "probe_scope": "XercesDOMParser::parse(MemBufInputSource) and getDocumentElement only; no DOM traversal, output summarization, or adapter postprocessing",
        "base_project_receipt_sha256": sha256((PROJECT / "verification.json").read_bytes()).hexdigest(),
        "overlay_receipt_sha256": sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": BASE["image_id"], "overlay_image_id": AFL["image_id"],
        "afl_package": AFL["afl_package"], "afl_map_size": AFL["afl_map_size"],
        "repeats_per_control": 2,
        "first_control": controls[0][0], "first_sha256": controls[0][1],
        "second_control": controls[1][0], "second_sha256": controls[1][1],
        "exact_tree_outputs_verified": True,
        "first_tree_output": expected[0], "second_tree_output": expected[1],
        "first_scanner_lines_stable": len(results[0][0]),
        "second_scanner_lines_stable": len(results[1][0]),
        "scanner_line_difference": line_difference,
        "scanner_line_repeat_variation": [results[0][3], results[1][3]],
        "first_afl_tuples": len(results[0][2]),
        "second_afl_tuples": len(results[1][2]),
        "afl_tuple_difference": tuple_difference,
        "repeated_afl_feedback_identical": True,
        "second_case_kind": "valid_control",
    }
    (OVERLAY / "differential.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
