"""Check SQL pilot paths: both valid controls match the oracle, and AFL++ feedback is stable and input-dependent.

For one sql/<ecosystem>/<slug> project this script:

1. checks that the manifest's expected outputs equal the hand-written oracle
   summaries in controls/sql/expected.json for both controls;
2. runs the verified base image's ``summary_command`` (from the manifest,
   ``/input/case`` is the mounted control) on both controls and compares the
   printed summary (last stdout line, JSON) with the oracle;
3. runs the AFL++ overlay image under ``afl-showmap`` three times per control
   (stdin for Rust targets, a file argument otherwise, or the manifest's
   ``afl_input_mode``), and, when the overlay has a source-line bridge
   (/work/afl_trace), records the parser source features of each run too.

Repeats must be identical per control, and the two controls must differ in
AFL++ tuples. The record is written to
fuzzing/afl-native/sql/<ecosystem>/<slug>/differential.json. No mutation
campaign is run and no malformed input is used.
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

from run_case import ROOT, image_for, project_for

REPEATS = 3
ORACLE = ROOT / "controls/sql/expected.json"


def run(command: list[str], stdin: bytes | None = None, timeout: int = 300) -> str:
    result = subprocess.run(command, input=stdin, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr).decode("utf-8", "replace")[-3000:])
    return result.stdout.decode("utf-8", "replace")


def sandbox(platform: str, mounts: list[str], interactive: bool = False) -> list[str]:
    return ["docker", "run", "--rm", *(["-i"] if interactive else []), "--platform", platform,
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", *mounts]


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("ecosystem")
    cli.add_argument("slug")
    args = cli.parse_args()
    project, manifest = project_for("sql", args.ecosystem, args.slug)
    relative = Path("sql") / args.ecosystem / args.slug
    oracle = json.loads(ORACLE.read_text())["controls"]
    controls = [manifest["control"], manifest["differential_control"]]
    expected = [manifest["expected_output"], manifest["differential_expected_output"]]
    for control, output in zip(controls, expected):
        if oracle[Path(control).name] != output:
            raise ValueError(f"manifest output for {control} differs from the oracle")
    digests = [manifest["control_sha256"], manifest["differential_control_sha256"]]
    for control, digest in zip(controls, digests):
        if sha256((ROOT / control).read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {control}")
    overlay = ROOT / "fuzzing/afl-native" / relative
    overlay_receipt = json.loads((overlay / "verification.json").read_text())
    base_receipt_sha = sha256((project / "verification.json").read_bytes()).hexdigest()
    if overlay_receipt.get("pass") is not True or overlay_receipt["base_project_receipt_sha256"] != base_receipt_sha:
        raise ValueError("overlay receipt does not match the base project receipt")
    _, base_image_id = image_for(project, manifest)
    if base_image_id != json.loads((project / "verification.json").read_text())["image_id"]:
        raise ValueError("base image differs from the project receipt")
    overlay_image = overlay_receipt["image_id"]
    platform = manifest["platform"]

    observed = []
    command = manifest["summary_command"]
    for control in controls:
        output = run([*sandbox(platform, ["-v", f"{ROOT / control}:/input/case:ro"]),
                      "--entrypoint", command[0], base_image_id, *command[1:]])
        lines = [line for line in output.splitlines() if line.strip()]
        observed.append(json.loads(lines[-1]))
    if observed != expected:
        raise RuntimeError(f"control summaries differ from the oracle: {observed}")

    inspect = json.loads(run(["docker", "image", "inspect", overlay_image]))[0]["Config"]
    target = (inspect.get("Entrypoint") or [])[:1]
    if not target:
        raise ValueError("overlay image has no entrypoint")
    mode = manifest.get("afl_input_mode", "stdin" if args.ecosystem == "rust" else "file")
    has_trace = (overlay / "afl_trace").is_file()
    map_size = str(overlay_receipt.get("afl_map_size", 65536))
    features: list[set[str]] = []
    maps: list[set[str]] = []
    with tempfile.TemporaryDirectory(prefix="parsarium-sql-diff-") as temporary:
        work = Path(temporary)
        os.chmod(work, 0o777)
        for index, control in enumerate(controls):
            run_features, run_maps = [], []
            for attempt in range(REPEATS):
                name = f"{index}-{attempt}"
                mounts = ["-v", f"{ROOT / control}:/input/case:ro", "-v", f"{work}:/coverage"]
                if has_trace:
                    run([*sandbox(platform, mounts), "--entrypoint", "/bin/sh", overlay_image,
                         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
                    run_features.append(set((work / f"{name}.features").read_text().splitlines()) - {""})
                showmap = [*sandbox(platform, mounts, interactive=mode == "stdin"),
                           "--workdir", "/tmp", "-e", f"AFL_MAP_SIZE={map_size}",
                           "--entrypoint", "afl-showmap", overlay_image, "-m", "none", "-t", "30000",
                           "-o", f"/coverage/{name}.map", "--", *target]
                if mode == "file":
                    run([*showmap, "/input/case"])
                else:
                    run(showmap, stdin=(ROOT / control).read_bytes())
                run_maps.append(set((work / f"{name}.map").read_text().splitlines()) - {""})
            if any(item != run_maps[0] for item in run_maps):
                raise RuntimeError(f"{control}: AFL++ maps differ between repeats")
            if has_trace and any(item != run_features[0] for item in run_features):
                raise RuntimeError(f"{control}: parser features differ between repeats")
            maps.append({line.split(":", 1)[0] for line in run_maps[0]})
            features.append(run_features[0] if has_trace else set())
    tuple_difference = len(maps[0] ^ maps[1])
    feature_difference = len(features[0] ^ features[1])
    if tuple_difference < 2 or (has_trace and not feature_difference):
        raise RuntimeError(f"{relative}: controls did not give different feedback")
    prefix = manifest.get("afl_coverage_subject_prefix", manifest.get("coverage_subject_prefix", ""))

    def by_file(items: set[str]) -> dict:
        return dict(sorted(Counter(item.rsplit(":", 1)[0].removeprefix(prefix) for item in items).items()))

    record = {
        "schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(relative), "pass": True,
        "feedback_kind": overlay_receipt.get("feedback_kind", "native_afl_edges"),
        "base_project_receipt_sha256": base_receipt_sha,
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base_image_id, "overlay_image_id": overlay_image,
        "afl_input_mode": mode, "repeats_per_control": REPEATS,
        "repeat_maps_identical": True,
        "repeat_features_identical": True if has_trace else None,
        "mutation_campaign_run": False,
        "oracle": "controls/sql/expected.json",
        "first_control": controls[0], "first_sha256": digests[0], "first_control_output": observed[0],
        "second_control": controls[1], "second_sha256": digests[1], "second_control_output": observed[1],
        "first_afl_tuples": len(maps[0]), "second_afl_tuples": len(maps[1]),
        "afl_tuple_difference": tuple_difference,
        "first_parser_features": len(features[0]) if has_trace else None,
        "second_parser_features": len(features[1]) if has_trace else None,
        "parser_feature_difference": feature_difference if has_trace else None,
        "first_only_features_by_file": by_file(features[0] - features[1]) if has_trace else None,
        "second_only_features_by_file": by_file(features[1] - features[0]) if has_trace else None,
    }
    (overlay / "differential.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print(f"{relative}: oracle match on both controls; {tuple_difference} AFL++ tuples"
          + (f", {feature_difference} parser features" if has_trace else "")
          + f" differ; {REPEATS} repeats per control identical", flush=True)


if __name__ == "__main__":
    main()
