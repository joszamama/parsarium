"""Validate and run a prepared AFL++ campaign for a bounded duration."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid

from prepare_afl_run import commands_for
from run_case import MAX_CASE_BYTES, ROOT, project_for


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(run_dir: Path, plan: dict) -> None:
    relative = Path(plan["project"])
    if len(relative.parts) != 3:
        raise ValueError("invalid project path in plan")
    project, manifest = project_for(*relative.parts)
    receipt_path = ROOT / "fuzzing/afl-native" / relative / "verification.json"
    receipt = json.loads(receipt_path.read_text())
    if sha256(receipt_path.read_bytes()).hexdigest() != plan["overlay_receipt_sha256"]:
        raise ValueError("AFL++ overlay receipt changed since preparation")
    if receipt["base_project_receipt_sha256"] != sha256(
        (project / "verification.json").read_bytes()
    ).hexdigest():
        raise ValueError("project receipt changed since AFL++ overlay verification")
    if manifest["source_sha256"] != plan["source_sha256"] or (
        manifest["control_sha256"] != plan["control_sha256"]
    ):
        raise ValueError("parser or control changed since preparation")
    image = subprocess.run(["docker", "image", "inspect", plan["image_id"],
                            "--format", "{{.Id}}"], capture_output=True, text=True)
    if image.returncode or image.stdout.strip() != receipt["image_id"]:
        raise ValueError("verified AFL++ image is unavailable")
    seeds = run_dir / "seeds"
    output = run_dir / "afl-out"
    if not seeds.is_dir() or not output.is_dir() or not output.is_relative_to(run_dir):
        raise ValueError("seed or output directory missing")
    actual = {path.name for path in seeds.iterdir() if path.is_file()}
    expected = {item["sha256"] for item in plan["seed_sources"]}
    if actual != expected or len(actual) != plan["unique_seeds"]:
        raise ValueError("seed file set changed since preparation")
    for name in actual:
        data = (seeds / name).read_bytes()
        if not data or len(data) > MAX_CASE_BYTES or sha256(data).hexdigest() != name:
            raise ValueError(f"seed changed since preparation: {name}")
    command, resume = commands_for(manifest, receipt, seeds, output,
                                   plan["timeout_ms"], plan["container_name"])
    if plan["command"] != command or plan["resume_command"] != resume:
        raise ValueError("AFL++ command changed since preparation")
    if plan["output_directory"] != str(output):
        raise ValueError("run directory moved since preparation")


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("run_dir", type=Path)
    cli.add_argument("--seconds", type=int, default=3600,
                     help="AFL++ time budget; default 3600")
    cli.add_argument("--check", action="store_true", help="validate without starting AFL++")
    cli.add_argument("--resume", action="store_true", help="resume an existing AFL++ output directory")
    args = cli.parse_args()
    if args.seconds < 1:
        cli.error("--seconds must be positive")
    run_dir = args.run_dir.resolve(strict=True)
    plan_path = run_dir / "plan.json"
    try:
        plan = json.loads(plan_path.read_text())
        verify(run_dir, plan)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        cli.error(str(error))
    if args.check:
        print(f"Ready: {plan['project']} ({plan['unique_seeds']} seeds, {plan['feedback_kind']})")
        return
    if args.resume:
        if not any((run_dir / "afl-out").iterdir()):
            cli.error("AFL++ output is empty; start without --resume")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
        receipt_path = run_dir / f"campaign-resume-{stamp}.json"
        log_path = run_dir / f"campaign-resume-{stamp}.log"
        command = list(plan["resume_command"])
    else:
        receipt_path = run_dir / "campaign.json"
        log_path = run_dir / "campaign.log"
        if receipt_path.exists() or any((run_dir / "afl-out").iterdir()):
            cli.error("AFL++ output already exists; use --resume")
        command = list(plan["command"])
    command[command.index("--"):command.index("--")] = ["-V", str(args.seconds)]
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    status = "completed"
    with log_path.open("wb") as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        try:
            exit_code = process.wait(timeout=args.seconds + 120)
            if exit_code:
                status = "engine_nonzero"
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            status = "interrupted" if isinstance(error, KeyboardInterrupt) else "time_limit"
            subprocess.run(["docker", "rm", "-f", plan["container_name"]],
                           capture_output=True, timeout=15)
            exit_code = process.wait(timeout=15)
    summary_command = subprocess.run(
        [sys.executable, str(ROOT / "scripts/summarize_afl_run.py"), str(run_dir)],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )
    if summary_command.returncode and status == "completed":
        status = "missing_statistics"
    receipt = {"schema_version": 1, "project": plan["project"],
               "status": status, "exit_code": exit_code,
               "started_at_utc": started_at,
               "finished_at_utc": datetime.now(timezone.utc).isoformat(),
               "elapsed_seconds": round(time.monotonic() - started, 3),
               "duration_seconds": args.seconds, "resumed": args.resume,
               "image_id": plan["image_id"],
               "plan_sha256": sha256(plan_path.read_bytes()).hexdigest(),
               "log_sha256": file_sha256(log_path),
               "summary": "afl-summary.json" if summary_command.returncode == 0 else None}
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"{status}: {plan['project']} ({receipt['elapsed_seconds']}s)")
    if summary_command.returncode == 0:
        print(summary_command.stdout, end="")
    else:
        print(summary_command.stderr, file=sys.stderr, end="")
    if status in {"engine_nonzero", "missing_statistics"}:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
