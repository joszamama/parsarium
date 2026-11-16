"""Build and replay the pinned PyQt6 SVG Docker control without a feedback claim."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.docker_slots import docker_build_slot  # noqa: E402

MANIFEST = json.loads((PROJECT / "manifest.json").read_text())
IMAGE = "parsarium/svg-python-pyqt6:local"
MODULE = "/opt/venv/lib/python3.14/site-packages/PyQt6/Qt6/lib/libQt6Svg.so.6"


def command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, errors="replace", capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)} failed: {result.stderr[-1500:]}")
    return result.stdout.strip()


def build_image() -> None:
    with docker_build_slot():
        command(["docker", "build", "--quiet", "--platform", MANIFEST["platform"],
                 "-t", IMAGE, str(PROJECT)])


def run_file(path: Path) -> dict:
    path = path.resolve(strict=True)
    output = command(["docker", "run", "--rm", "--platform", MANIFEST["platform"],
                      "--network", "none", "--read-only", "--cap-drop", "ALL",
                      "--security-opt", "no-new-privileges",
                      "--user", f"{os.getuid()}:{os.getgid()}",
                      "--tmpfs", "/tmp:rw,nosuid,size=64m", "-e", "XDG_CACHE_HOME=/tmp",
                      "-v", f"{path}:/input/case.svg:ro",
                      "--entrypoint", "/opt/venv/bin/python", IMAGE,
                      "/work/adapter.py", "/input/case.svg"])
    return json.loads(output)


def verify() -> None:
    control = ROOT / MANIFEST["control"]
    variant = ROOT / MANIFEST["control_variant"]
    if (sha256(control.read_bytes()).hexdigest() != MANIFEST["control_sha256"]
            or sha256(variant.read_bytes()).hexdigest() != MANIFEST["control_variant_sha256"]):
        raise RuntimeError("valid control hash changed")
    build_image()
    output = run_file(control)
    if output != MANIFEST["expected_output"]:
        raise RuntimeError(f"control output mismatch: {output}")
    variant_output = run_file(variant)
    expected_variant = {"size": [4, 2], "red": [255, 0, 0, 255],
                        "green": [255, 0, 0, 255]}
    if variant_output != expected_variant:
        raise RuntimeError(f"variant output mismatch: {variant_output}")

    coverage = PROJECT / "target" / "control-coverage"
    if coverage.exists():
        shutil.rmtree(coverage)
    coverage.mkdir(parents=True)
    command(["docker", "run", "--rm", "--platform", MANIFEST["platform"],
             "--network", "none", "--read-only", "--cap-drop", "ALL",
             "--security-opt", "no-new-privileges",
             "--user", f"{os.getuid()}:{os.getgid()}",
             "--tmpfs", "/tmp:rw,nosuid,size=64m", "-e", "XDG_CACHE_HOME=/tmp",
             "-v", f"{control}:/input/control:ro", "-v", f"{coverage}:/coverage",
             IMAGE])
    summary = json.loads((coverage / "summary.json").read_text())
    if not summary.get("control_pass") or summary.get("output") != output:
        raise RuntimeError("container control summary did not match")
    module_hash = command(["docker", "run", "--rm", "--platform", MANIFEST["platform"],
                           "--entrypoint", "/usr/bin/sha256sum", IMAGE, MODULE]).split()[0]
    if module_hash != MANIFEST["qtsvg_module_sha256"]:
        raise RuntimeError("QtSvg binary hash changed")

    files = {str(path.relative_to(PROJECT)): sha256(path.read_bytes()).hexdigest()
             for path in sorted(PROJECT.rglob("*"))
             if path.is_file() and path.name not in {"control-verification.json", "README.md"}
             and "target" not in path.relative_to(PROJECT).parts
             and "__pycache__" not in path.relative_to(PROJECT).parts}
    receipt = {
        "schema_version": 1,
        "status": "verified_control_only",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "image_id": command(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"]),
        "platform": MANIFEST["platform"],
        "base_image": MANIFEST["base_image"],
        "release": MANIFEST["release"],
        "source_sha256": MANIFEST["source_sha256"],
        "qtsvg_module_sha256": module_hash,
        "control_sha256": MANIFEST["control_sha256"],
        "output": output,
        "variant_sha256": MANIFEST["control_variant_sha256"],
        "variant_output": variant_output,
        "binding_lines_traced": summary["parser_source_lines_covered"],
        "parser_source_lines_covered": None,
        "parser_feedback_available": False,
        "afl_feedback_edges": None,
        "project_file_sha256": files,
    }
    (PROJECT / "control-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "output": output,
                      "variant_output": variant_output,
                      "parser_feedback_available": False}))


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest="action", required=True)
    commands.add_parser("verify")
    run = commands.add_parser("run")
    run.add_argument("file", type=Path)
    args = cli.parse_args()
    if args.action == "verify":
        verify()
    else:
        build_image()
        print(json.dumps(run_file(args.file)))


if __name__ == "__main__":
    main()
