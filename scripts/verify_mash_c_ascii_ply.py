"""Replay Mash's tagged C PLY loader with graphics upload observation."""

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
MOCK = ADAPTER_DIR / "mash_mock"
LOCK = json.loads((DATA / "source-lock.json").read_text())["mash"]
PARSER = next(x for x in json.loads((DATA / "parsers.json").read_text()) if x["name"] == "mash")
ARCHIVE = Path(os.environ.get("PARSARIUM_MASH_ARCHIVE", str(Path(tempfile.gettempdir()) / "parsarium-mash-0.2.0.tar.gz")))


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
        with tempfile.TemporaryDirectory(prefix="parsarium-mash-") as work:
            archive.extractall(work, filter="data")
            source = Path(work) / LOCK["archive_root"] / "mash"
            binary = Path(work) / "mash-ply-control"
            cc = os.environ.get("CC", "clang")
            build = [cc, "-std=gnu11", "-O2", "-Wno-deprecated-declarations",
                     "-DMASH_COMPILATION", "-include", str(MOCK / "mash_compat.h"),
                     "-I", str(MOCK), "-I", str(source),
                     *shlex.split(run(["pkg-config", "--cflags", "glib-2.0", "gobject-2.0"])),
                     str(ADAPTER_DIR / "mash.c"),
                     *[str(source / file) for file in
                       ("mash-data.c", "mash-data-loader.c", "mash-ply-loader.c", "rply/rply.c")],
                     *shlex.split(run(["pkg-config", "--libs", "glib-2.0", "gobject-2.0"])),
                     "-o", str(binary)]
            run(build)
            execute = [str(binary), str(CONTROL)]
            output = json.loads(run(execute))
            assert output == PARSER["expected_output"], output

    results = json.loads((DATA / "verification.json").read_text())
    results["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    results.setdefault("local_libraries", {})["mash"] = {
        "source_sha256": LOCK["source_sha256"],
        "release_commit": LOCK["release_commit"],
        "adapter_files": LOCK["adapter_files"],
        "compiler": run([cc, "--version"]).splitlines()[0],
        "platform": platform.platform(),
        "glib": run(["pkg-config", "--modversion", "glib-2.0"]),
        "build_scope": "Unmodified tagged Mash data and PLY loader sources with bundled RPly; preincluded compatibility header fixes upstream's data-loader type alias, and Cogl upload functions observe parsed geometry. Full Clutter rendering is not verified.",
    }
    results["third_party"] = [x for x in results["third_party"] if x["package"] != "mash"]
    results["third_party"].append({
        "package": "mash", "version": "0.2.0", "control": PARSER["control"],
        "build_command": shlex.join(build), "command": shlex.join(execute),
        "output": output, "pass": True,
        "note": "Public mash_data_load parsed local ASCII PLY through bundled RPly; graphics upload was observed with stand-ins, and a published type-alias typo needed a compile-time correction.",
    })
    (DATA / "verification.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    print("mash@0.2.0: C ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
