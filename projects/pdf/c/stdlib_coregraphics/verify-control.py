"""Build and check the Core Graphics valid control on the pinned macOS host."""

from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess


PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parents[3]


def command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)} failed ({result.returncode}): "
                           f"{(result.stdout + result.stderr)[-4000:]}")
    return result.stdout.strip()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if platform.system() != "Darwin":
        raise RuntimeError("Core Graphics requires macOS; no container fallback exists")
    manifest = json.loads((PROJECT / "macos-manifest.json").read_text())
    control = ROOT / manifest["control"]
    adapter = ROOT / manifest["evidence_adapter"]
    if digest(control) != manifest["control_sha256"]:
        raise RuntimeError("valid control changed")
    if digest(adapter) != manifest["evidence_adapter_sha256"]:
        raise RuntimeError("evidence adapter changed")
    entry = next(item for item in json.loads((ROOT / manifest["standard_inventory"]).read_text())["verified_apis"]
                 if item["name"] == manifest["api"])
    if entry["input_api"] != manifest["input_api"] or entry["expected_output"] != manifest["expected_output"]:
        raise RuntimeError("standard inventory no longer matches this project")

    replay = Path(command([str(PROJECT / manifest["build"])]).splitlines()[-1])
    toolchain = json.loads((PROJECT / "target/toolchain.json").read_text())
    pinned = {key: value for key, value in manifest["toolchain"].items() if key != "xcode"}
    if toolchain.pop("pinned") is not True or toolchain != pinned:
        raise RuntimeError(f"toolchain differs from pins: {toolchain}")

    output = json.loads(command([str(replay), str(control)]))
    adapter_binary = PROJECT / "target/coregraphics-adapter"
    command(["xcrun", "clang", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", str(adapter),
             "-framework", "CoreGraphics", "-framework", "CoreFoundation", "-o", str(adapter_binary)])
    adapter_output = json.loads(command([str(adapter_binary), str(control)]))
    if output != manifest["expected_output"] or adapter_output != output:
        raise RuntimeError(f"unexpected control result: replay={output} adapter={adapter_output}")

    receipt = {
        "schema_version": 1,
        "status": "verified_control_only",
        "api": manifest["api"],
        "runtime": manifest["runtime"],
        "execution": "macos_host",
        "toolchain": manifest["toolchain"],
        "replay_binary_sha256": digest(replay),
        "evidence_adapter_sha256": manifest["evidence_adapter_sha256"],
        "evidence_adapter_output": adapter_output,
        "control_sha256": manifest["control_sha256"],
        "output": output,
        "container": "unavailable",
        "parser_source_coverage": "unavailable",
        "parser_feedback_available": False,
        "afl_feedback": "unavailable",
        "project_file_sha256": {
            str(file.relative_to(PROJECT)): digest(file)
            for file in sorted(PROJECT.rglob("*"))
            if file.is_file() and file.name not in {"control-verification.json", "README.md"}
            and "target" not in file.relative_to(PROJECT).parts
            and "__pycache__" not in file.relative_to(PROJECT).parts
        },
    }
    (PROJECT / "control-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(output))


if __name__ == "__main__":
    main()
