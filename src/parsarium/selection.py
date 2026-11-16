"""Run a target selection downloaded from https://parsarium.com/bench/."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MODES = ("control", "file", "replay", "afl")


def load(manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema") != "parsarium-selection/1":
        raise ValueError(f"{manifest_path} is not a Parsarium selection manifest")
    if not manifest.get("targets"):
        raise ValueError(f"{manifest_path} lists no targets")
    return manifest


def run(manifest_path: Path, root: Path, mode: str, input_path: Path | None,
        out: Path | None, seconds: int, dry_run: bool = False) -> int:
    manifest = load(manifest_path)
    snapshot = root / "parsarium-snapshot.json"
    snapshot_commit = json.loads(snapshot.read_text()).get("commit") if snapshot.is_file() else None
    if manifest.get("commit") and snapshot_commit and not snapshot_commit.startswith(manifest["commit"]):
        print(f"parsarium: note: selection {manifest['id']} was built from commit {manifest['commit']}, "
              f"this snapshot is {snapshot_commit[:8]}; targets missing here are reported as failed.",
              file=sys.stderr)
    formats = sorted({t["format"] for t in manifest["targets"]})
    if mode in {"file", "replay"} and input_path is None:
        raise ValueError(f"--input is required for mode {mode}")
    if input_path is not None:
        input_path = input_path.expanduser().resolve()
    out = (out or Path("runs") / manifest["id"]).expanduser().resolve()
    entry = [sys.executable, str(root / "parsarium.py")]

    def per_format(fmt: str) -> Path:
        # One format: the input is used as given. Several: one subdirectory per format.
        return input_path if len(formats) == 1 else input_path / fmt

    failed = []
    for t in manifest["targets"]:
        fmt, eco, slug = t["id"].split("/")
        name = f"{fmt}-{eco}-{slug}"
        dest = out / name
        if mode == "control":
            steps = [["run", fmt, eco, slug, str(root / t["control"]), "--results", str(dest)]]
        elif mode == "file":
            source = per_format(fmt)
            files = [source] if source.is_file() else sorted(p for p in source.glob("*") if p.is_file())
            steps = [["run", fmt, eco, slug, str(f), "--results", str(dest / f.name)] for f in files]
        elif mode == "replay":
            steps = [["replay", fmt, eco, slug, str(per_format(fmt)), str(dest)]]
        else:
            steps = [["afl", "build", fmt, eco, slug],
                     ["afl", "prepare", fmt, eco, slug, str(dest)],
                     ["afl", "run", str(dest), "--seconds", str(seconds)],
                     ["afl", "summary", str(dest)]]
        print(f"== {t['id']}", flush=True)
        for step in steps:
            if dry_run:
                print("   parsarium " + " ".join(step))
                continue
            if subprocess.call([*entry, *step]) != 0:
                failed.append(t["id"])
                break
    if dry_run:
        return 0
    out.mkdir(parents=True, exist_ok=True)
    (out / "failed.txt").write_text("".join(f"{i}\n" for i in failed))
    print(f"parsarium: {len(manifest['targets']) - len(failed)}/{len(manifest['targets'])} targets "
          f"finished; receipts in {out}", file=sys.stderr)
    return 1 if failed else 0
