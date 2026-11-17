"""Check a PHP plain MP3 AFL++ bridge: repeated control probes match and a second valid control differs.

The base project image replays the differential control against its pinned
expected output. The bridge overlay then traces parser package source lines
and maps each valid control three times with afl-showmap; parser features and
tuples must repeat exactly per control and differ between the two controls.
Mp3Info's report also compares both controls with the header-walk oracle in
controls/mp3/check_controls.py.

Usage: python3 verify_php_mp3_feedback.py [getid3|wapmorgan_mp3info]
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for


REPEATS = 3
TARGETS = {
    "getid3": {
        "report": ROOT / "data/php/mp3/afl-feedback.json",
        "module": "/module.audio.mp3.php:",
        "module_key": "mp3_module_feature_difference",
        "scope": "Xdebug executed lines under /work/vendor/james-heinrich/getid3/ mapped to the AFL++ bitmap by the bridge proxy; PHP runtime and harness lines are not counted.",
    },
    "wapmorgan_mp3info": {
        "report": ROOT / "data/php/mp3/wapmorgan_mp3info-feedback.json",
        "module": "/src/Mp3Info.php:",
        "module_key": "mp3info_class_feature_difference",
        "scope": "Xdebug executed lines under /work/vendor/wapmorgan/mp3info/ mapped to the AFL++ bitmap by the bridge proxy; PHP runtime and harness lines are not counted.",
    },
}


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


def oracle(path: Path) -> dict:
    """Walk every frame header with the independent control checker."""
    sys.path.insert(0, str(ROOT / "controls/mp3"))
    from check_controls import walk
    data = path.read_bytes()
    walked = walk(data)
    samples = walked["frames"] * walked["samples_per_frame"]
    return {"mpeg_version": 1 if data[1] >> 3 & 3 == 3 else 2, "layer": 3,
            "sample_rate": walked["sample_rate"], "channels": walked["channels"],
            "bitrate": walked["bitrate"], "frames": walked["frames"],
            "frame_bytes": walked["frame_bytes"], "samples": samples,
            "duration": round(samples / walked["sample_rate"], 5)}


def compare(observed: dict, expected: dict) -> dict:
    channels = 1 if observed["channel"] == "mono" else 2
    return {"header_fields_match": (observed["mpeg_version"], observed["layer"], observed["sample_rate"],
                                    channels, observed["bitrate"]) ==
                                   (expected["mpeg_version"], expected["layer"], expected["sample_rate"],
                                    expected["channels"], expected["bitrate"]),
            "frames_match": observed["frames"] == expected["frames"],
            "audio_bytes_match": observed["audio_size"] == expected["frame_bytes"]}


def main() -> None:
    slug = sys.argv[1] if len(sys.argv) > 1 else "getid3"
    target = TARGETS[slug]
    project, manifest = project_for("mp3", "php", slug)
    relative = Path("mp3/php") / slug
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
    mp3_feature_difference = len({item for item in first_features ^ second_features if target["module"] in item})
    if not feature_difference or not tuple_difference:
        raise RuntimeError("differential control did not change parser feedback")
    print(f"{relative}: stable repeats; {len(first_tuples)} vs {len(second_tuples)} tuples, "
          f"{tuple_difference} edge ids and {feature_difference} parser lines differ "
          f"({mp3_feature_difference} in {target['module'].strip('/:')})", flush=True)
    report = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(relative),
        "pass": True,
        "feedback_kind": receipt["feedback_kind"],
        "feedback_scope": target["scope"],
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
        target["module_key"]: mp3_feature_difference,
        "first_afl_tuples": len(first_tuples),
        "second_afl_tuples": len(second_tuples),
        "afl_tuple_difference": tuple_difference,
    }
    if slug == "wapmorgan_mp3info":
        first_oracle, second_oracle = oracle(controls[0]), oracle(controls[1])
        report["differing_parser_lines"] = sorted(first_features ^ second_features)
        report["independent_oracle"] = "controls/mp3/check_controls.py walk()"
        report["oracle_comparison"] = [
            {"control": manifest["control"], "observed": manifest["expected_output"], "oracle": first_oracle,
             **compare(manifest["expected_output"], first_oracle)},
            {"control": manifest["differential_control"], "observed": observed, "oracle": second_oracle,
             **compare(observed, second_oracle)},
        ]
        if not all(report["oracle_comparison"][0][key] for key in ("header_fields_match", "frames_match", "audio_bytes_match")):
            raise RuntimeError("primary control no longer matches the header-walk oracle")
        if report["oracle_comparison"][1]["header_fields_match"] != manifest["differential_matches_oracle"]:
            raise RuntimeError("differential oracle agreement differs from the manifest")
    target["report"].write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
