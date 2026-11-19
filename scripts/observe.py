"""Record what each runnable target of a format read from every file in a corpus.

`run` and `replay` go through a target's fuzz entry point and report only an
exit status. The parsed result exists in each project's verification check
(run-control.* or the Go reporter): it reads /input/control, computes an
observed summary and compares it with the control's expected value. This
command runs that verification image unchanged, with each corpus file mounted
at /input/control and /coverage on a fresh host directory, and extracts the
observed value:

1. the check passed: observed is the check's summary output (the expected value);
2. an observed file the check wrote to /coverage (observed.json, observed.raw, tree.json);
3. the "mismatch: <value>" message the check failed with (JSON, Python literal,
   or Go %+v; otherwise kept as observed_raw).

Every (target, input) pair gets one JSON line in RESULTS/<ecosystem>/<slug>.jsonl
with class accepted, rejected, harness_error or timeout. Coverage steps that
run after the comparison may fail or time out without turning an accepted
observation into an error. Existing records are skipped, so an interrupted
run resumes; --retry-errors reruns harness_error and timeout records.
"""

import argparse
import ast
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
import time
import uuid


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 1
TAIL = 4000
MAX_CASE_BYTES = 1 << 20
# Files a verification check writes before comparing, in the order they are read.
OBSERVED_FILES = ("observed.json", "observed.raw", "tree.json")
MISMATCH = re.compile(r"mismatch: ")
# Failures raised only after the check compared the observed value and found it equal.
POST_COMPARISON = re.compile(
    r"no (?:instrumented )?[\w .+/-]*?(?:source )?lines covered|missing coverage in|"
    r"underlying parser source was not instrumented", re.IGNORECASE)
# Failures that are about the container or the check, not the parser.
INFRASTRUCTURE = [
    (re.compile(r"Unable to find image|No such image|pull access denied"), "image missing"),
    (re.compile(r"exec format error"), "wrong image platform"),
    (re.compile(r"Cannot connect to the Docker daemon"), "docker daemon unreachable"),
    (re.compile(r"OCI runtime|failed to create task|Error response from daemon"), "container failed to start"),
    (re.compile(r"No space left on device"), "no space left on device"),
    (re.compile(r"Read-only file system: '/coverage|Permission denied: '/coverage|EACCES[^\n]*/coverage"),
     "coverage directory not writable"),
    (re.compile(r"Xdebug coverage extension is missing"), "coverage extension missing"),
    (re.compile(r"[Cc](?:an ?not|ould not) read valid control|No such file or directory: '/input/control'"),
     "input not mounted"),
    (re.compile(r"ModuleNotFoundError|Cannot find module|ClassNotFoundException|"
                r"NoClassDefFoundError|error while loading shared libraries"), "check environment broken"),
]


def project_id(manifest: dict, project: Path) -> str:
    return f"{manifest['format']}/{manifest['ecosystem']}/{project.name}"


# ---------------------------------------------------------------------------
# Extraction (pure functions; tested without Docker)

def plain(value):
    """Turn a Python literal into JSON-compatible data, or raise ValueError."""
    if isinstance(value, dict):
        if not all(isinstance(key, (str, int, float, bool)) or key is None for key in value):
            raise ValueError("non-scalar key")
        return {str(key) if not isinstance(key, str) else key: plain(item)
                for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise ValueError(f"not JSON data: {type(value).__name__}")


def balanced_prefix(text: str) -> str | None:
    """Return the bracketed value at the start of text, honoring quoted strings."""
    if not text or text[0] not in "{[":
        return None
    pairs = {"{": "}", "[": "]", "(": ")"}
    stack = []
    quote = None
    escaped = False
    for index, char in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
        elif char in pairs:
            stack.append(pairs[char])
        elif char in "}])":
            if not stack or stack.pop() != char:
                return None
            if not stack:
                return text[:index + 1]
    return None


def go_field_tags(sources: list[str]) -> dict[str, str]:
    """Map Go struct field names to their json tag names."""
    tags = {}
    for source in sources:
        for name, tag in re.findall(r'(?m)^\s*([A-Z]\w*)\s+[^`\n]*`[^`]*json:"([^",]+)', source):
            tags.setdefault(name, tag)
    return tags


def parse_go_value(text: str, tags: dict[str, str]):
    """Parse the %+v rendering of a struct of numbers, strings, bools and slices."""
    position = 0

    def skip():
        nonlocal position
        while position < len(text) and text[position] == " ":
            position += 1

    def value():
        nonlocal position
        skip()
        if text.startswith("{", position):
            position += 1
            result = {}
            while True:
                skip()
                if text.startswith("}", position):
                    position += 1
                    return result
                match = re.compile(r"([A-Za-z_]\w*):").match(text, position)
                if not match:
                    raise ValueError("expected field name")
                position = match.end()
                result[tags.get(match.group(1), match.group(1).lower())] = value()
        if text.startswith("[", position):
            position += 1
            result = []
            while True:
                skip()
                if text.startswith("]", position):
                    position += 1
                    return result
                result.append(value())
        if text.startswith("<nil>", position):
            position += 5
            return None
        match = re.compile(r"[^\s{}\[\]]+").match(text, position)
        if not match:
            raise ValueError("expected scalar")
        position = match.end()
        token = match.group(0)
        if token in {"true", "false"}:
            return token == "true"
        try:
            return int(token)
        except ValueError:
            pass
        try:
            return float(token)
        except ValueError:
            return token

    parsed = value()
    return parsed, text[:position]


def decode_value(text: str, go_tags: dict[str, str] | None = None) -> tuple[bool, object, str]:
    """Decode the value after "mismatch: ". Returns (ok, value, raw text)."""
    if go_tags is not None and text.startswith("got {"):
        try:
            value, raw = parse_go_value(text[4:], go_tags)
            return True, value, raw
        except (ValueError, IndexError):
            return False, None, text.splitlines()[0] if text else ""
    candidate = balanced_prefix(text)
    if candidate is None:
        line = text.splitlines()[0] if text else ""
        candidate = re.sub(r" in /\S+:\d+$", "", line).strip()
    try:
        value, _ = json.JSONDecoder().raw_decode(text)
        return True, value, text[:len(candidate)] if candidate else text
    except ValueError:
        pass
    try:
        return True, json.loads(candidate), candidate
    except ValueError:
        pass
    try:
        return True, plain(ast.literal_eval(candidate)), candidate
    except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
        return False, None, candidate


def message_observation(text: str, go_tags: dict[str, str] | None = None) -> dict | None:
    """Find the first decodable "mismatch: <value>" in the check's output."""
    raw_fallback = None
    for match in MISMATCH.finditer(text):
        rest = text[match.end():]
        if rest.startswith(("${", "{observed", "%", "' .", '" .')):
            continue  # source line of the check, printed in a stack trace
        ok, value, raw = decode_value(rest, go_tags)
        if ok:
            return {"observed": value, "route": "mismatch_message"}
        if raw and raw_fallback is None:
            raw_fallback = raw
    if raw_fallback is not None:
        return {"observed_raw": raw_fallback[:TAIL], "route": "mismatch_message_raw"}
    return None


def file_observation(files: dict[str, str]) -> dict | None:
    for name in OBSERVED_FILES:
        text = files.get(name)
        if text is None or not text.strip():
            continue
        candidates = [text]
        if name == "observed.raw":
            candidates = [line for line in reversed(text.strip().splitlines()) if line.strip()][:1]
        for candidate in candidates:
            try:
                return {"observed": json.loads(candidate), "route": f"file:{name}"}
            except ValueError:
                continue
    return None


def parser_error(stdout: str, stderr: str, files: dict[str, str]) -> str:
    """Pick the line that best states why the parser or harness failed."""
    text = stderr + "\n" + stdout
    patterns = [
        r"harness_test\.go:\d+: (.+)",                                   # Go t.Fatal
        r"panic: (.+)",                                                  # Go panic
        r"Uncaught ([\w\\]+(?:Exception|Error)[^\n]*?)(?: in /\S+:\d+)?$",  # PHP
        r'Exception in thread "main" (.+)',                              # Java
        r"Caused by: (.+)",                                              # Java
        r"^(?:Uncaught )?([\w.$]*(?:Error|Exception|Exit)(?:: .*)?)$",  # JS / Python
        r"thread '[^']*' panicked at (.+)",                              # Rust
        r"^Error: (.+)$",                                                # Rust main()
    ]
    for pattern in patterns:
        found = re.findall(pattern, text, re.MULTILINE)
        found = [item for item in found if "control replay failed" not in item]
        if found:
            return found[-1].strip()[:1000]
    observed = files.get("observed.json") or files.get("observed.raw") or ""
    lines = [line.strip() for line in (observed + "\n" + stderr).splitlines() if line.strip()]
    return lines[-1][:1000] if lines else ""


PROGRAMMING_ERRORS = re.compile(
    r"\b(?:TypeError|IndexError|KeyError|AttributeError|NameError|UnboundLocalError|ZeroDivisionError|"
    r"ReferenceError|NullPointerException|ArrayIndexOutOfBoundsException|IndexOutOfBoundsException|"
    r"ClassCastException|ArithmeticException|ArgumentCountError|runtime error: index out of range|"
    r"invalid memory address or nil pointer dereference)\b")


def harness_frame(text: str) -> str | None:
    """Return the harness location when a programming error was raised in harness code.

    A harness that assumes the control's layout (four channels, two pixels) can fail
    while summarizing a result the parser produced; that is not a parser rejection.
    """
    def own(path: str) -> bool:
        return (path.startswith("/work/") and not re.search(
            r"site-packages|dist-packages|node_modules|/vendor/|/lib/python", path))

    # Python: innermost traceback frame, then the exception line.
    frames = re.findall(r'^\s*File "([^"]+)", line (\d+)', text, re.MULTILINE)
    final = re.findall(r"^([\w.]+(?:Error|Exception)\b.*)$", text, re.MULTILINE)
    if frames and final and PROGRAMMING_ERRORS.search(final[-1]) and own(frames[-1][0]):
        return f"{frames[-1][0]}:{frames[-1][1]}: {final[-1][:300]}"
    # JavaScript: first stack frame after the error line.
    for match in re.finditer(r"^\s*(?:Uncaught )?([\w.$]*(?:Error|Exception)\b[^\n]*)\n"
                             r"\s+at (?:[^\n(]*\()?(/[^\s():]+)", text, re.MULTILINE):
        if PROGRAMMING_ERRORS.search(match.group(1)) and own(match.group(2)):
            return f"{match.group(2)}: {match.group(1)[:300]}"
    # Java: first frame is a class in the default package (the harness classes).
    for match in re.finditer(r"([\w.$]*(?:Error|Exception)\b[^\n]*)\n\s+at ([\w.$<>]+)\(", text):
        method = match.group(2)
        if PROGRAMMING_ERRORS.search(match.group(1)) and "." not in method.rsplit(".", 1)[0]:
            return f"{method}: {match.group(1)[:300]}"
    # PHP: fatal error location.
    match = re.search(r"Uncaught ((?:TypeError|Error|ArgumentCountError|DivisionByZeroError)[^\n]*?) in (/\S+):(\d+)", text)
    if match and own(match.group(2)):
        return f"{match.group(2)}:{match.group(3)}: {match.group(1)[:300]}"
    # Go: panic whose first frame after the goroutine header is harness code.
    match = re.search(r"panic: ([^\n]*)[\s\S]*?goroutine \d+ \[running\]:\n(?:[^\n]*\n\s+[^\n]*\n)*?"
                      r"[^\n]*\n\s+(\S*harness[^\s:]*\.go):(\d+)", text)
    if match and PROGRAMMING_ERRORS.search(match.group(1)):
        return f"{match.group(2)}:{match.group(3)}: panic: {match.group(1)[:300]}"
    return None


def same_value(left, right) -> bool:
    return json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True)


def classify(expected, exit_code: int | None, stdout: str, stderr: str,
             files: dict[str, str], timed_out: bool,
             go_tags: dict[str, str] | None = None) -> dict:
    """Classify one verification-check run. `files` maps /coverage names to text."""
    text = stderr + "\n" + stdout
    if not timed_out and exit_code == 0:
        try:
            summary = json.loads(files.get("summary.json", ""))
            observed = summary["output"]
            route = "check_passed:summary"
        except (ValueError, KeyError, TypeError):
            observed, route = expected, "check_passed:expected_output"
        return {"class": "accepted", "observed": observed, "observed_route": route,
                "matches_control_expected": same_value(observed, expected),
                "check_completed": True}
    from_file = file_observation(files)
    from_message = message_observation(text, go_tags)
    found = from_file or (from_message if from_message and "observed" in from_message else None)
    if found:
        record = {"class": "accepted", "observed": found["observed"], "observed_route": found["route"],
                  "matches_control_expected": same_value(found["observed"], expected),
                  "check_completed": False}
        if from_file and from_message and "observed" in from_message and not same_value(
                from_file["observed"], from_message["observed"]):
            record["message_observed"] = from_message["observed"]
        if timed_out:
            record["timed_out_after_observation"] = True
        return record
    if from_message:
        return {"class": "accepted", "observed": None, "observed_raw": from_message["observed_raw"],
                "observed_route": from_message["route"], "matches_control_expected": False,
                "check_completed": False}
    if not timed_out and POST_COMPARISON.search(text):
        return {"class": "accepted", "observed": expected, "observed_route": "post_comparison_failure",
                "matches_control_expected": True, "check_completed": False,
                "error": POST_COMPARISON.search(text).group(0)}
    if timed_out:
        return {"class": "timeout"}
    if exit_code in {125, 126, 127}:
        return {"class": "harness_error", "error": f"docker run exit {exit_code}: "
                + parser_error(stdout, stderr, files)}
    location = harness_frame(text)
    if location:
        return {"class": "harness_error", "error": "harness failed while summarizing the result: " + location}
    for pattern, reason in INFRASTRUCTURE:
        if pattern.search(text):
            return {"class": "harness_error", "error": f"{reason}: " + parser_error(stdout, stderr, files)}
    if exit_code == 137:
        return {"class": "harness_error", "error": "killed (exit 137, likely out of memory)"}
    message = parser_error(stdout, stderr, files)
    return {"class": "rejected", "error": message or f"exit code {exit_code} with no message"}


# ---------------------------------------------------------------------------
# Docker

def select_targets(format_name: str, ecosystem: str | None, wanted: list[str]) -> list[tuple[Path, dict]]:
    from run_format import targets

    selected = targets(format_name, ecosystem)
    if wanted:
        names = {item.strip("/") for item in wanted}
        selected = [(path, manifest) for path, manifest in selected
                    if f"{manifest['ecosystem']}/{path.parent.name}" in names
                    or project_id(manifest, path.parent) in names]
        known = {f"{m['ecosystem']}/{p.parent.name}" for p, m in selected} | {
            project_id(m, p.parent) for p, m in selected}
        missing = sorted(names - known)
        if missing:
            raise ValueError(f"not a runnable {format_name} target: {', '.join(missing)}")
    return selected


def prepare_image(path: Path, manifest: dict) -> dict:
    from docker_slots import docker_build_slot
    from run_case import image_for, project_for

    project = path.parent
    try:
        project, manifest = project_for(manifest["format"], manifest["ecosystem"], project.name)
        with docker_build_slot():
            image, image_id = image_for(project, manifest)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        return {"error": str(error)[-2000:]}
    receipt_id = None
    for name in ("verification.json", "control-verification.json"):
        receipt = project / name
        if receipt.is_file():
            receipt_id = json.loads(receipt.read_text()).get("image_id")
            break
    go_tags = None
    if manifest["ecosystem"] == "go":
        go_tags = go_field_tags([source.read_text(errors="replace") for source in sorted(project.glob("*.go"))])
    return {"image": image, "image_id": image_id, "image_matches_receipt": image_id == receipt_id,
            "go_tags": go_tags}


def tmpfs_for(manifest: dict) -> str:
    if manifest.get("coverage_kind") == "native_source_afl_feedback":
        return "/tmp:rw,exec,nosuid,size=256m"
    return "/tmp:rw,exec,nosuid,size=64m" if manifest.get("tmpfs_exec") else "/tmp:rw,nosuid,size=64m"


def read_coverage_files(directory: Path) -> dict[str, str]:
    files = {}
    for name in (*OBSERVED_FILES, "summary.json"):
        path = directory / name
        if path.is_file() and path.stat().st_size <= 64 << 20:
            files[name] = path.read_text(errors="replace")
    return files


def observe_one(manifest: dict, image: dict, case: Path, timeout: int) -> dict:
    data = case.read_bytes()
    base = {"input_sha256": sha256(data).hexdigest(), "input_bytes": len(data),
            "image": image["image"], "image_id": image["image_id"],
            "image_matches_receipt": image["image_matches_receipt"]}
    if len(data) > MAX_CASE_BYTES:
        return {**base, "class": "harness_error", "error": f"input larger than {MAX_CASE_BYTES} bytes",
                "exit_code": None, "duration_seconds": 0.0}
    name = f"parsarium-observe-{uuid.uuid4().hex[:16]}"
    with tempfile.TemporaryDirectory(prefix="parsarium-observe-") as tmp:
        coverage = Path(tmp) / "coverage"
        coverage.mkdir()
        command = ["docker", "run", "--rm", "--name", name, "--pull", "never",
                   "--platform", manifest["platform"], "--network", "none", "--read-only",
                   "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
                   "--user", f"{os.getuid()}:{os.getgid()}", "--tmpfs", tmpfs_for(manifest),
                   "--mount", f"type=bind,src={case},dst=/input/control,readonly",
                   "--mount", f"type=bind,src={coverage},dst=/coverage",
                   image["image"]]
        started = time.monotonic()
        timed_out = False
        try:
            result = subprocess.run(command, capture_output=True, text=True, errors="replace",
                                    timeout=timeout)
            exit_code, stdout, stderr = result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired as expired:
            try:
                subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=120)
            except subprocess.TimeoutExpired:
                pass  # a busy daemon removes the container later; never abort the run for it
            timed_out, exit_code = True, None

            def text(value):
                return value.decode(errors="replace") if isinstance(value, bytes) else (value or "")
            stdout, stderr = text(expired.stdout), text(expired.stderr)
        elapsed = round(time.monotonic() - started, 3)
        files = read_coverage_files(coverage)
    record = classify(manifest["expected_output"], exit_code, stdout, stderr, files, timed_out,
                      image.get("go_tags"))
    return {**base, **record, "exit_code": exit_code, "duration_seconds": elapsed,
            "stdout_tail": stdout[-TAIL:], "stderr_tail": stderr[-TAIL:]}


# ---------------------------------------------------------------------------
# Records

def corpus_files(corpus: Path) -> list[tuple[str, Path]]:
    files = [(str(path.relative_to(corpus)), path.resolve()) for path in sorted(corpus.rglob("*"))
             if path.is_file() and not path.name.startswith(".")]
    if not files:
        raise ValueError(f"no files in {corpus}")
    return files


def load_records(path: Path) -> dict[tuple[str, str], dict]:
    records = {}
    if path.is_file():
        for line in path.read_text().splitlines():
            try:
                record = json.loads(line)
                records[(record["input"], record["input_sha256"])] = record
            except (ValueError, KeyError):
                continue  # a line cut short by an interrupted run is redone
    return records


def write_sorted(path: Path, records: dict) -> None:
    lines = [json.dumps(records[key], sort_keys=True) for key in sorted(records)]
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False) as handle:
        handle.write("".join(line + "\n" for line in lines))
        temporary = Path(handle.name)
    temporary.replace(path)


def control_only(records: dict, control_sha: str) -> bool:
    others = [record for (_, digest), record in records.items() if digest != control_sha]
    control = [record for (_, digest), record in records.items() if digest == control_sha]
    return bool(others and control) and all(record["class"] == "rejected" for record in others) and all(
        record["class"] == "accepted" for record in control)


def constant_observation(records: dict) -> bool:
    values = {json.dumps(record.get("observed"), sort_keys=True) for record in records.values()
              if record["class"] == "accepted" and "observed" in record}
    accepted = sum(1 for record in records.values() if record["class"] == "accepted")
    return accepted >= 3 and len(values) == 1


def summarize(results: Path, selected: list[tuple[Path, dict]], inputs: list[tuple[str, Path]],
              format_name: str, build_errors: dict) -> dict:
    expected_keys = {(name, sha256(path.read_bytes()).hexdigest()) for name, path in inputs}
    targets = []
    for path, manifest in selected:
        ecosystem, slug = manifest["ecosystem"], path.parent.name
        records = load_records(results / ecosystem / f"{slug}.jsonl")
        records = {key: value for key, value in records.items() if key in expected_keys}
        counts = Counter(record["class"] for record in records.values())
        routes = Counter(record.get("observed_route") for record in records.values()
                         if record["class"] == "accepted")
        targets.append({
            "target": f"{ecosystem}/{slug}", "package": manifest["package"],
            "kind": manifest.get("kind", "third_party"),
            "records": len(records),
            "fully_classified": len(records) == len(expected_keys) and counts["harness_error"] == 0,
            "classes": dict(sorted(counts.items())),
            "observed_routes": dict(sorted(routes.items())),
            "matches_control_expected": sum(1 for record in records.values()
                                            if record.get("matches_control_expected")),
            "observed_raw": sum(1 for record in records.values() if "observed_raw" in record),
            # Accepts only its own control: often a harness gated on the control's shape
            # (for example width 2, height 1) rather than a parser rejection.
            "rejects_every_other_input": control_only(records, manifest["control_sha256"]),
            # Same observed value for every accepted input: the harness reports something
            # fixed (for example a thumbnail of the control's size), not what was read.
            "observed_constant": constant_observation(records),
            **({"image_error": build_errors[f"{ecosystem}/{slug}"]}
               if f"{ecosystem}/{slug}" in build_errors else {}),
        })
    by_ecosystem = {}
    for item in targets:
        ecosystem = item["target"].split("/")[0]
        entry = by_ecosystem.setdefault(ecosystem, {"targets": 0, "fully_classified": 0, "classes": Counter()})
        entry["targets"] += 1
        entry["fully_classified"] += item["fully_classified"]
        entry["classes"].update(item["classes"])
    for entry in by_ecosystem.values():
        entry["classes"] = dict(sorted(entry["classes"].items()))
    return {"schema_version": SCHEMA_VERSION, "format": format_name,
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "inputs": [{"input": name, "input_sha256": sha256(path.read_bytes()).hexdigest()}
                       for name, path in inputs],
            "targets": len(targets),
            "fully_classified": sum(item["fully_classified"] for item in targets),
            "classes": dict(sorted(sum((Counter(item["classes"]) for item in targets), Counter()).items())),
            "rejects_every_other_input": [item["target"] for item in targets if item["rejects_every_other_input"]],
            "observed_constant": [item["target"] for item in targets if item["observed_constant"]],
            "by_ecosystem": dict(sorted(by_ecosystem.items())),
            "results": targets}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("format")
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--ecosystem")
    parser.add_argument("--target", action="append", default=[],
                        help="ECOSYSTEM/SLUG (repeatable); default: every runnable target")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--retry-errors", action="store_true",
                        help="rerun records classified harness_error or timeout")
    parser.add_argument("--list", action="store_true", help="show the selected targets and inputs only")
    args = parser.parse_args()
    if not 1 <= args.workers <= 16 or args.timeout < 1:
        parser.error("workers must be 1-16 and timeout positive")
    if not args.corpus.is_dir():
        parser.error("--corpus must be a directory")
    selected = select_targets(args.format, args.ecosystem, args.target)
    if not selected:
        parser.error("no runnable targets match")
    inputs = corpus_files(args.corpus.resolve())
    if args.list:
        print(f"{len(selected)} targets x {len(inputs)} inputs")
        for path, manifest in selected:
            print(f"{manifest['ecosystem']}/{path.parent.name}")
        return 0
    results = args.results.resolve()
    results.mkdir(parents=True, exist_ok=True)
    hashes = {name: sha256(path.read_bytes()).hexdigest() for name, path in inputs}

    existing = {}
    jobs = []
    for path, manifest in selected:
        key = f"{manifest['ecosystem']}/{path.parent.name}"
        records = load_records(results / manifest["ecosystem"] / f"{path.parent.name}.jsonl")
        if args.retry_errors:
            records = {k: v for k, v in records.items() if v["class"] not in {"harness_error", "timeout"}}
        existing[key] = records
        for name, case in inputs:
            if (name, hashes[name]) not in records:
                jobs.append((path, manifest, name, case))
    print(f"{len(selected)} targets x {len(inputs)} inputs: {len(jobs)} to run", flush=True)

    needed = {}
    for path, manifest, _, _ in jobs:
        needed[f"{manifest['ecosystem']}/{path.parent.name}"] = (path, manifest)
    images, build_errors = {}, {}
    with ThreadPoolExecutor(max_workers=min(args.workers, 4)) as pool:
        futures = {pool.submit(prepare_image, path, manifest): key for key, (path, manifest) in needed.items()}
        for future in as_completed(futures):
            key = futures[future]
            image = future.result()
            if "error" in image:
                build_errors[key] = image["error"]
                print(f"image error: {key}: {image['error'][-300:]}", flush=True)
            else:
                images[key] = image

    locks = {key: threading.Lock() for key in existing}

    def run(path: Path, manifest: dict, name: str, case: Path) -> tuple[str, dict]:
        key = f"{manifest['ecosystem']}/{path.parent.name}"
        identity = {"schema_version": SCHEMA_VERSION, "format": manifest["format"],
                    "target": key, "package": manifest["package"],
                    "kind": manifest.get("kind", "third_party"), "input": name}
        if key in build_errors:
            record = {**identity, "input_sha256": hashes[name], "class": "harness_error",
                      "error": "image unavailable: " + build_errors[key][-1000:],
                      "exit_code": None, "duration_seconds": 0.0}
        else:
            record = {**identity, **observe_one(manifest, images[key], case, args.timeout)}
        destination = results / manifest["ecosystem"] / f"{path.parent.name}.jsonl"
        with locks[key]:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("a") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
            existing[key][(name, record["input_sha256"])] = record
        return key, record

    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, *job) for job in jobs]
        for future in as_completed(futures):
            key, record = future.result()
            done += 1
            print(f"[{done}/{len(jobs)}] {record['class']}: {key} {record['input']}"
                  f" ({record['duration_seconds']}s)", flush=True)
    for path, manifest in selected:
        key = f"{manifest['ecosystem']}/{path.parent.name}"
        destination = results / manifest["ecosystem"] / f"{path.parent.name}.jsonl"
        if existing[key]:
            write_sorted(destination, existing[key])
    summary = summarize(results, selected, inputs, args.format, build_errors)
    (results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"targets": summary["targets"], "fully_classified": summary["fully_classified"],
                      "classes": summary["classes"]}))
    print(f"Saved {results / 'summary.json'}")
    return 0 if summary["fully_classified"] == summary["targets"] else 1


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main())
