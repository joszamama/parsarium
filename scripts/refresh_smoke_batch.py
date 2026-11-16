"""Refresh smoke reports for newly verified managed-language paths.

Run only the named projects, then retain existing checked records. This keeps
large matrix expansions reviewable without replaying unrelated containers.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import fcntl
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for
from smoke_afl_plans import check as check_afl_plan
from smoke_case_bridge import check as check_case
from smoke_corpus_batch import check as check_batch
from smoke_ecosystem_feedback import check_one as check_feedback


def check_native_plan(relative: Path, scratch: Path) -> dict:
    project, manifest = project_for(*relative.parts)
    if manifest.get("native_campaign_supported") is False:
        rejected = subprocess.run(
            [sys.executable, str(ROOT / "scripts/prepare_native_run.py"),
             *relative.parts, str(scratch / "native" / "-".join(relative.parts))],
            capture_output=True, text=True, timeout=90,
        )
        if rejected.returncode == 0 or "unsupported" not in rejected.stderr:
            raise RuntimeError(f"native campaign was not rejected: {relative}")
        return {"project": str(relative), "status": "unsupported",
                "engine": "in-process native campaign",
                "reason": "parser state persists across inputs; use one-shot AFL++",
                "image_id": json.loads((project / "verification.json").read_text())["image_id"],
                "control_sha256": manifest["control_sha256"],
                "project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest()}
    run_dir = scratch / "native" / "-".join(relative.parts)
    prepare = subprocess.run(
        [sys.executable, str(ROOT / "scripts/prepare_native_run.py"),
         *relative.parts, str(run_dir)], capture_output=True, text=True, timeout=90,
    )
    if prepare.returncode:
        raise RuntimeError(f"native prepare {relative}: {prepare.stderr[-1000:]}")
    check = subprocess.run(
        [sys.executable, str(ROOT / "scripts/run_prepared_native.py"),
         str(run_dir), "--check"], capture_output=True, text=True, timeout=90,
    )
    if check.returncode:
        raise RuntimeError(f"native check {relative}: {check.stderr[-1000:]}")
    plan = json.loads((run_dir / "plan.json").read_text())
    if plan["control_sha256"] != manifest["control_sha256"] or plan["unique_seeds"] != 1:
        raise ValueError(f"native plan mismatch: {relative}")
    return {"project": str(relative), "status": "ready", "engine": plan["engine"],
            "image_id": plan["image_id"], "control_sha256": plan["control_sha256"],
            "project_receipt_sha256": plan["project_receipt_sha256"],
            "unique_seeds": plan["unique_seeds"]}


def update_report(name: str, additions: list[dict], count_fields: dict[str, str]) -> None:
    path = ROOT / "data" / name
    with (ROOT / "data/.smoke-report.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        report = json.loads(path.read_text())
        rows = {item["project"]: item for item in report["results"]}
        for item in additions:
            rows[item["project"]] = item
        report["results"] = [rows[key] for key in sorted(rows)]
        report["projects_total"] = len(rows)
        for field, status in count_fields.items():
            report[field] = sum(item["status"] == status for item in rows.values())
        report["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
        path.write_text(json.dumps(report, indent=2) + "\n")


def check_project(relative: Path, scratch: Path) -> dict:
    project, manifest = project_for(*relative.parts)
    if manifest["ecosystem"] not in {"python", "javascript", "go", "php", "java", "rust", "c", "cpp"}:
        raise ValueError(f"unsupported project batch ecosystem: {relative}")
    path = project / "manifest.json"
    receipt = json.loads((project / "verification.json").read_text())
    if not receipt.get("pass"):
        raise ValueError(f"project has no passing verification: {relative}")
    case = check_case(path)
    batch = check_batch(path)
    native = check_native_plan(relative, scratch)
    afl_plan = check_afl_plan(relative, scratch / "afl")
    if (case["status"] != "ok" or batch["status"] not in {"ok", "per_case_only"}
            or afl_plan["status"] != "ready"):
        raise ValueError(f"smoke check failed: {relative}")
    feedback = check_feedback(path) if manifest["ecosystem"] in {
        "python", "javascript", "go", "php", "java"} else None
    if feedback is not None and feedback["status"] != "verified":
        raise ValueError(f"feedback check failed: {relative}")
    overlay = ROOT / "fuzzing/afl-native" / relative / "verification.json"
    overlay_record = json.loads(overlay.read_text())
    if (not overlay_record["pass"] or overlay_record["base_project_receipt_sha256"] !=
            sha256((project / "verification.json").read_bytes()).hexdigest()):
        raise ValueError(f"AFL++ overlay mismatch: {relative}")
    kind = ("python_afl" if manifest["ecosystem"] == "python" else
            "rust_afl" if manifest["ecosystem"] == "rust" else
            "native_afl" if manifest["ecosystem"] in {"c", "cpp"} else "bridge_afl")
    return {"case": case, "batch": batch, "native": native,
            "afl_plan": afl_plan, "feedback": feedback, kind: overlay_record}


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("project", nargs="+", help="format/ecosystem/slug")
    cli.add_argument("--workers", type=int, default=3,
                     help="independent project checks to run at once")
    args = cli.parse_args()
    relatives = [Path(item) for item in args.project]
    if len(set(relatives)) != len(relatives) or any(len(path.parts) != 3 for path in relatives):
        cli.error("give distinct format/ecosystem/slug paths")
    if not 1 <= args.workers <= 8:
        cli.error("--workers must be between 1 and 8")
    case, batch, native, feedback, afl_plan, python_afl, bridge_afl, native_afl, rust_afl = [], [], [], [], [], [], [], [], []
    failures = []
    with tempfile.TemporaryDirectory(prefix="parsarium-refresh-smoke-") as temporary:
        scratch = Path(temporary)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(check_project, relative, scratch): relative
                       for relative in relatives}
            for future in as_completed(futures):
                relative = futures[future]
                try:
                    result = future.result()
                except Exception as error:
                    failures.append((str(relative), str(error)))
                    print(f"Failed {relative}: {error}", flush=True)
                    continue
                for field, rows in (("case", case), ("batch", batch),
                                    ("native", native),
                                    ("afl_plan", afl_plan)):
                    rows.append(result[field])
                if result["feedback"] is not None:
                    feedback.append(result["feedback"])
                if "native_afl" in result:
                    record = result["native_afl"]
                    native_afl.append({"project": record["project"], "status": "verified",
                                       "feedback_edges": record["feedback_edges"],
                                       "image_id": record["image_id"]})
                elif "rust_afl" in result:
                    record = result["rust_afl"]
                    rust_afl.append({"project": record["project"], "status": "verified",
                                     "feedback_edges": record["feedback_edges"],
                                     "image_id": record["image_id"]})
                elif "python_afl" in result:
                    python_afl.append(result["python_afl"])
                else:
                    bridge_afl.append(result["bridge_afl"])
                print(f"Checked {relative}", flush=True)
    update_report("fuzz-case-smoke.json", case, {"projects_passing": "ok"})
    update_report("fuzz-batch-smoke.json", batch,
                  {"batch_passing": "ok", "per_case_only": "per_case_only"})
    update_report("native-plan-smoke.json", native, {"projects_ready": "ready"})
    update_report("afl-plan-smoke.json", afl_plan, {"projects_ready": "ready"})
    if feedback:
        update_report("ecosystem-feedback-smoke.json", feedback,
                      {"projects_verified": "verified"})
    if native_afl:
        update_report("afl-native-smoke.json", native_afl,
                      {"projects_verified": "verified"})
    if rust_afl:
        update_report("afl-rust-smoke.json", rust_afl,
                      {"projects_verified": "verified"})
    for name, additions in (("afl-python-smoke.json", python_afl),
                            ("afl-bridge-smoke.json", bridge_afl)):
        if not additions:
            continue
        path = ROOT / "data" / name
        with (ROOT / "data/.smoke-report.lock").open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            report = json.loads(path.read_text())
            rows = {item["project"]: item for item in report["results"]}
            rows.update({item["project"]: item for item in additions})
            report["results"] = [rows[key] for key in sorted(rows)]
            report["projects_total"] = len(rows)
            report["projects_verified"] = sum(item["pass"] for item in rows.values())
            report["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
            path.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Refreshed {len(relatives)} projects across smoke reports")
    if failures:
        raise SystemExit(f"{len(failures)} project smoke checks failed: {failures}")


if __name__ == "__main__":
    main()
