"""One fixed valid Fandango output, replay, and AFL++ plan per format.

Prerequisites: `python3 parsarium.py fandango setup` and verified Docker/AFL
images for the selected projects. This never starts an AFL++ campaign.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("png", "cpp", "opencv"),
    ("zip", "cpp", "poco"),
    ("mp4", "cpp", "exiv2"),
    ("wav", "c", "dr_wav"),
    ("pdf", "cpp", "poppler"),
    ("svg", "c", "librsvg"),
    ("http11", "cpp", "poco"),
    ("ascii_ply", "c", "assetkit"),
    ("ascii_pnm", "cpp", "openimageio"),
    ("mp3", "c", "mpv"),
    ("json", "python", "simplejson"),
    ("xml", "python", "xmltodict"),
    ("mp3", "go", "github_com_dmulholl_mp3lib"),
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                          errors="replace", timeout=timeout)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--fandango", type=Path,
                        help="pinned Fandango executable; defaults to Parsarium's managed installation")
    parser.add_argument("--case", action="append", default=[], metavar="FORMAT/ECOSYSTEM/SLUG",
                        help="check only this default case (repeatable)")
    args = parser.parse_args()
    cases = CASES
    if args.case:
        cases = tuple(case for case in CASES if "/".join(case) in args.case)
        if len(cases) != len(set(args.case)):
            parser.error("--case must name entries of the default case list")
    output = args.run_dir.expanduser().resolve()
    if output.exists() and any(output.iterdir()):
        parser.error("run directory must be empty")
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for fmt, ecosystem, slug in cases:
        path = output / f"{fmt}-{ecosystem}"
        command = [sys.executable, str(ROOT / "parsarium.py"), "fandango", "generate",
                   fmt, ecosystem, slug, str(path), "--count", "1", "--seed", "7",
                   "--timeout", "120", "--replay", "--prepare-afl"]
        if args.fandango:
            command += ["--fandango", str(args.fandango.resolve())]
        try:
            generated = run(command, 180)
        except subprocess.TimeoutExpired as error:
            rows.append({"format": fmt, "project": f"{fmt}/{ecosystem}/{slug}",
                         "status": "timeout", "error": str(error)})
            print(f"{fmt}: timeout", flush=True)
            continue
        path.mkdir(exist_ok=True)
        (path / "smoke-console.txt").write_text(generated.stdout + "\n" + generated.stderr)
        receipt_path = path / "fandango.json"
        receipt = json.loads(receipt_path.read_text()) if receipt_path.is_file() else {}
        replay_path = path / "replay/summary.json"
        replay = json.loads(replay_path.read_text()) if replay_path.is_file() else {}
        plan_path = path / "afl/plan.json"
        plan = json.loads(plan_path.read_text()) if plan_path.is_file() else {}
        check = None
        if generated.returncode == 0 and plan:
            checked = run([sys.executable, str(ROOT / "parsarium.py"), "afl", "run",
                           str(path / "afl"), "--check"], 30)
            check = {"exit_code": checked.returncode,
                     "result": (checked.stdout + checked.stderr).strip()[-300:]}
        files = receipt.get("outputs", [])
        spec = {key: receipt.get("spec", {}).get(key)
                for key in ("kind", "name", "sha256", "matches_registry_index")
                if key in receipt.get("spec", {})}
        if spec.get("kind") == "file" and spec.get("name"):
            spec_path = Path(spec["name"])
            if spec_path.is_relative_to(ROOT):
                spec["name"] = str(spec_path.relative_to(ROOT))
        good = (generated.returncode == 0 and not receipt.get("problems")
                and len(files) == 1 and replay.get("counts") == {"ok": 1}
                and replay.get("batch_status") == "ok" and check is not None
                and check["exit_code"] == 0)
        row = {
            "format": fmt, "project": f"{fmt}/{ecosystem}/{slug}",
            "status": "pass" if good else "fail", "generator_exit_code": generated.returncode,
            "generator_version": receipt.get("fandango", {}).get("version"),
            "generator_sha256": receipt.get("fandango", {}).get("executable_sha256"),
            "source_sha256": receipt.get("source_sha256"),
            "spec": spec,
            "output": {key: files[0].get(key) for key in ("sha256", "bytes", "format_validation")
                       if key in files[0]} if len(files) == 1 else None,
            "replay": {"batch_status": replay.get("batch_status"),
                       "counts": replay.get("counts"),
                       "image_ids": replay.get("image_ids")},
            "afl": {"prepared": bool(plan), "image_id": plan.get("image_id"),
                    "feedback_kind": plan.get("feedback_kind"),
                    "unique_seeds": plan.get("unique_seeds"), "check": check},
            "problems": receipt.get("problems", []),
            "fandango_receipt_sha256": digest(receipt_path) if receipt_path.is_file() else None,
            "replay_receipt_sha256": digest(replay_path) if replay_path.is_file() else None,
            "afl_plan_sha256": digest(plan_path) if plan_path.is_file() else None,
        }
        rows.append(row)
        print(f"{fmt}: {row['status']} ({row['project']})", flush=True)
    result = {"schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "seed": 7, "count_per_format": 1, "fuzz_campaign_started": False,
              "formats": len(cases), "passed": sum(row["status"] == "pass" for row in rows),
              "rows": rows}
    (output / "smoke.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"{result['passed']}/{result['formats']} passed; {output / 'smoke.json'}")
    return 0 if result["passed"] == result["formats"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
