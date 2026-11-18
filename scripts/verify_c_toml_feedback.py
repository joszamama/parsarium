"""Audit parser-scoped coverage and AFL++ feedback for the C TOML paths on two valid controls.

For each path the base image's replay prints the typed tree built from the parser's own value
tree; it must equal the hand-written expected tree of both controls. The parser-only probe
(parse and free, no traversal or printing) gives own-library source lines under LLVM coverage in
the base image and AFL++ tuples under a parser-scoped allowlist in the overlay image. Each control
is probed three times; repeats must be identical and the two controls must differ.

Writes fuzzing/afl-native/toml/c/<slug>/differential.json and data/c/toml/afl-feedback.json.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ("tomlc17",)
REPORT = ROOT / "data/c/toml/afl-feedback.json"
REPEATS = 3


def run(command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-3000:])
    return result.stdout


def coverage_view(path, prefix):
    """Covered line set (segment entries with a nonzero count) and per-file covered-line summary."""
    files = [f for f in json.loads(path.read_text())["data"][0]["files"]
             if f["filename"].startswith(prefix)]
    lines = {f'{f["filename"].removeprefix(prefix)}:{segment[0]}'
             for f in files for segment in f["segments"] if segment[2] and segment[3]}
    summary = {f["filename"].removeprefix(prefix): f["summary"]["lines"]["covered"]
               for f in files if f["summary"]["lines"]["covered"]}
    return lines, dict(sorted(summary.items()))


def by_file(items):
    counts = {}
    for item in items:
        name = item.rsplit(":", 1)[0]
        counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items()))


def check(slug):
    project = ROOT / "projects/toml/c" / slug
    overlay = ROOT / "fuzzing/afl-native/toml/c" / slug
    manifest = json.loads((project / "manifest.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    afl = json.loads((overlay / "verification.json").read_text())
    prefix = manifest["coverage_subject_prefix"]
    if afl["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise RuntimeError(f"{slug}: AFL++ overlay refers to a different project receipt")
    local = run(["docker", "image", "inspect", f"parsarium/toml-c-{slug}:local",
                 "--format", "{{.Id}}"]).strip()
    if local != base["image_id"]:
        raise RuntimeError(f"{slug}: local project image differs from its receipt")
    instrumented = run(["docker", "run", "--rm", "--platform", manifest["platform"],
                        "--entrypoint", "cat", afl["image_id"],
                        "/work/afl-instrumented-objects.txt"]).split()
    controls = [(manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                (manifest["differential_control"], manifest["differential_control_sha256"],
                 manifest["differential_expected_output"])]
    results = []
    with tempfile.TemporaryDirectory(prefix=f"parsarium-toml-{slug}-") as tmp:
        output = Path(tmp)
        for index, (name, expected_hash, expected_tree) in enumerate(controls):
            case = ROOT / name
            if sha256(case.read_bytes()).hexdigest() != expected_hash:
                raise RuntimeError(f"control changed: {name}")
            attempts = []
            for repeat in range(REPEATS):
                key = f"{index}-{repeat}"
                sandbox = ["docker", "run", "--rm", "--platform", manifest["platform"],
                           "--network", "none", "--read-only", "--cap-drop", "ALL",
                           "--security-opt", "no-new-privileges",
                           "--user", f"{os.getuid()}:{os.getgid()}",
                           "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
                           "-v", f"{case}:/input/case:ro", "-v", f"{output}:/coverage"]
                tree = json.loads(run([*sandbox, "-e", "LLVM_PROFILE_FILE=/tmp/replay.profraw",
                                       "--entrypoint", "/work/replay", base["image_id"], "/input/case"]))
                if tree != expected_tree:
                    raise RuntimeError(f"{slug}: typed TOML tree differs from the expected tree: {name}")
                script = ("set -eu; LLVM_PROFILE_FILE=/tmp/case.profraw "
                          "/work/parser-probe /input/case; "
                          "llvm-profdata merge -sparse /tmp/case.profraw -o /tmp/case.profdata; "
                          f"llvm-cov export /work/parser-probe -instr-profile=/tmp/case.profdata > /coverage/{key}.json")
                run([*sandbox, "--entrypoint", "/bin/sh", base["image_id"], "-c", script])
                lines, per_file = coverage_view(output / f"{key}.json", prefix)
                if not lines:
                    raise RuntimeError(f"no {slug} parser source lines covered")
                run([*sandbox, "-e", f"AFL_MAP_SIZE={afl['afl_map_size']}",
                     "--workdir", "/tmp", "--entrypoint", "afl-showmap", afl["image_id"],
                     "-m", "none", "-t", "10000", "-o", f"/coverage/{key}.map",
                     "--", manifest["afl_entrypoint"], "/input/case"])
                tuples = {line.split(":", 1)[0] for line in
                          (output / f"{key}.map").read_text().splitlines() if line}
                if not tuples:
                    raise RuntimeError(f"{slug}: no parser-only AFL++ tuples")
                attempts.append((lines, per_file, tuples))
            if any(attempts[0] != attempt for attempt in attempts[1:]):
                raise RuntimeError(f"{slug}: feedback varied on repeated {name}")
            results.append(attempts[0])
    (first_lines, first_files, first_tuples), (second_lines, second_files, second_tuples) = results
    line_diff = len(first_lines ^ second_lines)
    tuple_diff = len(first_tuples ^ second_tuples)
    if line_diff < 2 or tuple_diff < 2:
        raise RuntimeError(f"{slug}: valid controls did not differ in parser source and AFL++ feedback")
    if len(first_tuples) != afl["feedback_edges"]:
        raise RuntimeError(f"{slug}: control probe differs from overlay receipt")
    record = {
        "schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": f"toml/c/{slug}", "pass": True,
        "feedback_kind": "afl_clang_fast_parser_scoped_edges_and_source_lines",
        "probe": f"projects/toml/c/{slug}/parser-probe.c",
        "probe_scope": "parse the local bytes and free the result; no tree traversal, printing, or result formatting",
        "tree_oracle": "hand-written typed trees controls/toml/*.expected.json (checked against tomllib by controls/toml/check_controls.py)",
        "exact_tree_outputs_verified": True,
        "base_project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"], "overlay_image_id": afl["image_id"],
        "afl_package": afl["afl_package"], "afl_map_size": afl["afl_map_size"],
        "allowlist": f"projects/toml/c/{slug}/afl-allowlist.txt",
        "allowlist_entries": [line for line in (project / "afl-allowlist.txt").read_text().splitlines() if line],
        "afl_instrumented_objects": instrumented,
        "source_line_scope": f"covered lines under {prefix} in the parser-only probe (llvm-cov export line summaries; differences over covered segment lines)",
        "repeats_per_control": REPEATS,
        "first_control": controls[0][0], "first_sha256": controls[0][1],
        "second_control": controls[1][0], "second_sha256": controls[1][1],
        "first_parser_lines_by_file": first_files, "second_parser_lines_by_file": second_files,
        "first_parser_lines": sum(first_files.values()), "second_parser_lines": sum(second_files.values()),
        "first_segment_lines": len(first_lines), "second_segment_lines": len(second_lines),
        "parser_line_difference": line_diff,
        "first_only_lines_by_file": by_file(first_lines - second_lines),
        "second_only_lines_by_file": by_file(second_lines - first_lines),
        "first_afl_tuples": len(first_tuples), "second_afl_tuples": len(second_tuples),
        "first_only_afl_tuples": len(first_tuples - second_tuples),
        "second_only_afl_tuples": len(second_tuples - first_tuples),
        "afl_tuple_difference": tuple_diff, "repeated_feedback_identical": True,
        "second_case_kind": "valid_control",
    }
    (overlay / "differential.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"toml/c/{slug}: stable repeats; {line_diff} parser lines, {tuple_diff} AFL++ tuples differ",
          flush=True)
    return record


def main():
    slugs = sys.argv[1:] or SLUGS
    records = {slug: check(slug) for slug in slugs}
    previous = json.loads(REPORT.read_text())["results"] if REPORT.is_file() else []
    merged = {item["project"]: item for item in previous}
    for slug, record in records.items():
        merged[f"toml/c/{slug}"] = {
            "project": record["project"], "pass": True,
            "overlay_receipt_sha256": record["overlay_receipt_sha256"],
            "differential_receipt_sha256": sha256(
                (ROOT / "fuzzing/afl-native/toml/c" / slug / "differential.json").read_bytes()).hexdigest(),
            "control_afl_tuples": record["first_afl_tuples"],
            "differential_afl_tuples": record["second_afl_tuples"],
            "afl_tuple_difference": record["afl_tuple_difference"],
            "control_parser_lines": record["first_parser_lines"],
            "differential_parser_lines": record["second_parser_lines"],
            "source_line_difference": record["parser_line_difference"],
            "repeats_per_control": record["repeats_per_control"],
        }
    results = [merged[f"toml/c/{slug}"] for slug in SLUGS if f"toml/c/{slug}" in merged]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed valid second control controls/toml/typed-scalars.toml; parser-only probes with parser-scoped AFL++ allowlists and three repeats per control",
        "parser_feature_scope": "covered LLVM source lines under each pinned parser source prefix in the parser-only probe; harness and typed-tree printing excluded",
        "afl_feedback_scope": "parser-only probe with an AFL_LLVM_ALLOWLIST naming the single parser source file; the instrumented object set is checked with nm during the build",
        "standard_feedback": "none: the ISO C standard library documents no TOML API",
        "results": results}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
