"""Build and verify the bounded V8 JSON.parse function-entry AFL++ bridge.

Only the two documented valid JSON controls are executed. No campaign starts.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
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
IMAGE = "parsarium-afl/json-javascript-stdlib_json_parse:local"
BASE_IMAGE = "parsarium/json-javascript-stdlib_json_parse:local"
PROBE_IMAGE = "parsarium/json-javascript-stdlib_json_parse-native-feedback:local"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def call(command: list[str], timeout: int = 120) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{command[:6]}: exit {result.returncode}: "
                           f"{(result.stdout + result.stderr)[-1200:]}")
    return result.stdout


def docker_run(image: str, entrypoint: str, args: list[str],
               mounts: list[str] | None = None) -> str:
    command = ["docker", "run", "--rm", "--pull", "never", "--platform", "linux/arm64",
               "--network", "none", "--read-only", "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
               "--cap-drop", "ALL", "--cap-add", "SYS_PTRACE", "--security-opt",
               "seccomp=unconfined", "--security-opt", "no-new-privileges",
               "--user", f"{__import__('os').getuid()}:{__import__('os').getgid()}"]
    for mount in mounts or []:
        command += ["-v", mount]
    return call(command + ["--entrypoint", entrypoint, image, *args])


def probe(input_path: str, mounts: list[str]) -> tuple[int, list[str]]:
    lines = docker_run(IMAGE, "sh", ["/work/probe.sh", input_path], mounts).splitlines()
    if not lines or not lines[0].startswith("SYMBOLS "):
        raise RuntimeError("V8 symbol probe produced no symbol inventory")
    return int(lines[0].split()[1]), [line[4:] for line in lines[1:] if line.startswith("HIT ")]


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
    if manifest["source_sha256"] != docker_run(
            PROBE_IMAGE, "sha256sum", ["/usr/local/bin/node"]).split()[0]:
        raise RuntimeError("V8/Node binary changed")
    probe_image_id = call(["docker", "image", "inspect", PROBE_IMAGE,
                           "--format", "{{.Id}}"], 30).strip()
    probe_hashes = {}
    for name in ("probe.py", "probe.sh"):
        expected = digest(PROJECT / "native-feedback-probe" / name)
        observed = docker_run(PROBE_IMAGE, "sha256sum", ["/work/" + name]).split()[0]
        if observed != expected:
            raise RuntimeError(f"pinned V8 symbol probe changed: {name}")
        probe_hashes[name] = expected
    gdb_version = docker_run(PROBE_IMAGE, "gdb", ["--version"]).splitlines()[0]

    with docker_build_slot():
        call(["docker", "build", "--quiet", "-t", IMAGE, "-f", str(OVERLAY / "Dockerfile"),
              str(ROOT)], 900)
    image_id = call(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"], 30).strip()
    controls = str(ROOT / "controls/json") + ":/controls:ro"
    for name, expected in (("nested-object.json", manifest["expected_output"]),
                           ("nested-array.json", manifest["differential_expected_output"])):
        observed = json.loads(docker_run(IMAGE, "node", ["/work/adapter.mjs", "/controls/" + name],
                                         [controls]))
        if observed != expected:
            raise RuntimeError(f"valid {name} parse differs: {observed}")

    symbols, baseline = probe("--baseline", [controls])
    _, control = probe("/controls/nested-object.json", [controls])
    _, repeat = probe("/controls/nested-object.json", [controls])
    _, variant = probe("/controls/nested-array.json", [controls])
    if not (symbols == 142 and not baseline and control == repeat and control != variant):
        raise RuntimeError("native V8 parser function-entry probe is not stable and distinct")

    with tempfile.TemporaryDirectory(prefix="parsarium-node-json-afl-") as temporary:
        maps = Path(temporary)
        for name, input_path in (("baseline", "--baseline"),
                                 ("control1", "/controls/nested-object.json"),
                                 ("control2", "/controls/nested-object.json"),
                                 ("variant", "/controls/nested-array.json")):
            docker_run(IMAGE, "afl-showmap", ["-q", "-m", "none", "-t", "30000",
                                               "-o", "/maps/" + name, "--",
                                               "/work/afl_proxy", input_path],
                       [controls, str(maps) + ":/maps"])
        values = {name: (maps / name).read_bytes()
                  for name in ("baseline", "control1", "control2", "variant")}
    counts = {name: len(value.splitlines()) for name, value in values.items()}
    if not (values["control1"] == values["control2"]
            and values["control1"] != values["variant"]
            and counts["baseline"] < counts["control1"]
            and counts["baseline"] < counts["variant"]):
        raise RuntimeError(f"AFL bitmap is not stable, parser-sensitive, and above baseline: {counts}")

    # Six repeats of the same valid control estimate the substantial gdb cost.
    # They are run in one fresh container; no mutation or campaign takes place.
    timing_start = time.monotonic()
    docker_run(IMAGE, "sh", ["-c", "for i in 1 2 3 4 5 6; do "
                             "afl-showmap -q -m none -t 30000 -o /tmp/map-$i -- "
                             "/work/afl_proxy /controls/nested-object.json || exit; done"],
               [controls])
    six_case_seconds = round(time.monotonic() - timing_start, 3)

    record = {
        "schema_version": 1,
        "project": "json/javascript/stdlib_json_parse",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "pass": True,
        "coverage_kind": "native_function_entries",
        "feedback_kind": "v8_json_parser_function_entries_to_afl_bitmap",
        "source_lines_covered": None,
        "afl_package": "4.21c-5",
        "afl_map_size": 65536,
        "feedback_tuples": counts["control1"],
        "afl_requires_ptrace": True,
        "fixed_valid_control_timing": {
            "cases": 6, "wall_seconds": six_case_seconds,
            "seconds_per_case": round(six_case_seconds / 6, 3),
            "approx_cases_per_second": round(6 / six_case_seconds, 2),
            "measurement": "Six fixed valid afl-showmap replays in one fresh Docker container; not a fuzz campaign or a sustained throughput measurement.",
        },
        "native_feedback": {
            "scope": "v8::internal::JsonParser<...> text symbols in pinned /usr/local/bin/node",
            "scope_symbols": symbols,
            "baseline_functions": len(baseline),
            "control_functions": len(control),
            "repeat_identical": control == repeat,
            "variant_functions": len(variant),
            "variant_differs": control != variant,
            "control_only": sorted(set(control) - set(variant)),
            "variant_only": sorted(set(variant) - set(control)),
            "bitmap_tuples": counts,
            "bitmap_sha256": {name: sha256(value).hexdigest() for name, value in values.items()},
            "limit": "Function entries hashed into AFL bitmap with bridge instrumentation; no source lines or parser basic-block/edge coverage. Each AFL case launches gdb; SYS_PTRACE and seccomp=unconfined required.",
        },
        "source_sha256": manifest["source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "base_project_receipt_sha256": digest(base_receipt),
        "probe_image_id": probe_image_id,
        "probe_file_sha256": probe_hashes,
        "gdb_version": gdb_version,
        "image_id": image_id,
        "overlay_file_sha256": {name: digest(OVERLAY / name)
                                for name in ("Dockerfile", "afl_trace", "build.py", "README.md")},
        "bridge_file_sha256": {"afl_proxy.c": digest(ROOT / "fuzzing/afl-bridge/afl_proxy.c")},
    }
    (OVERLAY / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"pass": True, "image_id": image_id, "functions":
                      [len(baseline), len(control), len(variant)], "tuples": counts,
                      "repeat_identical": True, "variant_differs": True}))


if __name__ == "__main__":
    main()
