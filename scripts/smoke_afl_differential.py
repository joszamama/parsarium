"""Check that parser-source differences reach AFL++ in each bridge family."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


PILOTS = (
    ("ascii_ply", "go", "polyform_ply", "controls/ascii_ply/triangle.ply",
     "controls/ascii_ply/triangle-colour.ply"),
    ("png", "java", "commons_imaging", "controls/png/red-green.png", None),
    ("pdf", "javascript", "pdf_lib", "controls/pdf/one-page.pdf",
     "controls/pdf/two-page.pdf"),
    ("ascii_ply", "python", "plyfile", "controls/ascii_ply/triangle.ply",
     "controls/ascii_ply/triangle-colour.ply"),
    ("svg", "php", "php_svg_lib", "controls/svg/red-green.svg", None),
)


def run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, timeout=90)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--project", help="rerun one format/ecosystem/slug pilot")
    args = cli.parse_args()
    report_path = ROOT / "data/afl-feedback-differential.json"
    previous = (json.loads(report_path.read_text())["results"] if args.project else [])
    results = {item["project"]: item for item in previous}
    for format_name, ecosystem, slug, first, second in PILOTS:
        relative = Path(format_name) / ecosystem / slug
        if args.project and str(relative) != args.project:
            continue
        _, manifest = project_for(format_name, ecosystem, slug)
        overlay = ROOT / "fuzzing/afl-native" / relative
        receipt = json.loads((overlay / "verification.json").read_text())
        image = receipt["image_id"]
        with tempfile.TemporaryDirectory(prefix="parsarium-afl-diff-") as temporary:
            work = Path(temporary)
            cases = [ROOT / first]
            if second is None:
                comparison = work / f"truncated.{format_name}"
                comparison.write_bytes(b"<svg" if format_name == "svg" else b"\x89PNG")
                cases.append(comparison)
            else:
                cases.append(ROOT / second)
            features = []
            maps = []
            for index, case in enumerate(cases):
                common = ["docker", "run", "--rm", "--platform", manifest["platform"],
                          "--network", "none", "--read-only", "--cap-drop", "ALL",
                          "--security-opt", "no-new-privileges",
                          "--user", f"{os.getuid()}:{os.getgid()}",
                          "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
                          "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]
                feature_path = work / f"{index}.features"
                run([*common, "--entrypoint", "/bin/sh", image,
                     "/work/afl_trace", "/input/case", f"/coverage/{index}.features"])
                features.append(set(feature_path.read_text().splitlines()) - {""})
                run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
                     image, "-m", "none", "-t", "10000", "-o", f"/coverage/{index}.map",
                     "--", "/work/afl_proxy", "/input/case"])
                maps.append(set(line.split(":", 1)[0] for line in
                                (work / f"{index}.map").read_text().splitlines()))
            feature_difference = len(features[0] ^ features[1])
            map_difference = len(maps[0] ^ maps[1])
            if not feature_difference or not map_difference:
                raise RuntimeError(f"{relative}: parser source or AFL++ map did not differ")
            record = {
                "project": str(relative), "pass": True,
                "feedback_kind": receipt["feedback_kind"],
                "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
                "first_sha256": sha256(cases[0].read_bytes()).hexdigest(),
                "second_sha256": sha256(cases[1].read_bytes()).hexdigest(),
                "first_parser_features": len(features[0]),
                "second_parser_features": len(features[1]),
                "parser_feature_difference": feature_difference,
                "first_afl_tuples": len(maps[0]),
                "second_afl_tuples": len(maps[1]),
                "afl_tuple_difference": map_difference,
                "second_case_kind": "truncated_input" if second is None else "valid_control",
            }
            results[str(relative)] = record
            print(f"{relative}: {feature_difference} parser features, "
                  f"{map_difference} AFL++ tuples differ", flush=True)
    if args.project and args.project not in results:
        raise ValueError(f"unknown pilot: {args.project}")
    ordered = [results[f"{fmt}/{eco}/{slug}"] for fmt, eco, slug, _, _ in PILOTS]
    report = {"schema_version": 1,
              "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "projects_total": len(ordered), "projects_passed": len(ordered),
              "results": ordered}
    report_path.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
