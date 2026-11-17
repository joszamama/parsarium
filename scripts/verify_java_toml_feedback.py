"""Check the Java TOML AFL++ bridge: each control repeats identically and the two controls differ.

For every selected Java TOML project this replays both valid controls three times through the
built overlay image: the JaCoCo parser-line tracer (``/work/afl_trace``) and ``afl-showmap`` over
``/work/afl_proxy``. It requires identical repeats per control, at least two AFL++ tuples and two
parser source lines that differ between the controls, the typed tree of both controls printed by
the project harness inside the same image, and an overlay receipt bound to the current project
receipt. Results go to ``data/java/toml/afl-feedback.json``. No campaign and no malformed input.
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

from run_case import ROOT, project_for


PROJECTS = ("jackson_dataformat_toml", "tomlj", "night_config_toml")
CONTROL = "controls/toml/service-config.toml"
DIFFERENTIAL = "controls/toml/typed-scalars.toml"
REPEATS = 3
REPORT = ROOT / "data/java/toml/afl-feedback.json"


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1500:])
    return result.stdout


def docker_common(manifest: dict, case: Path) -> list[str]:
    return ["docker", "run", "--rm", "--platform", manifest["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
            "-v", f"{case}:/input/case:ro"]


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> tuple[frozenset, frozenset]:
    common = [*docker_common(manifest, case), "-v", f"{work}:/coverage"]
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "30000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = frozenset((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = frozenset((work / f"{name}.map").read_text().splitlines()) - {""}
    return features, tuples


def typed_tree(manifest: dict, image: str, case: Path) -> dict:
    classpath = next(arg.removeprefix("--cp=") for arg in manifest["fuzz_smoke_args"]
                     if arg.startswith("--cp="))
    output = run([*docker_common(manifest, case), "--entrypoint", "java", image,
                  "-Dstdout.encoding=UTF-8", "-cp", classpath, "GenericHarness", "/input/case"])
    return json.loads(output.strip().splitlines()[-1])


def per_file(features: frozenset) -> dict[str, int]:
    return dict(sorted(Counter(item.rsplit(":", 1)[0] for item in features).items()))


def check(slug: str) -> dict:
    relative = Path("toml/java") / slug
    project, manifest = project_for("toml", "java", slug)
    if manifest["control"] != CONTROL or manifest["differential_control"] != DIFFERENTIAL:
        raise ValueError(f"{relative}: unexpected controls")
    for key in ("control", "differential_control"):
        if sha256((ROOT / manifest[key]).read_bytes()).hexdigest() != manifest[f"{key}_sha256"]:
            raise ValueError(f"{relative}: {key} hash changed")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base_receipt_sha = sha256((project / "verification.json").read_bytes()).hexdigest()
    if receipt["base_project_receipt_sha256"] != base_receipt_sha:
        raise RuntimeError(f"{relative}: overlay receipt predates the project receipt")
    image = receipt["image_id"]
    runs = {}
    with tempfile.TemporaryDirectory(prefix="parsarium-toml-java-") as temporary:
        work = Path(temporary)
        for label, control in (("control", CONTROL), ("differential", DIFFERENTIAL)):
            runs[label] = [probe(manifest, image, ROOT / control, work, f"{label}-{index}")
                           for index in range(REPEATS)]
        outputs = {"control": typed_tree(manifest, image, ROOT / CONTROL),
                   "differential": typed_tree(manifest, image, ROOT / DIFFERENTIAL)}
    if outputs["control"] != manifest["expected_output"]:
        raise RuntimeError(f"{relative}: primary control typed tree changed")
    if outputs["differential"] != manifest["differential_expected_output"]:
        raise RuntimeError(f"{relative}: differential typed tree changed: {outputs['differential']}")
    for label, probes in runs.items():
        if any(item != probes[0] for item in probes[1:]):
            raise RuntimeError(f"{relative}: repeated {label} probe changed parser lines or AFL++ map")
    (control_lines, control_map), (other_lines, other_map) = runs["control"][0], runs["differential"][0]
    if len(control_lines) != receipt["parser_source_features"] or len(control_map) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    control_ids = {item.split(":", 1)[0] for item in control_map}
    other_ids = {item.split(":", 1)[0] for item in other_map}
    tuple_difference = len(control_ids ^ other_ids)
    line_difference = len(control_lines ^ other_lines)
    if tuple_difference < 2 or line_difference < 2:
        raise RuntimeError(f"{relative}: the two controls do not differ in parser feedback")
    print(f"{relative}: {REPEATS} identical repeats per control; {line_difference} parser lines, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)
    return {
        "project": str(relative), "pass": True,
        "feedback_kind": receipt["feedback_kind"],
        "feedback_scope": manifest["coverage"],
        "base_project_receipt_sha256": base_receipt_sha,
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "image_id": image,
        "control": CONTROL, "control_sha256": manifest["control_sha256"],
        "differential": DIFFERENTIAL, "differential_sha256": manifest["differential_control_sha256"],
        "differential_output": outputs["differential"],
        "repeats_per_control": REPEATS,
        "repeated_control_identical": True,
        "repeated_differential_identical": True,
        "control_parser_lines": len(control_lines),
        "control_afl_tuples": len(control_map),
        "differential_parser_lines": len(other_lines),
        "differential_afl_tuples": len(other_map),
        "parser_lines_only_in_control": len(control_lines - other_lines),
        "parser_lines_only_in_differential": len(other_lines - control_lines),
        "afl_tuples_only_in_control": len(control_ids - other_ids),
        "afl_tuples_only_in_differential": len(other_ids - control_ids),
        "parser_line_difference": line_difference,
        "afl_tuple_difference": tuple_difference,
        "control_parser_lines_per_file": per_file(control_lines),
        "differential_parser_lines_per_file": per_file(other_lines),
    }


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--project", choices=PROJECTS, help="refresh one project; keep the other rows")
    selected = cli.parse_args().project
    now = datetime.now(timezone.utc).isoformat()
    rows = {}
    if selected and REPORT.is_file():
        rows = {row["project"].rsplit("/", 1)[-1]: row for row in json.loads(REPORT.read_text())["results"]}
    for slug in ((selected,) if selected else PROJECTS):
        rows[slug] = {**check(slug), "checked_at_utc": now}
    results = [rows[slug] for slug in PROJECTS if slug in rows]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": now,
        "projects_total": len(results), "projects_passed": sum(row["pass"] for row in results),
        "differential_kind": "fixed_valid_typed_scalars",
        "mutation_campaign_run": False,
        "results": results}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
