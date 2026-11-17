"""Check the Java YAML AFL++ bridges: three identical probes per valid control, and the two controls differ.

Each selected project replays controls/yaml/catalog.yaml and controls/yaml/order.yaml
three times through its parser-line trace and afl-showmap. Both typed trees must
equal the hand-written oracle in controls/yaml/check_controls.py. Writes
data/java/yaml/afl-feedback.json.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for

sys.path.insert(0, str(ROOT / "controls/yaml"))
import check_controls  # noqa: E402


PROJECTS = ("snakeyaml", "snakeyaml_engine", "circe_yaml", "kjson_yaml", "snakeyaml_engine_kmp")
SOURCE_PREFIX = {"snakeyaml": ("org/yaml/snakeyaml/",), "snakeyaml_engine": ("org/snakeyaml/engine/",),
                 # wrapper path: java_dual_trace.py labels circe-yaml lines wrapper/ and SnakeYAML lines core/
                 "circe_yaml": ("wrapper/io/circe/yaml/", "core/org/yaml/snakeyaml/"),
                 "kjson_yaml": ("io/kjson/yaml/",),
                 "snakeyaml_engine_kmp": ("it/krzeminski/snakeyaml/engine/kmp/",)}
WRAPPERS = {"circe_yaml"}
CONTROL = "controls/yaml/catalog.yaml"
DIFFERENTIAL = "controls/yaml/order.yaml"
REPEATS = 3
REPORT = ROOT / "data/java/yaml/afl-feedback.json"


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
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


def probe(manifest: dict, image: str, case: Path, work: Path, name: str, prefix: tuple[str, ...]) -> tuple[set, set]:
    common = sandbox(manifest, case, work)
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "20000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = set((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = {line.split(":", 1)[0] for line in (work / f"{name}.map").read_text().splitlines() if line}
    if not features or not tuples or any(not item.startswith(prefix) for item in features):
        raise RuntimeError("feedback is empty or outside the parser source")
    return features, tuples


def tree(manifest: dict, image: str, case: Path, work: Path) -> dict:
    output = run([*sandbox(manifest, case, work), "--entrypoint", "java", image,
                  "-Dstdout.encoding=UTF-8", "-cp", "/work/classes:/work/lib/*", "GenericHarness",
                  "/input/case"])
    return json.loads(output.strip().splitlines()[-1])


def per_file(features: set) -> Counter:
    return Counter(item.rsplit(":", 1)[0] for item in features)


def check(slug: str) -> dict:
    relative = Path("yaml/java") / slug
    _, manifest = project_for("yaml", "java", slug)
    if manifest["control"] != CONTROL or manifest["differential_control"] != DIFFERENTIAL:
        raise ValueError(f"{relative}: unexpected controls")
    for path, digest in ((CONTROL, manifest["control_sha256"]),
                         (DIFFERENTIAL, manifest["differential_control_sha256"])):
        if sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"{relative}: control hash changed")
    expected = {"tree": check_controls.EXPECTED["catalog.yaml"]}
    differential = {"tree": check_controls.EXPECTED["order.yaml"]}
    if manifest["expected_output"] != expected or manifest["differential_expected_output"] != differential:
        raise RuntimeError(f"{relative}: manifest trees differ from the controls oracle")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    image = receipt["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-yaml-java-") as temporary:
        work = Path(temporary)
        if tree(manifest, image, ROOT / CONTROL, work) != expected:
            raise RuntimeError(f"{relative}: control tree changed")
        if tree(manifest, image, ROOT / DIFFERENTIAL, work) != differential:
            raise RuntimeError(f"{relative}: differential tree changed")
        firsts = [probe(manifest, image, ROOT / CONTROL, work, f"control-{i}", SOURCE_PREFIX[slug]) for i in range(REPEATS)]
        others = [probe(manifest, image, ROOT / DIFFERENTIAL, work, f"variant-{i}", SOURCE_PREFIX[slug]) for i in range(REPEATS)]
    if any(item != firsts[0] for item in firsts) or any(item != others[0] for item in others):
        raise RuntimeError(f"{relative}: repeated probes changed parser features or AFL++ map")
    first, other = firsts[0], others[0]
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len(first[1] ^ other[1])
    if not feature_difference or not tuple_difference:
        raise RuntimeError(f"{relative}: the valid controls give the same parser feedback")
    changed = per_file(first[0] ^ other[0])
    layers = {}
    if slug in WRAPPERS:
        # A wrapper may show no differential in its own lines; the underlying parser must.
        for layer in ("wrapper", "core"):
            mine = {item for item in first[0] if item.startswith(layer + "/")}
            theirs = {item for item in other[0] if item.startswith(layer + "/")}
            layers[f"{layer}_control_features"] = len(mine)
            layers[f"{layer}_feature_difference"] = len(mine ^ theirs)
        if not layers["core_feature_difference"]:
            raise RuntimeError(f"{relative}: the underlying parser shows no differential")
    print(f"{relative}: {REPEATS} identical repeats per control; {feature_difference} parser lines, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)
    return {"project": str(relative), "pass": True,
            "feedback_kind": receipt["feedback_kind"],
            "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
            "control": CONTROL, "control_sha256": manifest["control_sha256"],
            "differential": DIFFERENTIAL, "differential_sha256": manifest["differential_control_sha256"],
            "oracle": "hand-written typed trees in controls/yaml/check_controls.py (cross-checked with Ruby Psych)",
            "control_tree_matches_oracle": True, "differential_tree_matches_oracle": True,
            "runs_per_control": REPEATS,
            "control_repeat_identical": True, "differential_repeat_identical": True,
            "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
            "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
            "parser_feature_difference": feature_difference,
            "afl_tuple_difference": tuple_difference,
            **layers,
            "control_lines_by_file": dict(sorted(per_file(first[0]).items())),
            "differing_lines_by_file": dict(sorted(changed.items()))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", choices=PROJECTS, help="verify one project; keep the other receipts")
    selected = parser.parse_args().project
    now = datetime.now(timezone.utc).isoformat()
    rows = {}
    if selected and REPORT.is_file():
        rows = {row["project"].split("/")[-1]: row for row in json.loads(REPORT.read_text())["results"]}
    for slug in ([selected] if selected else PROJECTS):
        rows[slug] = {**check(slug), "checked_at_utc": now}
    results = [rows[slug] for slug in PROJECTS if slug in rows]
    REPORT.write_text(json.dumps({
        "schema_version": 1, "checked_at_utc": now,
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_block_sequence_root",
        "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
