"""Run a prepared native fuzz campaign, or preflight it with --check.

Only the person invoking this script without --check starts mutation. The run
log and execution receipt are kept in the prepared run directory.
"""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time

from run_case import project_for


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(run_dir: Path, plan: dict) -> None:
    relative = Path(plan["project"])
    project, manifest = project_for(*relative.parts)
    if sha256((project / "verification.json").read_bytes()).hexdigest() != plan["project_receipt_sha256"]:
        raise ValueError("project receipt changed since preparation")
    if manifest["source_sha256"] != plan["source_sha256"]:
        raise ValueError("parser source changed since preparation")
    inspection = subprocess.run(
        ["docker", "image", "inspect", plan["image"], "--format", "{{.Id}}"],
        capture_output=True, text=True)
    if inspection.returncode or inspection.stdout.strip() != plan["image_id"]:
        raise ValueError("local image differs from the prepared image")
    corpus = run_dir / "corpus"
    actual = sorted(path.name for path in corpus.iterdir() if path.is_file())
    expected = sorted(item["name"] for item in plan["corpus_files"])
    if actual != expected:
        raise ValueError("seed corpus file set changed since preparation")
    for item in plan["corpus_files"]:
        data = (corpus / item["name"]).read_bytes()
        if len(data) != item["bytes"] or sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(f"seed corpus changed: {item['name']}")
    if not (run_dir / "artifacts").is_dir():
        raise ValueError("artifact directory missing")
    if relative.parts[1] == "go" and not (run_dir / "go-cache").is_dir():
        raise ValueError("Go fuzz cache directory missing")
    if plan["command"][:5] != ["docker", "run", "--rm", "--name", plan["container_name"]]:
        raise ValueError("prepared command has an unexpected shape")
    if plan["image_id"] not in plan["command"]:
        raise ValueError("prepared command does not use the pinned image")


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("run_dir", type=Path)
    cli.add_argument("--check", action="store_true", help="validate without starting mutation")
    args = cli.parse_args()
    run_dir = args.run_dir.resolve(strict=True)
    plan = json.loads((run_dir / "plan.json").read_text())
    try:
        verify(run_dir, plan)
    except (OSError, ValueError, KeyError) as exc:
        cli.error(str(exc))
    if args.check:
        print(f"Ready: {plan['project']} ({plan['engine']}, {plan['unique_seeds']} seeds)")
        return
    receipt_path = run_dir / "campaign.json"
    if receipt_path.exists():
        cli.error("campaign receipt already exists; use a new run directory")
    log_path = run_dir / "campaign.log"
    started_utc = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    status = "completed"
    exit_code = None
    with log_path.open("wb") as log:
        process = subprocess.Popen(plan["command"], stdout=log, stderr=subprocess.STDOUT)
        try:
            grace = 120 if plan["duration_enforced_by_engine"] else 0
            exit_code = process.wait(timeout=plan["duration_seconds"] + grace)
            if exit_code:
                status = "engine_nonzero"
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
            status = "interrupted" if isinstance(exc, KeyboardInterrupt) else "time_limit"
            subprocess.run(["docker", "rm", "-f", plan["container_name"]],
                           capture_output=True, timeout=10)
            exit_code = process.wait(timeout=15)
    receipt = {"schema_version": 1, "project": plan["project"], "engine": plan["engine"],
               "status": status, "exit_code": exit_code, "started_at_utc": started_utc,
               "finished_at_utc": datetime.now(timezone.utc).isoformat(),
               "elapsed_seconds": round(time.monotonic() - started, 3),
               "image_id": plan["image_id"], "plan_sha256": sha256((run_dir / "plan.json").read_bytes()).hexdigest(),
               "log_sha256": file_sha256(log_path)}
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"{status}: {plan['project']} ({receipt['elapsed_seconds']}s); log: {log_path}")
    if status == "engine_nonzero":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
