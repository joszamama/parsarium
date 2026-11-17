"""Reverify managed harnesses whose AFL++ bridge source hash has changed."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from build_afl_bridge import build_one as build_bridge
from build_afl_python import build_one as build_python
from run_case import ROOT


def pending_paths() -> list[Path]:
    stale = []
    for receipt_path in sorted((ROOT / "fuzzing/afl-native").glob("*/*/*/verification.json")):
        relative = receipt_path.parent.relative_to(ROOT / "fuzzing/afl-native")
        manifest_path = ROOT / "projects" / relative / "manifest.json"
        if not manifest_path.is_file():
            continue
        manifest = json.loads(manifest_path.read_text())
        if manifest["ecosystem"] not in {"python", "go", "java", "javascript", "php"}:
            continue
        receipt = json.loads(receipt_path.read_text())
        for name, digest in receipt.get("bridge_file_sha256", {}).items():
            file = ROOT / "fuzzing/afl-bridge" / name
            if not file.is_file() or sha256(file.read_bytes()).hexdigest() != digest:
                stale.append(relative)
                break
    return stale


def run(*args: str) -> None:
    process = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if process.returncode:
        raise RuntimeError((process.stdout + process.stderr)[-2000:])
    if process.stdout.strip():
        print(process.stdout.strip().splitlines()[-1], flush=True)


def repair(relative: Path) -> str:
    project = ROOT / "projects" / relative
    manifest = json.loads((project / "manifest.json").read_text())
    base_receipt = json.loads((project / "verification.json").read_text())
    tag = f"parsarium/{manifest['format']}-{manifest['ecosystem']}-{relative.name}:local"
    inspection = subprocess.run(["docker", "image", "inspect", tag, "--format", "{{.Id}}"],
                                text=True, capture_output=True)
    if inspection.returncode or inspection.stdout.strip() != base_receipt["image_id"]:
        run(sys.executable, str(ROOT / "scripts/run_project.py"), *relative.parts)
    (build_python if manifest["ecosystem"] == "python" else build_bridge)(relative)
    return str(relative)


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--apply", action="store_true")
    cli.add_argument("--workers", type=int, default=2)
    cli.add_argument("--limit", type=int, default=0, help="maximum number to refresh this run")
    args = cli.parse_args()
    if not 1 <= args.workers <= 4 or args.limit < 0:
        cli.error("workers must be 1..4 and limit must be nonnegative")
    paths = pending_paths()
    if args.limit:
        paths = paths[:args.limit]
    print(f"{len(paths)} stale managed AFL++ bridge receipts selected", flush=True)
    if not args.apply or not paths:
        return
    repaired = []
    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(repair, path): path for path in paths}
        for future in as_completed(futures):
            relative = futures[future]
            try:
                repaired.append(future.result())
            except Exception as error:
                failures.append((str(relative), str(error)))
                print(f"FAILED {relative}: {error}", flush=True)
    if repaired:
        run(sys.executable, str(ROOT / "scripts/refresh_smoke_batch.py"),
            *sorted(repaired), "--workers", str(args.workers))
        run(sys.executable, str(ROOT / "scripts/audit_projects.py"), "--write")
        run(sys.executable, str(ROOT / "scripts/build_readmes.py"))
    if failures:
        raise SystemExit(f"{len(failures)} bridge refreshes failed")


if __name__ == "__main__":
    main()
