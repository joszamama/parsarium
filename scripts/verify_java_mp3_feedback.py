"""Check the Java plain MP3 AFL++ bridge: repeated control probes match and a second valid stream differs."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for


PROJECTS = ("jcodec", "mp3spi", "jlayer", "jaudiotagger")
CONTROL = "controls/mp3/tone-44k-mono.mp3"
DIFFERENTIAL = "controls/mp3/tone-22k-stereo.mp3"
REPORT = ROOT / "data/java/mp3/afl-feedback.json"


def run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> tuple[set, set]:
    common = ["docker", "run", "--rm", "--platform", manifest["platform"],
              "--network", "none", "--read-only", "--cap-drop", "ALL",
              "--security-opt", "no-new-privileges",
              "--user", f"{os.getuid()}:{os.getgid()}",
              "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
              "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "10000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = set((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = set((work / f"{name}.map").read_text().splitlines()) - {""}
    return features, tuples


def check(slug: str) -> dict:
    relative = Path("mp3/java") / slug
    _, manifest = project_for("mp3", "java", slug)
    if manifest["control"] != CONTROL:
        raise ValueError(f"{relative}: unexpected control")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    image = receipt["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-mp3-java-") as temporary:
        work = Path(temporary)
        first = probe(manifest, image, ROOT / CONTROL, work, "first")
        repeat = probe(manifest, image, ROOT / CONTROL, work, "repeat")
        repeat_two = probe(manifest, image, ROOT / CONTROL, work, "repeat_two")
        other = probe(manifest, image, ROOT / DIFFERENTIAL, work, "other")
        classpath = next(arg.removeprefix("--cp=") for arg in manifest["fuzz_smoke_args"]
                         if arg.startswith("--cp="))
        parsed = subprocess.run(
            ["docker", "run", "--rm", "--platform", manifest["platform"], "--network", "none",
             "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
             "--user", f"{os.getuid()}:{os.getgid()}", "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
             "-v", f"{ROOT / DIFFERENTIAL}:/input/case:ro", "--entrypoint", "java", image,
             "-cp", classpath, "GenericHarness",
             "/input/case"], capture_output=True, text=True, timeout=120, check=True)
        differential_output = json.loads(parsed.stdout.strip().splitlines()[-1])
    if differential_output != manifest["differential_expected_output"]:
        raise RuntimeError(f"{relative}: differential output changed: {differential_output}")
    if first != repeat or first != repeat_two:
        raise RuntimeError(f"{relative}: repeated control probe changed parser features or AFL++ map")
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len({item.split(":", 1)[0] for item in first[1]} ^
                           {item.split(":", 1)[0] for item in other[1]})
    if not feature_difference or not tuple_difference:
        raise RuntimeError(f"{relative}: differential input did not change parser feedback")
    groups = {}
    if slug == "mp3spi":
        for group in ("wrapper", "core"):
            prefix = group + "/"
            control_features = {item for item in first[0] if item.startswith(prefix)}
            other_features = {item for item in other[0] if item.startswith(prefix)}
            if not control_features or not other_features:
                raise RuntimeError(f"{relative}: {group} parser features absent")
            groups[group] = {"control_features": len(control_features),
                             "differential_features": len(other_features),
                             "feature_difference": len(control_features ^ other_features)}
    print(f"{relative}: stable repeat; {feature_difference} parser features, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)
    return {"project": str(relative), "pass": True,
            "feedback_kind": receipt["feedback_kind"],
            "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
            "control": CONTROL,
            "control_sha256": sha256((ROOT / CONTROL).read_bytes()).hexdigest(),
            "differential": DIFFERENTIAL,
            "differential_sha256": sha256((ROOT / DIFFERENTIAL).read_bytes()).hexdigest(),
            "differential_output": differential_output,
            "repeated_control_identical": True,
            "control_parser_features": len(first[0]),
            "control_afl_tuples": len(first[1]),
            "differential_parser_features": len(other[0]),
            "differential_afl_tuples": len(other[1]),
            "parser_feature_difference": feature_difference,
            "afl_tuple_difference": tuple_difference,
            **({"source_groups": groups} if groups else {})}


def main() -> None:
    selected = tuple(sys.argv[1:]) or PROJECTS
    if any(slug not in PROJECTS for slug in selected):
        raise ValueError(f"unknown Java MP3 project: {selected}")
    results = [check(slug) for slug in selected]
    if sys.argv[1:]:
        for result in results:
            slug = result["project"].rsplit("/", 1)[-1]
            path = ROOT / "data/java/mp3" / f"{slug}-feedback-differential.json"
            path.write_text(json.dumps({"schema_version": 1, **result}, indent=2) + "\n")
        kept = json.loads(REPORT.read_text())["results"] if REPORT.is_file() else []
        rows = {item["project"]: item for item in kept} | {item["project"]: item for item in results}
        results = [rows[f"mp3/java/{slug}"] for slug in PROJECTS if f"mp3/java/{slug}" in rows]
        REPORT.write_text(json.dumps({
            "schema_version": 1,
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "projects_total": len(results), "projects_passed": len(results),
            "differential_kind": "fixed_valid_mpeg2_stereo",
            "results": results}, indent=2) + "\n")
        print(json.dumps(results, indent=2))
        return
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_mpeg2_stereo",
        "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
