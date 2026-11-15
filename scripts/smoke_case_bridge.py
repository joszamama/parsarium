"""Replay each project's valid control once through the external case bridge."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from run_case import ROOT, project_for, run_case


def check(manifest_path: Path) -> dict:
    relative = manifest_path.parent.relative_to(ROOT / "projects")
    format_name, ecosystem, slug = relative.parts
    project, manifest = project_for(format_name, ecosystem, slug)
    result = run_case(project, manifest, (ROOT / manifest["control"]).resolve(), 90)
    return {"project": str(relative), "control": manifest["control"],
            "control_sha256": manifest["control_sha256"],
            "project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
            "status": result["status"], "case_sha256": result["case_sha256"],
            "image_id": result.get("image_id"), "exit_code": result.get("exit_code"),
            "duration_seconds": result.get("duration_seconds"),
            "stderr_tail": result.get("stderr_tail", "")[-1000:] if result["status"] != "ok" else ""}


def main() -> None:
    manifests = sorted((ROOT / "projects").glob("*/*/*/manifest.json"))
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        pending = [pool.submit(check, path) for path in manifests]
        for task in as_completed(pending):
            result = task.result()
            results.append(result)
            print(f"{result['project']}: {result['status']}", flush=True)
    results.sort(key=lambda item: item["project"])
    report = {"schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "projects_total": len(results),
              "projects_passing": sum(result["status"] == "ok" for result in results),
              "results": results}
    (ROOT / "data/fuzz-case-smoke.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['projects_passing']}/{report['projects_total']} one-input controls passed")
    if report["projects_passing"] != report["projects_total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
