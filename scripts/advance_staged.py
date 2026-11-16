"""Advance current base receipts through AFL++ and case smoke verification.

Run after a base build batch. Docker compilation is bounded separately by
docker_slots.py, so independent invocations share the same local build limit.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from run_case import ROOT, project_for


BUILDERS = {
    "c": "build_afl_native.py", "cpp": "build_afl_native.py",
    "go": "build_afl_bridge.py", "java": "build_afl_bridge.py",
    "javascript": "build_afl_bridge.py", "php": "build_afl_bridge.py",
    "python": "build_afl_python.py", "rust": "build_afl_rust.py",
}


def base_ready(relative: Path) -> bool:
    try:
        project, _ = project_for(*relative.parts)
        return json.loads((project / "verification.json").read_text()).get("pass") is True
    except (OSError, KeyError, ValueError, AssertionError):
        return False


def overlay_ready(relative: Path) -> bool:
    project = ROOT / "projects" / relative
    receipt = ROOT / "fuzzing/afl-native" / relative / "verification.json"
    if not receipt.is_file():
        return False
    try:
        record = json.loads(receipt.read_text())
        return (record.get("pass") is True and
                record["base_project_receipt_sha256"] ==
                sha256((project / "verification.json").read_bytes()).hexdigest())
    except (OSError, KeyError, ValueError):
        return False


def build_one(relative: Path) -> tuple[str, bool, str]:
    script = BUILDERS[relative.parts[1]]
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script),
                             *relative.parts], cwd=ROOT, capture_output=True,
                            text=True, errors="replace")
    return str(relative), result.returncode == 0, (result.stdout + result.stderr)[-2000:]


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--ecosystem", action="append", choices=sorted(BUILDERS),
                     help="repeat to select multiple ecosystems; default is all")
    cli.add_argument("--workers", type=int, default=3)
    cli.add_argument("--no-smoke", action="store_true")
    args = cli.parse_args()
    if not 1 <= args.workers <= 8:
        cli.error("workers must be between 1 and 8")
    ecosystems = set(args.ecosystem or BUILDERS)
    paths = sorted(path.parent.relative_to(ROOT / "projects")
                   for path in (ROOT / "projects").glob("*/*/*/manifest.json")
                   if path.parent.parent.name in ecosystems)
    candidates = [relative for relative in paths if base_ready(relative)]
    to_build = [relative for relative in candidates if not overlay_ready(relative)]
    print(f"Base ready: {len(candidates)}; AFL++ builds: {len(to_build)}", flush=True)
    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        tasks = {pool.submit(build_one, relative): relative for relative in to_build}
        for future in as_completed(tasks):
            relative, passed, output = future.result()
            print(f"{'PASS' if passed else 'FAIL'} {relative}: {output[-180:]}", flush=True)
            if not passed:
                failures.append(relative)
    ready = [relative for relative in candidates if overlay_ready(relative)]
    checked = {item["project"]: item for item in json.loads(
        (ROOT / "data/fuzz-case-smoke.json").read_text())["results"]
               if item["status"] == "ok"}
    afl_checked = {item["project"]: item for item in json.loads(
        (ROOT / "data/afl-plan-smoke.json").read_text())["results"]
                   if item["status"] == "ready"}
    to_smoke = []
    for relative in ready:
        name = str(relative)
        project = ROOT / "projects" / relative
        overlay = ROOT / "fuzzing/afl-native" / relative / "verification.json"
        base_sha = sha256((project / "verification.json").read_bytes()).hexdigest()
        overlay_sha = sha256(overlay.read_bytes()).hexdigest()
        if (checked.get(name, {}).get("project_receipt_sha256") != base_sha
                or afl_checked.get(name, {}).get("overlay_receipt_sha256") != overlay_sha):
            to_smoke.append(name)
    print(f"AFL++ ready: {len(ready)}; smoke checks: {len(to_smoke)}", flush=True)
    if to_smoke and not args.no_smoke:
        smoke = subprocess.run([sys.executable, str(ROOT / "scripts/refresh_smoke_batch.py"),
                                "--workers", str(args.workers), *to_smoke], cwd=ROOT)
        if smoke.returncode:
            raise SystemExit(smoke.returncode)
    if failures:
        raise SystemExit(f"{len(failures)} AFL++ builds failed: {failures}")


if __name__ == "__main__":
    main()
