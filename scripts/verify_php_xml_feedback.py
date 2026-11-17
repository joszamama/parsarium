"""Check PHP XML AFL++ feedback: three control probes match and the second valid control differs.

Native overlays are probed through the instrumented PHP runtime; parser-line bridges also compare the
package source-line features that the bridge maps into the AFL++ bitmap. Named slugs refresh only
their rows of the report."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for


PROJECTS = ("stdlib_xmlreader", "stdlib_domdocument", "stdlib_simplexml", "stdlib_xml_parser", "sabre_xml", "symfony_dom_crawler", "symfony_serializer", "veewee_xml", "mtownsend_xml_to_array")
CONTROL = "controls/xml/catalog-ns.xml"
DIFFERENTIAL = "controls/xml/order-default-ns.xml"
REPORT = ROOT / "data/php/xml/afl-feedback.json"
REPEATS = 3


def run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])


def probe(manifest: dict, image: str, case: Path, work: Path, name: str,
          bridge: bool) -> tuple[frozenset, frozenset]:
    common = ["docker", "run", "--rm", "--platform", manifest["platform"],
              "--network", "none", "--read-only", "--cap-drop", "ALL",
              "--security-opt", "no-new-privileges",
              "--user", f"{os.getuid()}:{os.getgid()}",
              "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
              "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]
    features = frozenset()
    if bridge:
        run([*common, "--entrypoint", "/bin/sh", image,
             "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
        features = frozenset(set((work / f"{name}.features").read_text().splitlines()) - {""})
        target = ["/work/afl_proxy", "/input/case"]
    else:
        target = ["/opt/php/bin/php", "/work/fuzz-target.php", "/input/case"]
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap", image,
         "-m", "none", "-t", "30000", "-o", f"/coverage/{name}.map", "--", *target])
    return features, frozenset(set((work / f"{name}.map").read_text().splitlines()) - {""})


def check(slug: str) -> dict:
    relative = Path("xml/php") / slug
    _, manifest = project_for("xml", "php", slug)
    if manifest["control"] != CONTROL:
        raise ValueError(f"{relative}: unexpected control")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    image = receipt["image_id"]
    bridge = (overlay / "afl_trace").is_file()
    with tempfile.TemporaryDirectory(prefix="parsarium-xml-php-") as temporary:
        work = Path(temporary)
        controls = [probe(manifest, image, ROOT / CONTROL, work, f"control{i}", bridge) for i in range(REPEATS)]
        others = [probe(manifest, image, ROOT / DIFFERENTIAL, work, f"other{i}", bridge) for i in range(REPEATS)]
    if len(set(controls)) != 1 or len(set(others)) != 1:
        raise RuntimeError(f"{relative}: repeated control probes changed the AFL++ map")
    (first_features, first), (other_features, other) = controls[0], others[0]
    if len(first) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    if bridge and len(first_features) != receipt["parser_source_features"]:
        raise RuntimeError(f"{relative}: control features differ from overlay receipt")
    prefix = manifest.get("afl_coverage_subject_prefix", manifest["coverage_subject_prefix"])
    if any(not item.startswith(prefix) for item in first_features | other_features):
        raise RuntimeError(f"{relative}: bridge feature outside the package source prefix")
    first_edges = {item.split(":", 1)[0] for item in first}
    other_edges = {item.split(":", 1)[0] for item in other}
    if (bridge and not first_features ^ other_features) or not first_edges ^ other_edges:
        raise RuntimeError(f"{relative}: differential input did not change parser feedback")
    features = f"{len(first_features ^ other_features)} package source lines, " if bridge else ""
    print(f"{relative}: {REPEATS} identical probes per control; "
          f"{features}{len(first_edges ^ other_edges)} AFL++ edges differ", flush=True)
    bridge_fields = {
        "control_parser_features": len(first_features),
        "differential_parser_features": len(other_features),
        "control_only_parser_features": sorted(item.removeprefix(prefix) for item in first_features - other_features),
        "differential_only_parser_features": sorted(item.removeprefix(prefix) for item in other_features - first_features),
    } if bridge else {}
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
            "afl_tuple_difference": len(first_edges ^ other_edges),
            **bridge_fields}


def main() -> None:
    slugs = sys.argv[1:] or list(PROJECTS)
    if not set(slugs) <= set(PROJECTS):
        raise SystemExit(f"unknown PHP XML project: {sorted(set(slugs) - set(PROJECTS))}")
    fresh = {f"xml/php/{slug}": check(slug) for slug in slugs}
    kept = json.loads(REPORT.read_text())["results"] if REPORT.is_file() else []
    rows = {item["project"]: item for item in kept} | fresh
    results = [rows[f"xml/php/{slug}"] for slug in PROJECTS if f"xml/php/{slug}" in rows]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_default_namespace_order",
        "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
