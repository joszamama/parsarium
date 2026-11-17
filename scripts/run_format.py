"""Replay one format across its verified Docker harnesses."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from audit_projects import ROOT, fully_runnable


def targets(format_name: str, ecosystem: str | None) -> list[tuple[Path, dict]]:
    selected = []
    for path in sorted((ROOT / "projects" / format_name).glob("*/*/manifest.json")):
        manifest = json.loads(path.read_text())
        if ecosystem and manifest["ecosystem"] != ecosystem:
            continue
        if fully_runnable(path, manifest):
            selected.append((path, manifest))
    return selected


def run_one(path: Path, manifest: dict, shared_file: Path | None,
            results: Path, timeout: int) -> dict:
    ecosystem, slug = path.parent.parent.name, path.parent.name
    input_file = shared_file or ROOT / manifest["control"]
    destination = results / ecosystem / slug
    command = [sys.executable, str(ROOT / "scripts/run_case.py"),
               manifest["format"], ecosystem, slug, str(input_file),
               "--timeout", str(timeout), "--results", str(destination)]
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    except OSError as exc:
        return {"project": f"{manifest['format']}/{ecosystem}/{slug}",
                "package": manifest["package"], "input": str(input_file),
                "status": "infrastructure_error", "receipt_dir": str(destination.relative_to(results)),
                "detail": str(exc)}
    try:
        receipt = json.loads(result.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        receipt = {"status": "infrastructure_error", "detail": result.stderr[-1000:] or
                   "the target did not emit a JSON receipt"}
    return {"project": f"{manifest['format']}/{ecosystem}/{slug}",
            "package": manifest["package"], "input": str(input_file),
            "status": receipt["status"], "receipt_dir": str(destination.relative_to(results)),
            **({"detail": receipt["detail"]} if receipt.get("detail") else {})}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("format")
    parser.add_argument("--ecosystem")
    parser.add_argument("--file", type=Path, help="send the same file to every target; otherwise use each target's pinned control")
    parser.add_argument("--results", type=Path, help="directory for one receipt per target and summary.json")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--limit", type=int, help="run only the first N targets")
    parser.add_argument("--list", action="store_true", help="show the selected targets without starting Docker")
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 8 or args.timeout < 1 or (args.limit is not None and args.limit < 1):
        parser.error("workers must be 1–8; timeout and limit must be positive")
    if args.file and not args.file.is_file():
        parser.error("--file must name a regular file")
    selected = targets(args.format, args.ecosystem)
    if args.limit:
        selected = selected[:args.limit]
    if not selected:
        parser.error("no fully verified harnesses match this format and ecosystem")
    if args.list:
        print(f"{len(selected)} verified Docker targets for {args.format}")
        for path, manifest in selected:
            print(f"{manifest['ecosystem']}/{path.parent.name}: {manifest['package']} "
                  f"({manifest.get('release', manifest.get('runtime'))})")
        return 0
    if args.results is None:
        parser.error("--results DIR is required when running targets")
    results = args.results.resolve()
    results.mkdir(parents=True, exist_ok=True)
    shared_file = args.file.resolve() if args.file else None
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run_one, path, manifest, shared_file, results, args.timeout): path
                   for path, manifest in selected}
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(f"{row['status']}: {row['project']}", flush=True)
    rows.sort(key=lambda row: row["project"])
    counts = dict(sorted(Counter(row["status"] for row in rows).items()))
    summary = {"schema_version": 1, "format": args.format, "ecosystem": args.ecosystem,
               "mode": "shared_file" if shared_file else "pinned_controls",
               "input": str(shared_file) if shared_file else None,
               "checked_at_utc": datetime.now(timezone.utc).isoformat(),
               "targets": len(rows), "status_counts": counts, "results": rows}
    with tempfile.NamedTemporaryFile(mode="w", dir=results, delete=False) as handle:
        handle.write(json.dumps(summary, indent=2) + "\n")
        temporary = Path(handle.name)
    temporary.replace(results / "summary.json")
    print(f"Saved {results / 'summary.json'}")
    return 0 if counts == {"ok": len(rows)} else 1


if __name__ == "__main__":
    sys.exit(main())
