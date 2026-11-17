"""Rebuild and check this browser control without claiming parser feedback."""

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
    image = f"parsarium/{manifest['format']}-{manifest['ecosystem']}-{PROJECT.name}:local"
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
        "--tmpfs", "/tmp:rw,exec,nosuid,size=256m", "--shm-size", "256m",
        "-e", "HOME=/tmp", "-v", f"{control}:/input/control:ro",
        "-v", f"{output}:/coverage", image,
    ])
    summary = json.loads((output / "summary.json").read_text())
    if (summary["output"] != manifest["expected_output"]
            or summary["browser"] != "153.0.8010.12"
            or summary["adapter_js_functions_covered"] <= 0
            or summary["native_decoder_source_coverage"] != "unavailable"
            or summary["parser_feedback_available"] is not False):
        raise RuntimeError(f"unexpected browser control result: {summary}")
    receipt = {
        "schema_version": 1,
        "status": "verified_control_only",
        "api": manifest["api"],
        "runtime": manifest["runtime"],
        "image_id": command(["docker", "image", "inspect", image, "--format", "{{.Id}}"]),
        "base_image": manifest["base_image"],
        "browser_binary_sha256": manifest["source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "output": summary["output"],
        "adapter_js_functions_covered": summary["adapter_js_functions_covered"],
        "adapter_coverage_scope": summary["adapter_coverage_scope"],
        "native_decoder_source_coverage": "unavailable",
        "parser_feedback_available": False,
        "project_file_sha256": {
            str(file.relative_to(PROJECT)): sha256(file.read_bytes()).hexdigest()
            for file in sorted(PROJECT.rglob("*"))
            if file.is_file() and file.name not in {"control-verification.json", "README.md"}
            and "target" not in file.relative_to(PROJECT).parts
            and "__pycache__" not in file.relative_to(PROJECT).parts
        },
    }
    (PROJECT / "control-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(observed)


if __name__ == "__main__":
    main()
