"""Replay Rig's tagged C PLY loader with mesh/GPU observation stand-ins."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import os
import platform
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER_DIR = ROOT / "adapters/c/ascii_ply"
LOCK = json.loads((DATA / "source-lock.json").read_text())["rig"]
PARSER = next(x for x in json.loads((DATA / "parsers.json").read_text()) if x["name"] == "rig")
ARCHIVE = Path(os.environ.get("PARSARIUM_RIG_ARCHIVE", str(Path(tempfile.gettempdir()) / "parsarium-rig-2.tar.gz")))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path = ROOT) -> str:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=180)
    if completed.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{completed.stdout}\n{completed.stderr}")
    return completed.stdout.strip()


def verify() -> None:
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    for relative, expected in LOCK["adapter_files"].items():
        assert digest(ROOT / relative) == expected, relative
    if not ARCHIVE.exists() or digest(ARCHIVE) != LOCK["source_sha256"]:
        with urlopen(Request(LOCK["source_url"], headers={"User-Agent": "Parsarium C PLY verifier"}), timeout=120) as response, ARCHIVE.open("wb") as target:
            while chunk := response.read(1024 * 1024):
                target.write(chunk)
    assert digest(ARCHIVE) == LOCK["source_sha256"]
    with tarfile.open(ARCHIVE) as archive:
        for member, expected in LOCK["source_members"].items():
            file = archive.extractfile(member)
            assert file and sha256(file.read()).hexdigest() == expected, member
        with tempfile.TemporaryDirectory(prefix="parsarium-rig-") as work:
            archive.extractall(work, filter="data")
            source = Path(work) / LOCK["archive_root"] / "rut"
            binary = Path(work) / "rig-ply-control"
            cc = os.environ.get("CC", "clang")
            build = [cc, "-std=gnu11", "-O2", "-Wall", "-Wextra",
                     "-Wno-unused-parameter", "-include", str(ADAPTER_DIR / "rig_compat.h"),
                     "-I", str(ADAPTER_DIR), "-I", str(source),
                     *shlex.split(run(["pkg-config", "--cflags", "glib-2.0", "gobject-2.0"])),
                     str(ADAPTER_DIR / "rig.c"), str(source / "rut-mesh-ply.c"),
                     str(source / "rply.c"),
                     *shlex.split(run(["pkg-config", "--libs", "glib-2.0", "gobject-2.0"])),
                     "-o", str(binary)]
            run(build)
            execute = [str(binary), str(CONTROL)]
            output = json.loads(run(execute))
            assert output == PARSER["expected_output"], output

    results = json.loads((DATA / "verification.json").read_text())
    results["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    results.setdefault("local_libraries", {})["rig"] = {
        "source_sha256": LOCK["source_sha256"],
        "release_commit": LOCK["release_commit"],
        "adapter_files": LOCK["adapter_files"],
        "compiler": run([cc, "--version"]).splitlines()[0],
        "platform": platform.platform(),
        "glib": run(["pkg-config", "--modversion", "glib-2.0"]),
        "build_scope": "Unmodified tagged rut-mesh-ply.c and bundled rply.c; mesh allocation and Cogl feature calls are observation stand-ins, not a full Rig graphics build.",
    }
    results["third_party"] = [x for x in results["third_party"] if x["package"] != "rig"]
    results["third_party"].append({
        "package": "rig", "version": "2", "control": PARSER["control"],
        "build_command": shlex.join(build), "command": shlex.join(execute),
        "output": output, "pass": True,
        "note": "Tagged Rig C loader parsed the local ASCII PLY triangle through bundled RPly; stand-ins only retain parsed mesh fields. Full graphics integration is not verified.",
    })
    (DATA / "verification.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    print("rig@2: C ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
