"""Verify a pinned Open Pointcloud Studio C SDK against an ASCII PLY control."""

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
SOURCE = json.loads((DATA / "source-lock.json").read_text())["ops_pointcloud"]
PARSER = next(p for p in json.loads((DATA / "parsers.json").read_text()) if p["name"] == "ops_pointcloud")
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
CACHE = Path(os.environ.get("PARSARIUM_OPS_CACHE", tempfile.gettempdir())) / "parsarium-ops-pointcloud-2026.45.1"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def download(url: str, expected: str, path: Path) -> None:
    if path.exists() and digest(path) == expected:
        return
    with urlopen(Request(url, headers={"User-Agent": "Parsarium ASCII PLY verifier"}), timeout=120) as response, path.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)
    assert digest(path) == expected


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def verify_native() -> tuple[dict, dict]:
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    CACHE.mkdir(parents=True, exist_ok=True)
    source_archive = CACHE / "source.tar.gz"
    sdk_archive = CACHE / "sdk.tar.gz"
    download(SOURCE["source_url"], SOURCE["source_sha256"], source_archive)
    download(SOURCE["sdk_url"], SOURCE["sdk_sha256"], sdk_archive)
    with tarfile.open(source_archive) as archive:
        for member, expected in SOURCE["source_members"].items():
            file = archive.extractfile(member)
            assert file is not None and sha256(file.read()).hexdigest() == expected, member
    sdk_dir = CACHE / "sdk"
    (sdk_dir / "include").mkdir(parents=True, exist_ok=True)
    (sdk_dir / "lib").mkdir(parents=True, exist_ok=True)
    with tarfile.open(sdk_archive) as archive:
        for short, expected in SOURCE["sdk_members"].items():
            file = archive.extractfile(SOURCE["sdk_prefix"] + "/" + short)
            assert file is not None
            dest = sdk_dir / short
            dest.write_bytes(file.read())
            assert digest(dest) == expected, short
    assert SOURCE["sdk_members"]["include/ops_pointcloud.h"] == SOURCE["source_members"]["open-pointcloud-studio-2026.45.1/native/sdk/include/ops_pointcloud.h"]
    binary = CACHE / "ops-pointcloud-c-ply"
    command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
               f"-I{sdk_dir / 'include'}", str(ROOT / PARSER["adapter"]),
               f"-L{sdk_dir / 'lib'}", f"-Wl,-rpath,{sdk_dir / 'lib'}",
               "-lops_pointcloud", "-o", str(binary)]
    run(command)
    execute = [str(binary), str(CONTROL)]
    output = json.loads(run(execute))
    assert output == PARSER["expected_output"], output
    row = {"package": "ops_pointcloud", "version": PARSER["version"],
           "control": PARSER["control"], "build_command": shlex.join(command),
           "command": shlex.join(execute), "output": output, "pass": True}
    local = {"source_sha256": SOURCE["source_sha256"], "sdk_sha256": SOURCE["sdk_sha256"],
             "installed_files": {str(sdk_dir / short): expected for short, expected in SOURCE["sdk_members"].items()}}
    return row, local


if __name__ == "__main__":
    print(json.dumps(verify_native(), indent=2))
