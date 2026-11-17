"""Check that two valid pilot controls parse and reach AFL++ as different, repeatable feedback.

The base project image replays the second control against its pinned expected
output. The AFL++ bridge then traces each control twice; parser features and
AFL++ tuples must repeat exactly per control and differ between controls.
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


REPEATS = 2


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(platform: str, mounts: list[str]) -> list[str]:
    return ["docker", "run", "--rm", "--platform", platform,
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", *mounts]


def source_file(feature: str) -> str:
    return feature.rsplit(":", 1)[0]


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("ecosystem")
    cli.add_argument("slug")
    args = cli.parse_args()
    project, manifest = project_for(args.format, args.ecosystem, args.slug)
    if not manifest.get("pilot") or "differential_control" not in manifest:
        raise ValueError("pilot manifest with differential_control required")
    relative = Path(args.format) / args.ecosystem / args.slug
    overlay = ROOT / "fuzzing/afl-native" / relative
    overlay_receipt = json.loads((overlay / "verification.json").read_text())
    base_receipt = json.loads((project / "verification.json").read_text())
    _, base_image_id = image_for(project, manifest)
    if base_image_id != base_receipt["image_id"] or base_image_id != overlay_receipt["base_image_id"]:
        raise ValueError("base image differs from project or overlay receipt")
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    digests = [manifest["control_sha256"], manifest["differential_control_sha256"]]
    for path, digest in zip(controls, digests):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")
    platform = manifest["platform"]

    replay = run([*sandbox(platform, ["-v", f"{controls[1]}:/input/differential:ro"]),
                  "--entrypoint", "/work/harness.test", base_image_id,
                  "-test.run=^TestDifferentialControl$", "-test.v"])
    observed = [json.loads(line.removeprefix("OBSERVED_JSON:"))
                for line in replay.splitlines() if line.startswith("OBSERVED_JSON:")]
    if observed != [manifest["differential_expected_output"]]:
        raise RuntimeError(f"differential control output mismatch: {observed}")

    features: list[set[str]] = []
    maps: list[set[str]] = []
    with tempfile.TemporaryDirectory(prefix="parsarium-pilot-diff-") as temporary:
        work = Path(temporary)
        for index, control in enumerate(controls):
            runs_features = []
            runs_maps = []
            for attempt in range(REPEATS):
                name = f"{index}-{attempt}"
                common = sandbox(platform, ["-v", f"{control}:/input/case:ro",
                                            "-v", f"{work}:/coverage"])
                run([*common, "--entrypoint", "/bin/sh", overlay_receipt["image_id"],
                     "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
                runs_features.append(set((work / f"{name}.features").read_text().splitlines()) - {""})
                run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
                     overlay_receipt["image_id"], "-m", "none", "-t", "30000",
                     "-o", f"/coverage/{name}.map", "--", "/work/afl_proxy", "/input/case"])
                runs_maps.append(set((work / f"{name}.map").read_text().splitlines()) - {""})
            if any(item != runs_features[0] for item in runs_features):
                raise RuntimeError(f"{control.name}: parser features differ between repeats")
            if any(item != runs_maps[0] for item in runs_maps):
                raise RuntimeError(f"{control.name}: AFL++ tuples differ between repeats")
            features.append(runs_features[0])
            maps.append({line.split(":", 1)[0] for line in runs_maps[0]})
    feature_difference = len(features[0] ^ features[1])
    map_difference = len(maps[0] ^ maps[1])
    if not feature_difference or not map_difference:
        raise RuntimeError(f"{relative}: parser source or AFL++ map did not differ")
    prefix = manifest["coverage_subject_prefix"]
    record = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(relative), "pass": True,
        "feedback_kind": overlay_receipt["feedback_kind"],
        "base_project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base_image_id,
        "overlay_image_id": overlay_receipt["image_id"],
        "repeats_per_control": REPEATS,
        "first_control": manifest["control"],
        "first_sha256": digests[0],
        "second_control": manifest["differential_control"],
        "second_sha256": digests[1],
        "second_control_output": observed[0],
        "first_parser_features": len(features[0]),
        "second_parser_features": len(features[1]),
        "parser_feature_difference": feature_difference,
        "first_only_features_by_file": dict(sorted(Counter(
            source_file(item).removeprefix(prefix) for item in features[0] - features[1]).items())),
        "second_only_features_by_file": dict(sorted(Counter(
            source_file(item).removeprefix(prefix) for item in features[1] - features[0]).items())),
        "first_afl_tuples": len(maps[0]),
        "second_afl_tuples": len(maps[1]),
        "afl_tuple_difference": map_difference,
        "second_case_kind": "valid_control",
    }
    (overlay / "differential.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"{relative}: {feature_difference} parser features, {map_difference} AFL++ tuples differ; "
          f"{REPEATS} repeats per control identical", flush=True)


if __name__ == "__main__":
    main()
