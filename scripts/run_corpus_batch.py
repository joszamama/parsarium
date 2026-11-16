"""Replay a preserved corpus in one container without mutation iterations."""

import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import uuid

from run_case import image_for


def run_batch(project: Path, manifest: dict, inputs_dir: Path, timeout: int) -> dict | None:
    ecosystem = manifest["ecosystem"]
    if ecosystem == "php":
        return None  # php-fuzzer exposes run-single; replay these in parallel.
    image, image_id = image_for(project, manifest)
    inputs = sorted(path for path in inputs_dir.iterdir() if path.is_file())
    tmpfs = "/tmp:rw,exec,nosuid,size=64m" if manifest.get("tmpfs_exec") else "/tmp:rw,nosuid,size=64m"
    name = f"parsarium-batch-{uuid.uuid4().hex[:16]}"
    command = ["docker", "run", "--rm", "--name", name, "--pull", "never",
               "--platform", manifest["platform"], "--network", "none", "--read-only",
               "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
               "--user", f"{os.getuid()}:{os.getgid()}", "--tmpfs", tmpfs,
               "--workdir", "/" if ecosystem == "go" else "/tmp"]
    with tempfile.TemporaryDirectory(prefix="parsarium-batch-") as scratch:
        if ecosystem == "go":
            entry = manifest["fuzz_entry"]
            corpus = Path(scratch) / entry
            corpus.mkdir()
            for path in inputs:
                raw = path.read_bytes()
                encoded = "".join(f"\\x{byte:02x}" for byte in raw)
                (corpus / path.name).write_text(f'go test fuzz v1\n[]byte("{encoded}")\n')
            command += ["-v", f"{corpus}:/testdata/fuzz/{entry}:ro"]
            entrypoint = "/work/harness.test"
            args = [f"-test.run=^{entry}$", "-test.v"]
        else:
            command += ["-v", f"{inputs_dir}:/corpus:ro"]
            if ecosystem in {"c", "cpp", "rust"}:
                entrypoint = "/work/fuzzer"
                args = ["/corpus", "-runs=0", "-max_len=1048576"]
            elif ecosystem == "java":
                entrypoint = manifest["fuzz_smoke_entrypoint"]
                args = [arg for arg in manifest["fuzz_smoke_args"] if arg != "-help=1"]
                args += ["/corpus", "-runs=0"]
            elif ecosystem == "javascript":
                entrypoint = manifest["fuzz_smoke_entrypoint"]
                args = manifest["fuzz_smoke_args"]
                args = args[:args.index("--")] if "--" in args else list(args)
                args += ["--timeout", "30000", "/corpus", "--", "-runs=0"]
            elif ecosystem == "python":
                entrypoint = manifest["fuzz_smoke_entrypoint"]
                args = ["/work/fuzz.py", "/corpus", "-runs=0"]
            else:
                raise ValueError(f"unsupported ecosystem: {ecosystem}")
        command += ["--entrypoint", entrypoint, image, *args]
        started = time.monotonic()
        try:
            result = subprocess.run(command, capture_output=True, text=True,
                                    errors="replace", timeout=timeout)
            status = "ok" if result.returncode == 0 else "target_nonzero"
            if ecosystem == "go" and status == "ok":
                seen = set(re.findall(r"Fuzz[^/\s]+/([0-9a-f]{64})", result.stdout))
                if seen != {path.name for path in inputs}:
                    status = "infrastructure_error"
            return {"status": status, "image_id": image_id,
                    "input_count": len(inputs), "exit_code": result.returncode,
                    "duration_seconds": round(time.monotonic() - started, 3),
                    "stdout_tail": result.stdout[-8000:], "stderr_tail": result.stderr[-8000:]}
        except subprocess.TimeoutExpired as exc:
            subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=10)
            return {"status": "timeout", "image_id": image_id,
                    "input_count": len(inputs),
                    "duration_seconds": round(time.monotonic() - started, 3),
                    "stdout_tail": str(exc.stdout or "")[-8000:],
                    "stderr_tail": str(exc.stderr or "")[-8000:]}
