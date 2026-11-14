"""Replay McCode's tagged McStas OFF/PLY C runtime on the ASCII control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import os
import platform
import re
import shlex
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
SOURCE = json.loads((DATA / "source-lock.json").read_text())["mccode"]
PARSER = next(p for p in json.loads((DATA / "parsers.json").read_text()) if p["name"] == "mccode")
LOCK = json.loads((ROOT / SOURCE["conda_lock"]).read_text())
CACHE = Path(os.environ.get("PARSARIUM_MCCODE_CACHE", tempfile.gettempdir()))
ENV = Path(os.environ.get("PARSARIUM_MCCODE_ENV", str(CACHE / "parsarium-mcstas-core")))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path = ROOT, timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout[-3000:]}\n{result.stderr[-3000:]}")
    return result.stdout.strip()


def verify() -> None:
    assert platform.system() == "Darwin" and platform.machine() == "arm64"
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    assert digest(ROOT / PARSER["adapter"]) == SOURCE["adapter_sha256"]
    assert digest(ROOT / SOURCE["conda_lock"]) == SOURCE["conda_lock_sha256"]
    assert LOCK["platform"] == "osx-arm64" and len(LOCK["packages"]) == 80
    CACHE.mkdir(parents=True, exist_ok=True)
    for label, item in SOURCE["tagged_files"].items():
        cached = CACHE / f"parsarium-mccode-v3.10.2-{label}"
        if not cached.exists() or digest(cached) != item["sha256"]:
            with urlopen(Request(item["url"], headers={"User-Agent": "Parsarium C ASCII PLY verifier"}), timeout=120) as response:
                cached.write_bytes(response.read())
        assert digest(cached) == item["sha256"], label
    if not (ENV / "conda-meta").exists():
        explicit = CACHE / "parsarium-mccode-explicit.txt"
        explicit.write_text("@EXPLICIT\n" + "\n".join(p["url"] for p in LOCK["packages"]) + "\n")
        run(["micromamba", "create", "-y", "-p", str(ENV), "--file", str(explicit)], timeout=3600)
    for package in LOCK["packages"]:
        metadata = ENV / "conda-meta" / f"{package['name']}-{package['version']}-{package['build']}.json"
        installed = json.loads(metadata.read_text())
        assert installed["url"] == package["url"] and installed["sha256"] == package["sha256"], package["name"]
    for member, expected in SOURCE["installed_files"].items():
        assert digest(ENV / member) == expected, member
    assert SOURCE["installed_files"]["share/mcstas/resources/share/interoff-lib.c"] == SOURCE["tagged_files"]["interoff-lib.c"]["sha256"]
    assert SOURCE["installed_files"]["share/mcstas/resources/optics/Guide_anyshape.comp"] == SOURCE["tagged_files"]["Guide_anyshape.comp"]["sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-mccode-") as scratch:
        working = Path(scratch)
        instrument = working / "ParsariumPLY.instr"
        instrument.write_bytes((ROOT / PARSER["adapter"]).read_bytes())
        command = ["micromamba", "run", "-p", str(ENV), "mcrun", "-c", "-n", "1",
                   "--no-output-files", "--dir", str(working / "run"), str(instrument),
                   f"geometry={CONTROL}"]
        output_text = run(command, cwd=working, timeout=360)
    assert f"Loading geometry file (OFF/PLY): {CONTROL}" in output_text
    def extract(pattern: str) -> float:
        match = re.search(pattern, output_text)
        assert match, pattern
        return float(match.group(1))
    output = {"vertices": int(extract(r"Number of vertices:\s*(\d+)")),
              "faces": int(extract(r"Number of polygons:\s*(\d+)")),
              "length": extract(r"Length=([0-9.]+)"),
              "width": extract(r"Width=\s*([0-9.]+)")}
    assert output == PARSER["expected_output"], output
    path = DATA / "verification.json"
    result = json.loads(path.read_text())
    result["third_party"] = [row for row in result["third_party"] if row["package"] != "mccode"] + [{
        "package": "mccode", "version": PARSER["version"], "control": PARSER["control"],
        "command": shlex.join(command), "output": output, "pass": True,
        "note": "Guide_anyshape initialized McCode's tagged C OFF/PLY runtime on local ASCII PLY and reported parsed vertices, polygon and bounding-box dimensions.",
    }]
    result["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    result["platform"] = platform.platform()
    result.setdefault("local_libraries", {})["mccode"] = {
        "source_sha256": SOURCE["source_sha256"], "release_commit": SOURCE["release_commit"],
        "conda_lock": SOURCE["conda_lock"], "installed_files": SOURCE["installed_files"],
    }
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("mccode@3.10.2: C ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
