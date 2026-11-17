"""Check PHP XML AFL++ feedback: three control probes match and the second valid control differs."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


PROJECTS = ("stdlib_xmlreader", "sabre_xml")
CONTROL = "controls/xml/catalog-ns.xml"
DIFFERENTIAL = "controls/xml/order-default-ns.xml"
REPORT = ROOT / "data/php/xml/afl-feedback.json"
REPEATS = 3


def run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> frozenset:
    run(["docker", "run", "--rm", "--platform", manifest["platform"],
         "--network", "none", "--read-only", "--cap-drop", "ALL",
         "--security-opt", "no-new-privileges",
         "--user", f"{os.getuid()}:{os.getgid()}",
         "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
         "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage",
         "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap", image,
         "-m", "none", "-t", "30000", "-o", f"/coverage/{name}.map", "--",
         "/opt/php/bin/php", "/work/fuzz-target.php", "/input/case"])
    return frozenset(set((work / f"{name}.map").read_text().splitlines()) - {""})


def check(slug: str) -> dict:
    relative = Path("xml/php") / slug
    _, manifest = project_for("xml", "php", slug)
    if manifest["control"] != CONTROL:
        raise ValueError(f"{relative}: unexpected control")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    image = receipt["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-xml-php-") as temporary:
        work = Path(temporary)
        controls = [probe(manifest, image, ROOT / CONTROL, work, f"control{i}") for i in range(REPEATS)]
        others = [probe(manifest, image, ROOT / DIFFERENTIAL, work, f"other{i}") for i in range(REPEATS)]
    if len(set(controls)) != 1 or len(set(others)) != 1:
        raise RuntimeError(f"{relative}: repeated control probes changed the AFL++ map")
    first, other = controls[0], others[0]
    if len(first) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    first_edges = {item.split(":", 1)[0] for item in first}
    other_edges = {item.split(":", 1)[0] for item in other}
    if not first_edges ^ other_edges:
        raise RuntimeError(f"{relative}: differential input did not change parser feedback")
    print(f"{relative}: {REPEATS} identical probes per control; "
          f"{len(first_edges ^ other_edges)} AFL++ edges differ", flush=True)
    return {"project": str(relative), "pass": True,
            "feedback_kind": receipt["feedback_kind"],
            "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
            "control": CONTROL,
            "control_sha256": sha256((ROOT / CONTROL).read_bytes()).hexdigest(),
            "differential": DIFFERENTIAL,
            "differential_sha256": sha256((ROOT / DIFFERENTIAL).read_bytes()).hexdigest(),
            "repeats_per_control": REPEATS,
            "repeated_control_identical": True,
            "control_afl_tuples": len(first),
            "differential_afl_tuples": len(other),
            "stable_shared_edges": len(first_edges & other_edges),
            "control_only_edges": len(first_edges - other_edges),
            "differential_only_edges": len(other_edges - first_edges),
            "afl_tuple_difference": len(first_edges ^ other_edges)}


def main() -> None:
    results = [check(slug) for slug in PROJECTS]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_default_namespace_order",
        "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
