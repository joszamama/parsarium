"""Replay pcprep's tagged public C PLY input API on the ASCII control."""

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
ADAPTER = ROOT / "adapters/c/ascii_ply/pcprep.c"
LOCK = json.loads((DATA / "source-lock.json").read_text())["pcprep"]
PARSER = next(p for p in json.loads((DATA / "parsers.json").read_text()) if p["name"] == "pcprep")
ARCHIVE = Path(os.environ.get("PARSARIUM_PCPREP_ARCHIVE", str(Path(tempfile.gettempdir()) / "parsarium-pcprep-v1.0.tar.gz")))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def verify() -> None:
    assert platform.system() == "Darwin", "This replay uses the macOS dead-strip linker flag"
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    assert digest(ADAPTER) == LOCK["adapter_sha256"]
    if not ARCHIVE.exists() or digest(ARCHIVE) != LOCK["source_sha256"]:
        with urlopen(Request(LOCK["source_url"], headers={"User-Agent": "Parsarium C ASCII PLY verifier"}), timeout=120) as response:
            ARCHIVE.write_bytes(response.read())
    assert digest(ARCHIVE) == LOCK["source_sha256"]
    with tarfile.open(ARCHIVE) as archive:
        for member, expected in LOCK["source_members"].items():
            item = archive.extractfile(member)
            assert item is not None and sha256(item.read()).hexdigest() == expected, member
        with tempfile.TemporaryDirectory(prefix="parsarium-pcprep-") as scratch:
            archive.extractall(scratch)
            source = Path(scratch) / "pcprep-pcprep-v1.0"
            build = Path(scratch) / "build"
            run(["cmake", "-S", str(source), "-B", str(build), "-DBUILD_APP=OFF", "-DBUILD_VPCC=OFF"])
            png_version = run(["pkg-config", "--modversion", "libpng"])
            png_flags = shlex.split(run(["pkg-config", "--cflags", "libpng"]))
            include = ["-I", str(source / "include"), "-I", str(build / "export"),
                       "-I", str(source / "source/include"), *png_flags]
            cc, cxx = os.getenv("CC", "cc"), os.getenv("CXX", "c++")
            objects = []
            commands = []
            for filename in ("pointcloud.c", "wrapper.cpp", "miniply.cpp"):
                compiler = cxx if filename.endswith(".cpp") else cc
                language = "-std=c++17" if filename.endswith(".cpp") else "-std=c99"
                obj = build / (filename + ".o")
                command = [compiler, language, "-ffunction-sections", *include, "-c",
                           str(source / "source" / filename), "-o", str(obj)]
                run(command)
                objects.append(str(obj))
                commands.append(shlex.join(command))
            adapter_obj = build / "pcprep-adapter.o"
            command = [cc, "-std=c99", *include, "-c", str(ADAPTER), "-o", str(adapter_obj)]
            run(command)
            commands.append(shlex.join(command))
            binary = build / "pcprep-ply-control"
            command = [cxx, "-Wl,-dead_strip", str(adapter_obj), *objects, "-o", str(binary)]
            run(command)
            commands.append(shlex.join(command))
            execute = [str(binary), str(CONTROL)]
            output = json.loads(run(execute))
            assert output == PARSER["expected_output"], output

    path = DATA / "verification.json"
    result = json.loads(path.read_text())
    result["third_party"] = [row for row in result["third_party"] if row["package"] != "pcprep"] + [{
        "package": "pcprep", "version": PARSER["version"], "control": PARSER["control"],
        "build_commands": commands, "command": shlex.join(execute), "output": output, "pass": True,
        "note": "Tagged public C pointcloud_load parsed three local ASCII PLY coordinates through bundled miniply. The targeted build omits unrelated source functions using dead stripping.",
    }]
    result["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    result["platform"] = platform.platform()
    result.setdefault("local_libraries", {})["pcprep"] = {
        "source_sha256": LOCK["source_sha256"], "release_commit": LOCK["release_commit"],
        "adapter_sha256": LOCK["adapter_sha256"], "libpng_header_version": png_version,
    }
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("pcprep@pcprep-v1.0: C ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
