"""Preflight AFL++ seed and command preparation for every verified project."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for


def check(relative: Path, scratch: Path) -> dict:
    project, manifest = project_for(*relative.parts)
    run_dir = scratch / "-".join(relative.parts)
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/prepare_afl_run.py"),
         *relative.parts, str(run_dir)], cwd=ROOT,
        capture_output=True, text=True, timeout=90,
    )
    if result.returncode:
        raise RuntimeError(result.stderr[-1000:])
    plan = json.loads((run_dir / "plan.json").read_text())
    receipt_path = ROOT / "fuzzing/afl-native" / relative / "verification.json"
    receipt = json.loads(receipt_path.read_text())
    assert plan["project"] == str(relative)
    assert plan["unique_seeds"] == 1
    assert plan["image_id"] == receipt["image_id"]
    assert plan["control_sha256"] == manifest["control_sha256"]
    assert plan["overlay_receipt_sha256"] == sha256(receipt_path.read_bytes()).hexdigest()
    php_native = (manifest["ecosystem"] == "php" and manifest.get("fuzz_engine") == "AFL++"
                  and (manifest.get("kind") == "standard" or manifest.get("afl_entrypoint")))
    if manifest.get("coverage_kind") == "native_binary_edges":
        expected_tail = ["--", "/opt/venv/bin/python", "/work/binary-run-once.py", "@@"]
    elif php_native:
        expected_tail = ([manifest["afl_entrypoint"], "@@"] if manifest.get("afl_entrypoint")
                         else ["/opt/php/bin/php", "/work/fuzz-target.php", "@@"])
    else:
        expected_tail = (["/work/afl_proxy", "@@"] if manifest["ecosystem"] in
                                      {"go", "java", "javascript", "python", "php"} else
                                      ["--", "/work/afl_fuzzer", "@@"] if manifest["ecosystem"] == "rust" else
                                      ["--", manifest.get("afl_entrypoint", "/work/fuzzer"),
                                       *(["@@"] if manifest.get("afl_file_input") is True else [])])
    assert plan["command"][-len(expected_tail):] == expected_tail
    return {"project": str(relative), "status": "ready",
            "image_id": plan["image_id"], "control_sha256": plan["control_sha256"],
            "overlay_receipt_sha256": plan["overlay_receipt_sha256"],
            "feedback_kind": plan["feedback_kind"]}


def main() -> None:
    projects = sorted(path.parent.relative_to(ROOT / "projects")
                      for path in (ROOT / "projects").glob("*/*/*/manifest.json"))
    results = []
    with tempfile.TemporaryDirectory(prefix="parsarium-afl-plans-") as temporary:
        with ThreadPoolExecutor(max_workers=4) as pool:
            tasks = {pool.submit(check, relative, Path(temporary)): relative
                     for relative in projects}
            for task in as_completed(tasks):
                relative = tasks[task]
                try:
                    results.append(task.result())
                    print(f"Ready {relative}", flush=True)
                except Exception as exc:
                    results.append({"project": str(relative), "status": "failed",
                                    "error": str(exc)})
                    print(f"FAILED {relative}: {exc}", flush=True)
    results.sort(key=lambda item: item["project"])
    report = {"schema_version": 1,
              "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "projects_total": len(results),
              "projects_ready": sum(item["status"] == "ready" for item in results),
              "results": results}
    (ROOT / "data/afl-plan-smoke.json").write_text(json.dumps(report, indent=2) + "\n")
    if report["projects_ready"] != report["projects_total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
