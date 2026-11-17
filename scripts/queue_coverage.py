"""Bounded, one-shot source coverage replay of saved AFL++ queue files.

This module never invokes afl-fuzz. It uses the verified control image, not the
AFL feedback image, so llvm-cov can report parser source lines.
"""

from __future__ import annotations

from hashlib import sha256
import heapq
import json
import os
from pathlib import Path
import re
import shlex
import stat
import subprocess
import tempfile
import uuid

from run_case import MAX_CASE_BYTES

MAX_QUEUE_SAMPLE = 128
MAX_PROFILE_BYTES = 256 << 20
MAX_PROFILE_FILES = 1024
MAX_EXPORT_BYTES = 128 << 20


class QueueCoverageError(ValueError):
    pass


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def plan_for(run_dir: Path, root: Path, evidence: dict) -> tuple[dict, dict]:
    """Bind a prepared directory to the current verified project and AFL overlay."""
    path = run_dir / "plan.json"
    if not path.is_file() or path.stat().st_size > (1 << 20):
        raise QueueCoverageError("AFL++ plan.json is missing or too large")
    plan = json.loads(path.read_text())
    if not isinstance(plan, dict):
        raise QueueCoverageError("AFL++ plan is not a JSON object")
    identity, manifest = evidence["identity"], evidence["manifest"]
    project = f"{identity['format']}/{identity['ecosystem']}/{identity['slug']}"
    if plan.get("schema_version") != 1 or plan.get("project") != project:
        raise QueueCoverageError(f"AFL++ plan is not for {project}")
    for field in ("source_sha256", "control_sha256"):
        if plan.get(field) != manifest[field]:
            raise QueueCoverageError(f"AFL++ plan {field} differs from the verified project")
    overlay_path = root / "fuzzing/afl-native" / project / "verification.json"
    if not overlay_path.is_file():
        raise QueueCoverageError("verified AFL++ overlay receipt is missing")
    overlay_bytes = overlay_path.read_bytes()
    if len(overlay_bytes) > (1 << 20) or sha256(overlay_bytes).hexdigest() != plan.get("overlay_receipt_sha256"):
        raise QueueCoverageError("AFL++ overlay receipt changed since preparation")
    overlay = json.loads(overlay_bytes)
    if not isinstance(overlay, dict):
        raise QueueCoverageError("AFL++ overlay receipt is not a JSON object")
    if overlay.get("pass") is not True or overlay.get("image_id") != plan.get("image_id"):
        raise QueueCoverageError("AFL++ plan image differs from the verified overlay")
    base_field = ("base_control_receipt_sha256" if manifest.get("coverage_kind") ==
                  "native_source_afl_feedback" else "base_project_receipt_sha256")
    if overlay.get(base_field) != evidence["evidence"]["receipt_sha256"]:
        raise QueueCoverageError("AFL++ overlay points to another project receipt")
    if plan.get("platform") != manifest.get("platform"):
        raise QueueCoverageError("AFL++ plan platform differs from the verified project")
    return plan, overlay


def queue_files(run_dir: Path, maximum: int) -> tuple[int, list[tuple[str, Path]]]:
    output = run_dir / "afl-out"
    if not output.is_dir() or output.is_symlink():
        raise QueueCoverageError("AFL++ output directory is missing or is a symlink")
    total = 0
    chosen: list[tuple[str, Path]] = []
    for instance in sorted(output.iterdir()):
        queue = instance / "queue"
        if not instance.is_dir() or instance.is_symlink() or not queue.is_dir() or queue.is_symlink():
            continue
        def candidates():
            nonlocal total
            with os.scandir(queue) as entries:
                for item in entries:
                    if item.name.startswith("id:") and item.is_file(follow_symlinks=False):
                        total += 1
                        yield item.name
        for name in heapq.nsmallest(maximum, candidates()):
            chosen.append((f"{instance.name}/{name}", queue / name))
        chosen = heapq.nsmallest(maximum, chosen, key=lambda item: item[0])
    return total, chosen


def export_objects(project: Path) -> list[str]:
    """Read literal llvm-cov object paths from the verified control script.

    Dynamic shell expressions are outside this pilot. A control may request
    --summary-only; queue replay deliberately exports the full line map from
    the same instrumented replay binary and merged profiles.
    No project script is executed during reporting.
    """
    script = (project / "run-control.sh").read_text().replace("\\\n", " ")
    match = re.search(r"llvm-cov export\s+(.+?)\s*>\s*/coverage/coverage\.json\b", script, re.S)
    if not match:
        raise QueueCoverageError("project has no supported llvm-cov control export")
    try:
        tokens = shlex.split(match.group(1))
    except ValueError as error:
        raise QueueCoverageError("project llvm-cov export has dynamic or invalid quoting") from error
    if not tokens or tokens[0] != "/work/replay":
        raise QueueCoverageError("project llvm-cov export does not use /work/replay")
    objects = []
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--summary-only":
            pass
        elif token == "-object" and index + 1 < len(tokens):
            index += 1
            value = tokens[index]
            objects.append(value)
        elif token.startswith("-object="):
            objects.append(token.partition("=")[2])
        elif token.startswith("-instr-profile=") or token == "-instr-profile" and index + 1 < len(tokens):
            if token == "-instr-profile":
                index += 1
        else:
            raise QueueCoverageError(f"project llvm-cov option is outside this pilot: {token}")
        index += 1
    if any(not re.fullmatch(r"/work/[A-Za-z0-9_./+\-]+", item) or ".." in Path(item).parts
           for item in objects):
        raise QueueCoverageError("project llvm-cov object path is dynamic or outside /work")
    return objects


def replay_queue(run_dir: Path, root: Path, evidence: dict, maximum: int,
                 timeout: int) -> tuple[dict, dict | None]:
    manifest = evidence["manifest"]
    if evidence["identity"]["ecosystem"] not in {"c", "cpp"} or \
            evidence["feedback"]["coverage_kind"] != "source_lines":
        raise QueueCoverageError("queue source replay supports LLVM-covered C/C++ projects only")
    if not 1 <= maximum <= MAX_QUEUE_SAMPLE or not 1 <= timeout <= 60:
        raise QueueCoverageError("queue sample must be 1–128 and timeout 1–60 seconds")
    plan, _ = plan_for(run_dir, root, evidence)
    total, selected = queue_files(run_dir, maximum)
    if not selected:
        raise QueueCoverageError("no saved AFL++ queue inputs exist yet")
    objects = export_objects(evidence["project"])
    image_id = evidence["receipt"].get("image_id")
    inspect = subprocess.run(["docker", "image", "inspect", image_id, "--format",
                              "{{.Id}} {{.Os}}/{{.Architecture}}"], capture_output=True, text=True,
                             timeout=15)
    if inspect.returncode or inspect.stdout.strip() != f"{image_id} {manifest['platform']}":
        raise QueueCoverageError("verified coverage image is unavailable or has the wrong platform")
    common = ["docker", "run", "--rm", "--pull", "never", "--platform", manifest["platform"],
              "--network", "none", "--read-only", "--cap-drop", "ALL", "--security-opt",
              "no-new-privileges", "--memory", "2g", "--pids-limit", "128",
              "--ulimit", "core=0", "--ulimit", "fsize=67108864:67108864",
              "--user", f"{os.getuid()}:{os.getgid()}",
              "--tmpfs", "/tmp:rw,exec,nosuid,size=64m" if manifest.get("tmpfs_exec") else
              "/tmp:rw,nosuid,size=64m", "--workdir", "/tmp", "-e", "HOME=/tmp",
              "-e", "XDG_CACHE_HOME=/tmp"]
    inputs = []
    with tempfile.TemporaryDirectory(prefix="parsarium-queue-coverage-") as temp:
        scratch = Path(temp)
        profiles = scratch / "profiles"
        profiles.mkdir()
        data_dir = scratch / "data"
        data_dir.mkdir()
        for number, (label, original) in enumerate(selected):
            try:
                descriptor = os.open(original, os.O_RDONLY | os.O_NOFOLLOW)
            except OSError as error:
                raise QueueCoverageError(f"queue input cannot be opened without links: {label}") from error
            with os.fdopen(descriptor, "rb") as source:
                metadata = os.fstat(source.fileno())
                if not stat.S_ISREG(metadata.st_mode):
                    raise QueueCoverageError(f"queue input is not a regular file: {label}")
                if metadata.st_size > MAX_CASE_BYTES:
                    raise QueueCoverageError(f"queue input exceeds {MAX_CASE_BYTES} bytes: {label}")
                data = source.read(MAX_CASE_BYTES + 1)
            if len(data) != metadata.st_size:
                raise QueueCoverageError(f"queue input changed while reading: {label}")
            size = len(data)
            sample = data_dir / f"{number:03d}"
            sample.write_bytes(data)
            checksum = sha256(data).hexdigest()
            container_name = f"parsarium-report-{uuid.uuid4().hex[:16]}"
            command = [*common, "--name", container_name,
                       "-e", f"LLVM_PROFILE_FILE=/profiles/{number:03d}-%m-%p.profraw",
                       "-v", f"{sample}:/input/case:ro", "-v", f"{profiles}:/profiles",
                       "--entrypoint", "/work/replay", image_id, "/input/case"]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                        timeout=timeout)
                status = "exit" if result.returncode else "ok"
                exit_code = result.returncode
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "rm", "-f", container_name],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
                status, exit_code = "timeout", None
            if exit_code in (125, 126, 127):
                raise QueueCoverageError(f"Docker could not replay queue input {label} (exit {exit_code})")
            generated = list(profiles.glob(f"{number:03d}-*.profraw"))
            inputs.append({"queue_path": label, "sha256": checksum, "bytes": size,
                           "status": status, "exit_code": exit_code,
                           "profile_files": len(generated)})
            all_profiles = list(profiles.glob("*.profraw"))
            if len(all_profiles) > MAX_PROFILE_FILES or \
                    sum(path.stat().st_size for path in all_profiles) > MAX_PROFILE_BYTES:
                raise QueueCoverageError("queue profiles exceed the reporting size limit")
        replay = {"status": "source_replay", "plan_sha256": digest(run_dir / "plan.json"),
                  "afl_image_id": plan["image_id"], "coverage_image_id": image_id,
                  "coverage_binary": "/work/replay", "llvm_cov_objects": objects,
                  "llvm_cov_export_options": ["--skip-functions", "--skip-expansions"],
                  "queue_inputs_available": total, "queue_inputs_sampled": len(inputs),
                  "selection": "lexicographically first AFL id files across instances",
                  "timeout_seconds_per_input": timeout, "inputs": inputs}
        if not list(profiles.glob("*.profraw")):
            replay["status"] = "no_profiles"
            return replay, None
        merged = scratch / "aggregate.profdata"
        exported = scratch / "coverage.json"
        script = ("llvm-profdata merge -sparse /profiles/*.profraw -o /coverage/aggregate.profdata "
                  "&& llvm-cov export /work/replay --skip-functions --skip-expansions " +
                  " ".join(f"-object={shlex.quote(obj)}" for obj in objects) +
                  " -instr-profile=/coverage/aggregate.profdata > /coverage/coverage.json")
        container_name = f"parsarium-report-{uuid.uuid4().hex[:16]}"
        command = [*common, "--name", container_name,
                   "-v", f"{profiles}:/profiles:ro", "-v", f"{scratch}:/coverage",
                   "--entrypoint", "/bin/sh", image_id, "-c", script]
        try:
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    timeout=60)
        except subprocess.TimeoutExpired as error:
            subprocess.run(["docker", "rm", "-f", container_name],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            raise QueueCoverageError("llvm-cov export timed out") from error
        if result.returncode or not merged.is_file() or not exported.is_file() or \
                merged.stat().st_size > MAX_PROFILE_BYTES or \
                exported.stat().st_size > MAX_EXPORT_BYTES:
            raise QueueCoverageError("llvm-profdata merge or llvm-cov export failed or exceeded size limit")
        coverage = json.loads(exported.read_bytes())
        if not isinstance(coverage, dict) or coverage.get("type") != "llvm.coverage.json.export":
            raise QueueCoverageError("coverage image did not emit an LLVM source export")
        data = coverage.get("data")
        if not isinstance(data, list) or not data or not isinstance(data[0], dict):
            raise QueueCoverageError("LLVM coverage export has no file data")
        files = data[0].get("files", [])
        prefix = manifest["coverage_subject_prefix"]
        if not any(item.get("filename", "").startswith(prefix) for item in files):
            raise QueueCoverageError("aggregate has no instrumented parser source files")
        replay["profdata_sha256"] = digest(merged)
        replay["coverage_sha256"] = digest(exported)
        replay["coverage_bytes"] = exported.stat().st_size
    return replay, coverage
