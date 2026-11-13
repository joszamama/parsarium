"""Build pinned MDAL 1.3.3 and verify its C ABI on a local ASCII PLY."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(tempfile.gettempdir()) / "parsarium-mdal-1.3.3"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
CONTROL_HASH = "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
EXPECTED = {"vertices": 3, "faces": 1, "indices": [0, 1, 2]}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout[-3000:]}\n{result.stderr[-3000:]}")
    return result.stdout.strip()


def verify() -> tuple[dict, dict]:
    lock = json.loads((ROOT / "data/c/ascii_ply/source-lock.json").read_text())["mdal"]
    assert digest(CONTROL) == CONTROL_HASH
    CACHE.mkdir(exist_ok=True)
    archive = CACHE / "source.tar.gz"
    if not archive.exists() or digest(archive) != lock["source_sha256"]:
        request = Request(lock["source_url"], headers={"User-Agent": "Parsarium MDAL verifier"})
        with urlopen(request, timeout=120) as response, archive.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
    assert digest(archive) == lock["source_sha256"]
    source = CACHE / "MDAL-release-1.3.3"
    if not (source / "CMakeLists.txt").exists():
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                parts = Path(member.name).parts
                assert parts and parts[0] == source.name and ".." not in parts
            tar.extractall(CACHE, filter="data")
    for member, expected in lock["source_members"].items():
        assert digest(CACHE / member) == expected, member
    compat = ROOT / "adapters/c/ascii_ply/mdal_c_compat.h"
    assert digest(compat) == lock["compat_header_sha256"]
    build = CACHE / "build"
    configure = ["cmake", "-S", str(source), "-B", str(build),
                 "-DENABLE_TESTS=OFF", "-DWITH_HDF5=OFF", "-DWITH_GDAL=OFF",
                 "-DWITH_NETCDF=OFF", "-DWITH_XML=OFF", "-DWITH_SQLITE3=OFF",
                 "-DBUILD_TOOLS=OFF", "-DBUILD_EXTERNAL_DRIVERS=OFF",
                 "-DBUILD_PLY=ON", "-DBUILD_STATIC=OFF", "-DBUILD_SHARED=ON",
                 "-DCMAKE_BUILD_TYPE=Release"]
    run(configure, timeout=240)
    run(["cmake", "--build", str(build), "--parallel", "8"], timeout=1200)
    library = build / "mdal/libmdal.dylib"
    assert library.exists()
    source_file = ROOT / "adapters/c/ascii_ply/mdal.c"
    binary = CACHE / "mdal-c-ply"
    command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
               str(source_file), "-L" + str(library.parent),
               "-Wl,-rpath," + str(library.parent), "-lmdal", "-o", str(binary)]
    run(command)
    execute = [str(binary), str(CONTROL)]
    output = json.loads(run(execute))
    assert output == EXPECTED, output
    row = {"package": "mdal", "version": "1.3.3", "control": "controls/ascii_ply/triangle.ply",
           "build_command": shlex.join(command), "command": shlex.join(execute),
           "output": output, "pass": True}
    local = {"source_sha256": lock["source_sha256"],
             "compat_header_sha256": lock["compat_header_sha256"],
             "underlying_family": "MDAL PLY driver over bundled libplyxx"}
    return row, local


if __name__ == "__main__":
    print(json.dumps(verify()[0]))
