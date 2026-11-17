"""Build native minimp3 C AFL++ feedback under its Rust binding and verify both valid controls.

Only the vendored minimp3.h decoder functions named in the project allowlist are
compiled by afl-clang-fast; rustc output is never AFL-instrumented. The base
image replays both controls through its Rust-coverage and Clang-coverage builds,
then afl-showmap runs five times per control. No mutation campaign and no
malformed input is run.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from docker_slots import docker_build_slot  # noqa: E402

RELATIVE = Path("mp3/rust/minimp3")
PROJECT = ROOT / "projects" / RELATIVE
OVERLAY = ROOT / "fuzzing/afl-native" / RELATIVE
IMAGE = "parsarium-afl/mp3-rust-minimp3:local"
BASE = "parsarium/mp3-rust-minimp3:local"
C_SOURCE = ("/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/"
            "minimp3-sys-0.6.0/minimp3/minimp3.h")
REPEATS = 5
LINE_REPEATS = 3


def call(args: list[str], timeout: int = 1200) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-3000:])
    return result.stdout.strip()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def sandbox(platform: str) -> list[str]:
    return ["docker", "run", "--rm", "--platform", platform, "--network", "none",
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m"]


def showmap(image_id: str, control: Path, output: Path, platform: str,
            raw: bool = False) -> set[str]:
    call([*sandbox(platform), "-e", "AFL_MAP_SIZE=65536",
          "-v", f"{control}:/input/control:ro", "-v", f"{output.parent}:/coverage",
          "--entrypoint", "afl-showmap", image_id, *(["-r"] if raw else []),
          "-m", "none", "-t", "30000", "-o", f"/coverage/{output.name}",
          "--", "/work/afl-target", "/input/control"], 120)
    return set(output.read_text().splitlines()) - {""}


def source_lines(base_id: str, control: Path, output: Path, platform: str) -> tuple[dict, dict]:
    """Replay one control through both coverage builds; return its summary and line sets."""
    output.mkdir()
    call([*sandbox(platform), "-v", f"{control}:/input/control:ro",
          "-v", f"{output}:/coverage", base_id], 300)
    summary = json.loads((output / "summary.json").read_text())
    files = json.loads((output / "coverage.json").read_text())["data"][0]["files"]
    native, = [file for file in files if file["filename"] == C_SOURCE]
    binding = {file["filename"]: file["summary"]["lines"]["covered"]
               for file in files if file["filename"] != C_SOURCE}
    return summary, {"native": native["executed_lines"], "binding": binding}


def main() -> None:
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    if not manifest.get("afl_native_c_binding") or manifest["afl_entrypoint"] != "/work/afl-target":
        raise ValueError("native C binding AFL++ manifest is missing")
    base_receipt_path = PROJECT / "verification.json"
    base_receipt = json.loads(base_receipt_path.read_text())
    if (base_receipt.get("pass") is not True or
            (base_receipt.get("underlying_source_lines_covered") or 0) < 100):
        raise ValueError("native C source coverage is not verified")
    base_id = call(["docker", "image", "inspect", BASE, "--format", "{{.Id}}"])
    if base_id != base_receipt["image_id"]:
        raise ValueError("base image differs from verified control receipt")
    allowlist = PROJECT / "afl-allowlist.txt"
    names = [line.removeprefix("fun: ") for line in allowlist.read_text().splitlines()]
    if (len(names) != 47 or len(set(names)) != len(names) or
            not all(name and " " not in name for name in names) or
            "mp3dec_decode_frame" not in names):
        raise ValueError("pinned native parser function allowlist changed")
    platform = manifest["platform"]
    header = call(["docker", "run", "--rm", "--platform", platform, "--network", "none",
                   "--entrypoint", "cat", base_id, C_SOURCE])
    if sha256((header + "\n").encode()).hexdigest() != manifest["underlying_native_source_sha256"]:
        raise ValueError("vendored minimp3.h differs from the source lock")
    missing = [name for name in names
               if not re.search(rf"(?m)^[A-Za-z].*[ *]{name}\(", header)]
    if missing:
        raise ValueError(f"allowlisted functions absent from minimp3.h: {missing}")
    with docker_build_slot():
        call(["docker", "build", "--quiet", "--platform", platform,
              "-f", str(OVERLAY / "Dockerfile"), "-t", IMAGE, str(PROJECT)])
    image_id = call(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"])
    version = call(["docker", "run", "--rm", "--platform", platform,
                    "--entrypoint", "dpkg-query", image_id, "-W", "-f=${Version}", "afl++"])
    if version != "4.04c-4":
        raise ValueError(f"AFL++ version changed: {version}")
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    expected = [manifest["expected_output"], manifest["differential_expected_output"]]
    for control, want in zip(controls, [manifest["control_sha256"],
                                        manifest["differential_control_sha256"]]):
        if digest(control) != want:
            raise ValueError(f"control hash mismatch: {control}")
    with tempfile.TemporaryDirectory(prefix="parsarium-rust-minimp3-afl-") as temp:
        output = Path(temp)
        replays = [[source_lines(base_id, control, output / f"lines-{index}-{attempt}", platform)
                    for attempt in range(LINE_REPEATS)]
                   for index, control in enumerate(controls)]
        runs = [[showmap(image_id, control, output / f"{index}-{attempt}.map", platform)
                 for attempt in range(REPEATS)]
                for index, control in enumerate(controls)]
        raw_runs = [[showmap(image_id, control, output / f"raw-{index}-{attempt}.map", platform, True)
                     for attempt in range(REPEATS)]
                    for index, control in enumerate(controls)]
    for index, group in enumerate(replays):
        if any(summary["output"] != expected[index] for summary, _ in group):
            raise ValueError(f"control {index} decoded output differs: {group[0][0]['output']}")
        if any(lines != group[0][1] for _, lines in group[1:]):
            raise ValueError(f"control {index} source lines are unstable across replays")
    native = [set(group[0][1]["native"]) for group in replays]
    if len(native[0] ^ native[1]) < 2:
        raise ValueError("valid controls did not yield different native source lines")
    for index, group in enumerate(runs):
        if not group[0] or any(item != group[0] for item in group[1:]):
            raise ValueError(f"control {index} native AFL++ tuples are empty or unstable")
    edge_ids = [{line.split(":", 1)[0] for line in group[0]} for group in runs]
    raw_ids = []
    for index, group in enumerate(raw_runs):
        if any(item != group[0] for item in group[1:]):
            raise ValueError(f"control {index} raw native AFL++ maps are unstable")
        raw_ids.append({line.split(":", 1)[0] for line in group[0]})
        # afl-showmap 4.04c's bucketed output lists a subset of the raw nonzero tuples.
        if not edge_ids[index] <= raw_ids[index]:
            raise ValueError(f"control {index} bucketed tuples are not a subset of raw tuples")
    edge_difference = len(edge_ids[0] ^ edge_ids[1])
    if edge_difference < 2:
        raise ValueError("valid controls did not yield different native parser feedback")
    scope = ("AFL++ CLASSIC allowlist of 47 vendored minimp3.h C decoder functions compiled by "
             "afl-clang-fast; Rust binding, harness and std are built by rustc without AFL instrumentation")
    validation = {
        "schema_version": 1, "pass": True, "project": str(RELATIVE),
        "feedback_scope": scope,
        "first_control": manifest["control"], "first_sha256": manifest["control_sha256"],
        "first_control_output": manifest["expected_output"],
        "second_control": manifest["differential_control"],
        "second_sha256": manifest["differential_control_sha256"],
        "second_control_output": manifest["differential_expected_output"],
        "repeats_per_control": REPEATS,
        "first_native_tuples": len(edge_ids[0]), "second_native_tuples": len(edge_ids[1]),
        "native_tuple_difference": edge_difference,
        "repeat_maps_identical": True,
        "first_raw_nonzero_tuples": len(raw_ids[0]), "second_raw_nonzero_tuples": len(raw_ids[1]),
        "raw_tuple_difference": len(raw_ids[0] ^ raw_ids[1]),
        "raw_repeat_maps_identical": True,
        "showmap_note": ("Default afl-showmap 4.04c output (the Go minimp3 receipt method) lists a "
                         "subset of the nonzero tuples that -r lists; on the primary control the listed "
                         "tuples had raw hit counts 1, 2, 3, 4, 8 or 16. Both views are recorded."),
        "source_line_repeats_per_control": LINE_REPEATS,
        "source_lines_identical_across_repeats": True,
        "first_native_source_lines": len(native[0]),
        "second_native_source_lines": len(native[1]),
        "native_lines_only_first": len(native[0] - native[1]),
        "native_lines_only_second": len(native[1] - native[0]),
        "first_binding_source_lines": replays[0][0][1]["binding"],
        "second_binding_source_lines": replays[1][0][1]["binding"],
        "mutation_campaign_run": False,
        "allowlist_sha256": digest(allowlist),
    }
    validation_path = OVERLAY / "feedback-validation.json"
    validation_path.write_text(json.dumps(validation, indent=2) + "\n")
    receipt = {
        "schema_version": 1, "project": str(RELATIVE), "pass": True,
        "feedback_kind": "rust_ffi_minimp3_native_c_parser_edges",
        "feedback_scope": scope,
        "base_project_receipt_sha256": digest(base_receipt_path),
        "base_image_id": base_id, "image_id": image_id,
        "platform": platform, "control_sha256": manifest["control_sha256"],
        "source_sha256": manifest["source_sha256"],
        "underlying_native_source_sha256": manifest["underlying_native_source_sha256"],
        "parser_source_features": len(names),
        "feedback_edges": len(edge_ids[0]), "raw_nonzero_feedback_edges": len(raw_ids[0]),
        "afl_map_size": 65536,
        "afl_package": version,
        "afl_entrypoint": "/work/afl-target", "afl_file_input": True,
        "allowlist_sha256": digest(allowlist),
        "overlay_file_sha256": {
            name: digest(OVERLAY / name)
            for name in ("Dockerfile", "build.py", "feedback-validation.json")
        },
    }
    (OVERLAY / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {RELATIVE}: {len(edge_ids[0])} native C AFL++ tuples, "
          f"{edge_difference} differ on second valid control; {REPEATS} stable repeats each; "
          f"{len(native[0])}/{len(native[1])} native minimp3.h lines")


if __name__ == "__main__":
    main()
