"""Replay Gmsh's tagged C PLY loader with its official macOS ARM SDK."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER = ROOT / "adapters/c/ascii_ply/gmsh.c"
LOCK = json.loads((DATA / "source-lock.json").read_text())["gmsh"]
PARSER = next(x for x in json.loads((DATA / "parsers.json").read_text()) if x["name"] == "gmsh")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def fetch(url: str, path: Path, expected: str) -> None:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium Gmsh PLY verifier"}), timeout=120) as response:
        path.write_bytes(response.read())
    assert digest(path) == expected, url


def verify() -> None:
    assert platform.system() == "Darwin" and platform.machine() == "arm64"
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    assert digest(ADAPTER) == LOCK["adapter_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-gmsh-") as temporary:
        work = Path(temporary)
        source_archive = work / "source.tgz"
        sdk_archive = work / "sdk.tgz"
        fetch(LOCK["source_url"], source_archive, LOCK["source_sha256"])
        fetch(LOCK["sdk_url"], sdk_archive, LOCK["sdk_sha256"])
        with tarfile.open(source_archive) as tar:
            tar.extractall(work, filter="data")
        with tarfile.open(sdk_archive) as tar:
            tar.extractall(work, filter="data")
        source = work / "gmsh-4.15.2-source"
        sdk = work / "gmsh-4.15.2-MacOSARM-sdk"
        for filename, expected in LOCK["source_files_sha256"].items():
            assert digest(source / filename) == expected, filename
        for filename, expected in LOCK["sdk_files_sha256"].items():
            assert digest(sdk / filename) == expected, filename
        assert (source / "api/gmshc.h").read_bytes() == (sdk / "include/gmshc.h").read_bytes()

        binary = work / "gmsh-ply-control"
        compiler = "clang"
        build = [compiler, "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                 "-I", str(sdk / "include"), str(ADAPTER), "-L", str(sdk / "lib"),
                 f"-Wl,-rpath,{sdk / 'lib'}", "-lgmsh", "-o", str(binary)]
        run(build)
        execute = [str(binary), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == PARSER["expected_output"], output

    results = json.loads((DATA / "verification.json").read_text())
    results["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    results.setdefault("local_libraries", {})["gmsh"] = {
        "source_sha256": LOCK["source_sha256"],
        "sdk_sha256": LOCK["sdk_sha256"],
        "adapter_sha256": LOCK["adapter_sha256"],
        "compiler": run([compiler, "--version"]).splitlines()[0],
        "platform": platform.platform(),
        "build_scope": "Official 4.15.2 SDK's libgmsh and C header; source archive and matching header checked against the tagged release. No source build."
    }
    results["third_party"] = [x for x in results["third_party"] if x["package"] != "gmsh"]
    results["third_party"].append({
        "package": "gmsh", "version": "4.15.2", "control": PARSER["control"],
        "build_command": shlex.join(build), "command": shlex.join(execute),
        "output": output, "pass": True,
        "note": "Gmsh's C gmshOpen parsed the local ASCII PLY triangle; mesh getters returned three coordinates, one triangle and its three node references."
    })
    (DATA / "verification.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    print("Gmsh@4.15.2: C ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
