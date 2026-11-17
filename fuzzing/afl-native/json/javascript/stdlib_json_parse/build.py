"""Build and verify the parser-only AFL++ target for Node.js JSON.parse.

Node.js 26.10.0 is built from the official source tarball with only V8's
deps/v8/src/json/json-parser.cc compiled with SanitizerCoverage trace-pc-guard
and the node executable linked against AFL++'s compiler runtime. Every map
entry therefore comes from that one parser object. The target runs the same
adapter as the project (bytes -> strict UTF-8 TextDecoder -> JSON.parse) on one
local file. Only the two valid JSON controls and two no-parser baselines are
executed; no campaign starts. AFL++ map entries are coverage points, not lines.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from docker_slots import docker_build_slot  # noqa: E402

PROJECT = ROOT / "projects/json/javascript/stdlib_json_parse"
OVERLAY = Path(__file__).resolve().parent
RELATIVE = "json/javascript/stdlib_json_parse"
IMAGE = "parsarium-afl/json-javascript-stdlib_json_parse:local"
BASE_IMAGE = "parsarium/json-javascript-stdlib_json_parse:local"
NODE = "/opt/node/bin/node"
ADAPTER = "/work/adapter.mjs"
MAP_SIZE = 65536
AFL_PACKAGE = "4.33c-1.1ubuntu1"
OVERLAY_FILES = ("Dockerfile", "afl-cc.sh", "build.py", "README.md")
CLI_FILES = ("parsarium.py", "scripts/prepare_afl_run.py", "scripts/run_prepared_afl.py")
DECODE_ONLY = ("import { readFile } from 'node:fs/promises';"
               "new TextDecoder('utf-8', { fatal: true }).decode(await readFile('/controls/nested-object.json'));")
REPEATS = 3


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def call(command: list[str], timeout: int = 120) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
    if result.returncode:
        raise RuntimeError(f"{command[:6]}: exit {result.returncode}: "
                           f"{(result.stdout + result.stderr)[-1200:]}")
    return result.stdout


def docker_run(entrypoint: str, args: list[str], mounts: list[str] | None = None) -> str:
    command = ["docker", "run", "--rm", "--pull", "never", "--platform", "linux/arm64",
               "--network", "none", "--read-only", "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
               "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
               "--user", f"{os.getuid()}:{os.getgid()}", "-e", f"AFL_MAP_SIZE={MAP_SIZE}"]
    for mount in mounts or []:
        command += ["-v", mount]
    return call(command + ["--entrypoint", entrypoint, IMAGE, *args])


def read_map(path: Path) -> dict[int, int]:
    entries = {}
    for line in path.read_text().splitlines():
        index, count = line.split(":")
        entries[int(index)] = int(count)
    return entries


def map_sha256(entries: dict[int, int]) -> str:
    return sha256("".join(f"{index:06d}:{count}\n" for index, count in sorted(entries.items()))
                  .encode()).hexdigest()


def main() -> None:
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    base_receipt = PROJECT / "verification.json"
    base = json.loads(base_receipt.read_text())
    if not base.get("pass") or base["image_id"] != call(
            ["docker", "image", "inspect", BASE_IMAGE, "--format", "{{.Id}}"], 30).strip():
        raise RuntimeError("base image differs from verified Node JSON.parse project")
    for key in ("control", "differential_control"):
        if digest(ROOT / manifest[key]) != manifest[key + "_sha256"]:
            raise RuntimeError(f"{key} changed")
    if digest(PROJECT / "adapter.mjs") != manifest["adapter_sha256"]:
        raise RuntimeError("adapter changed")
    expected_afl = manifest["afl_feedback"]

    with docker_build_slot():
        call(["docker", "build", "--quiet", "--platform", "linux/arm64", "-t", IMAGE,
              "-f", str(OVERLAY / "Dockerfile"), str(ROOT)], 7200)
    image_id = call(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"], 30).strip()

    def lines(name: str) -> list[str]:
        return docker_run("cat", ["/work/" + name]).splitlines()

    objects = lines("instrumented-objects.txt")
    runtime_symbols = lines("afl-runtime-symbols.txt")
    object_guard_bytes = sum(int(value) for value in lines("object-guard-bytes.txt"))
    node_guard_bytes, = (int(value) for value in lines("node-guard-bytes.txt"))
    toolchain = lines("toolchain.txt")
    source_hashes = {Path(line.split()[1]).name: line.split()[0] for line in lines("source-hashes.txt")}
    node_sha256 = docker_run("sha256sum", [NODE]).split()[0]
    adapter_sha256 = docker_run("sha256sum", [ADAPTER]).split()[0]
    guards = node_guard_bytes // 4
    if not (len(objects) == 1 and objects[0].endswith("/deps/v8/src/json/json-parser.o")
            and runtime_symbols == ["__afl_area_ptr", "__sanitizer_cov_trace_pc_guard",
                                    "__sanitizer_cov_trace_pc_guard_init"]
            and 0 < node_guard_bytes <= object_guard_bytes and node_guard_bytes % 4 == 0
            and guards < MAP_SIZE
            and source_hashes["node"] == node_sha256 == expected_afl["instrumented_node_sha256"]
            and adapter_sha256 == manifest["adapter_sha256"]
            and f"v8 {manifest['v8']}" in toolchain and "v26.10.0" in toolchain
            and f"afl++ {AFL_PACKAGE}" in toolchain
            and source_hashes["json-parser.cc"] == manifest["source_feedback"]["source_sha256"]["json-parser.cc"]
            and source_hashes["json-parser.h"] == manifest["source_feedback"]["source_sha256"]["json-parser.h"]):
        raise RuntimeError(f"AFL++ instrumentation gate failed: {objects} {runtime_symbols} "
                           f"{object_guard_bytes} {node_guard_bytes} {source_hashes} {toolchain}")

    controls = str(ROOT / "controls/json") + ":/controls:ro"
    outputs = {}
    for name, expected in (("nested-object.json", manifest["expected_output"]),
                           ("nested-array.json", manifest["differential_expected_output"])):
        observed = json.loads(docker_run(NODE, [ADAPTER, "/controls/" + name], [controls]))
        if observed != expected:
            raise RuntimeError(f"valid {name} parse differs: {observed}")
        outputs[name] = observed

    runs = [("baseline", ["-e", "0"]),
            ("decode-only", ["--input-type=module", "-e", DECODE_ONLY])]
    runs += [(f"object-{index}", [ADAPTER, "/controls/nested-object.json"])
             for index in range(1, REPEATS + 1)]
    runs += [(f"array-{index}", [ADAPTER, "/controls/nested-array.json"])
             for index in range(1, REPEATS + 1)]
    maps: dict[str, dict[int, int]] = {}
    raw: dict[str, dict[int, int]] = {}
    with tempfile.TemporaryDirectory(prefix="parsarium-node-json-afl-") as temporary:
        work = Path(temporary)
        os.chmod(work, 0o777)
        for name, args in runs:
            for mode, flags in (("map", []), ("raw", ["-r"])):
                docker_run("afl-showmap", ["-q", *flags, "-m", "none", "-t", "30000",
                                           "-o", f"/maps/{name}.{mode}", "--", NODE, *args],
                           [controls, f"{work}:/maps"])
                (maps if mode == "map" else raw)[name] = read_map(work / f"{name}.{mode}")

    objects_runs = [f"object-{index}" for index in range(1, REPEATS + 1)]
    array_runs = [f"array-{index}" for index in range(1, REPEATS + 1)]
    object_ids, array_ids = set(maps["object-1"]), set(maps["array-1"])
    max_index = max([index for entries in maps.values() for index in entries], default=0)
    checks = {
        "baseline_empty": not maps["baseline"] and not raw["baseline"],
        "decode_only_empty": not maps["decode-only"] and not raw["decode-only"],
        "object_repeat_identical_maps": all(maps[name] == maps["object-1"] for name in objects_runs),
        "array_repeat_identical_maps": all(maps[name] == maps["array-1"] for name in array_runs),
        "object_repeat_identical_raw_counts": all(raw[name] == raw["object-1"] for name in objects_runs),
        "array_repeat_identical_raw_counts": all(raw[name] == raw["array-1"] for name in array_runs),
        "object_array_maps_differ": maps["object-1"] != maps["array-1"],
        "indices_within_parser_guards": max_index <= guards + 8,
    }
    differential = len(object_ids ^ array_ids)
    if not (all(checks.values()) and differential > 0 and object_ids and array_ids):
        raise RuntimeError(f"AFL++ parser map is not empty at baseline, stable, and input-dependent: "
                           f"{checks} differential={differential} "
                           f"tuples={ {name: len(entries) for name, entries in maps.items()} }")

    # Six fixed valid replays of the object control estimate per-case cost; no mutation.
    timing_start = time.monotonic()
    docker_run("sh", ["-c", "for i in 1 2 3 4 5 6; do afl-showmap -q -m none -t 30000 "
                            f"-o /tmp/map-$i -- {NODE} {ADAPTER} /controls/nested-object.json || exit; done"],
               [controls])
    six_case_seconds = round(time.monotonic() - timing_start, 3)

    record = {
        "schema_version": 1,
        "project": RELATIVE,
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "pass": True,
        "coverage_kind": "native_parser_afl_edges",
        "feedback_kind": expected_afl["kind"],
        "source_lines_covered": None,
        "afl_package": AFL_PACKAGE,
        "afl_map_size": MAP_SIZE,
        "afl_requires_ptrace": False,
        "afl_target": [NODE, ADAPTER, "@@"],
        "feedback_edges": len(maps["object-1"]),
        "variant_feedback_edges": len(maps["array-1"]),
        "instrumentation": {
            "runtime": expected_afl["runtime"],
            "compiler_flag": "-fsanitize-coverage=trace-pc-guard (json-parser.cc only)",
            "afl_runtime": "/usr/lib/afl/afl-compiler-rt.o linked into executables",
            "afl_runtime_sha256": source_hashes["afl-compiler-rt.o"],
            "instrumented_objects": objects,
            "afl_runtime_symbols": runtime_symbols,
            "object_guard_bytes": object_guard_bytes,
            "node_guard_bytes": node_guard_bytes,
            "node_guards": guards,
            "node_sha256": node_sha256,
            "source_sha256": {"json-parser.cc": source_hashes["json-parser.cc"],
                              "json-parser.h": source_hashes["json-parser.h"]},
            "toolchain": toolchain,
        },
        "maps": {
            "tuples": {name: len(entries) for name, entries in maps.items()},
            "sha256": {name: map_sha256(entries) for name, entries in maps.items()},
            "raw_hit_sum": {name: sum(entries.values()) for name, entries in raw.items()},
            "raw_sha256": {name: map_sha256(entries) for name, entries in raw.items()},
            "object_only_tuples": len(object_ids - array_ids),
            "array_only_tuples": len(array_ids - object_ids),
            "shared_tuples": len(object_ids & array_ids),
            "max_tuple_index": max_index,
            **checks,
        },
        "outputs": outputs,
        "fixed_valid_control_timing": {
            "cases": 6, "wall_seconds": six_case_seconds,
            "seconds_per_case": round(six_case_seconds / 6, 3),
            "measurement": "Six fixed valid afl-showmap replays in one fresh Docker container; "
                           "not a fuzz campaign or a sustained throughput measurement.",
        },
        "limit": manifest["afl_feedback_limit"],
        "source_sha256": manifest["source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "differential_control_sha256": manifest["differential_control_sha256"],
        "adapter_sha256": manifest["adapter_sha256"],
        "base_project_receipt_sha256": digest(base_receipt),
        "image_id": image_id,
        "overlay_file_sha256": {name: digest(OVERLAY / name) for name in OVERLAY_FILES},
    }
    receipt_path = OVERLAY / "verification.json"
    receipt_path.write_text(json.dumps(record, indent=2) + "\n")

    # CLI preflight: prepare a plan from the control seed and validate it without starting AFL++.
    with tempfile.TemporaryDirectory(prefix="parsarium-node-json-plan-") as temporary:
        run_dir = Path(temporary) / "run"
        prepare = [sys.executable, "parsarium.py", "afl", "prepare", *RELATIVE.split("/"), str(run_dir),
                   "--seed", manifest["differential_control"]]
        prepared = call(prepare, 120)
        checked = call([sys.executable, "parsarium.py", "afl", "run", str(run_dir), "--check"], 120)
        plan = json.loads((run_dir / "plan.json").read_text())
    command = plan["command"]
    target = command[command.index("--") + 1:]
    if not (checked.startswith(f"Ready: {RELATIVE} (2 seeds, {expected_afl['kind']})")
            and target == record["afl_target"] and plan["image_id"] == image_id
            and "SYS_PTRACE" not in command and plan["unique_seeds"] == 2
            and plan["overlay_receipt_sha256"] == digest(receipt_path)):
        raise RuntimeError(f"AFL++ plan preflight failed: {checked} {target}")
    smoke = {
        "schema_version": 1,
        "project": RELATIVE,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "ready",
        "prepare_command": ["python3", "parsarium.py", "afl", "prepare", *RELATIVE.split("/"),
                            "RUN_DIR", "--seed", manifest["differential_control"]],
        "prepare_output_first_line": prepared.splitlines()[0].replace(str(run_dir.resolve()), "RUN_DIR"),
        "check_command": ["python3", "parsarium.py", "afl", "run", "RUN_DIR", "--check"],
        "check_output": checked.strip(),
        "afl_target": target,
        "unique_seeds": plan["unique_seeds"],
        "feedback_kind": plan["feedback_kind"],
        "image_id": plan["image_id"],
        "campaign_started": False,
        "overlay_receipt_sha256": digest(receipt_path),
        "cli_file_sha256": {name: digest(ROOT / name) for name in CLI_FILES},
    }
    (OVERLAY / "plan-smoke.json").write_text(json.dumps(smoke, indent=2) + "\n")
    print(json.dumps({"pass": True, "image_id": image_id, "guards": guards,
                      "tuples": record["maps"]["tuples"],
                      "object_only": record["maps"]["object_only_tuples"],
                      "array_only": record["maps"]["array_only_tuples"],
                      "check": checked.strip()}))


if __name__ == "__main__":
    main()
