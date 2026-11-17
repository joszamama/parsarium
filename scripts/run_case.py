"""Replay one supplied input through a verified project's fuzz entry point.

This is an external black-box bridge for generators such as Fandango. It does
not start a mutation campaign or interpret a nonzero exit as a vulnerability.
"""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import uuid


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
MAX_CASE_BYTES = 1 << 20


def project_for(format_name: str, ecosystem: str, slug: str) -> tuple[Path, dict]:
    project = (PROJECTS / format_name / ecosystem / slug).resolve()
    if not project.is_relative_to(PROJECTS) or not (project / "manifest.json").is_file():
        raise ValueError("unknown project")
    manifest = json.loads((project / "manifest.json").read_text())
    if (manifest["format"], manifest["ecosystem"]) != (format_name, ecosystem):
        raise ValueError("project path and manifest disagree")
    if manifest.get("coverage_kind") == "native_source_afl_feedback":
        from audit_projects import native_source_feedback_verified
        if not native_source_feedback_verified(project / "manifest.json", manifest):
            raise ValueError("standard API control or AFL++ feedback receipt changed")
        return project, manifest
    receipt = json.loads((project / "verification.json").read_text())
    if not receipt.get("pass"):
        raise ValueError("project has no passing verification receipt")
    present = {str(path.relative_to(project)) for path in project.rglob("*")
               if path.is_file() and path.name != "verification.json"
               and path.relative_to(project) != Path("README.md")
               and "target" not in path.relative_to(project).parts
               and "vendor" not in path.relative_to(project).parts
               and "__pycache__" not in path.relative_to(project).parts}
    if present != set(receipt["project_file_sha256"]):
        raise ValueError("project file set changed since verification")
    for name, expected in receipt["project_file_sha256"].items():
        if sha256((project / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"project changed since verification: {name}")
    return project, manifest


def image_for(project: Path, manifest: dict) -> tuple[str, str]:
    image = f"parsarium/{manifest['format']}-{manifest['ecosystem']}-{project.name}:local"
    inspection = subprocess.run(
        ["docker", "image", "inspect", image, "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"],
        capture_output=True, text=True,
    )
    if inspection.returncode or not inspection.stdout.strip().endswith(manifest["platform"]):
        build = subprocess.run(
            ["docker", "build", "--quiet", "--platform", manifest["platform"],
             "-t", image, str(project)], capture_output=True, text=True,
        )
        if build.returncode:
            raise RuntimeError(f"image build failed: {build.stderr[-4000:]}")
        inspection = subprocess.run(
            ["docker", "image", "inspect", image, "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"],
            capture_output=True, text=True, check=True,
        )
    image_id, platform = inspection.stdout.strip().split()
    if platform != manifest["platform"]:
        raise RuntimeError(f"image platform mismatch: {platform}")
    return image, image_id


def target_command(manifest: dict, case_sha: str, scratch: Path) -> tuple[str, list[str], list[str]]:
    ecosystem = manifest["ecosystem"]
    mounts: list[str] = []
    if manifest.get("coverage_kind") == "native_source_afl_feedback":
        return "/opt/python/bin/python3.13", ["/work/replay-cli.py", "/input/case"], mounts
    if ecosystem == "go":
        entry = manifest["fuzz_entry"]
        corpus = scratch / entry
        corpus.mkdir()
        raw = (scratch / "case-bytes").read_bytes()
        encoded = "".join(f"\\x{byte:02x}" for byte in raw)
        (corpus / case_sha).write_text(f'go test fuzz v1\n[]byte("{encoded}")\n')
        mounts.append(f"{corpus}:/testdata/fuzz/{entry}:ro")
        return "/work/harness.test", [f"-test.run=^{entry}$", "-test.v"], mounts
    if ecosystem in {"c", "cpp", "rust"} or (ecosystem == "python" and
            manifest.get("fuzz_engine", "").startswith("libFuzzer")):
        return manifest.get("fuzz_smoke_entrypoint", "/work/fuzzer"), ["/input/case"], mounts
    args = list(manifest["fuzz_smoke_args"])
    if ecosystem == "javascript" and "--" in args:
        args = args[:args.index("--")]
        args += ["--timeout", "30000"]
    else:
        args = [arg for arg in args if arg != "-help=1"]
    args = [arg.replace("/input/control", "/input/case") for arg in args]
    if ecosystem != "php":
        args.append("/input/case")
    return manifest["fuzz_smoke_entrypoint"], args, mounts


def run_case(project: Path, manifest: dict, case: Path, timeout: int) -> dict:
    data = case.read_bytes()
    case_sha = sha256(data).hexdigest()
    if len(data) > MAX_CASE_BYTES:
        return {"status": "input_too_large", "case_sha256": case_sha,
                "case_bytes": len(data), "max_bytes": MAX_CASE_BYTES}
    image, image_id = image_for(project, manifest)
    with tempfile.TemporaryDirectory(prefix="parsarium-case-") as tmp:
        scratch = Path(tmp)
        (scratch / "case-bytes").write_bytes(data)
        entrypoint, args, extra_mounts = target_command(manifest, case_sha, scratch)
        tmpfs = ("/tmp:rw,exec,nosuid,size=256m" if
                 manifest.get("coverage_kind") == "native_source_afl_feedback" else
                 "/tmp:rw,exec,nosuid,size=64m" if manifest.get("tmpfs_exec") else
                 "/tmp:rw,nosuid,size=64m")
        container_name = f"parsarium-case-{uuid.uuid4().hex[:16]}"
        command = [
            "docker", "run", "--rm", "--name", container_name,
            "--pull", "never", "--platform", manifest["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", tmpfs, "--workdir", "/" if manifest["ecosystem"] == "go" else "/tmp",
            "-v", f"{case}:/input/case:ro",
        ]
        for mount in extra_mounts:
            command += ["-v", mount]
        command += ["--entrypoint", entrypoint, image, *args]
        started = time.monotonic()
        try:
            result = subprocess.run(command, capture_output=True, text=True,
                                    errors="replace", timeout=timeout)
            elapsed = time.monotonic() - started
            status = "ok" if result.returncode == 0 else "target_nonzero"
            if manifest["ecosystem"] == "go" and status == "ok":
                if case_sha not in result.stdout:
                    status = "infrastructure_error"
            return {"status": status, "case_sha256": case_sha, "case_bytes": len(data),
                    "image_id": image_id, "exit_code": result.returncode,
                    "duration_seconds": round(elapsed, 3),
                    "stdout_tail": result.stdout[-4000:], "stderr_tail": result.stderr[-4000:]}
        except subprocess.TimeoutExpired as exc:
            subprocess.run(["docker", "rm", "-f", container_name],
                           capture_output=True, timeout=10)
            return {"status": "timeout", "case_sha256": case_sha,
                    "case_bytes": len(data), "image_id": image_id,
                    "duration_seconds": round(time.monotonic() - started, 3),
                    "stdout_tail": str(exc.stdout or "")[-4000:],
                    "stderr_tail": str(exc.stderr or "")[-4000:]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("format")
    parser.add_argument("ecosystem")
    parser.add_argument("package_slug")
    parser.add_argument("case", type=Path)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--results", type=Path, help="write one JSON receipt per input SHA-256")
    args = parser.parse_args()
    try:
        project, manifest = project_for(args.format, args.ecosystem, args.package_slug)
        case = args.case.resolve(strict=True)
        if not case.is_file():
            raise ValueError("case is not a regular file")
        result = run_case(project, manifest, case, args.timeout)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        result = {"status": "infrastructure_error", "detail": str(exc)}
    result = {"schema_version": 1, "project": f"{args.format}/{args.ecosystem}/{args.package_slug}",
              "input": str(args.case), **result}
    if args.results:
        args.results.mkdir(parents=True, exist_ok=True)
        name = result.get("case_sha256", "infrastructure-error") + ".json"
        destination = args.results / name
        with tempfile.NamedTemporaryFile(mode="w", dir=args.results, delete=False) as handle:
            handle.write(json.dumps(result, sort_keys=True) + "\n")
            temporary = Path(handle.name)
        temporary.replace(destination)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
