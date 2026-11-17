"""Write an offline HTML and JSON report for one verified project run.

RUN_DIR is a valid-control coverage directory written by `parsarium.py build`
(projects/F/E/S/target/coverage), a `parsarium.py replay` directory, or a
prepared AFL++ directory. `--replay-queue` measures a bounded saved queue
sample through the verified LLVM coverage image without starting AFL++.
Source text for the line view comes only from
explicit `--source CONTAINER_DIR=ARCHIVE` mappings whose SHA-256 matches the
project manifest.

Example: python3 scripts/coverage_report.py svg c libvips \
  projects/svg/c/libvips/target/coverage reports/libvips \
  --source /work/source=vips-8.18.7.tar.xz
"""

import argparse
from hashlib import sha256
import html
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
import zipfile

import run_case
from run_case import MAX_CASE_BYTES, project_for
from queue_coverage import QueueCoverageError, export_objects, plan_for, queue_files, replay_queue


LLVM_EXPORT_TYPE = "llvm.coverage.json.export"
MAX_JSON_BYTES = 1 << 30
MAX_RECEIPT_BYTES = 1 << 20
MAX_SOURCE_BYTES = 4 << 20
MAX_TEXT = 300
SHA256 = re.compile(r"[0-9a-f]{64}")
# C0 controls (except tab) and bidirectional overrides are shown as code points.
UNSAFE_CHARACTERS = re.compile("[\x00-\x08\x0b-\x1f\x7f‪-‮⁦-⁩]")


class ReportError(ValueError):
    pass


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path, limit: int = MAX_JSON_BYTES):
    if not path.is_file():
        raise ReportError(f"missing file: {path}")
    if path.stat().st_size > limit:
        raise ReportError(f"file exceeds {limit} bytes: {path}")
    return json.loads(path.read_bytes())


def line_counts(segments: list) -> dict[int, int]:
    """Return {line: execution count} for mapped lines, as llvm-cov show does.

    Segments are llvm-cov export [line, column, count, has_count,
    is_region_entry, is_gap_region] entries sorted by position. This follows
    LLVM's LineCoverageIterator and LineCoverageStats.
    """
    counts: dict[int, int] = {}
    if not segments:
        return counts
    index, wrapped, line = 0, None, segments[0][0]
    while index < len(segments):
        starts = []
        while index < len(segments) and segments[index][0] == line:
            starts.append(segments[index])
            index += 1
        regions = [s for s in starts if s[3] and s[4] and not (len(s) > 5 and s[5])]
        skipped = bool(starts) and not starts[0][3] and starts[0][4]
        if not skipped and ((wrapped is not None and wrapped[3]) or regions):
            count = wrapped[2] if wrapped is not None else 0
            for segment in regions:
                count = max(count, segment[2])
            counts[line] = count
        if starts:
            wrapped = starts[-1]
        line += 1
    return counts


def clean_text(value, limit: int = MAX_TEXT) -> str:
    text = str(value)
    if len(text) > limit:
        text = text[:limit] + "…"
    return UNSAFE_CHARACTERS.sub(lambda m: f"<U+{ord(m.group()):04X}>", text)


def escape(value, limit: int = MAX_TEXT) -> str:
    return html.escape(clean_text(value, limit), quote=True)


def relative_member(container_dir: str, path: str) -> str | None:
    prefix = container_dir.rstrip("/") + "/"
    if not path.startswith(prefix):
        return None
    relative = PurePosixPath(path[len(prefix):])
    if not relative.parts or relative.is_absolute() or ".." in relative.parts:
        return None
    return str(relative)


class SourceArchive:
    """Pinned release archive mapped to the directory it was unpacked into."""

    def __init__(self, container_dir: str, path: Path, strip: int, manifest: dict):
        directory = PurePosixPath(container_dir)
        if not directory.is_absolute():
            prefixes = (manifest.get("coverage_subject_prefix", ""),
                        manifest.get("underlying_coverage_subject_prefix", ""))
            if manifest.get("ecosystem") != "go" or ".." in directory.parts or \
                    container_dir.rstrip("/") not in {prefix.rstrip("/") for prefix in prefixes}:
                raise ReportError(f"container directory must be absolute or a pinned Go "
                                  f"package prefix: {container_dir}")
        self.container_dir = container_dir.rstrip("/")
        self.path = path.resolve(strict=True)
        self.strip = strip
        self.sha256 = file_sha256(self.path)
        pins = {field: manifest[field] for field in ("source_sha256", "underlying_source_sha256")
                if field in manifest}
        matches = [field for field, value in pins.items() if value == self.sha256]
        if not matches:
            raise ReportError(f"source archive {self.path.name} has SHA-256 {self.sha256}, "
                              f"which matches no manifest source pin {sorted(pins.values())}")
        self.pinned_field = matches[0]

    def member_name(self, name: str) -> str | None:
        parts = PurePosixPath(name).parts[self.strip:]
        if not parts or ".." in parts or PurePosixPath(name).is_absolute():
            return None
        return str(PurePosixPath(*parts))

    def read(self, relatives: set[str]) -> dict[str, tuple[bytes | None, str]]:
        """Read the wanted members in one pass; oversized members map to None."""
        found: dict[str, tuple[bytes | None, str]] = {}
        if zipfile.is_zipfile(self.path):
            with zipfile.ZipFile(self.path) as archive:
                for info in archive.infolist():
                    relative = self.member_name(info.filename)
                    if info.is_dir() or relative not in relatives or relative in found:
                        continue
                    data = (archive.read(info) if info.file_size <= MAX_SOURCE_BYTES else None)
                    found[relative] = (data, info.filename)
            return found
        with tarfile.open(self.path, "r:*") as archive:
            for info in archive:
                relative = self.member_name(info.name)
                if not info.isreg() or relative not in relatives or relative in found:
                    continue
                data = (archive.extractfile(info).read() if info.size <= MAX_SOURCE_BYTES
                        else None)
                found[relative] = (data, info.name)
        return found


def output_directory(path: Path, run_dir: Path, root: Path) -> Path:
    output = path.resolve()
    for protected in (root / "website", root / "projects", root / "data",
                      root / "controls", run_dir):
        if output == protected or output.is_relative_to(protected):
            raise ReportError(f"report directory may not be inside {protected}")
    if output == root or run_dir.is_relative_to(output):
        raise ReportError("report directory may not contain the repository or run directory")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ReportError("report directory must be new or empty")
    return output


def project_evidence(root: Path, format_name: str, ecosystem: str, slug: str) -> dict:
    project, manifest = project_for(format_name, ecosystem, slug)
    source_feedback = manifest.get("coverage_kind") == "native_source_afl_feedback"
    receipt_path = project / ("control-verification.json" if source_feedback else "verification.json")
    receipt_bytes = receipt_path.read_bytes()
    receipt = json.loads(receipt_bytes)
    if source_feedback:
        receipt["parser_source_files"] = 1
    receipt_sha = sha256(receipt_bytes).hexdigest()
    if receipt.get("control_sha256") != manifest["control_sha256"] or \
            receipt.get("source_sha256") != manifest["source_sha256"]:
        raise ReportError("verification receipt pins differ from manifest")
    if receipt.get("output") != manifest["expected_output"]:
        raise ReportError("verification receipt output differs from manifest")
    control = root / manifest["control"]
    control_sha = file_sha256(control) if control.is_file() else None
    if control_sha != manifest["control_sha256"]:
        raise ReportError(f"control file hash differs from manifest: {manifest['control']}")
    overlay = None
    overlay_path = root / "fuzzing/afl-native" / format_name / ecosystem / slug / "verification.json"
    if overlay_path.is_file():
        data = read_json(overlay_path, MAX_RECEIPT_BYTES)
        base_field = "base_control_receipt_sha256" if source_feedback else "base_project_receipt_sha256"
        current = data.get(base_field) == receipt_sha and data.get("pass") is True
        overlay = {"receipt": str(overlay_path.relative_to(root)),
                   "receipt_sha256": file_sha256(overlay_path),
                   "matches_project_receipt": current}
        if current:
            overlay.update({key: data.get(key) for key in (
                "feedback_kind", "feedback_edges", "afl_package", "afl_map_size", "image_id")})
            if source_feedback:
                overlay["feedback_kind"] = "tk_png_decoder_source_edges"
                overlay["feedback_edges"] = data["control_edges"]
    return {"project": project, "manifest": manifest, "receipt": receipt,
            "identity": {
                "format": format_name, "ecosystem": ecosystem, "slug": slug,
                "kind": manifest.get("kind", "third_party"),
                "package": manifest["package"],
                "release": manifest.get("release", manifest.get("runtime")),
                "api": manifest.get("api"), "runtime": manifest.get("runtime"),
                "underlying_package": manifest.get("underlying_package"),
                "underlying_release": manifest.get("underlying_release"),
            },
            "evidence": {
                "project": str(project.relative_to(root)),
                "manifest_sha256": file_sha256(project / "manifest.json"),
                "receipt": str(receipt_path.relative_to(root)),
                "receipt_sha256": receipt_sha,
                "verified_at_utc": receipt.get("verified_at_utc"),
                "image_id": receipt.get("image_id"),
                "platform": receipt.get("platform", manifest.get("platform")),
                "toolchain": receipt.get("toolchain"),
                "source_sha256": manifest["source_sha256"],
                "underlying_source_sha256": manifest.get("underlying_source_sha256"),
                "source_lock": manifest.get("source_lock"),
                "control": manifest["control"],
                "control_sha256": manifest["control_sha256"],
            },
            "feedback": {
                "coverage_kind": manifest.get("coverage_kind", "source_lines"),
                "description": manifest.get("coverage"),
                "fuzz_engine": manifest.get("fuzz_engine", "libFuzzer" if ecosystem in
                                            {"c", "cpp", "rust"} else None),
                "afl_overlay": overlay,
                "binary_feedback": receipt.get("binary_feedback"),
                "binary_feedback_scope": receipt.get("binary_feedback_scope"),
                "native_feedback": receipt.get("native_feedback"),
                "native_feedback_limit": receipt.get("native_feedback_limit"),
            }}


def coverage_groups(manifest: dict) -> list[tuple[str, str, str, str]]:
    if manifest.get("coverage_kind") == "native_source_afl_feedback":
        decoder = (manifest["coverage_subject_prefix"].rstrip("/") +
                   manifest["format_specific_coverage_file_suffix"])
        return [("parser", decoder, "parser_source_files", "parser_source_lines_covered")]
    groups = [("parser", manifest["coverage_subject_prefix"],
               "parser_source_files", "parser_source_lines_covered")]
    if "underlying_coverage_subject_prefix" in manifest:
        groups.append(("underlying", manifest["underlying_coverage_subject_prefix"],
                       "underlying_source_files", "underlying_source_lines_covered"))
    return groups


def control_run(run_dir: Path, evidence: dict) -> tuple[dict, dict | None]:
    manifest, receipt = evidence["manifest"], evidence["receipt"]
    summary_path, coverage_path = run_dir / "summary.json", run_dir / "coverage.json"
    summary = read_json(summary_path, MAX_RECEIPT_BYTES)
    if summary.get("control_pass") is not True or summary.get("output") != manifest["expected_output"]:
        raise ReportError("control summary does not record the expected parser output")
    run = {"kind": "valid_control", "summary_sha256": file_sha256(summary_path),
           "inputs": [{"sha256": manifest["control_sha256"], "label": manifest["control"],
                       "status": "control_pass",
                       "observed_output": clean_text(json.dumps(summary["output"],
                                                                sort_keys=True), 4000)}]}
    kind = evidence["feedback"]["coverage_kind"]
    coverage = read_json(coverage_path)
    run["coverage_sha256"] = file_sha256(coverage_path)
    files = coverage["data"][0]["files"]
    if kind == "native_binary_edges":
        binding = [f for f in files if f["filename"].startswith(manifest["coverage_subject_prefix"])]
        binding_lines = sum(f["summary"]["lines"]["covered"] for f in binding)
        if binding_lines != receipt.get("binding_source_lines_covered") or \
                binding_lines != summary.get("parser_source_lines_covered"):
            raise ReportError("binding coverage differs from the verification receipt; "
                              "rerun parsarium.py build")
        return run, None
    if kind == "native_function_entries":
        if files or summary.get("parser_source_files") is not None or \
                summary.get("parser_source_lines_covered") is not None or \
                receipt.get("parser_source_files") is not None or \
                receipt.get("parser_source_lines_covered") is not None:
            raise ReportError("native function-entry path unexpectedly records parser source "
                              "lines; rerun parsarium.py build")
        return run, coverage
    for name, prefix, files_field, lines_field in coverage_groups(manifest):
        selected = [f for f in files if f["filename"].startswith(prefix)]
        covered = sum(f["summary"]["lines"]["covered"] for f in selected)
        if (len(selected), covered) != (receipt.get(files_field), receipt.get(lines_field)):
            raise ReportError(f"{name} coverage ({len(selected)} files, {covered} lines) differs "
                              f"from the verification receipt ({receipt.get(files_field)} files, "
                              f"{receipt.get(lines_field)} lines); rerun parsarium.py build")
    return run, coverage


def replay_run(run_dir: Path, evidence: dict, max_inputs: int) -> dict:
    manifest, receipt = evidence["manifest"], evidence["receipt"]
    identity = evidence["identity"]
    summary_path = run_dir / "summary.json"
    summary = read_json(summary_path, 64 << 20)
    expected = f"{identity['format']}/{identity['ecosystem']}/{identity['slug']}"
    if summary.get("schema_version") != 1 or summary.get("project") != expected:
        raise ReportError(f"replay summary is not for {expected}")
    for field in ("source_sha256", "control_sha256"):
        if summary.get(field) != manifest[field]:
            raise ReportError(f"replay {field} differs from the current manifest")
    stale = [image for image in summary.get("image_ids", []) if image != receipt.get("image_id")]
    if stale:
        raise ReportError(f"replay used image {stale[0]}, not the verified image "
                          f"{receipt.get('image_id')}")
    unique = sorted({item["sha256"] for item in summary["original_inputs"]})
    if len(unique) != summary.get("unique_inputs"):
        raise ReportError("replay summary input count is inconsistent")
    if len(unique) > max_inputs:
        raise ReportError(f"replay has {len(unique)} inputs; limit is {max_inputs}")
    receipts = {path.stem for path in (run_dir / "executions").glob("*.json")}
    if receipts != set(unique):
        raise ReportError("execution receipts do not match the replay inputs")
    paths: dict[str, list[str]] = {}
    for item in summary["original_inputs"]:
        paths.setdefault(item["sha256"], []).append(clean_text(item["path"]))
    inputs, counts, execution_image_ids = [], {}, set()
    for digest in unique:
        if not SHA256.fullmatch(digest):
            raise ReportError(f"invalid input hash: {digest!r}")
        result = read_json(run_dir / "executions" / f"{digest}.json", MAX_RECEIPT_BYTES)
        if result.get("sha256") != digest:
            raise ReportError(f"execution receipt names another input: {digest}")
        image_id = result.get("image_id")
        if image_id != receipt.get("image_id"):
            raise ReportError(f"execution receipt used image {image_id}, not the verified image "
                              f"{receipt.get('image_id')}: {digest}")
        execution_image_ids.add(image_id)
        stored = run_dir / "inputs" / digest
        if not stored.is_file() or stored.stat().st_size > MAX_CASE_BYTES or \
                file_sha256(stored) != digest:
            raise ReportError(f"preserved input is missing or altered: {digest}")
        counts[result["status"]] = counts.get(result["status"], 0) + 1
        inputs.append({"sha256": digest, "bytes": stored.stat().st_size,
                       "status": result["status"], "exit_code": result.get("exit_code"),
                       "duration_seconds": result.get("duration_seconds"),
                       "batch_replay": result.get("batch_replay", False),
                       "original_paths": paths[digest][:5]})
    if counts != summary.get("counts"):
        raise ReportError("execution receipts disagree with replay summary counts")
    if sorted(execution_image_ids) != summary.get("image_ids"):
        raise ReportError("execution receipt image IDs disagree with replay summary")
    return {"kind": "replay", "summary_sha256": file_sha256(summary_path),
            "checked_at_utc": summary.get("checked_at_utc"),
            "execution_mode": summary.get("execution_mode"),
            "generator": {key: summary.get(key) for key in (
                "generator", "generator_version", "spec", "spec_sha256", "generator_command")},
            "counts": counts, "inputs": inputs}


def afl_run(run_dir: Path, root: Path, evidence: dict, replay: bool,
            sample_limit: int, timeout: int) -> tuple[dict, dict | None]:
    plan, _ = plan_for(run_dir, root, evidence)
    total, _ = queue_files(run_dir, sample_limit)
    run = {"kind": "afl", "summary_sha256": file_sha256(run_dir / "plan.json"),
           "afl_image_id": plan["image_id"], "queue_inputs_available": total,
           "queue_sample": None, "inputs": []}
    campaign = run_dir / "campaign.json"
    if campaign.is_file():
        receipt = read_json(campaign, MAX_RECEIPT_BYTES)
        if not isinstance(receipt, dict) or receipt.get("plan_sha256") != run["summary_sha256"] or \
                receipt.get("image_id") != plan["image_id"]:
            raise ReportError("AFL++ campaign receipt differs from the prepared plan")
        run["campaign_receipt_sha256"] = file_sha256(campaign)
        run["campaign_status"] = receipt.get("status")
    if not replay:
        return run, None
    if evidence["identity"]["ecosystem"] not in {"c", "cpp"} or \
            evidence["feedback"]["coverage_kind"] != "source_lines":
        run["queue_replay_unsupported"] = (
            "Source replay currently supports LLVM-covered C/C++ projects; "
            "this project's saved AFL++ feedback remains separately documented.")
        return run, None
    try:
        export_objects(evidence["project"])
    except (QueueCoverageError, OSError) as error:
        run["queue_replay_unsupported"] = str(error)
        return run, None
    sample, coverage = replay_queue(run_dir, root, evidence, sample_limit, timeout)
    run["queue_sample"] = sample
    run["inputs"] = sample["inputs"]
    if coverage is not None:
        run["coverage_sha256"] = sample["coverage_sha256"]
    return run, coverage


def source_files(coverage: dict, manifest: dict, archives: list[SourceArchive],
                 limits: dict, executed_only: bool = False) -> tuple[list[dict], int]:
    groups = coverage_groups(manifest)
    selected, excluded = [], 0
    for item in coverage["data"][0]["files"]:
        names = [name for name, prefix, _, _ in groups if item["filename"].startswith(prefix)]
        if names:
            selected.append((item, names))
        else:
            excluded += 1
    selected.sort(key=lambda pair: pair[0]["filename"])
    wanted: dict[int, set[str]] = {}
    for item, _ in selected:
        for index, archive in enumerate(archives):
            relative = relative_member(archive.container_dir, item["filename"])
            if relative is not None:
                wanted.setdefault(index, set()).add(relative)
                break
    loaded = {index: archives[index].read(names) for index, names in wanted.items()}
    files = []
    for number, (item, names) in enumerate(selected, 1):
        if executed_only:
            observed = item.get("executed_lines")
            if not isinstance(observed, list) or any(type(n) is not int or n < 1 or n > 10_000_000
                                                     for n in observed) or observed != sorted(set(observed)):
                raise ReportError("Go executed lines are not a sorted unique list of valid line numbers")
            counts = {line: 1 for line in observed}
        else:
            counts = line_counts(item.get("segments", []))
        prefix = next(prefix for name, prefix, _, _ in groups if name == names[0])
        entry = {"number": number, "filename": item["filename"], "groups": names,
                 "relative": item["filename"][len(prefix.rsplit("/", 1)[0]) + 1:]
                 if "/" in prefix else item["filename"],
                 "line_kind": "executed_only" if executed_only else "llvm_segments",
                 "llvm_summary_lines": {"count": None if executed_only else item["summary"]["lines"]["count"],
                                        "covered": item["summary"]["lines"]["covered"]},
                 "segment_lines": {"mapped": len(counts),
                                   "covered": sum(1 for c in counts.values() if c > 0)},
                 "source": {"status": "unmapped"}, "page": None}
        entry["segment_lines"]["uncovered"] = (entry["segment_lines"]["mapped"] -
                                               entry["segment_lines"]["covered"])
        entry["segment_summary_agrees"] = executed_only or (
            entry["segment_lines"]["mapped"] == entry["llvm_summary_lines"]["count"] and
            entry["segment_lines"]["covered"] == entry["llvm_summary_lines"]["covered"])
        if executed_only and len(counts) != item["summary"]["lines"]["covered"]:
            raise ReportError("Go executed lines differ from the verified file summary")
        for index, archive in enumerate(archives):
            relative = relative_member(archive.container_dir, item["filename"])
            if relative is None:
                continue
            data, member = loaded[index].get(relative, (None, None))
            source = {"archive": archive.path.name, "archive_sha256": archive.sha256,
                      "pinned_by": archive.pinned_field, "member": member}
            if member is None:
                source["status"] = "not_in_archive"
            elif data is None:
                source["status"] = "too_large"
            else:
                text = data.decode("utf-8", errors="replace").splitlines()
                last = max(counts, default=0)
                source.update(sha256=sha256(data).hexdigest(), lines=len(text))
                if last > len(text) + 1:
                    source["status"] = "rejected_line_mismatch"
                    source["detail"] = (f"coverage maps line {last}; source has "
                                        f"{len(text)} lines")
                else:
                    source["status"] = "pinned_archive"
                    entry["_text"] = text
            entry["source"] = source
            break
        entry["_counts"] = counts
        entry["lines"] = [[line, True if executed_only else count]
                          for line, count in sorted(counts.items())]
        files.append(entry)
    return files, excluded


STYLE = """
:root{color-scheme:light dark;--fg:#1b1b1b;--bg:#fff;--muted:#555;--line:#ccc;
--hit:#d7f0dd;--miss:#fbd9dc;--link:#0b57d0}
@media (prefers-color-scheme:dark){:root{--fg:#e8e8e8;--bg:#161616;--muted:#b0b0b0;
--line:#444;--hit:#16391f;--miss:#4a1c22;--link:#8ab4f8}}
body{font:16px/1.5 system-ui,sans-serif;color:var(--fg);background:var(--bg);margin:0 auto;
max-width:72rem;padding:1rem}
a{color:var(--link)}.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem}
table{border-collapse:collapse;margin:1rem 0;width:100%}
th,td{border:1px solid var(--line);padding:.2rem .5rem;text-align:left;vertical-align:top}
td.n{text-align:right;font-variant-numeric:tabular-nums}
code,.src td.code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.85rem}
.src td{border-width:0 1px;padding:0 .5rem}.src td.code{white-space:pre;width:100%}
tr.covered,tr.executed{background:var(--hit)}tr.uncovered{background:var(--miss)}
.note{border-left:4px solid var(--line);padding:.25rem .75rem;color:var(--muted)}
.warn{border-left:4px solid #c5221f;padding:.25rem .75rem}
.src thead th{position:sticky;top:0;background:var(--bg)}
details{margin:.75rem 0}summary{cursor:pointer;font-weight:600}
.wrap{overflow-x:auto}
"""


def page(title: str, body: str) -> str:
    return ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; "
            "style-src 'unsafe-inline'\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<meta name=\"referrer\" content=\"no-referrer\">"
            f"<title>{escape(title)}</title><style>{STYLE}</style></head><body>"
            "<a class=\"skip\" href=\"#main\">Skip to content</a>"
            f"<main id=\"main\">{body}</main></body></html>\n")


def table(caption: str, headers: tuple[str, ...], rows: list[tuple], numeric=()) -> str:
    head = "".join(f"<th scope=\"col\">{escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(
        f"<td class=\"n\">{cell}</td>" if index in numeric else f"<td>{cell}</td>"
        for index, cell in enumerate(row)) + "</tr>" for row in rows)
    return (f"<div class=\"wrap\"><table><caption>{escape(caption)}</caption>"
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>")


def definition_rows(caption: str, items: dict) -> str:
    rows = "".join(f"<tr><th scope=\"row\">{escape(key.replace('_', ' '))}</th>"
                   f"<td><code>{escape(json.dumps(value) if isinstance(value, (list, dict)) else value, 2000)}</code></td></tr>"
                   for key, value in items.items() if value is not None)
    return f"<div class=\"wrap\"><table><caption>{escape(caption)}</caption><tbody>{rows}</tbody></table></div>"


def file_page(entry: dict, report: dict, max_lines: int) -> tuple[str, bool]:
    counts, text = entry["_counts"], entry.get("_text")
    executed_only = entry.get("line_kind") == "executed_only"
    numbers = range(1, len(text) + 1) if text is not None else sorted(counts)
    rows, truncated = [], False
    for shown, line in enumerate(numbers):
        if shown >= max_lines:
            truncated = True
            break
        count = counts.get(line)
        status = "" if count is None else "executed" if executed_only else "covered" if count > 0 else "uncovered"
        source = escape(text[line - 1], 10000) if text is not None else ""
        rows.append(f"<tr class=\"{status}\" id=\"L{line}\"><td class=\"n\">{line}</td>"
                    f"<td class=\"n\">{'' if count is None else 'yes' if executed_only else count}</td><td>{status}</td>"
                    f"<td class=\"code\">{source}</td></tr>")
    identity = report["identity"]
    source = entry["source"]
    notes = []
    if text is None:
        notes.append(f"<p class=\"warn\">Source text not shown: {escape(source['status'])}"
                     f"{' — ' + escape(source['detail']) if source.get('detail') else ''}. "
                     + ("Only executed line numbers are listed.</p>" if executed_only else
                        "Only mapped lines and their counts are listed.</p>"))
    if not entry["segment_summary_agrees"]:
        notes.append("<p class=\"note\">The per-line view follows the file's llvm-cov segments; "
                     "llvm-cov's file summary aggregates per-function line counts and differs here.</p>")
    if truncated:
        notes.append(f"<p class=\"warn\">Truncated after {max_lines} lines.</p>")
    line_details = ({"executed_source_lines": entry["segment_lines"]["covered"]}
                    if executed_only else {
                        "segment_mapped_lines": entry["segment_lines"]["mapped"],
                        "segment_covered_lines": entry["segment_lines"]["covered"],
                        "segment_uncovered_lines": entry["segment_lines"]["uncovered"],
                        "llvm_summary_lines": entry["llvm_summary_lines"]["count"],
                        "llvm_summary_covered": entry["llvm_summary_lines"]["covered"]})
    details = ("<details><summary>Evidence and line-count details</summary>"
            + definition_rows("Path mapping", {
                "container_path": entry["filename"],
                "archive": source.get("archive"), "archive_sha256": source.get("archive_sha256"),
                "pinned_by_manifest_field": source.get("pinned_by"),
                "archive_member": source.get("member"), "source_sha256": source.get("sha256")})
            + definition_rows("Line counts", line_details)
            + "</details>")
    summary = (f"{entry['segment_lines']['covered']} executed lines are recorded. "
               "Other lines have no execution information in this Go export."
               if executed_only else
               f"{entry['segment_lines']['covered']} of {entry['segment_lines']['mapped']} "
               "mapped lines executed.")
    caption = ("Observed execution per source line. Blank: no execution information."
               if executed_only else
               "Execution count per source line. Blank count: not instrumented.")
    body = (f"<p><a href=\"../index.html\">Report index</a></p>"
            f"<h1><code>{escape(entry['relative'], 1000)}</code></h1>"
            f"<p>{escape(identity['package'])} {escape(identity['release'])} — "
            f"{escape(', '.join(entry['groups']))} source. "
            f"{summary}</p>"
            + "".join(notes)
            + details
            + f"<div class=\"wrap\"><table class=\"src\"><caption>{caption}</caption>"
              "<thead><tr><th scope=\"col\">Line</th>"
              f"<th scope=\"col\">{'Observed' if executed_only else 'Count'}</th><th scope=\"col\">Status</th>"
              "<th scope=\"col\">Source</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table></div>")
    return page(f"{entry['relative']} — {identity['package']} coverage", body), truncated


def index_page(report: dict) -> str:
    identity, evidence, feedback = report["identity"], report["evidence"], report["feedback"]
    coverage, run = report["coverage"], report["run"]
    title = f"{identity['package']} {identity['release']} — {identity['format']}/{identity['ecosystem']}"
    parts = [f"<h1>{escape(title)}</h1>",
             "<p class=\"note\">Offline report generated from local receipts. A completed run "
             "shows that the harness ran; it is not a parser safety or defect claim.</p>"]
    evidence_details = ("<details><summary>Parser identity and evidence</summary>"
                        + definition_rows("Parser", identity)
                        + definition_rows("Evidence", {**evidence,
                            "run_directory": run["directory"],
                            "run_kind": run["kind"],
                            "afl_plan_sha256" if run["kind"] == "afl" else
                            "run_summary_sha256": run["summary_sha256"],
                            "coverage_json_sha256": run.get("coverage_sha256")})
                        + "</details>")
    overlay = feedback.get("afl_overlay")
    feedback_items = {key: feedback[key] for key in (
        "coverage_kind", "description", "fuzz_engine", "binary_feedback_scope")}
    if overlay:
        feedback_items["afl_overlay_receipt"] = overlay["receipt"]
        feedback_items["afl_overlay_matches_project_receipt"] = overlay["matches_project_receipt"]
        if overlay["matches_project_receipt"]:
            feedback_items["afl_feedback_kind"] = overlay.get("feedback_kind") or "not recorded"
            feedback_items["afl_feedback_edges"] = overlay.get("feedback_edges")
    if feedback.get("binary_feedback"):
        binary = feedback["binary_feedback"]
        feedback_items.update({"binary_feedback_kind": binary.get("feedback_kind"),
                               "binary_module": binary.get("module"),
                               "binary_module_sha256": binary.get("module_sha256"),
                               "control_tuples": binary.get("control_tuples")})
    if feedback.get("native_feedback"):
        native = feedback["native_feedback"]
        feedback_items.update({"native_feedback_kind": native.get("feedback_kind"),
                               "native_scope": native.get("scope"),
                               "baseline_functions": native.get("baseline_functions"),
                               "control_functions": native.get("control_functions"),
                               "variant_functions": native.get("variant_functions"),
                               "repeat_identical": native.get("repeat_identical"),
                               "variant_differs": native.get("variant_differs"),
                               "native_feedback_limit": feedback.get("native_feedback_limit")})
    feedback_table = definition_rows("Feedback", feedback_items)
    if run["kind"] == "replay":
        run_table = definition_rows("Replay", {"checked_at_utc": run["checked_at_utc"],
                                               "execution_mode": run["execution_mode"],
                                               "counts": run["counts"], **run["generator"]})
        rows = [(f"<code>{escape(item['sha256'])}</code>", item["bytes"], escape(item["status"]),
                 escape(item["exit_code"]) if item["exit_code"] is not None else "",
                 escape(item["duration_seconds"]) if item["duration_seconds"] is not None else "",
                 "<br>".join(escape(path) for path in item["original_paths"]))
                for item in run["inputs"]]
        run_table += table("Inputs and outcomes (input bytes are not embedded)",
                           ("SHA-256", "Bytes", "Status", "Exit", "Seconds", "Original paths"),
                           rows, numeric=(1, 3, 4))
    elif run["kind"] == "afl":
        sample = run.get("queue_sample")
        run_table = definition_rows("Prepared AFL++ run", {
            "afl_image_id": run["afl_image_id"],
            "campaign_status": run.get("campaign_status"),
            "queue_inputs_available": run["queue_inputs_available"],
            "queue_inputs_sampled": sample["queue_inputs_sampled"] if sample else 0,
            "coverage_image_id": sample["coverage_image_id"] if sample else None,
            "coverage_binary": sample["coverage_binary"] if sample else None,
            "llvm_cov_objects": sample["llvm_cov_objects"] if sample else None,
            "profdata_sha256": sample.get("profdata_sha256") if sample else None,
            "coverage_json_sha256": sample.get("coverage_sha256") if sample else None,
            "selection": sample["selection"] if sample else None,
            "timeout_seconds_per_input": sample["timeout_seconds_per_input"] if sample else None,
        })
        if sample:
            rows = [(escape(item["queue_path"], 1000), f"<code>{escape(item['sha256'])}</code>",
                     item["bytes"], escape(item["status"]),
                     item["exit_code"] if item["exit_code"] is not None else "",
                     item["profile_files"]) for item in run["inputs"]]
            run_table += table("Saved queue inputs replayed once (bytes are not embedded)",
                               ("Queue file", "SHA-256", "Bytes", "Status", "Exit", "Profiles"),
                               rows, numeric=(2, 4, 5))
    else:
        rows = [(f"<code>{escape(item['sha256'])}</code>", escape(item["label"]),
                 escape(item["status"]), f"<code>{escape(item['observed_output'], 4000)}</code>")
                for item in run["inputs"]]
        run_table = table("Valid control", ("SHA-256", "Control", "Outcome", "Observed output"),
                          rows)
    parts.append("<h2>Source-line coverage</h2>")
    parts.append(f"<p>{escape(coverage['statement'], 2000)}</p>")
    if coverage["status"] == "llvm_source_lines":
        rows = [(escape(group["name"]), f"<code>{escape(group['prefix'])}</code>", group["files"],
                 group["llvm_summary_lines"], group["llvm_summary_covered"],
                 group["segment_mapped"], group["segment_covered"])
                for group in coverage["groups"]]
        parts.append(table("Totals by source group (adapter and harness files excluded)",
                           ("Group", "Container prefix", "Files", "llvm-cov lines",
                            "llvm-cov covered", "Line-view lines", "Line-view covered"),
                           rows, numeric=(2, 3, 4, 5, 6)))
        if any(not entry["segment_summary_agrees"] for entry in coverage["files"]):
            parts.append("<p class=\"note\">The line view follows llvm-cov segments. "
                         "Its totals can differ from llvm-cov's per-function file summaries; "
                         "both are shown above.</p>")
        rows = []
        for entry in coverage["files"]:
            name = escape(entry["relative"], 1000)
            link = f"<a href=\"{entry['page']}\">{name}</a>" if entry["page"] else name
            mapped, covered = entry["segment_lines"]["mapped"], entry["segment_lines"]["covered"]
            rows.append((link, escape(", ".join(entry["groups"])), covered,
                         mapped - covered, mapped,
                         f"{100 * covered / mapped:.1f}" if mapped else "",
                         escape(entry["source"]["status"])))
        parts.append(table("Files (line-view counts from llvm-cov segments)",
                           ("File", "Group", "Covered", "Uncovered", "Mapped", "%", "Source text"),
                           rows, numeric=(2, 3, 4, 5)))
    elif coverage["status"] in {f"{language}_executed_lines" for language in
                               ("go", "python", "javascript", "java", "php")}:
        language = {"go": "Go", "python": "Python", "javascript": "JavaScript",
                    "java": "Java", "php": "PHP"}[coverage["status"].removesuffix("_executed_lines")]
        rows = [(escape(group["name"]), f"<code>{escape(group['prefix'])}</code>",
                 group["files"], group["executed_lines"]) for group in coverage["groups"]]
        parts.append(table(f"Observed {language} parser source by group",
                           ("Group", "Source prefix", "Files", "Executed lines"), rows,
                           numeric=(2, 3)))
        rows = []
        for entry in coverage["files"]:
            name = escape(entry["relative"], 1000)
            link = f"<a href=\"{entry['page']}\">{name}</a>" if entry["page"] else name
            rows.append((link, escape(", ".join(entry["groups"])),
                         entry["segment_lines"]["covered"],
                         escape(entry["source"]["status"])))
        parts.append(table("Files (executed line numbers; no denominator recorded)",
                           ("File", "Group", "Executed", "Source text"), rows, numeric=(2,)))
    elif coverage["status"] == "non_llvm_source_lines":
        rows = [(escape(group["name"]), f"<code>{escape(group['prefix'])}</code>",
                 group["files"], group["covered_lines"]) for group in coverage["groups"]]
        parts.append(table("Covered source by group (verification receipt totals; no line view)",
                           ("Group", "Container prefix", "Files", "Covered lines"), rows,
                           numeric=(2, 3)))
    elif coverage["status"] == "native_function_entries":
        native = coverage["functions"]
        rows = [("Baseline", native["baseline_functions"]),
                ("Valid control", native["control_functions"]),
                ("Valid variant", native["variant_functions"])]
        parts.append(table("Observed native parser function entries",
                           ("Input", "Functions entered"), rows, numeric=(1,)))
    for warning in report["warnings"]:
        parts.append(f"<p class=\"warn\">{escape(warning, 2000)}</p>")
    parts.append("<h2>Run outcomes</h2>")
    parts.append(run_table)
    parts.append("<h2>Feedback</h2>")
    parts.append(feedback_table)
    parts.append(evidence_details)
    return page(f"{title} coverage report", "".join(parts))


def build_report(root: Path, format_name: str, ecosystem: str, slug: str, run_dir: Path,
                 output: Path, sources: list[tuple[str, Path]], strip: int,
                 limits: dict, queue_replay: bool = False, queue_limit: int = 32,
                 queue_timeout: int = 15) -> dict:
    run_dir = run_dir.resolve(strict=True)
    output = output_directory(output, run_dir, root)
    evidence = project_evidence(root, format_name, ecosystem, slug)
    manifest = evidence["manifest"]
    archives = [SourceArchive(directory, path, strip, manifest) for directory, path in sources]
    if (run_dir / "plan.json").is_file():
        run, coverage = afl_run(run_dir, root, evidence, queue_replay, queue_limit, queue_timeout)
    elif (run_dir / "executions").is_dir():
        run, coverage = replay_run(run_dir, evidence, limits["max_inputs"]), None
    else:
        if queue_replay:
            raise ReportError("--replay-queue requires a prepared AFL++ run directory")
        run, coverage = control_run(run_dir, evidence)
    run["directory"] = str(run_dir)
    warnings = []
    if manifest.get("source_patch"):
        warnings.append("This project patches its source during the build; archive text may "
                        "differ from the compiled source.")
    overlay = evidence["feedback"]["afl_overlay"]
    if overlay and not overlay["matches_project_receipt"]:
        warnings.append("The AFL++ overlay receipt names a different project receipt; its "
                        "feedback counts are omitted.")
    kind = evidence["feedback"]["coverage_kind"]
    if run["kind"] == "replay":
        coverage_info = {"status": "not_recorded",
                         "statement": "Replay runs record outcomes only, not coverage. The "
                                      "project's valid-control directory reports its verified "
                                      "source coverage or native feedback."}
    elif run["kind"] == "afl" and coverage is None:
        sample = run.get("queue_sample")
        if run.get("queue_replay_unsupported"):
            statement = run["queue_replay_unsupported"]
        elif sample:
            statement = ("No LLVM profiles were produced by the bounded queue replay; "
                         "no source coverage is claimed.")
        else:
            statement = ("AFL++ saves edge feedback and queue files, not source-line coverage. "
                         "Use --replay-queue to replay up to 32 saved queue inputs in the "
                         "verified coverage image.")
        coverage_info = {"status": "unsupported" if run.get("queue_replay_unsupported") else
                         "not_recorded", "statement": statement}
    elif kind == "native_binary_edges":
        binary = evidence["feedback"]["binary_feedback"] or {}
        coverage_info = {"status": "binary_edges_only",
                         "statement": f"Native binary-edge feedback only: {binary.get('control_tuples')} "
                                      f"control tuples in {binary.get('module')}. No parser "
                                      "source-line coverage exists for this project; binding "
                                      "lines are not parser lines."}
    elif kind == "native_function_entries":
        native = evidence["feedback"]["native_feedback"]
        if not isinstance(native, dict) or native.get("feedback_kind") != \
                "native_function_entries_not_source_coverage":
            raise ReportError("native function-entry receipt is missing or inconsistent")
        coverage_info = {"status": "native_function_entries",
                         "statement": "The pinned runtime entered format-parser functions on the "
                                      "valid controls. This is function-entry feedback, not "
                                      "source-line, branch, edge, or AFL++ coverage. No source "
                                      "line view or percentage is available.",
                         "functions": native}
    elif ecosystem in {"go", "python", "javascript", "java", "php"} and \
            coverage.get("type") != LLVM_EXPORT_TYPE and all(
            "executed_lines" in item for item in coverage["data"][0]["files"]):
        files, excluded = source_files(coverage, manifest, archives, limits, executed_only=True)
        groups = []
        for name, prefix, _, _ in coverage_groups(manifest):
            members = [entry for entry in files if name in entry["groups"]]
            groups.append({"name": name, "prefix": prefix, "files": len(members),
                           "executed_lines": sum(entry["segment_lines"]["covered"]
                                                 for entry in members)})
        language, mechanism = {
            "go": ("Go", "Go coverprofile"),
            "python": ("Python", "Python trace"),
            "javascript": ("JavaScript", "V8 coverage"),
            "java": ("Java", "JaCoCo coverage"),
            "php": ("PHP", "Xdebug coverage"),
        }[ecosystem]
        coverage_info = {"status": f"{ecosystem}_executed_lines",
                         "statement": f"{mechanism} source lines executed by the verified valid "
                                      "control. The export does not record unexecuted mapped "
                                      "lines or per-line execution counts; no coverage "
                                      "percentage is inferred.",
                         "excluded_files": excluded, "groups": groups, "files": files}
        if not archives:
            warnings.append(f"No --source archive was supplied; {language} line views list executed "
                            "line numbers without source text.")
        if any(entry["source"]["status"] == "rejected_line_mismatch" for entry in files):
            warnings.append(f"Some {language} source files were rejected because executed lines exceed "
                            "the pinned archive length.")
    elif coverage.get("type") != LLVM_EXPORT_TYPE:
        receipt = evidence["receipt"]
        groups = [{"name": name, "prefix": prefix,
                   "files": receipt.get(files_field),
                   "covered_lines": receipt.get(lines_field)}
                  for name, prefix, files_field, lines_field in coverage_groups(manifest)]
        totals = "; ".join(f"{group['covered_lines']} {group['name']} source lines in "
                           f"{group['files']} {'file' if group['files'] == 1 else 'files'}"
                           for group in groups)
        coverage_info = {"status": "non_llvm_source_lines",
                         "statement": f"{totals} (verification receipt totals). This coverage "
                                      "was not exported by llvm-cov, so no line view is produced.",
                         "groups": groups}
    else:
        files, excluded = source_files(coverage, manifest, archives, limits)
        groups = []
        for name, prefix, _, _ in coverage_groups(manifest):
            members = [entry for entry in files if name in entry["groups"]]
            groups.append({"name": name, "prefix": prefix, "files": len(members),
                           "llvm_summary_lines": sum(e["llvm_summary_lines"]["count"] for e in members),
                           "llvm_summary_covered": sum(e["llvm_summary_lines"]["covered"] for e in members),
                           "segment_mapped": sum(e["segment_lines"]["mapped"] for e in members),
                           "segment_covered": sum(e["segment_lines"]["covered"] for e in members)})
        provenance = "the bounded AFL++ queue sample" if run["kind"] == "afl" else "the valid control"
        coverage_info = {"status": "llvm_source_lines",
                         "llvm_cov_export_version": coverage.get("version"),
                         "statement": f"LLVM source coverage for {provenance}. {excluded} "
                                      "instrumented files outside the parser prefixes (adapter, "
                                      "harness, system headers) are excluded.",
                         "excluded_files": excluded, "groups": groups, "files": files}
        if not archives:
            warnings.append("No --source archive was supplied; line views list counts without "
                            "source text.")
        if any(not entry["segment_summary_agrees"] for entry in files):
            warnings.append("Some per-line views differ from llvm-cov's per-function file summary; "
                            "both counts are reported.")
        if any(entry["source"]["status"] == "rejected_line_mismatch" for entry in files):
            warnings.append("Some source files were rejected because coverage maps lines beyond "
                            "their length; they may not match the compiled source.")
    report = {"schema_version": 1, "identity": evidence["identity"],
              "evidence": evidence["evidence"], "feedback": evidence["feedback"], "run": run,
              "coverage": coverage_info, "warnings": warnings,
              "limits": {key: value for key, value in limits.items()}, "truncated": []}
    write_report(output, report, limits)
    return report


def write_report(output: Path, report: dict, limits: dict) -> None:
    pages: list[tuple[Path, bytes]] = []
    pages_bytes = 0

    files = report["coverage"].get("files", [])
    budget = limits["max_report_bytes"] // 2  # the other half is for index and JSON
    for count, entry in enumerate(files):
        if count >= limits["max_files"]:
            report["truncated"].append(f"line views stop after {limits['max_files']} files")
            break
        text, cut = file_page(entry, report, limits["max_lines"])
        data = text.encode()
        if pages_bytes + len(data) > budget:
            report["truncated"].append(f"line views stop at {entry['relative']} "
                                       "(report size limit)")
            break
        entry["page"] = f"files/{entry['number']:05d}.html"
        if cut:
            report["truncated"].append(f"{entry['relative']} line view truncated")
        pages.append((Path(entry["page"]), data))
        pages_bytes += len(data)
    for entry in files:
        entry.pop("_text", None)
        entry.pop("_counts", None)
    if len(json.dumps(report).encode()) > limits["max_report_bytes"] // 2:
        for entry in files:
            entry["lines"] = None
        report["truncated"].append("per-line counts omitted from report.json (size limit)")
    report["warnings"] += [f"Truncated: {item}" for item in report["truncated"]]
    index = index_page(report).encode()
    data = (json.dumps(report, indent=1, sort_keys=True) + "\n").encode()
    total = pages_bytes + len(index) + len(data)
    if total > limits["max_report_bytes"]:
        raise ReportError(f"report needs {total} bytes, above the "
                          f"{limits['max_report_bytes']}-byte limit")
    output.mkdir(parents=True, exist_ok=True)
    if pages:
        (output / "files").mkdir()
    for relative, payload in [*pages, (Path("index.html"), index), (Path("report.json"), data)]:
        with (output / relative).open("xb") as handle:
            handle.write(payload)


def source_argument(value: str) -> tuple[str, Path]:
    directory, separator, path = value.partition("=")
    if not separator or not directory or not path:
        raise argparse.ArgumentTypeError("expected CONTAINER_DIR=ARCHIVE")
    return directory, Path(path)


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("format")
    cli.add_argument("ecosystem")
    cli.add_argument("package_slug")
    cli.add_argument("run_dir", type=Path)
    cli.add_argument("output", type=Path)
    cli.add_argument("--source", type=source_argument, action="append", default=[],
                     help="CONTAINER_DIR=ARCHIVE; the archive must match a manifest source pin")
    cli.add_argument("--strip-components", type=int, default=1)
    cli.add_argument("--max-files", type=int, default=1000)
    cli.add_argument("--max-lines-per-file", type=int, default=50000)
    cli.add_argument("--max-inputs", type=int, default=10000)
    cli.add_argument("--max-report-mib", type=int, default=256)
    cli.add_argument("--replay-queue", action="store_true",
                     help="replay a bounded saved AFL++ queue sample through the verified coverage image")
    cli.add_argument("--max-queue-inputs", type=int, default=32)
    cli.add_argument("--queue-timeout", type=int, default=15,
                     help="seconds per saved queue input (maximum 60)")
    args = cli.parse_args()
    if min(args.max_files, args.max_lines_per_file, args.max_inputs, args.max_report_mib) < 1 \
            or args.strip_components < 0 or not 1 <= args.max_queue_inputs <= 128 \
            or not 1 <= args.queue_timeout <= 60:
        cli.error("limits must be positive")
    limits = {"max_files": args.max_files, "max_lines": args.max_lines_per_file,
              "max_inputs": args.max_inputs, "max_report_bytes": args.max_report_mib << 20}
    try:
        report = build_report(run_case.ROOT, args.format, args.ecosystem, args.package_slug,
                              args.run_dir, args.output, args.source, args.strip_components,
                              limits, args.replay_queue, args.max_queue_inputs,
                              args.queue_timeout)
    except (ReportError, QueueCoverageError, OSError, KeyError, json.JSONDecodeError, tarfile.TarError,
            zipfile.BadZipFile, subprocess.SubprocessError) as error:
        raise SystemExit(f"coverage report: {error}") from error
    print(f"{report['coverage']['status']}: {args.output.resolve() / 'index.html'}")


if __name__ == "__main__":
    main()
