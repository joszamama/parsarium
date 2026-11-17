"""Repeat two valid JSON controls through the parser-only native AFL++ probe."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[4]
PROJECT = Path(__file__).resolve().parent
OVERLAY = ROOT / "fuzzing/afl-native/json/cpp/poco-json"
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
                ("/JSON/src/ParserImpl.cpp", "/dependencies/pdjson/src/pdjson.c")):
            number, hits, *_ = line[3:].split(",")
            if int(hits) > 0:
                lines.add(f"{source}:{number}")
    return lines


def typed_tree(text: str) -> object:
    def canon(value: object) -> object:
        if isinstance(value, tuple): return ("object", [(key, canon(child)) for key, child in value[1]])
        if isinstance(value, list): return ("array", [canon(child) for child in value])
        return (type(value).__name__, value)
    return canon(json.loads(text, object_pairs_hook=lambda pairs: ("object", pairs)))


def summarize_tree(value: object) -> dict:
    result = {"arrays": 0, "booleans": 0, "max_depth": 0,
              "nulls": 0, "numbers": [], "objects": 0, "strings": []}
    def walk(node: object, depth: int) -> None:
        if isinstance(node, dict):
            result["objects"] += 1
            result["max_depth"] = max(result["max_depth"], depth)
            for child in node.values(): walk(child, depth + 1)
        elif isinstance(node, list):
            result["arrays"] += 1
            result["max_depth"] = max(result["max_depth"], depth)
            for child in node: walk(child, depth + 1)
        elif node is None: result["nulls"] += 1
        elif isinstance(node, bool): result["booleans"] += 1
        elif isinstance(node, (int, float)): result["numbers"].append(node)
        elif isinstance(node, str): result["strings"].append(node)
    walk(value, 1)
    result["numbers"].sort(); result["strings"].sort()
    result["root"] = "object" if isinstance(value, dict) else "array"
    if isinstance(value, dict): result["top_level_keys"] = sorted(value)
    else: result["top_level_items"] = len(value)
    return result


def main() -> None:
    if AFL["base_project_receipt_sha256"] != sha256((PROJECT / "verification.json").read_bytes()).hexdigest():
        raise ValueError("AFL++ overlay was built from a different project receipt")
    controls = [(MANIFEST["control"], MANIFEST["control_sha256"]),
                (MANIFEST["differential_control"], MANIFEST["differential_control_sha256"])]
    expected = [MANIFEST["expected_output"], MANIFEST["differential_expected_output"]]
    results = []
    with tempfile.TemporaryDirectory(prefix="parsarium-poco-json-") as temp:
        output = Path(temp)
        for index, (name, digest) in enumerate(controls):
            control = ROOT / name
            if sha256(control.read_bytes()).hexdigest() != digest:
                raise ValueError(f"control changed: {name}")
            tree_text = run([*sandbox(control, output),
                             "-e", "LLVM_PROFILE_FILE=/tmp/replay.profraw",
                             "--entrypoint", "/work/replay", BASE["image_id"],
                             "/input/case"])
            if typed_tree(tree_text) != typed_tree(control.read_text()):
                raise RuntimeError(f"{name}: exact POCO JSON DOM output differs from control")
            if summarize_tree(json.loads(tree_text)) != expected[index]:
                raise RuntimeError(f"{name}: format-aware summary differs from manifest")
            attempts = []
            for repeat in range(2):
                key = f"{index}-{repeat}"
                base = sandbox(control, output)
                script = ("set -eu; LLVM_PROFILE_FILE=/tmp/case.profraw "
                          "/work/parser-probe /input/case; "
                          "llvm-profdata merge -sparse /tmp/case.profraw -o /tmp/case.profdata; "
                          "llvm-cov export -format=lcov /work/parser-probe -instr-profile=/tmp/case.profdata "
                          "/work/source/JSON/src/ParserImpl.cpp "
                          "/work/source/dependencies/pdjson/src/pdjson.c "
                          f"> /coverage/{key}.lcov")
                run([*base, "--entrypoint", "/bin/sh", BASE["image_id"], "-c", script])
                lines = covered_lines(output / f"{key}.lcov")
                if not lines:
                    raise RuntimeError("POCO JSON and pdjson parser sources have no covered lines")
                if not any("/JSON/src/ParserImpl.cpp:" in line for line in lines):
                    raise RuntimeError("POCO JSON ParserImpl.cpp has no covered lines")
                if not any("/dependencies/pdjson/src/pdjson.c:" in line for line in lines):
                    raise RuntimeError("bundled pdjson.c has no covered lines")
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
    # Count only parser lines present in both replays of one control and absent
    # from both replays of the other control as the reproducible line difference.
    line_difference = len((results[0][0] - results[1][1]) |
                          (results[1][0] - results[0][1]))
    pdjson_difference = len({line for line in results[0][0] - results[1][1]
                             if "/pdjson.c:" in line} |
                            {line for line in results[1][0] - results[0][1]
                             if "/pdjson.c:" in line})
    tuple_difference = len(results[0][2] ^ results[1][2])
    if not line_difference or not pdjson_difference or not tuple_difference:
        raise RuntimeError("valid controls did not produce distinct native parser feedback")
    record = {
        "schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": "json/cpp/poco-json", "pass": True,
        "feedback_kind": "native_afl_clang_fast_parser_only_edges_with_poco_pdjson_source_lines",
        "probe": "projects/json/cpp/poco-json/parser-probe.cpp",
        "probe_scope": "Poco::JSON::Parser::parse(std::string) only; no DOM serialization, traversal, output summarization, or adapter postprocessing",
        "base_project_receipt_sha256": sha256((PROJECT / "verification.json").read_bytes()).hexdigest(),
        "overlay_receipt_sha256": sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": BASE["image_id"], "overlay_image_id": AFL["image_id"],
        "afl_package": AFL["afl_package"], "afl_map_size": AFL["afl_map_size"],
        "repeats_per_control": 2,
        "first_control": controls[0][0], "first_sha256": controls[0][1],
        "second_control": controls[1][0], "second_sha256": controls[1][1],
        "exact_tree_outputs_verified": True,
        "first_tree_output": expected[0], "second_tree_output": expected[1],
        "first_parser_lines_stable": len(results[0][0]),
        "second_parser_lines_stable": len(results[1][0]),
        "parser_line_difference": line_difference,
        "pdjson_line_difference": pdjson_difference,
        "parser_line_repeat_variation": [results[0][3], results[1][3]],
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
