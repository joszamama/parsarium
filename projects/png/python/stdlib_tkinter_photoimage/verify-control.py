"""Rebuild and check the Tk PNG reader control and its native source coverage."""

from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from docker_slots import docker_build_slot  # noqa: E402


def command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)} failed: {(result.stdout + result.stderr)[-4000:]}")
    return result.stdout.strip()


def main() -> None:
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    control = ROOT / manifest["control"]
    if sha256(control.read_bytes()).hexdigest() != manifest["control_sha256"]:
        raise RuntimeError("valid control changed")
    image = "parsarium/png-python-stdlib_tkinter_photoimage:local"
    with docker_build_slot():
        command(["docker", "build", "--quiet", "--platform", manifest["platform"],
                 "-t", image, str(PROJECT)])
    output = PROJECT / "target/coverage"
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    observed = command([
        "docker", "run", "--rm", "--platform", manifest["platform"],
        "--network", "none", "--read-only", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
        "--tmpfs", "/tmp:rw,exec,nosuid,size=256m",
        "-v", f"{control}:/input/control:ro", "-v", f"{output}:/coverage", image,
    ])
    summary = json.loads((output / "summary.json").read_text())
    files = json.loads((output / "coverage.json").read_text())["data"][0]["files"]
    png_sources = [file for file in files if file["filename"].endswith("/tkImgPNG.c")]
    covered = sum(file["summary"]["lines"]["covered"] for file in png_sources)
    if (summary["output"] != manifest["expected_output"]
            or summary["parser_source_lines_covered"] != covered
            or covered <= 0
            or summary["afl_parser_feedback_available"] is not False):
        raise RuntimeError(f"unexpected Tk control result: {summary}")
    file_hashes = {
        str(file.relative_to(PROJECT)): sha256(file.read_bytes()).hexdigest()
        for file in sorted(PROJECT.rglob("*"))
        if file.is_file() and file.name not in {"control-verification.json", "README.md"}
        and "target" not in file.relative_to(PROJECT).parts
        and "__pycache__" not in file.relative_to(PROJECT).parts
    }
    receipt = {
        "schema_version": 1,
        "status": "verified_control_only",
        "api": manifest["api"], "runtime": manifest["runtime"],
        "image_id": command(["docker", "image", "inspect", image, "--format", "{{.Id}}"]),
        "base_image": manifest["base_image"],
        "source_sha256": manifest["source_sha256"],
        "python_source_sha256": manifest["python_source_sha256"],
        "png_reader_source_sha256": manifest["png_reader_source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "output": summary["output"],
        "parser_source_file": "tkImgPNG.c",
        "parser_source_lines_covered": covered,
        "parser_feedback_available": False,
        "project_file_sha256": file_hashes,
    }
    (PROJECT / "control-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(observed)


if __name__ == "__main__":
    main()
