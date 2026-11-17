"""Check Go JSON AFL++ bridges: repeated control probes match and a second valid input differs."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


PROJECTS = ("github_com_json_iterator_go", "stdlib_unmarshal")
CONTROL = "controls/json/nested-object.json"
DIFFERENTIAL = "controls/json/nested-array.json"
REPORT = ROOT / "data/go/json/afl-feedback.json"


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
    relative = Path("json/go") / slug
    _, manifest = project_for("json", "go", slug)
    if manifest["control"] != CONTROL:
        raise ValueError(f"{relative}: unexpected control")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    image = receipt["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-json-go-") as temporary:
        work = Path(temporary)
        first = probe(manifest, image, ROOT / CONTROL, work, "first")
        repeat = probe(manifest, image, ROOT / CONTROL, work, "repeat")
        other = probe(manifest, image, ROOT / DIFFERENTIAL, work, "other")
    if first != repeat:
        raise RuntimeError(f"{relative}: repeated control probe changed parser features or AFL++ map")
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len({item.split(":", 1)[0] for item in first[1]} ^
                           {item.split(":", 1)[0] for item in other[1]})
    if not feature_difference or not tuple_difference:
        raise RuntimeError(f"{relative}: differential input did not change parser feedback")
    print(f"{relative}: stable repeat; {feature_difference} parser features, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)
    return {"project": str(relative), "pass": True,
            "feedback_kind": receipt["feedback_kind"],
            "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
            "control": CONTROL,
            "control_sha256": sha256((ROOT / CONTROL).read_bytes()).hexdigest(),
            "differential": DIFFERENTIAL,
            "differential_sha256": sha256((ROOT / DIFFERENTIAL).read_bytes()).hexdigest(),
            "repeated_control_identical": True,
            "control_parser_features": len(first[0]),
            "control_afl_tuples": len(first[1]),
            "differential_parser_features": len(other[0]),
            "differential_afl_tuples": len(other[1]),
            "parser_feature_difference": feature_difference,
            "afl_tuple_difference": tuple_difference}


def main() -> None:
    results = [check(slug) for slug in PROJECTS]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_nested_array",
        "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
