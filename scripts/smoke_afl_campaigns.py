"""Run brief AFL++ campaigns for one bridge in each managed ecosystem."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT


PILOTS = (
    ("ascii_ply", "go", "polyform_ply"),
    ("png", "java", "commons_imaging"),
    ("ascii_pnm", "javascript", "image_size"),
    ("ascii_ply", "python", "plyfile"),
    ("svg", "php", "php_svg_lib"),
)


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--project", help="rerun one format/ecosystem/slug pilot")
    args = cli.parse_args()
    report_path = ROOT / "data/afl-campaign-smoke.json"
    previous = (json.loads(report_path.read_text())["results"] if args.project else [])
    results = {item["project"]: item for item in previous}
    for format_name, ecosystem, slug in PILOTS:
        project = f"{format_name}/{ecosystem}/{slug}"
        if args.project and project != args.project:
            continue
        with tempfile.TemporaryDirectory(prefix=f"parsarium-afl-{ecosystem}-") as temporary:
            run_dir = Path(temporary) / "run"
            prepare = subprocess.run(
                [sys.executable, str(ROOT / "scripts/prepare_afl_run.py"),
                 format_name, ecosystem, slug, str(run_dir)],
                cwd=ROOT, capture_output=True, text=True, timeout=60,
            )
            if prepare.returncode:
                raise RuntimeError(f"{project}: {prepare.stderr[-1000:]}")
            plan = json.loads((run_dir / "plan.json").read_text())
            command = list(plan["command"])
            command[command.index("--"):command.index("--")] = ["-V", "5"]
            campaign = subprocess.run(command, cwd=ROOT, capture_output=True,
                                      text=True, timeout=90)
            if campaign.returncode:
                raise RuntimeError(f"{project}: {(campaign.stdout + campaign.stderr)[-2000:]}")
            summarize = subprocess.run(
                [sys.executable, str(ROOT / "scripts/summarize_afl_run.py"), str(run_dir)],
                cwd=ROOT, capture_output=True, text=True, timeout=30,
            )
            if summarize.returncode:
                raise RuntimeError(f"{project}: {summarize.stderr[-1000:]}")
            summary = json.loads((run_dir / "afl-summary.json").read_text())
            instance = summary["instances"][0]
            stats = instance["fuzzer_stats"]
            executions = int(stats["execs_done"])
            edges = int(stats["edges_found"])
            if executions < 1 or edges < 1 or not instance["queue"]:
                raise RuntimeError(f"{project}: no AFL++ executions, feedback, or queue")
            receipt = ROOT / "fuzzing/afl-native" / project / "verification.json"
            record = {
                "project": project, "pass": True, "image_id": plan["image_id"],
                "overlay_receipt_sha256": sha256(receipt.read_bytes()).hexdigest(),
                "control_sha256": plan["control_sha256"],
                "afl_version": stats["afl_version"],
                "executions": executions, "edges_found": edges,
                "queue_items": len(instance["queue"]),
                "saved_crashes": len(instance["crashes"]),
                "saved_hangs": len(instance["hangs"]),
                "run_time_seconds": int(stats["run_time"]),
            }
            results[project] = record
            print(f"{project}: {executions} executions, {edges} edges", flush=True)
    if args.project and args.project not in results:
        raise ValueError(f"unknown pilot: {args.project}")
    ordered = [results[f"{fmt}/{eco}/{slug}"] for fmt, eco, slug in PILOTS]
    report = {"schema_version": 1,
              "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "projects_total": len(ordered), "projects_passed": sum(x["pass"] for x in ordered),
              "results": ordered}
    report_path.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
