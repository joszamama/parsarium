"""Replay each valid control as a one-file corpus, without mutation iterations."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import tempfile

from run_case import ROOT, project_for
from run_corpus_batch import run_batch


def check(manifest_path: Path) -> dict:
    relative = manifest_path.parent.relative_to(ROOT / "projects")
    project, manifest = project_for(*relative.parts)
    with tempfile.TemporaryDirectory(prefix="parsarium-corpus-smoke-") as temporary:
        inputs = Path(temporary)
        (inputs / manifest["control_sha256"]).write_bytes((ROOT / manifest["control"]).read_bytes())
        result = run_batch(project, manifest, inputs, 90)
    status = result["status"] if result is not None else "per_case_only"
    return {"project": str(relative), "status": status,
            "project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
            "control_sha256": manifest["control_sha256"],
            "image_id": result.get("image_id") if result else None,
            "stderr_tail": result.get("stderr_tail", "")[-1000:] if status not in {"ok", "per_case_only"} else ""}


def main() -> None:
    paths = sorted((ROOT / "projects").glob("*/*/*/manifest.json"))
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for task in as_completed([pool.submit(check, path) for path in paths]):
            item = task.result()
            results.append(item)
            print(f"{item['project']}: {item['status']}", flush=True)
    results.sort(key=lambda item: item["project"])
    report = {"schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "projects_total": len(results),
              "batch_passing": sum(item["status"] == "ok" for item in results),
              "per_case_only": sum(item["status"] == "per_case_only" for item in results),
              "results": results}
    (ROOT / "data/fuzz-batch-smoke.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['batch_passing']} batch paths, {report['per_case_only']} per-case paths")
    if report["batch_passing"] + report["per_case_only"] != report["projects_total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
