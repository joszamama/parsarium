"""Check Tkinter PNG one-input replay and AFL++ plan without starting a campaign."""

from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from audit_projects import ROOT, native_source_feedback_verified


RELATIVE = Path("png/python/stdlib_tkinter_photoimage")
PROJECT = ROOT / "projects" / RELATIVE
OVERLAY = ROOT / "fuzzing/afl-native" / RELATIVE
CLI_FILES = ("parsarium.py", "scripts/run_case.py", "scripts/prepare_afl_run.py",
             "scripts/run_prepared_afl.py", "scripts/replay_corpus.py",
             "scripts/run_corpus_batch.py", "scripts/verify_standard_feedback.py")


def run(*args: str) -> str:
    result = subprocess.run([sys.executable, str(ROOT / "parsarium.py"), *args],
                            cwd=ROOT, capture_output=True, text=True, timeout=90)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)} failed: {(result.stdout + result.stderr)[-1200:]}")
    return result.stdout.strip()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest_path = PROJECT / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if not native_source_feedback_verified(manifest_path, manifest):
        raise RuntimeError("pinned Tk control or decoder feedback receipt changed")
    outputs = []
    for field in ("control", "control_variant"):
        relative = manifest[field]
        observed = json.loads(run("run", *RELATIVE.parts, relative).splitlines()[-1])
        if observed.get("status") != "ok":
            raise RuntimeError(f"one-input replay failed for {relative}: {observed}")
        parsed = json.loads(observed["stdout_tail"].strip().splitlines()[-1])
        if parsed != manifest["expected_output"]:
            raise RuntimeError(f"PhotoImage output mismatch for {relative}: {parsed}")
        outputs.append((observed, parsed))
    base_path = PROJECT / "control-verification.json"
    overlay_path = OVERLAY / "verification.json"
    base = json.loads(base_path.read_text())
    overlay = json.loads(overlay_path.read_text())
    if any(observed["image_id"] != base["image_id"] for observed, _ in outputs):
        raise RuntimeError("one-input replay did not use the verified base image")
    with tempfile.TemporaryDirectory(prefix="parsarium-tk-plan-") as temporary:
        corpus = Path(temporary) / "corpus"
        corpus.mkdir()
        shutil.copy2(ROOT / manifest["control"], corpus / "control.png")
        shutil.copy2(ROOT / manifest["control_variant"], corpus / "variant.png")
        run("replay", *RELATIVE.parts, str(corpus), str(Path(temporary) / "replay"))
        summary = json.loads((Path(temporary) / "replay/summary.json").read_text())
        if (summary["unique_inputs"] != 2 or summary["counts"] != {"ok": 2}
                or summary["execution_mode"] != "per_case"):
            raise RuntimeError("two-input corpus replay did not use verified one-input path")
        plan_dir = Path(temporary) / "plan"
        run("afl", "prepare", *RELATIVE.parts, str(plan_dir))
        check = run("afl", "run", str(plan_dir), "--check")
        plan = json.loads((plan_dir / "plan.json").read_text())
        if (not check.startswith(f"Ready: {RELATIVE}")
                or plan["image_id"] != overlay["image_id"]
                or plan["overlay_receipt_sha256"] != digest(overlay_path)
                or plan["unique_seeds"] != 1
                or plan["afl_feedback_edges_on_control"] != overlay["control_edges"]
                or plan["command"][-4:] != ["--", "/work/afl-python", "/work/replay.py", "@@"]
                or plan["command"][plan["command"].index("--entrypoint") + 1]
                    != "/work/with-display.sh"):
            raise RuntimeError("AFL++ plan does not use the verified Tk decoder target")
    result = {
        "schema_version": 1,
        "project": str(RELATIVE),
        "status": "verified",
        "control_sha256": manifest["control_sha256"],
        "variant_sha256": manifest["control_variant_sha256"],
        "base_receipt_sha256": digest(base_path),
        "overlay_receipt_sha256": digest(overlay_path),
        "base_image_id": base["image_id"],
        "overlay_image_id": overlay["image_id"],
        "control_output": outputs[0][1],
        "variant_output": outputs[1][1],
        "afl_plan_status": "ready",
        "replay_status": "ok",
        "replay_unique_inputs": 2,
        "afl_target": ["/work/afl-python", "/work/replay.py", "@@"],
        "cli_file_sha256": {name: digest(ROOT / name) for name in CLI_FILES},
    }
    destination = ROOT / "data/standard-feedback-smoke.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print("Verified Tkinter PNG control, variant, and AFL++ preflight")


if __name__ == "__main__":
    main()
