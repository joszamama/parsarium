"""Run a target selection downloaded from https://parsarium.com/bench/."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MODES = ("control", "file", "replay", "afl", "fandango")


def load(manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema") != "parsarium-selection/1":
        raise ValueError(f"{manifest_path} is not a Parsarium selection manifest")
    if not isinstance(manifest.get("id"), str) or not re.fullmatch(r"[A-Za-z0-9_-]+", manifest["id"]):
        raise ValueError(f"{manifest_path} has an invalid selection ID")
    if not isinstance(manifest.get("targets"), list) or not manifest["targets"]:
        raise ValueError(f"{manifest_path} lists no targets")
    return manifest


def _snapshot_commit(root: Path) -> str | None:
    metadata = root / "parsarium-snapshot.json"
    if metadata.is_file():
        commit = json.loads(metadata.read_text()).get("commit")
        return commit if isinstance(commit, str) else None
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True).stdout.strip()
        if Path(top).resolve() != root.resolve():
            return None
        return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                              check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _validate_pins(manifest: dict, root: Path, allow_mismatch: bool) -> dict[str, dict]:
    """Resolve every saved target before displaying or running any command."""
    selected_commit = manifest.get("commit")
    actual_commit = _snapshot_commit(root)
    if (not isinstance(selected_commit, str)
            or not re.fullmatch(r"[0-9a-fA-F]{8,64}", selected_commit)
            or not isinstance(actual_commit, str)
            or not actual_commit.lower().startswith(selected_commit.lower())):
        detail = (f"selection {manifest['id']} pins commit {selected_commit or 'unknown'}, "
                  f"but this snapshot is {actual_commit or 'unknown'}")
        if not allow_mismatch:
            raise ValueError(f"{detail}; use the matching snapshot or --allow-mismatch")
        print(f"parsarium: warning: {detail}; --allow-mismatch was given", file=sys.stderr)

    current = {}
    for target in manifest["targets"]:
        if not isinstance(target, dict) or not isinstance(target.get("id"), str):
            raise ValueError(f"selection {manifest['id']} has a target without an ID")
        target_id = target["id"]
        parts = target_id.split("/")
        if (len(parts) != 3 or any(not part or part in {".", ".."} or "\\" in part
                                    for part in parts)):
            raise ValueError(f"invalid target ID {target_id!r}")
        fmt, eco, slug = parts
        if target.get("format") != fmt or target.get("ecosystem") != eco:
            raise ValueError(f"selection target {target_id} has inconsistent format or ecosystem")
        path = (root / "projects" / fmt / eco / slug / "manifest.json").resolve()
        if not path.is_relative_to((root / "projects").resolve()) or not path.is_file():
            raise ValueError(f"selection target {target_id} is absent from this snapshot")
        project = json.loads(path.read_text())
        if project.get("format") != fmt or project.get("ecosystem") != eco:
            raise ValueError(f"snapshot target {target_id} has inconsistent metadata")
        differences = [f"{field}: selection {target.get(field)!r}, snapshot {project.get(field)!r}"
                       for field in ("package", "release", "control")
                       if target.get(field) != project.get(field)]
        if differences:
            detail = f"selection target {target_id} differs from this snapshot ({'; '.join(differences)})"
            if not allow_mismatch:
                raise ValueError(f"{detail}; use the matching snapshot or --allow-mismatch")
            print(f"parsarium: warning: {detail}; --allow-mismatch was given", file=sys.stderr)
        control_path = project.get("control")
        if not isinstance(control_path, str):
            raise ValueError(f"snapshot target {target_id} has no local control file")
        control = (root / control_path).resolve()
        if not control.is_relative_to(root.resolve()) or not control.is_file():
            raise ValueError(f"snapshot target {target_id} has no local control file")
        current[target_id] = project
    return current


def run(manifest_path: Path, root: Path, mode: str, input_path: Path | None,
        out: Path | None, seconds: int, dry_run: bool = False,
        allow_mismatch: bool = False, count: int = 100, seed: int = 42) -> int:
    manifest = load(manifest_path)
    current = _validate_pins(manifest, root, allow_mismatch)
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
    if mode == "fandango":
        # Install the hash-locked Fandango once; every target then uses its format's default spec.
        if dry_run:
            print("   parsarium fandango setup")
        elif subprocess.call([*entry, "fandango", "setup"]) != 0:
            raise ValueError("parsarium fandango setup failed")
    for t in manifest["targets"]:
        fmt, eco, slug = t["id"].split("/")
        name = f"{fmt}-{eco}-{slug}"
        dest = out / name
        if mode == "control":
            steps = [["run", fmt, eco, slug, str(root / current[t["id"]]["control"]),
                      "--results", str(dest)]]
        elif mode == "file":
            source = per_format(fmt)
            files = [source] if source.is_file() else sorted(p for p in source.glob("*") if p.is_file())
            steps = [["run", fmt, eco, slug, str(f), "--results", str(dest / f.name)] for f in files]
        elif mode == "replay":
            steps = [["replay", fmt, eco, slug, str(per_format(fmt)), str(dest)]]
        elif mode == "fandango":
            steps = [["fandango", "generate", fmt, eco, slug, str(dest),
                      "--count", str(count), "--seed", str(seed), "--replay"]]
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
