"""Check no-mutation feedback evidence for Go, Java, JS, Python, and PHP.

These checks use valid controls only. They do not start fuzz campaigns or
compare feedback counts across language engines.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from run_case import ROOT, image_for, project_for
from run_corpus_batch import run_batch
from binary_feedback import check_binary_feedback
from audit_projects import lwjgl_assimp_native_feedback_verified


MANAGED = {"go", "java", "javascript", "python", "php"}


def check_one(path: Path) -> dict:
    relative = path.parent.relative_to(ROOT / "projects")
    project, manifest = project_for(*relative.parts)
    ecosystem = manifest["ecosystem"]
    verification = json.loads((project / "verification.json").read_text())
    binary = manifest.get("coverage_kind") == "native_binary_edges"
    if binary:
        assert verification["parser_source_lines_covered"] is None
        check_binary_feedback(project, ROOT, manifest, verification["binary_feedback"])
    else:
        assert verification["parser_source_lines_covered"] > 0
    with tempfile.TemporaryDirectory(prefix="parsarium-feedback-") as temp:
        scratch = Path(temp)
        corpus = scratch / "corpus"
        corpus.mkdir()
        control = ROOT / manifest["control"]
        shutil.copyfile(control, corpus / manifest["control_sha256"])
        if str(relative) == "ascii_ply/java/lwjgl_assimp":
            overlay = ROOT / "fuzzing/afl-native" / relative / "verification.json"
            record = json.loads(overlay.read_text())
            if (record.get("pass") is not True
                    or record.get("base_project_receipt_sha256") !=
                        sha256((project / "verification.json").read_bytes()).hexdigest()
                    or record.get("control_sha256") != manifest["control_sha256"]
                    or not lwjgl_assimp_native_feedback_verified(path, manifest, record)):
                raise RuntimeError("native Assimp PLY feedback is not current")
            _, image_id = image_for(project, manifest)
            feedback = {"kind": record["feedback_kind"],
                        "value": record["parser_source_features"]}
        elif binary:
            overlay = ROOT / "fuzzing/afl-native" / relative / "verification.json"
            record = json.loads(overlay.read_text())
            if (record.get("pass") is not True
                    or record.get("coverage_kind") != "native_binary_edges"
                    or record.get("source_lines_covered", False) is not None
                    or record.get("binary_feedback") != verification["binary_feedback"]
                    or record.get("base_project_receipt_sha256") !=
                    sha256((project / "verification.json").read_bytes()).hexdigest()):
                raise RuntimeError("native binary AFL++ feedback is not current")
            image_id = record["image_id"]
            feedback = {"kind": "underlying_shared_library_binary_edges",
                        "value": record["feedback_edges"]}
        elif (ecosystem == "php" and manifest.get("fuzz_engine") == "AFL++"
                and (manifest.get("kind") == "standard" or manifest.get("afl_entrypoint")
                     or manifest.get("native_campaign_supported") is False)):
            _, image_id = image_for(project, manifest)
            overlay = ROOT / "fuzzing/afl-native" / relative / "verification.json"
            record = json.loads(overlay.read_text())
            if (record.get("pass") is not True or record.get("feedback_edges", 0) <= 0
                    or record.get("base_project_receipt_sha256") !=
                    sha256((project / "verification.json").read_bytes()).hexdigest()):
                raise RuntimeError("native PHP parser AFL++ feedback is not current")
            feedback = {"kind": ("php_parser_source_lines_to_afl_bitmap"
                                 if record.get("feedback_kind") == "php_parser_source_lines_to_afl_bitmap"
                                 else "native_php_parser_afl_feedback_edges"),
                        "value": record["feedback_edges"]}
        elif ecosystem == "php":
            report = scratch / "report"
            report.mkdir()
            image, image_id = image_for(project, manifest)
            command = [
                "docker", "run", "--rm", "--platform", manifest["platform"],
                "--network", "none", "--read-only", "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges", "--tmpfs", "/tmp:rw,nosuid,size=64m",
                "-v", f"{corpus}:/corpus:ro", "-v", f"{report}:/report",
                "--entrypoint", "/usr/bin/php", image, "-d", "xdebug.mode=coverage",
                "/work/vendor/bin/php-fuzzer", "report-coverage", "/work/fuzz-target.php",
                "/corpus", "/report",
            ]
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            if suffix := (manifest.get("underlying_format_specific_coverage_file_suffix")
                          or manifest.get("format_specific_coverage_file_suffix")):
                parser_pages = [p for p in report.rglob(Path(suffix).name + ".html") if p.is_file()]
            else:
                parser_pages = [p for p in (report / "vendor" / manifest["package"]).rglob("*.php.html")
                                if p.is_file()]
            if result.returncode or not (report / "index.html").is_file() or not parser_pages:
                raise RuntimeError(f"PHP-Fuzzer parser coverage report failed: {result.stderr[-1000:]}")
            feedback = {"kind": "parser_source_coverage_report", "value": len(parser_pages)}
        else:
            outcome = run_batch(project, manifest, corpus, 120)
            if outcome is None or outcome["status"] != "ok":
                raise RuntimeError(f"valid-control engine replay failed: {outcome}")
            image_id = outcome["image_id"]
            log = outcome["stdout_tail"] + "\n" + outcome["stderr_tail"]
            if ecosystem == "go":
                match = re.search(r"coverage: ([0-9.]+)% of statements", log)
                if not match or float(match.group(1)) <= 0:
                    raise RuntimeError("Go parser package coverage was not reported")
                feedback = {"kind": "parser_package_statement_coverage_percent",
                            "value": float(match.group(1))}
            elif ecosystem == "python" and manifest.get("fuzz_engine", "").startswith("libFuzzer"):
                overlay = (ROOT / "fuzzing/afl-native" / relative / "verification.json")
                record = json.loads(overlay.read_text())
                if (record.get("pass") is not True or record.get("feedback_edges", 0) <= 0
                        or record.get("base_project_receipt_sha256") !=
                        sha256((project / "verification.json").read_bytes()).hexdigest()):
                    raise RuntimeError("native Python parser AFL++ feedback is not current")
                feedback = {"kind": "llvm_native_parser_afl_feedback_edges",
                            "value": record["feedback_edges"]}
            elif ecosystem in {"java", "python"}:
                match = re.search(r"DONE\s+cov:\s*(\d+)", log)
                if not match or int(match.group(1)) <= 0:
                    raise RuntimeError(f"{ecosystem} engine did not report positive coverage")
                feedback = {"kind": "engine_coverage_counter", "value": int(match.group(1))}
            elif ecosystem == "javascript":
                match = re.search(r"Loaded \d+ modules\s+\((\d+) inline 8-bit counters\)", log)
                if not match or int(match.group(1)) <= 0 or "--includes" not in manifest["fuzz_smoke_args"]:
                    raise RuntimeError("Jazzer.js package instrumentation was not active")
                coverage = re.search(r"DONE\s+cov:\s*(\d+)", log)
                if coverage and int(coverage.group(1)) > 0:
                    feedback = {"kind": "engine_coverage_counter", "value": int(coverage.group(1))}
                else:
                    feedback = {"kind": "engine_instrumentation_counters_available",
                                "value": int(match.group(1))}
            else:
                raise ValueError(ecosystem)
    return {"project": str(relative), "status": "verified", "ecosystem": ecosystem,
            "project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
            "control_sha256": manifest["control_sha256"], "image_id": image_id,
            "parser_source_lines_covered": verification["parser_source_lines_covered"],
            "feedback_evidence": feedback}


def main() -> None:
    paths = sorted(path for path in (ROOT / "projects").glob("*/*/*/manifest.json")
                   if path.parent.parent.name in MANAGED)
    records = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        tasks = {pool.submit(check_one, path): path for path in paths}
        for future in as_completed(tasks):
            path = tasks[future]
            relative = str(path.parent.relative_to(ROOT / "projects"))
            try:
                records.append(future.result())
                print(f"Verified {relative}", flush=True)
            except Exception as exc:
                records.append({"project": relative, "status": "failed", "error": str(exc)[-2000:]})
                print(f"FAILED {relative}: {exc}", flush=True)
    records.sort(key=lambda item: item["project"])
    report = {"schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "projects_total": len(records),
              "projects_verified": sum(item["status"] == "verified" for item in records),
              "results": records}
    (ROOT / "data/ecosystem-feedback-smoke.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['projects_verified']}/{report['projects_total']} ecosystem feedback checks passed")
    if report["projects_verified"] != report["projects_total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
