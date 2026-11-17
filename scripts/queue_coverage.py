"""Bounded, one-shot source coverage replay of saved AFL++ queue files.

This module never invokes afl-fuzz. It uses the verified control image, not the
AFL feedback image, for LLVM, Go coverprofile, JaCoCo, Python trace, PHP
Xdebug, or V8 parser lines.
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
import xml.etree.ElementTree as ET

from run_case import MAX_CASE_BYTES

MAX_QUEUE_SAMPLE = 128
MAX_PROFILE_BYTES = 256 << 20
MAX_PROFILE_FILES = 1024
MAX_EXPORT_BYTES = 128 << 20
MAX_INTERPRETED_TRACE_BYTES = 16 << 20
MAX_GO_PROFILE_BYTES = 16 << 20


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
    ecosystem = evidence["identity"]["ecosystem"]
    if ecosystem not in {"c", "cpp", "rust"} or \
            evidence["feedback"]["coverage_kind"] != "source_lines":
        raise QueueCoverageError("queue source replay supports LLVM-covered C/C++/Rust projects only")
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
        llvm_profdata = "/work/llvm-profdata" if ecosystem == "rust" else "llvm-profdata"
        llvm_cov = "/work/llvm-cov" if ecosystem == "rust" else "llvm-cov"
        script = (f"{llvm_profdata} merge -sparse /profiles/*.profraw -o /coverage/aggregate.profdata "
                  f"&& {llvm_cov} export /work/replay --skip-functions --skip-expansions " +
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


def replay_interpreted_queue(run_dir: Path, root: Path, evidence: dict, maximum: int,
                             timeout: int) -> tuple[dict, dict | None]:
    """Replay saved inputs through pinned interpreted harnesses and union parser lines.

    Python ``trace``, PHP Xdebug, or Node V8 observes package source in the
    verified control image. This does not claim native extension lines,
    uncovered lines, or a coverage percentage.
    """
    manifest = evidence["manifest"]
    ecosystem = evidence["identity"]["ecosystem"]
    if ecosystem not in {"python", "php", "javascript"} or \
            evidence["feedback"]["coverage_kind"] != "source_lines":
        raise QueueCoverageError("interpreted source replay needs a Python/PHP/JavaScript source-line project")
    if not 1 <= maximum <= MAX_QUEUE_SAMPLE or not 1 <= timeout <= 60:
        raise QueueCoverageError("queue sample must be 1–128 and timeout 1–60 seconds")
    interpreter = manifest.get("fuzz_smoke_entrypoint")
    if ecosystem == "python":
        if interpreter not in ("/opt/venv/bin/python", "/usr/local/bin/python") or \
                not (evidence["project"] / "harness.py").is_file():
            raise QueueCoverageError("project has no supported Python harness/interpreter")
        primary_prefix = manifest.get("coverage_subject_prefix", "")
        if not isinstance(primary_prefix, str) or not (
                "site-packages/" in primary_prefix or
                primary_prefix.startswith(("/usr/local/lib/python", "/usr/lib/python"))):
            raise QueueCoverageError("Python trace supports installed Python package source only; "
                                     "this project needs native source replay")
        script = root / "scripts/python_queue_trace.py"
    elif ecosystem == "php":
        if interpreter not in ("/usr/bin/php", "/opt/php/bin/php") or \
                not (evidence["project"] / "harness.php").is_file() or \
                "function parsarium_parse(" not in (evidence["project"] / "harness.php").read_text():
            raise QueueCoverageError("project has no supported PHP byte-input harness/interpreter")
        script = root / "scripts/php_queue_trace.php"
    else:
        replay = evidence["project"] / "replay.js"
        control = evidence["project"] / "run-control.js"
        if interpreter != "/usr/local/bin/node" or not replay.is_file() or \
                not control.is_file() or "process.argv[2]" not in replay.read_text() or \
                "NODE_V8_COVERAGE" not in control.read_text():
            raise QueueCoverageError("project has no supported Node V8 replay harness")
        script = root / "scripts/javascript_queue_trace.js"
    prefixes = [manifest["coverage_subject_prefix"]]
    if manifest.get("underlying_coverage_subject_prefix"):
        prefixes.append(manifest["underlying_coverage_subject_prefix"])
    if any(not isinstance(prefix, str) or not prefix.startswith("/") for prefix in prefixes):
        raise QueueCoverageError("interpreted parser source prefixes must be absolute")
    plan, _ = plan_for(run_dir, root, evidence)
    total, selected = queue_files(run_dir, maximum)
    if not selected:
        raise QueueCoverageError("no saved AFL++ queue inputs exist yet")
    image_id = evidence["receipt"].get("image_id")
    inspect = subprocess.run(["docker", "image", "inspect", image_id, "--format",
                              "{{.Id}} {{.Os}}/{{.Architecture}}"], capture_output=True,
                             text=True, timeout=15)
    if inspect.returncode or inspect.stdout.strip() != f"{image_id} {manifest['platform']}":
        raise QueueCoverageError("verified coverage image is unavailable or has the wrong platform")
    script_sha = digest(script)
    common = ["docker", "run", "--rm", "--pull", "never", "--platform", manifest["platform"],
              "--network", "none", "--read-only", "--cap-drop", "ALL", "--security-opt",
              "no-new-privileges", "--memory", "2g", "--pids-limit", "128",
              "--ulimit", "core=0", "--ulimit", "fsize=67108864:67108864",
              "--user", f"{os.getuid()}:{os.getgid()}",
              "--tmpfs", "/tmp:rw,exec,nosuid,size=64m" if manifest.get("tmpfs_exec") else
              "/tmp:rw,nosuid,size=64m", "--workdir", "/tmp", "-e", "HOME=/tmp",
              "-e", "XDG_CACHE_HOME=/tmp"]
    inputs = []
    union: dict[str, set[int]] = {}
    with tempfile.TemporaryDirectory(prefix="parsarium-python-queue-") as temp:
        scratch = Path(temp)
        for number, (label, original) in enumerate(selected):
            try:
                descriptor = os.open(original, os.O_RDONLY | os.O_NOFOLLOW)
            except OSError as error:
                raise QueueCoverageError(f"queue input cannot be opened without links: {label}") from error
            with os.fdopen(descriptor, "rb") as source:
                metadata = os.fstat(source.fileno())
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_CASE_BYTES:
                    raise QueueCoverageError(f"queue input is invalid or too large: {label}")
                data = source.read(MAX_CASE_BYTES + 1)
            if len(data) != metadata.st_size:
                raise QueueCoverageError(f"queue input changed while reading: {label}")
            sample = scratch / f"{number:03d}.input"
            sample.write_bytes(data)
            traced = scratch / f"{number:03d}.json"
            container_name = f"parsarium-report-{uuid.uuid4().hex[:16]}"
            command = [*common, "--name", container_name,
                       "-v", f"{sample}:/input/case:ro",
                       "-v", f"{script}:/input/{script.name}:ro",
                       "-v", f"{scratch}:/coverage",
                       "--entrypoint", interpreter, image_id,
                       *(["-d", "xdebug.mode=coverage"] if ecosystem == "php" else []),
                       f"/input/{script.name}", "/input/case",
                       f"/coverage/{number:03d}.json", json.dumps(prefixes)]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL, timeout=timeout)
                status, exit_code = ("ok" if result.returncode == 0 else "exit"), result.returncode
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "rm", "-f", container_name],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
                status, exit_code = "timeout", None
            if exit_code in (125, 126, 127):
                raise QueueCoverageError(f"Docker could not replay queue input {label} (exit {exit_code})")
            item = {"queue_path": label, "sha256": sha256(data).hexdigest(),
                    "bytes": len(data), "status": status, "exit_code": exit_code,
                    "trace_files": 0}
            if traced.is_file():
                if traced.stat().st_size > MAX_INTERPRETED_TRACE_BYTES:
                    raise QueueCoverageError(f"parser line trace exceeds size limit: {label}")
                record = json.loads(traced.read_bytes())
                if record.get("outcome") not in ("ok",) and not str(record.get("outcome", "")).startswith("exception:"):
                    raise QueueCoverageError(f"parser line trace outcome is invalid: {label}")
                item["target_outcome"] = record["outcome"]
                files = record.get("files")
                if not isinstance(files, list):
                    raise QueueCoverageError(f"parser line trace has no file list: {label}")
                for entry in files:
                    name, lines = entry.get("filename"), entry.get("executed_lines")
                    if not isinstance(name, str) or not any(name.startswith(p) for p in prefixes) or \
                            not isinstance(lines, list) or lines != sorted(set(lines)) or \
                            any(type(line) is not int or line < 1 or line > 10_000_000 for line in lines):
                        raise QueueCoverageError(f"parser line trace contains invalid parser lines: {label}")
                    union.setdefault(name, set()).update(lines)
                item["trace_files"] = len(files)
                item["trace_sha256"] = digest(traced)
            inputs.append(item)
        replay = {"status": "source_replay" if union else "no_profiles",
                  "mechanism": {"python": "Python trace", "php": "PHP Xdebug",
                                "javascript": "Node V8 coverage"}[ecosystem] +
                  " of package source in verified control image",
                  "plan_sha256": digest(run_dir / "plan.json"),
                  "afl_image_id": plan["image_id"], "coverage_image_id": image_id,
                  "coverage_binary": interpreter, "llvm_cov_objects": [],
                  "trace_script_sha256": script_sha,
                  "queue_inputs_available": total, "queue_inputs_sampled": len(inputs),
                  "selection": "lexicographically first AFL id files across instances",
                  "timeout_seconds_per_input": timeout, "inputs": inputs}
        if not union:
            return replay, None
        coverage = {"data": [{"files": [
            {"filename": name, "executed_lines": sorted(lines),
             "summary": {"lines": {"covered": len(lines)}}}
            for name, lines in sorted(union.items())]}]}
        exported = scratch / "coverage.json"
        exported.write_text(json.dumps(coverage, sort_keys=True) + "\n")
        if exported.stat().st_size > MAX_EXPORT_BYTES:
            raise QueueCoverageError("aggregate interpreted source export exceeds size limit")
        replay["coverage_sha256"] = digest(exported)
        replay["coverage_bytes"] = exported.stat().st_size
    return replay, coverage


def go_fuzz_corpus(data: bytes) -> bytes:
    """Encode exactly one byte slice in Go's documented fuzz corpus syntax."""
    literal = "".join(f"\\x{byte:02x}" for byte in data)
    return (f'go test fuzz v1\n[]byte("{literal}")\n').encode("ascii")


def go_profile_lines(raw: bytes, prefixes: list[str]) -> dict[str, set[int]]:
    """Apply the project's Go coverprofile span-to-line conversion."""
    if not raw.startswith((b"mode: set\n", b"mode: count\n", b"mode: atomic\n")):
        raise QueueCoverageError("Go coverprofile has an unsupported mode")
    files: dict[str, set[int]] = {}
    try:
        rows = raw.decode("utf-8").splitlines()[1:]
    except UnicodeDecodeError as error:
        raise QueueCoverageError("Go coverprofile is not UTF-8") from error
    for row in rows:
        fields = row.split()
        if len(fields) != 3:
            raise QueueCoverageError("Go coverprofile contains an invalid row")
        if not fields[0].startswith(tuple(prefixes)):
            continue
        try:
            hits = int(fields[2])
            location, span = fields[0].rsplit(":", 1)
            first, last = span.split(",", 1)
            first_line, _ = (int(part) for part in first.split("."))
            last_line, last_column = (int(part) for part in last.split("."))
        except (ValueError, IndexError) as error:
            raise QueueCoverageError("Go coverprofile contains an invalid source span") from error
        if hits <= 0:
            continue
        if last_column == 1 and last_line > first_line:
            last_line -= 1
        if first_line < 1 or last_line < first_line or last_line - first_line > 10_000:
            raise QueueCoverageError("Go coverprofile source span exceeds line limits")
        files.setdefault(location, set()).update(range(first_line, last_line + 1))
    return files


def replay_go_queue(run_dir: Path, root: Path, evidence: dict, maximum: int,
                    timeout: int) -> tuple[dict, dict | None]:
    """Replay Go fuzz test seeds once, unioning pinned package source lines."""
    manifest = evidence["manifest"]
    if evidence["identity"]["ecosystem"] != "go" or \
            evidence["feedback"]["coverage_kind"] != "source_lines":
        raise QueueCoverageError("Go source replay needs a Go source-line project")
    if not 1 <= maximum <= MAX_QUEUE_SAMPLE or not 1 <= timeout <= 60:
        raise QueueCoverageError("queue sample must be 1–128 and timeout 1–60 seconds")
    harness = evidence["project"] / "harness_test.go"
    if manifest.get("fuzz_smoke_entrypoint") != "/work/harness.test" or not harness.is_file():
        raise QueueCoverageError("project has no supported Go coverage harness")
    fuzz_names = re.findall(r"^func (Fuzz[A-Za-z0-9_]+)\(f \*testing\.F\)",
                            harness.read_text(), re.M)
    if len(fuzz_names) != 1 or "f.Add(" in harness.read_text():
        raise QueueCoverageError("project has no single seed-free Go fuzz test")
    fuzz_name = fuzz_names[0]
    prefixes = [manifest["coverage_subject_prefix"]]
    underlying = manifest.get("underlying_coverage_subject_prefix")
    native_underlying_unsupported = isinstance(underlying, str) and underlying.startswith("/")
    if underlying and not native_underlying_unsupported:
        prefixes.append(underlying)
    if any(not isinstance(prefix, str) or not prefix or prefix.startswith("/")
           for prefix in prefixes):
        raise QueueCoverageError("Go parser source prefixes must be module paths")
    plan, _ = plan_for(run_dir, root, evidence)
    total, selected = queue_files(run_dir, maximum)
    if not selected:
        raise QueueCoverageError("no saved AFL++ queue inputs exist yet")
    image_id = evidence["receipt"].get("image_id")
    inspect = subprocess.run(["docker", "image", "inspect", image_id, "--format",
                              "{{.Id}} {{.Os}}/{{.Architecture}}"], capture_output=True,
                             text=True, timeout=15)
    if inspect.returncode or inspect.stdout.strip() != f"{image_id} {manifest['platform']}":
        raise QueueCoverageError("verified coverage image is unavailable or has the wrong platform")
    common = ["docker", "run", "--rm", "--pull", "never", "--platform", manifest["platform"],
              "--network", "none", "--read-only", "--cap-drop", "ALL", "--security-opt",
              "no-new-privileges", "--memory", "2g", "--pids-limit", "128",
              "--ulimit", "core=0", "--ulimit", "fsize=67108864:67108864",
              "--user", f"{os.getuid()}:{os.getgid()}",
              "--tmpfs", "/tmp:rw,nosuid,size=64m", "--workdir", "/input"]
    inputs = []
    union: dict[str, set[int]] = {}
    with tempfile.TemporaryDirectory(prefix="parsarium-go-queue-") as temp:
        scratch = Path(temp)
        profiles = scratch / "profiles"
        profiles.mkdir()
        for number, (label, original) in enumerate(selected):
            try:
                descriptor = os.open(original, os.O_RDONLY | os.O_NOFOLLOW)
            except OSError as error:
                raise QueueCoverageError(f"queue input cannot be opened without links: {label}") from error
            with os.fdopen(descriptor, "rb") as source:
                metadata = os.fstat(source.fileno())
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_CASE_BYTES:
                    raise QueueCoverageError(f"queue input is invalid or too large: {label}")
                data = source.read(MAX_CASE_BYTES + 1)
            if len(data) != metadata.st_size:
                raise QueueCoverageError(f"queue input changed while reading: {label}")
            case_root = scratch / f"case-{number:03d}"
            corpus = case_root / "testdata" / "fuzz" / fuzz_name
            corpus.mkdir(parents=True)
            (corpus / "seed").write_bytes(go_fuzz_corpus(data))
            profile = profiles / f"{number:03d}.out"
            container_name = f"parsarium-report-{uuid.uuid4().hex[:16]}"
            command = [*common, "--name", container_name,
                       "-v", f"{case_root}:/input:ro", "-v", f"{profiles}:/coverage",
                       "--entrypoint", "/work/harness.test", image_id,
                       f"-test.run=^{fuzz_name}$", f"-test.coverprofile=/coverage/{number:03d}.out"]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL, timeout=timeout)
                status, exit_code = ("ok" if result.returncode == 0 else "exit"), result.returncode
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "rm", "-f", container_name],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
                status, exit_code = "timeout", None
            if exit_code in (125, 126, 127):
                raise QueueCoverageError(f"Docker could not replay queue input {label} (exit {exit_code})")
            item = {"queue_path": label, "sha256": sha256(data).hexdigest(),
                    "bytes": len(data), "status": status, "exit_code": exit_code,
                    "profile_files": 0}
            if profile.is_file():
                if profile.stat().st_size > MAX_GO_PROFILE_BYTES:
                    raise QueueCoverageError(f"Go coverprofile exceeds size limit: {label}")
                lines = go_profile_lines(profile.read_bytes(), prefixes)
                for filename, observed in lines.items():
                    union.setdefault(filename, set()).update(observed)
                item["profile_files"] = 1
                item["profile_sha256"] = digest(profile)
            inputs.append(item)
            if sum(path.stat().st_size for path in profiles.glob("*.out")) > MAX_PROFILE_BYTES:
                raise QueueCoverageError("Go coverprofiles exceed reporting size limit")
        replay = {"status": "source_replay" if union else "no_profiles",
                  "mechanism": "Go coverprofile from fuzz test in verified control image",
                  "plan_sha256": digest(run_dir / "plan.json"),
                  "afl_image_id": plan["image_id"], "coverage_image_id": image_id,
                  "coverage_binary": "/work/harness.test", "llvm_cov_objects": [],
                  "fuzz_test": fuzz_name,
                  "native_underlying_unsupported": native_underlying_unsupported,
                  "queue_inputs_available": total, "queue_inputs_sampled": len(inputs),
                  "selection": "lexicographically first AFL id files across instances",
                  "timeout_seconds_per_input": timeout, "inputs": inputs}
        if not union:
            return replay, None
        coverage = {"data": [{"files": [
            {"filename": name, "executed_lines": sorted(lines),
             "summary": {"lines": {"covered": len(lines)}}}
            for name, lines in sorted(union.items())]}]}
        exported = scratch / "coverage.json"
        exported.write_text(json.dumps(coverage, sort_keys=True) + "\n")
        if exported.stat().st_size > MAX_EXPORT_BYTES:
            raise QueueCoverageError("aggregate Go source export exceeds size limit")
        replay["coverage_sha256"] = digest(exported)
        replay["coverage_bytes"] = exported.stat().st_size
    return replay, coverage


def java_control_commands(project: Path, manifest: dict) -> tuple[list[str], list[dict]]:
    """Extract only literal JaCoCo commands already used by the verified control.

    The JDK module-patch and custom harness variants need project-specific
    replay, so this deliberately supports only the normal Java agent form.
    No shell from the project is executed while reporting.
    """
    control_script = project / "run-control.sh"
    if not control_script.is_file():
        raise QueueCoverageError("project has no supported Java JaCoCo control script")
    script = control_script.read_text().replace("\\\n", " ")
    match = re.search(r"(?m)^java\s+(.+?)\s+GenericHarness\s+/input/control\b", script)
    if not match:
        raise QueueCoverageError("project has no supported Java GenericHarness command")
    try:
        args = shlex.split(match.group(1))
    except ValueError as error:
        raise QueueCoverageError("Java control command has invalid quoting") from error
    agent = "-javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes="
    if len(args) not in (3, 4) or not args[0].startswith(agent) or \
            args[-2] != "-cp" or not args[-1]:
        raise QueueCoverageError("project has no supported Java agent/classpath command")
    if len(args) == 4 and args[1] != "-Dstdout.encoding=UTF-8":
        raise QueueCoverageError("Java control uses extra VM options outside this replay")
    if any(not path.startswith("/work/") or ".." in Path(path).parts
           for path in args[-1].split(":")):
        raise QueueCoverageError("Java classpath is not a literal /work path")
    report_lines = re.findall(
        r"(?m)^java -jar /work/jacococli\.jar report /coverage/jacoco\.exec\s+([^\n]+)",
        script)
    reports = []
    for line in report_lines:
        try:
            tokens = shlex.split(line)
        except ValueError as error:
            raise QueueCoverageError("JaCoCo report command has invalid quoting") from error
        if len(tokens) != 7 or tokens[0::2] != [
                "--classfiles", "--sourcefiles", "--xml", "--quiet"]:
            raise QueueCoverageError("JaCoCo report command has unsupported options")
        classes, source_root, output = tokens[1], tokens[3], tokens[5]
        if any(not path.startswith("/work/") or ".." in Path(path).parts
               for path in (classes, source_root)) or \
                not re.fullmatch(r"/coverage/jacoco(?:-[a-z]+)?\.xml", output):
            raise QueueCoverageError("JaCoCo report command has dynamic or unsafe paths")
        reports.append({"classfiles": classes, "sourcefiles": source_root,
                        "xml": output})
    if not reports:
        raise QueueCoverageError("project has no supported JaCoCo source report")
    prefixes = [manifest["coverage_subject_prefix"]]
    if manifest.get("underlying_coverage_subject_prefix"):
        prefixes.append(manifest["underlying_coverage_subject_prefix"])
    if any(not isinstance(prefix, str) or not prefix.startswith("/work/") or
           not any(prefix.rstrip("/") == report["sourcefiles"].rstrip("/") or
                   prefix.startswith(report["sourcefiles"].rstrip("/") + "/")
                   for report in reports) for prefix in prefixes):
        raise QueueCoverageError("JaCoCo source roots do not cover manifest parser prefixes")
    return args, reports


def java_jacoco_lines(path: Path, source_root: str,
                      prefixes: list[str]) -> dict[str, set[int]]:
    """Read JaCoCo line instructions from one bounded source XML report."""
    if path.stat().st_size > MAX_INTERPRETED_TRACE_BYTES:
        raise QueueCoverageError("JaCoCo XML exceeds the per-input size limit")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as error:
        raise QueueCoverageError("JaCoCo emitted invalid XML") from error
    if root.tag != "report":
        raise QueueCoverageError("JaCoCo XML is not a report")
    files: dict[str, set[int]] = {}
    for package in root.findall("package"):
        package_name = package.get("name", "")
        for source in package.findall("sourcefile"):
            filename = f"{source_root.rstrip('/')}/{package_name}/{source.get('name', '')}"
            if not any(filename.startswith(prefix) for prefix in prefixes):
                continue
            executed = set()
            for line in source.findall("line"):
                try:
                    number, instructions = int(line.attrib["nr"]), int(line.attrib["ci"])
                except (KeyError, ValueError) as error:
                    raise QueueCoverageError("JaCoCo XML has invalid line counters") from error
                if number < 1 or number > 10_000_000 or instructions < 0:
                    raise QueueCoverageError("JaCoCo XML has out-of-range line counters")
                if instructions > 0:
                    executed.add(number)
            if executed:
                files.setdefault(filename, set()).update(executed)
    return files


def replay_java_queue(run_dir: Path, root: Path, evidence: dict, maximum: int,
                      timeout: int) -> tuple[dict, dict | None]:
    """Replay each saved input in the verified Java image and union JaCoCo lines."""
    manifest = evidence["manifest"]
    if evidence["identity"]["ecosystem"] != "java" or \
            evidence["feedback"]["coverage_kind"] != "source_lines":
        raise QueueCoverageError("Java source replay needs a Java source-line project")
    if not 1 <= maximum <= MAX_QUEUE_SAMPLE or not 1 <= timeout <= 60:
        raise QueueCoverageError("queue sample must be 1–128 and timeout 1–60 seconds")
    vm_args, reports = java_control_commands(evidence["project"], manifest)
    prefixes = [manifest["coverage_subject_prefix"]]
    if manifest.get("underlying_coverage_subject_prefix"):
        prefixes.append(manifest["underlying_coverage_subject_prefix"])
    plan, _ = plan_for(run_dir, root, evidence)
    total, selected = queue_files(run_dir, maximum)
    if not selected:
        raise QueueCoverageError("no saved AFL++ queue inputs exist yet")
    image_id = evidence["receipt"].get("image_id")
    inspect = subprocess.run(["docker", "image", "inspect", image_id, "--format",
                              "{{.Id}} {{.Os}}/{{.Architecture}}"], capture_output=True,
                             text=True, timeout=15)
    if inspect.returncode or inspect.stdout.strip() != f"{image_id} {manifest['platform']}":
        raise QueueCoverageError("verified coverage image is unavailable or has the wrong platform")
    common = ["docker", "run", "--rm", "--pull", "never", "--platform", manifest["platform"],
              "--network", "none", "--read-only", "--cap-drop", "ALL", "--security-opt",
              "no-new-privileges", "--memory", "2g", "--pids-limit", "128",
              "--ulimit", "core=0", "--ulimit", "fsize=67108864:67108864",
              "--user", f"{os.getuid()}:{os.getgid()}",
              "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp",
              "-e", "HOME=/tmp"]
    inputs = []
    union: dict[str, set[int]] = {}
    with tempfile.TemporaryDirectory(prefix="parsarium-java-queue-") as temp:
        scratch = Path(temp)
        for number, (label, original) in enumerate(selected):
            try:
                descriptor = os.open(original, os.O_RDONLY | os.O_NOFOLLOW)
            except OSError as error:
                raise QueueCoverageError(f"queue input cannot be opened without links: {label}") from error
            with os.fdopen(descriptor, "rb") as source:
                metadata = os.fstat(source.fileno())
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_CASE_BYTES:
                    raise QueueCoverageError(f"queue input is invalid or too large: {label}")
                data = source.read(MAX_CASE_BYTES + 1)
            if len(data) != metadata.st_size:
                raise QueueCoverageError(f"queue input changed while reading: {label}")
            sample = scratch / f"{number:03d}.input"
            sample.write_bytes(data)
            coverage_dir = scratch / f"coverage-{number:03d}"
            coverage_dir.mkdir()
            container_name = f"parsarium-report-{uuid.uuid4().hex[:16]}"
            mounts = ["-v", f"{sample}:/input/control:ro",
                      "-v", f"{coverage_dir}:/coverage"]
            command = [*common, "--name", container_name, *mounts,
                       "--entrypoint", "java", image_id, *vm_args,
                       "GenericHarness", "/input/control"]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL, timeout=timeout)
                status, exit_code = ("ok" if result.returncode == 0 else "exit"), result.returncode
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "rm", "-f", container_name],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
                status, exit_code = "timeout", None
            if exit_code in (125, 126, 127):
                raise QueueCoverageError(f"Docker could not replay queue input {label} (exit {exit_code})")
            profile = coverage_dir / "jacoco.exec"
            item = {"queue_path": label, "sha256": sha256(data).hexdigest(),
                    "bytes": len(data), "status": status, "exit_code": exit_code,
                    "profile_files": 0, "report_xml": []}
            if profile.is_file():
                if profile.stat().st_size > MAX_INTERPRETED_TRACE_BYTES:
                    raise QueueCoverageError(f"JaCoCo execution profile exceeds size limit: {label}")
                item["profile_files"] = 1
                item["profile_sha256"] = digest(profile)
                for report in reports:
                    report_command = [*common, "--name", f"parsarium-report-{uuid.uuid4().hex[:16]}",
                                      "-v", f"{coverage_dir}:/coverage",
                                      "--entrypoint", "java", image_id,
                                      "-jar", "/work/jacococli.jar", "report", "/coverage/jacoco.exec",
                                      "--classfiles", report["classfiles"],
                                      "--sourcefiles", report["sourcefiles"],
                                      "--xml", report["xml"], "--quiet"]
                    try:
                        output = subprocess.run(report_command, stdout=subprocess.DEVNULL,
                                                stderr=subprocess.DEVNULL, timeout=timeout)
                    except subprocess.TimeoutExpired as error:
                        raise QueueCoverageError("JaCoCo source report timed out") from error
                    xml_file = coverage_dir / Path(report["xml"]).name
                    if output.returncode or not xml_file.is_file():
                        raise QueueCoverageError("JaCoCo source report failed")
                    item["report_xml"].append({"sha256": digest(xml_file),
                                                "sourcefiles": report["sourcefiles"]})
                    for filename, lines in java_jacoco_lines(
                            xml_file, report["sourcefiles"], prefixes).items():
                        union.setdefault(filename, set()).update(lines)
            inputs.append(item)
            if sum(path.stat().st_size for path in scratch.rglob("jacoco.exec")) > MAX_PROFILE_BYTES:
                raise QueueCoverageError("JaCoCo profiles exceed reporting size limit")
        replay = {"status": "source_replay" if union else "no_profiles",
                  "mechanism": "JaCoCo source report from verified Java control image",
                  "plan_sha256": digest(run_dir / "plan.json"),
                  "afl_image_id": plan["image_id"], "coverage_image_id": image_id,
                  "coverage_binary": "java GenericHarness", "llvm_cov_objects": [],
                  "control_script_sha256": digest(evidence["project"] / "run-control.sh"),
                  "source_report_roots": reports,
                  "queue_inputs_available": total, "queue_inputs_sampled": len(inputs),
                  "selection": "lexicographically first AFL id files across instances",
                  "timeout_seconds_per_input": timeout, "inputs": inputs}
        if not union:
            return replay, None
        coverage = {"data": [{"files": [
            {"filename": name, "executed_lines": sorted(lines),
             "summary": {"lines": {"covered": len(lines)}}}
            for name, lines in sorted(union.items())]}]}
        exported = scratch / "coverage.json"
        exported.write_text(json.dumps(coverage, sort_keys=True) + "\n")
        if exported.stat().st_size > MAX_EXPORT_BYTES:
            raise QueueCoverageError("aggregate Java source export exceeds size limit")
        replay["coverage_sha256"] = digest(exported)
        replay["coverage_bytes"] = exported.stat().st_size
    return replay, coverage
