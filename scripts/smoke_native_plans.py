"""Prepare and preflight one native fuzz plan for every verified project."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT


def main() -> None:
    manifests = sorted((ROOT / "projects").glob("*/*/*/manifest.json"))
    records = []
    with tempfile.TemporaryDirectory(prefix="parsarium-native-plans-") as temp:
        scratch = Path(temp)
        for path in manifests:
            relative = path.parent.relative_to(ROOT / "projects")
            manifest = json.loads(path.read_text())
            if manifest.get("native_campaign_supported") is False:
                rejected = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/prepare_native_run.py"),
                     *relative.parts, str(scratch.joinpath(*relative.parts))],
                    capture_output=True, text=True,
                )
                if rejected.returncode == 0 or "unsupported" not in rejected.stderr:
                    raise RuntimeError(f"native campaign was not rejected: {relative}")
                receipt = path.parent / "verification.json"
                records.append({"project": str(relative), "status": "unsupported",
                                "engine": "in-process native campaign",
                                "reason": "parser state persists across inputs; use one-shot AFL++",
                                "image_id": json.loads(receipt.read_text())["image_id"],
                                "control_sha256": manifest["control_sha256"],
                                "project_receipt_sha256": sha256(receipt.read_bytes()).hexdigest()})
                continue
            run_dir = scratch.joinpath(*relative.parts)
            prepare = subprocess.run(
                [sys.executable, str(ROOT / "scripts/prepare_native_run.py"),
                 *relative.parts, str(run_dir)], capture_output=True, text=True)
            check = None
            if prepare.returncode == 0:
                check = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/run_prepared_native.py"),
                     str(run_dir), "--check"], capture_output=True, text=True)
            if prepare.returncode == 0 and check is not None and check.returncode == 0:
                plan = json.loads((run_dir / "plan.json").read_text())
                records.append({"project": str(relative), "status": "ready",
                                "engine": plan["engine"], "image_id": plan["image_id"],
                                "control_sha256": plan["control_sha256"],
                                "project_receipt_sha256": plan["project_receipt_sha256"],
                                "unique_seeds": plan["unique_seeds"]})
            else:
                detail = (prepare.stderr if prepare.returncode else check.stderr)[-2000:]
                records.append({"project": str(relative), "status": "failed", "error": detail})
                print(f"FAILED {relative}: {detail}", flush=True)
    report = {"schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "projects_total": len(records),
              "projects_ready": sum(item["status"] == "ready" for item in records),
              "results": records}
    (ROOT / "data/native-plan-smoke.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['projects_ready']}/{report['projects_total']} native campaign plans ready")
    if any(item["status"] == "failed" for item in records):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
