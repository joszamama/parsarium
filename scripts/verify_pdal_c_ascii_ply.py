"""Verify pinned pdal-c and PDAL releases against a valid ASCII PLY file."""

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
SOURCE = json.loads((DATA / "source-lock.json").read_text())["pdal_c"]
PARSER = next(p for p in json.loads((DATA / "parsers.json").read_text()) if p["name"] == "pdal_c")
LOCK = json.loads((ROOT / SOURCE["conda_lock"]).read_text())
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
CACHE = Path(os.environ.get("PARSARIUM_PDALC_CACHE", tempfile.gettempdir()))
ENV = Path(os.environ.get("PARSARIUM_PDALC_ENV", str(CACHE / "parsarium-pdal-c-env")))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def download(url: str, expected: str, path: Path) -> None:
    if path.exists() and digest(path) == expected:
        return
    with urlopen(Request(url, headers={"User-Agent": "Parsarium ASCII PLY verifier"}), timeout=120) as response, path.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)
    assert digest(path) == expected


def run(command: list[str], timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout[-2000:]}\n{result.stderr[-2000:]}")
    return result.stdout.strip()


def check_archive(archive_path: Path, members: dict[str, str]) -> None:
    with tarfile.open(archive_path) as archive:
        for member, expected in members.items():
            file = archive.extractfile(member)
            assert file is not None and sha256(file.read()).hexdigest() == expected, member


def verify_native() -> tuple[dict, dict]:
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    assert LOCK["platform"] == "osx-arm64" and len(LOCK["packages"]) == 60
    CACHE.mkdir(parents=True, exist_ok=True)
    capi_archive = CACHE / "parsarium-pdal-c-v2.2.3.tar.gz"
    pdal_archive = CACHE / "parsarium-pdal-2.10.2.tar.gz"
    download(SOURCE["source_url"], SOURCE["source_sha256"], capi_archive)
    download(SOURCE["pdal_source_url"], SOURCE["pdal_source_sha256"], pdal_archive)
    check_archive(capi_archive, SOURCE["source_members"])
    check_archive(pdal_archive, SOURCE["pdal_source_members"])
    if not (ENV / "conda-meta").exists():
        explicit = CACHE / "parsarium-pdal-c-explicit.txt"
        explicit.write_text("@EXPLICIT\n" + "\n".join(p["url"] for p in LOCK["packages"]) + "\n")
        run(["micromamba", "create", "-y", "-p", str(ENV), "--file", str(explicit)], timeout=3600)
    for package in LOCK["packages"]:
        metadata = ENV / "conda-meta" / f"{package['name']}-{package['version']}-{package['build']}.json"
        installed = json.loads(metadata.read_text())
        assert installed["url"] == package["url"] and installed["sha256"] == package["sha256"], package["name"]
    for member, expected in SOURCE["installed_files"].items():
        assert digest(ENV / member) == expected, member
    assert SOURCE["installed_files"]["include/pdal/pdalc.h"] == SOURCE["source_members"]["CAPI-2.2.3/source/pdal/pdalc.h"]
    binary = CACHE / "parsarium-pdal-c-ply"
    command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
               f"-I{ENV / 'include'}", str(ROOT / PARSER["adapter"]),
               f"-L{ENV / 'lib'}", f"-Wl,-rpath,{ENV / 'lib'}",
               "-lpdalc", "-o", str(binary)]
    run(command)
    execute = [str(binary), str(CONTROL)]
    output = json.loads(run(execute))
    assert output == PARSER["expected_output"], output
    row = {"package": "pdal_c", "version": PARSER["version"],
           "control": PARSER["control"], "build_command": shlex.join(command),
           "command": shlex.join(execute), "output": output, "pass": True}
    local = {"source_sha256": SOURCE["source_sha256"],
             "pdal_source_sha256": SOURCE["pdal_source_sha256"],
             "conda_lock": SOURCE["conda_lock"],
             "installed_files": {str(ENV / member): expected for member, expected in SOURCE["installed_files"].items()}}
    return row, local


if __name__ == "__main__":
    print(json.dumps(verify_native(), indent=2))
