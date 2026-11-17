"""Check the JavaScript MP3 AFL++ bridges: both valid controls replay to their pinned
outputs and agree with the independent frame-header walker, repeated probes match, and
the second control changes parser feedback."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for


PROJECTS = ("mediabunny", "music_metadata", "codec_parser")
REPEATS = 3
REPORT = ROOT / "data/javascript/mp3/afl-feedback.json"
_walker = importlib.util.spec_from_file_location("check_controls", ROOT / "controls/mp3/check_controls.py")
WALKER = importlib.util.module_from_spec(_walker)
_walker.loader.exec_module(WALKER)


def header_fields(data: bytes) -> dict:
    """MPEG version and layer from the first header's bits, as numbers."""
    return {"mpeg_version": {3: 1, 2: 2, 0: 2.5}[(data[1] >> 3) & 3], "layer": 4 - ((data[1] >> 1) & 3)}


def walker_agreement(path: Path, output: dict) -> dict:
    """Compare every field the parser reports with the header walker; the full input must be
    framed, either as frame bytes or as a frame-counted sample total."""
    data = path.read_bytes()
    walked = WALKER.walk(data)
    shared = sorted(key for key in walked if key in output)
    walked_samples = walked["frames"] * walked["samples_per_frame"]
    if "frame_bytes" in shared:
        if output["frame_bytes"] != len(data):
            raise RuntimeError(f"{path.name}: parser did not frame the full input")
    elif output.get("number_of_samples") != walked_samples:
        raise RuntimeError(f"{path.name}: parser did not count every frame")
    if any(output[key] != walked[key] for key in shared):
        raise RuntimeError(f"{path.name}: parser output differs from frame-header walker: {output}")
    if "total_samples" in output and output["total_samples"] != walked_samples:
        raise RuntimeError(f"{path.name}: total samples differ from walker frames")
    result = {"walker_output": walked, "compared_fields": shared}
    if "number_of_samples" in output:
        # Paths that report numeric version/layer and a duration are also checked against header bits.
        oracle = {**header_fields(data), "number_of_samples": walked_samples,
                  "duration": walked_samples / walked["sample_rate"]}
        if any(output[key] != value for key, value in oracle.items()):
            raise RuntimeError(f"{path.name}: parser output differs from header oracle: {output}")
        result.update(header_oracle=oracle, compared_fields=sorted([*shared, *oracle]))
    return result


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    return result.stdout


def sandbox(manifest: dict, case: Path, work: Path) -> list[str]:
    return ["docker", "run", "--rm", "--platform", manifest["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
            "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> tuple[set, set]:
    common = sandbox(manifest, case, work)
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "30000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = set((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = {line.split(":", 1)[0] for line in (work / f"{name}.map").read_text().splitlines() if line}
    return features, tuples


def check(slug: str) -> dict:
    project, manifest = project_for("mp3", "javascript", slug)
    relative = Path("mp3/javascript") / slug
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_image_id"] != base["image_id"]:
        raise ValueError("overlay was built from a different project image")
    control, differential = ROOT / manifest["control"], ROOT / manifest["differential_control"]
    for path, digest in ((control, manifest["control_sha256"]),
                         (differential, manifest["differential_control_sha256"])):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")
    with tempfile.TemporaryDirectory(prefix="parsarium-mp3-js-") as temporary:
        work = Path(temporary)
        replay = lambda case: json.loads(run([*sandbox(manifest, case, work), "--entrypoint", "node",
                                              base["image_id"], "/work/replay.js", "/input/case"]))
        control_output, replayed = replay(control), replay(differential)
        if control_output != manifest["expected_output"]:
            raise RuntimeError(f"first control output differs: {control_output}")
        if replayed != manifest["differential_expected_output"]:
            raise RuntimeError(f"second control output differs: {replayed}")
        api_agreement = None
        if (ROOT / "projects" / relative / "api-check.js").is_file():
            api_agreement = {}
            for case, expected in ((control, control_output), (differential, replayed)):
                checked = json.loads(run([*sandbox(manifest, case, work), "--entrypoint", "node",
                                          base["image_id"], "/work/api-check.js", "/input/case"]))
                if checked["output"] != expected:
                    raise RuntimeError(f"{relative}: documented APIs differ on {case.name}")
                api_agreement[case.name] = checked["apis"]
        controls = [probe(manifest, receipt["image_id"], control, work, f"control-{index}")
                    for index in range(REPEATS)]
        others = [probe(manifest, receipt["image_id"], differential, work, f"differential-{index}")
                  for index in range(REPEATS)]
    if any(item != controls[0] for item in controls) or any(item != others[0] for item in others):
        raise RuntimeError(f"{relative}: repeated probe changed parser features or AFL++ map")
    first, other = controls[0], others[0]
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len(first[1] ^ other[1])
    if not feature_difference or not tuple_difference:
        raise RuntimeError(f"{relative}: second control did not change parser feedback")
    prefix = manifest.get("afl_coverage_subject_prefix", manifest["coverage_subject_prefix"])
    by_file = lambda items: dict(sorted({name: sum(1 for item in items if item.startswith(prefix + name + ":"))
                                         for name in {item[len(prefix):].rsplit(":", 1)[0] for item in items}}.items()))
    result = {"project": str(relative), "pass": True,
              "feedback_kind": receipt["feedback_kind"],
              "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
              "base_image_id": base["image_id"], "overlay_image_id": receipt["image_id"],
              "control": manifest["control"], "control_sha256": manifest["control_sha256"],
              "differential": manifest["differential_control"],
              "differential_sha256": manifest["differential_control_sha256"],
              "differential_output": replayed,
              "control_walker": walker_agreement(control, control_output),
              "differential_walker": walker_agreement(differential, replayed),
              "repeats_per_control": REPEATS,
              "repeated_control_identical": True, "repeated_differential_identical": True,
              "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
              "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
              "parser_feature_difference": feature_difference, "afl_tuple_difference": tuple_difference,
              "control_only_features_by_file": by_file(first[0] - other[0]),
              "differential_only_features_by_file": by_file(other[0] - first[0]),
              "control_features_by_file": by_file(first[0]),
              "control_only_features": sorted(item[len(prefix):] for item in first[0] - other[0]),
              "differential_only_features": sorted(item[len(prefix):] for item in other[0] - first[0])}
    if api_agreement is not None:
        result["documented_api_agreement"] = api_agreement
    print(f"{relative}: stable repeats; {feature_difference} parser features, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)
    return result


def main() -> None:
    selected = tuple(sys.argv[1:]) or PROJECTS
    if any(slug not in PROJECTS for slug in selected):
        raise ValueError(f"unknown JavaScript MP3 project: {selected}")
    results = [check(slug) for slug in selected]
    if sys.argv[1:]:
        # A scoped receipt for newly added paths; the cell aggregate is refreshed by the integrator.
        for result in results:
            slug = result["project"].rsplit("/", 1)[-1]
            path = ROOT / "data/javascript/mp3" / f"{slug}-feedback-differential.json"
            path.write_text(json.dumps({"schema_version": 1,
                                        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
                                        **result}, indent=2, ensure_ascii=False) + "\n")
        return
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_22k_stereo_control",
        "standard_feedback": "none: Node.js documents no MPEG audio parser API",
        "results": results}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
