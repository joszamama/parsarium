"""Build and verify selected project harnesses, then refresh the coverage audit."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("--format")
    cli.add_argument("--ecosystem")
    cli.add_argument("--package-slug")
    cli.add_argument("--dry-run", action="store_true")
    cli.add_argument("--keep-going", action="store_true")
    cli.add_argument("--workers", type=int, default=1,
                     help="independent Docker builds to run concurrently (1-8; requires --keep-going)")
    args = cli.parse_args()
    if not 1 <= args.workers <= 8:
        cli.error("--workers must be between 1 and 8")
    if args.workers > 1 and not args.keep_going:
        cli.error("--workers > 1 requires --keep-going")

    selected = []
    for path in sorted((ROOT / "projects").glob("*/*/*/manifest.json")):
        format_name, ecosystem, package_slug = path.relative_to(ROOT / "projects").parts[:3]
        if ((args.format and format_name != args.format)
                or (args.ecosystem and ecosystem != args.ecosystem)
                or (args.package_slug and package_slug != args.package_slug)):
            continue
        selected.append((format_name, ecosystem, package_slug))
    if not selected:
        cli.error("no project manifests match the requested filters")

    failures = []
    if args.dry_run:
        for project in selected:
            print("/".join(project), flush=True)
    elif args.workers == 1:
        for project in selected:
            print("/".join(project), flush=True)
            result = subprocess.run([sys.executable, str(ROOT / "scripts/run_project.py"), *project],
                                    cwd=ROOT, check=False)
            if result.returncode:
                failures.append(project)
                if not args.keep_going:
                    break
    else:
        def run(project):
            result = subprocess.run([sys.executable, str(ROOT / "scripts/run_project.py"), *project],
                                    cwd=ROOT, capture_output=True, text=True, errors="replace")
            return result.returncode, result.stdout, result.stderr

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(run, project): project for project in selected}
            for future in as_completed(futures):
                project = futures[future]
                code, stdout, stderr = future.result()
                print(f"{'/'.join(project)}: {'verified' if code == 0 else 'FAILED'}", flush=True)
                if code:
                    failures.append(project)
                    print((stdout + stderr)[-4000:], file=sys.stderr, flush=True)
    if args.dry_run:
        print(f"{len(selected)} project(s) selected")
        return
    if failures:
        names = ", ".join("/".join(project) for project in failures)
        raise SystemExit(f"{len(failures)} project(s) failed: {names}")
    subprocess.run([sys.executable, str(ROOT / "scripts/audit_projects.py"), "--write"],
                   cwd=ROOT, check=True)
    print(f"{len(selected)} project(s) verified")


if __name__ == "__main__":
    main()
