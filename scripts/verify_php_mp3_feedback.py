"""Check the PHP plain MP3 AFL++ bridge: repeated control probes match and a second valid control differs.

The base project image replays the differential control against its pinned
expected output. The bridge overlay then traces getID3 source lines and maps
each valid control three times with afl-showmap; parser features and tuples
must repeat exactly per control and differ between the two controls.
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


SLUG = "getid3"
REPEATS = 3
REPORT = ROOT / "data/php/mp3/afl-feedback.json"


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


def probe(manifest: dict, receipt: dict, case: Path, work: Path, name: str) -> tuple[frozenset, frozenset]:
    mounts = ["-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]
    run([*sandbox(manifest["platform"], mounts), "--entrypoint", "/bin/sh", receipt["image_id"],
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    features = frozenset((work / f"{name}.features").read_text().splitlines()) - {""}
    run([*sandbox(manifest["platform"], mounts), "-e", f"AFL_MAP_SIZE={receipt['afl_map_size']}",
         "--entrypoint", "afl-showmap", receipt["image_id"], "-m", "none", "-t", "30000",
         "-o", f"/coverage/{name}.map", "--", "/work/afl_proxy", "/input/case"])
    tuples = frozenset((work / f"{name}.map").read_text().splitlines()) - {""}
    return features, tuples


def main() -> None:
    project, manifest = project_for("mp3", "php", SLUG)
    relative = Path("mp3/php") / SLUG
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise ValueError("overlay receipt does not match the base project receipt")
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    digests = [manifest["control_sha256"], manifest["differential_control_sha256"]]
    for path, digest in zip(controls, digests):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")

    replay = run([*sandbox(manifest["platform"], ["-v", f"{controls[1]}:/input/differential:ro"]),
                  "--entrypoint", "php", base["image_id"], "/work/replay.php", "/input/differential"])
    observed = json.loads(replay)
    if observed != manifest["differential_expected_output"]:
        raise RuntimeError(f"differential control output mismatch: {observed}")

    probes = []
    with tempfile.TemporaryDirectory(prefix="parsarium-mp3-php-") as temporary:
        work = Path(temporary)
        for index, control in enumerate(controls):
            runs = [probe(manifest, receipt, control, work, f"c{index}r{repeat}") for repeat in range(REPEATS)]
            if any(item != runs[0] for item in runs):
                raise RuntimeError(f"{control.name}: repeated parser features or AFL++ maps differ")
            probes.append(runs[0])
    (first_features, first_tuples), (second_features, second_tuples) = probes
    if len(first_tuples) != receipt["feedback_edges"] or len(first_features) != receipt["parser_source_features"]:
        raise RuntimeError("control probe differs from overlay receipt")
    feature_difference = len(first_features ^ second_features)
    tuple_difference = len({item.split(":", 1)[0] for item in first_tuples} ^
                           {item.split(":", 1)[0] for item in second_tuples})
    mp3_module = "/module.audio.mp3.php:"
    mp3_feature_difference = len({item for item in first_features ^ second_features if mp3_module in item})
    if not feature_difference or not tuple_difference:
        raise RuntimeError("differential control did not change parser feedback")
    print(f"{relative}: stable repeats; {len(first_tuples)} vs {len(second_tuples)} tuples, "
          f"{tuple_difference} edge ids and {feature_difference} parser lines differ "
          f"({mp3_feature_difference} in module.audio.mp3.php)", flush=True)
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(relative),
        "pass": True,
        "feedback_kind": receipt["feedback_kind"],
        "feedback_scope": "Xdebug executed lines under /work/vendor/james-heinrich/getid3/ mapped to the AFL++ bitmap by the bridge proxy; PHP runtime and harness lines are not counted.",
        "base_project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"],
        "overlay_image_id": receipt["image_id"],
        "repeats_per_control": REPEATS,
        "repeated_controls_identical": True,
        "first_control": manifest["control"],
        "first_sha256": manifest["control_sha256"],
        "second_control": manifest["differential_control"],
        "second_sha256": manifest["differential_control_sha256"],
        "second_control_output": observed,
        "second_case_kind": "valid_control",
        "first_parser_features": len(first_features),
        "second_parser_features": len(second_features),
        "parser_feature_difference": feature_difference,
        "mp3_module_feature_difference": mp3_feature_difference,
        "first_afl_tuples": len(first_tuples),
        "second_afl_tuples": len(second_tuples),
        "afl_tuple_difference": tuple_difference,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
