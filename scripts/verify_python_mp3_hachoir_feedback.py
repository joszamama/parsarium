"""Check hachoir plain MP3 parser feedback: stable repeats and an input-dependent mpeg_audio path.

Expected outputs come from the independent header walker in
controls/mp3/check_controls.py, plus channel-mode bits read here from every
frame header; none of them come from hachoir. The two controls differ in MPEG
version, channel mode, bitrate and frame count, so the full-length controls
must change feedback inside hachoir/parser/audio/mpeg_audio.py. No input may
reach hachoir/parser/audio/id3.py.
"""

from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


SLUG = "hachoir"
REPEATS = 3
REPORT = ROOT / "data/python/mp3/hachoir-valid-feedback.json"
PACKAGE = "/opt/venv/lib/python3.14/site-packages/hachoir/"
MPEG_MODULE = PACKAGE + "parser/audio/mpeg_audio.py"
ID3_MODULE = PACKAGE + "parser/audio/id3.py"
VERSION_NAMES = {3: "1", 2: "2", 0: "2.5"}
CHANNEL_MODES = {0: "Stereo", 1: "Joint stereo", 2: "Dual channel", 3: "Single channel"}


def walker():
    spec = importlib.util.spec_from_file_location("check_controls", ROOT / "controls/mp3/check_controls.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.walk


def header_bits(data: bytes, frames: int) -> tuple[str, str]:
    """Read version and channel-mode bits from each of the walked frame headers."""
    offset, versions, modes = 0, set(), set()
    for _ in range(frames):
        b1, b2, b3 = data[offset + 1], data[offset + 2], data[offset + 3]
        version_bits = (b1 >> 3) & 3
        lsf = version_bits != 3
        bitrate = {False: [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
                   True: [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]}[lsf][b2 >> 4] * 1000
        rate = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000]}[version_bits][(b2 >> 2) & 3]
        versions.add(VERSION_NAMES[version_bits])
        modes.add(CHANNEL_MODES[b3 >> 6])
        offset += (72 if lsf else 144) * bitrate // rate + ((b2 >> 1) & 1)
    if offset != len(data) or len(versions) != 1 or len(modes) != 1:
        raise ValueError("frame headers are not uniform or do not cover the input")
    return versions.pop(), modes.pop()


def expectation(walk, data: bytes) -> dict:
    header = walk(data)
    version, mode = header_bits(data, header["frames"])
    return {"version": version, "layer": "III", "sample_rate": header["sample_rate"],
            "bitrate": header["bitrate"], "channel_mode": mode, "channels": header["channels"],
            "frames": header["frames"], "frame_bytes": header["frame_bytes"]}


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
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp", *mounts]


def probe(manifest: dict, receipt: dict, case: Path, work: Path, name: str) -> tuple[set[str], set[str]]:
    mounts = ["-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]
    run([*sandbox(manifest["platform"], mounts), "--entrypoint", "/bin/sh", receipt["image_id"],
         "/work/afl_trace", "/input/case", f"/coverage/{name}.txt"])
    run([*sandbox(manifest["platform"], mounts), "-e", f"AFL_MAP_SIZE={receipt['afl_map_size']}",
         "--entrypoint", "afl-showmap", receipt["image_id"], "-m", "none", "-t", "120000",
         "-o", f"/coverage/{name}.map", "--", "/work/afl_proxy", "/input/case"])
    features = set((work / f"{name}.txt").read_text().splitlines()) - {""}
    tuples = {line.split(":", 1)[0] for line in (work / f"{name}.map").read_text().splitlines() if line}
    if not features or not tuples or any(not item.startswith(PACKAGE) for item in features):
        raise RuntimeError(f"{name}: feedback is empty or outside the hachoir package")
    return features, tuples


def in_module(features: set[str], module: str) -> set[str]:
    return {item for item in features if item.rsplit(":", 1)[0] == module}


def main() -> None:
    project, manifest = project_for("mp3", "python", SLUG)
    relative = Path("mp3/python") / SLUG
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise ValueError("overlay receipt does not match the base project receipt")

    walk = walker()
    cases = {"control": ((ROOT / manifest["control"]).read_bytes(), manifest["control_sha256"],
                         manifest["expected_output"]),
             "second": ((ROOT / manifest["differential_control"]).read_bytes(),
                        manifest["differential_control_sha256"], manifest["differential_expected_output"])}
    for name, (data, digest, expected) in cases.items():
        if sha256(data).hexdigest() != digest:
            raise ValueError(f"{name}: hash mismatch")
        if data[:3] == b"ID3" or data[-128:-125] == b"TAG":
            raise ValueError(f"{name}: control is tagged")
        if expectation(walk, data) != expected:
            raise ValueError(f"{name}: manifest output differs from the independent header walk")

    with tempfile.TemporaryDirectory(prefix="parsarium-mp3-hachoir-") as temporary:
        work = Path(temporary)
        paths = {}
        for name, (data, _, _) in cases.items():
            paths[name] = work / f"{name}.mp3"
            paths[name].write_bytes(data)
        outputs = {}
        for name, path in paths.items():
            outputs[name] = json.loads(run([*sandbox(manifest["platform"], ["-v", f"{path}:/input/case:ro"]),
                                            "--entrypoint", "/opt/venv/bin/python", base["image_id"],
                                            "/work/replay.py", "/input/case"]))
            if outputs[name] != cases[name][2]:
                raise RuntimeError(f"{name}: hachoir output {outputs[name]} differs from {cases[name][2]}")
        feedback = {}
        for name, path in paths.items():
            runs = [probe(manifest, receipt, path, work, f"{name}{repeat}") for repeat in range(REPEATS)]
            if any(item != runs[0] for item in runs):
                raise RuntimeError(f"{name}: repeated parser lines or AFL++ maps differ")
            feedback[name] = runs[0]

    lines = {name: item[0] for name, item in feedback.items()}
    maps = {name: item[1] for name, item in feedback.items()}
    if len(lines["control"]) != receipt["parser_source_features"] or len(maps["control"]) != receipt["feedback_edges"]:
        raise RuntimeError("control trace or map differs from overlay receipt")
    if any(in_module(item, ID3_MODULE) for item in lines.values()):
        raise RuntimeError("an untagged input reached hachoir's ID3 parser")
    if any(not in_module(item, MPEG_MODULE) for item in lines.values()):
        raise RuntimeError("an input did not reach the mpeg_audio frame parser")
    difference = lines["control"] ^ lines["second"]
    mpeg_difference = in_module(difference, MPEG_MODULE)
    if not mpeg_difference:
        raise RuntimeError("the two controls do not change mpeg_audio.py feedback")
    tuple_difference = len(maps["control"] ^ maps["second"])
    if not tuple_difference:
        raise RuntimeError("the two controls do not change AFL++ tuples")
    other_difference = sorted(item.removeprefix(PACKAGE) for item in difference - mpeg_difference)
    report = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(relative),
        "pass": True,
        "feedback_kind": receipt["feedback_kind"],
        "feedback_scope": "Executed lines of the pinned hachoir package (parser, field, stream and core modules) are hashed into the AFL++ bitmap by the bridge proxy; harness and interpreter lines are excluded. Lines in parser/audio/mpeg_audio.py, the MPEG audio frame parser, are counted separately; parser/audio/id3.py must stay at zero.",
        "independent_oracle": "controls/mp3/check_controls.py walk() for sample rate, channels, bitrate, frame count and frame bytes; version and channel-mode bits read from every frame header in this script",
        "base_project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"],
        "overlay_image_id": receipt["image_id"],
        "repeats_per_input": REPEATS,
        "repeated_inputs_identical": True,
        "first_control": manifest["control"],
        "first_sha256": manifest["control_sha256"],
        "first_output": outputs["control"],
        "second_control": manifest["differential_control"],
        "second_sha256": manifest["differential_control_sha256"],
        "second_output": outputs["second"],
        "first_parser_source_lines": len(lines["control"]),
        "first_mpeg_audio_lines": len(in_module(lines["control"], MPEG_MODULE)),
        "second_parser_source_lines": len(lines["second"]),
        "second_mpeg_audio_lines": len(in_module(lines["second"], MPEG_MODULE)),
        "id3_lines_any_input": 0,
        "controls_line_difference": len(difference),
        "controls_line_difference_in_mpeg_audio": len(mpeg_difference),
        "mpeg_audio_differing_lines": sorted(int(item.rsplit(":", 1)[1]) for item in mpeg_difference),
        "other_differing_lines": other_difference,
        "first_afl_tuples": len(maps["control"]),
        "second_afl_tuples": len(maps["second"]),
        "afl_tuple_difference": tuple_difference,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{relative}: stable repeats; control {len(lines['control'])} lines "
          f"({report['first_mpeg_audio_lines']} in mpeg_audio.py), second {len(lines['second'])}; "
          f"{len(difference)} lines differ ({len(mpeg_difference)} in mpeg_audio.py), "
          f"{tuple_difference} AFL++ tuples differ", flush=True)


if __name__ == "__main__":
    main()
