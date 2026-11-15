"""Build and verify selected project harnesses, then refresh the coverage audit."""

import argparse
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
    args = cli.parse_args()

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
    for project in selected:
        print("/".join(project), flush=True)
        if args.dry_run:
            continue
        result = subprocess.run([sys.executable, str(ROOT / "scripts/run_project.py"), *project],
                                cwd=ROOT, check=False)
        if result.returncode:
            failures.append(project)
            if not args.keep_going:
                break
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
