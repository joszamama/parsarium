"""Check TinyTag plain MP3 parser feedback: stable repeats and an input-dependent _MPEG path.

Expected outputs come from the independent header walker in
controls/mp3/check_controls.py, not from TinyTag. Both full-length controls are
CBR streams without Xing/Info/VBRI, so TinyTag runs the same lines on them; the
feedback difference is shown with a valid prefix of three whole frames, which
ends before TinyTag's five-frame CBR estimate. Every differing line must lie in
the _MPEG frame-header class, and no input may reach the _ID3 reader.
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


SLUG = "tinytag"
REPEATS = 2
REPORT = ROOT / "data/python/mp3/tinytag-valid-feedback.json"
MODULE = "/opt/venv/lib/python3.14/site-packages/tinytag/tinytag.py"


def walker():
    spec = importlib.util.spec_from_file_location("check_controls", ROOT / "controls/mp3/check_controls.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.walk


def expectation(walk, data: bytes) -> dict:
    header = walk(data)
    duration = header["frames"] * header["samples_per_frame"] / header["sample_rate"]
    return {"sample_rate": header["sample_rate"], "channels": header["channels"],
            "bitrate_kbps": header["bitrate"] / 1000,
            "duration_us": round(duration * 1_000_000)}


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
    if not features or not tuples or any(not item.startswith(MODULE + ":") for item in features):
        raise RuntimeError(f"{name}: feedback is empty or outside tinytag/tinytag.py")
    return features, tuples


def lines_in(features: set[str], span: range) -> set[int]:
    return {line for line in (int(item.rsplit(":", 1)[1]) for item in features) if line in span}


def main() -> None:
    project, manifest = project_for("mp3", "python", SLUG)
    relative = Path("mp3/python") / SLUG
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise ValueError("overlay receipt does not match the base project receipt")

    walk = walker()
    control = (ROOT / manifest["control"]).read_bytes()
    second = (ROOT / manifest["differential_control"]).read_bytes()
    variant = control[:manifest["feedback_variant_bytes"]]
    cases = {"control": (control, manifest["control_sha256"], manifest["expected_output"]),
             "second": (second, manifest["differential_control_sha256"],
                        manifest["differential_expected_output"]),
             "variant": (variant, manifest["feedback_variant_sha256"],
                         manifest["feedback_variant_expected_output"])}
    for name, (data, digest, expected) in cases.items():
        if sha256(data).hexdigest() != digest:
            raise ValueError(f"{name}: hash mismatch")
        if expectation(walk, data) != expected:
            raise ValueError(f"{name}: manifest output differs from the independent header walk")

    with tempfile.TemporaryDirectory(prefix="parsarium-mp3-tinytag-") as temporary:
        work = Path(temporary)
        paths = {}
        for name, (data, _, _) in cases.items():
            paths[name] = work / f"{name}.mp3"
            paths[name].write_bytes(data)
        spans = json.loads(run([*sandbox(manifest["platform"], []), "--entrypoint", "/opt/venv/bin/python",
                                base["image_id"], "-c",
                                "import json, sys; sys.path.insert(0, '/work'); import harness; "
                                "print(json.dumps([[harness.MPEG_LINES.start, harness.MPEG_LINES.stop], "
                                "[harness.ID3_LINES.start, harness.ID3_LINES.stop]]))"]))
        mpeg_span, id3_span = range(*spans[0]), range(*spans[1])
        outputs = {}
        for name, path in paths.items():
            outputs[name] = json.loads(run([*sandbox(manifest["platform"], ["-v", f"{path}:/input/case:ro"]),
                                            "--entrypoint", "/opt/venv/bin/python", base["image_id"],
                                            "/work/replay.py", "/input/case"]))
            if outputs[name] != cases[name][2]:
                raise RuntimeError(f"{name}: TinyTag output {outputs[name]} differs from {cases[name][2]}")
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
    if any(lines_in(item, id3_span) for item in lines.values()):
        raise RuntimeError("an untagged input reached the _ID3 reader")
    if any(not lines_in(item, mpeg_span) for item in lines.values()):
        raise RuntimeError("an input did not reach the _MPEG frame-header reader")
    variant_diff = lines["control"] ^ lines["variant"]
    if not variant_diff or lines_in(variant_diff, mpeg_span) != {int(item.rsplit(":", 1)[1]) for item in variant_diff}:
        raise RuntimeError("the valid prefix does not change feedback inside _MPEG only")
    variant_tuples = len(maps["control"] ^ maps["variant"])
    if not variant_tuples:
        raise RuntimeError("the valid prefix does not change AFL++ tuples")
    shared_diff = len(lines["control"] ^ lines["second"])
    shared_tuples = len(maps["control"] ^ maps["second"])
    report = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(relative),
        "pass": True,
        "feedback_kind": receipt["feedback_kind"],
        "feedback_scope": "Executed lines of the pinned tinytag/tinytag.py module are hashed into the AFL++ bitmap by the bridge proxy; harness and interpreter lines are excluded. Lines are also split by class: _MPEG is the frame-header reader, _ID3 must stay at zero.",
        "independent_oracle": "controls/mp3/check_controls.py walk(): frames x samples_per_frame / sample_rate, header bitrate / 1000",
        "base_project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"],
        "overlay_image_id": receipt["image_id"],
        "mpeg_class_lines": [mpeg_span.start, mpeg_span.stop - 1],
        "id3_class_lines": [id3_span.start, id3_span.stop - 1],
        "repeats_per_input": REPEATS,
        "repeated_inputs_identical": True,
        "first_control": manifest["control"],
        "first_sha256": manifest["control_sha256"],
        "first_output": outputs["control"],
        "second_control": manifest["differential_control"],
        "second_sha256": manifest["differential_control_sha256"],
        "second_output": outputs["second"],
        "variant": manifest["feedback_variant"],
        "variant_sha256": manifest["feedback_variant_sha256"],
        "variant_output": outputs["variant"],
        "variant_case_kind": "valid_whole_frame_prefix",
        "first_parser_source_lines": len(lines["control"]),
        "first_mpeg_lines": len(lines_in(lines["control"], mpeg_span)),
        "second_parser_source_lines": len(lines["second"]),
        "second_mpeg_lines": len(lines_in(lines["second"], mpeg_span)),
        "variant_parser_source_lines": len(lines["variant"]),
        "variant_mpeg_lines": len(lines_in(lines["variant"], mpeg_span)),
        "id3_lines_any_input": 0,
        "shared_controls_line_difference": shared_diff,
        "shared_controls_afl_tuple_difference": shared_tuples,
        "variant_line_difference": len(variant_diff),
        "variant_line_difference_in_mpeg": len(variant_diff),
        "variant_differing_lines": sorted(int(item.rsplit(":", 1)[1]) for item in variant_diff),
        "first_afl_tuples": len(maps["control"]),
        "second_afl_tuples": len(maps["second"]),
        "variant_afl_tuples": len(maps["variant"]),
        "variant_afl_tuple_difference": variant_tuples,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{relative}: stable repeats; control {len(lines['control'])} lines "
          f"({report['first_mpeg_lines']} in _MPEG), second control differs by {shared_diff}, "
          f"3-frame prefix differs by {len(variant_diff)} _MPEG lines and {variant_tuples} tuples", flush=True)


if __name__ == "__main__":
    main()
