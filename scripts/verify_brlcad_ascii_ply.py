"""Build pinned BRL-CAD libgcv and verify its C ASCII PLY import API."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import os
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
SOURCE = json.loads((DATA / "source-lock.json").read_text())["brlcad"]
PARSER = next(p for p in json.loads((DATA / "parsers.json").read_text()) if p["name"] == "brlcad")
CACHE = Path(os.environ.get("PARSARIUM_BRLCAD_CACHE", tempfile.gettempdir()))
ARCHIVE = CACHE / "parsarium-brlcad-7.46.0.tar.gz"
SOURCE_ROOT = CACHE / "parsarium-brlcad-7.46.0-source"
SOURCE_DIR = SOURCE_ROOT / "brlcad-7.46.0"
BUILD_DIR = CACHE / "parsarium-brlcad-7.46.0-build"
BEXT_DIR = BUILD_DIR / "bext"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int = 3600) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout[-4000:]}\n{result.stderr[-4000:]}")
    return result.stdout.strip()


def verify_native() -> tuple[dict, dict]:
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    CACHE.mkdir(parents=True, exist_ok=True)
    if not ARCHIVE.exists() or digest(ARCHIVE) != SOURCE["source_sha256"]:
        with urlopen(Request(SOURCE["source_url"], headers={"User-Agent": "Parsarium PLY verifier"}), timeout=120) as response, ARCHIVE.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
    assert digest(ARCHIVE) == SOURCE["source_sha256"]
    with tarfile.open(ARCHIVE) as archive:
        for member, expected in SOURCE["source_members"].items():
            file = archive.extractfile(member)
            assert file is not None and sha256(file.read()).hexdigest() == expected, member
        if not (SOURCE_DIR / "include/gcv/api.h").exists():
            for member in archive.getmembers():
                path = Path(member.name)
                assert not path.is_absolute() and ".." not in path.parts
                assert path.parts[0] == "brlcad-7.46.0"
            SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
            archive.extractall(SOURCE_ROOT, filter="data")
    assert digest(SOURCE_DIR / "include/gcv/api.h") == SOURCE["source_members"]["brlcad-7.46.0/include/gcv/api.h"]
    if not BEXT_DIR.exists():
        run(["git", "clone", "https://github.com/BRL-CAD/bext.git", str(BEXT_DIR)])
        run(["git", "-C", str(BEXT_DIR), "checkout", SOURCE["bext_commit"]])
    assert run(["git", "-C", str(BEXT_DIR), "rev-parse", "HEAD"]) == SOURCE["bext_commit"]
    run(["cmake", "-S", str(BEXT_DIR), "-B", str(BUILD_DIR / "bext_build"),
         "-DBEXT_REPOSITORY_ROOT:STRING=https://github.com/BRL-CAD/",
         "-DGIT_SHALLOW_CLONE:BOOL=ON", "-DENABLE_ALL=OFF", "-DUSE_GDAL=OFF",
         "-DUSE_QT=OFF", "-DUSE_TCL=OFF", "-DUSE_APPLESEED=OFF",
         "-DUSE_BRLCAD_EXTRA=OFF", "-DCMAKE_BUILD_TYPE=Release",
         f"-DCMAKE_INSTALL_PREFIX={BUILD_DIR / 'bext_output'}"])
    cmake_command = ["cmake", "-S", str(SOURCE_DIR), "-B", str(BUILD_DIR),
                     f"-DBRLCAD_EXT_SOURCE_DIR={BEXT_DIR}", "-DBRLCAD_ENABLE_MINIMAL=ON",
                     "-DBRLCAD_ENABLE_TCL=OFF", "-DBRLCAD_ENABLE_ASSETIMPORT=OFF",
                     "-DBRLCAD_ENABLE_STEP=OFF", "-DBRLCAD_ENABLE_GDAL=OFF",
                     "-DBRLCAD_ENABLE_OPENVDB=OFF", "-DBUILD_STATIC_LIBS=OFF",
                     "-DBRLCAD_VALIDATE_STATIC_LINKS=OFF", "-DCMAKE_BUILD_TYPE=Release"]
    run(cmake_command)
    run(["cmake", "--build", str(BUILD_DIR), "--target", "gcv-ply", "--parallel", "8"])
    library = BUILD_DIR / "lib/libgcv.dylib"
    plugin = BUILD_DIR / "libexec/gcv/libgcv-ply.dylib"
    assert library.exists() and plugin.exists()
    binary = CACHE / "parsarium-brlcad-c-ply"
    command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
               f"-I{SOURCE_DIR / 'include'}", f"-I{BUILD_DIR / 'include'}",
               str(ROOT / PARSER["adapter"]), f"-L{BUILD_DIR / 'lib'}",
               f"-Wl,-rpath,{BUILD_DIR / 'lib'}", "-lgcv", "-lrt", "-lbu",
               "-o", str(binary)]
    run(command)
    execute = [str(binary), str(CONTROL)]
    output = json.loads(run(execute))
    assert output == PARSER["expected_output"], output
    row = {"package": "brlcad", "version": PARSER["version"], "control": PARSER["control"],
           "configure_command": shlex.join(cmake_command), "build_target": "gcv-ply",
           "build_command": shlex.join(command), "command": shlex.join(execute),
           "output": output, "pass": True}
    local = {"source_sha256": SOURCE["source_sha256"], "bext_commit": SOURCE["bext_commit"],
             "libgcv_sha256": digest(library), "gcv_ply_plugin_sha256": digest(plugin)}
    return row, local


if __name__ == "__main__":
    print(json.dumps(verify_native(), indent=2))
