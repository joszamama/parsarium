"""Replay Blukpast's tagged C PLY loader with a GPU capture harness."""

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
ADAPTER = ROOT / "adapters/c/ascii_ply/blukpast.c"
LOCK = json.loads((DATA / "source-lock.json").read_text())["blukpast"]
PARSER = next(row for row in json.loads((DATA / "parsers.json").read_text()) if row["name"] == "blukpast")
ARCHIVE = Path(os.environ.get("PARSARIUM_BLUKPAST_ARCHIVE", str(Path(tempfile.gettempdir()) / "parsarium-blukpast-v1.0.6.tar.gz")))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def verify() -> None:
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    assert digest(ADAPTER) == LOCK["adapter_sha256"]
    if not ARCHIVE.exists() or digest(ARCHIVE) != LOCK["source_sha256"]:
        with urlopen(Request(LOCK["source_url"], headers={"User-Agent": "Parsarium C PLY verifier"}), timeout=120) as response, ARCHIVE.open("wb") as target:
            while chunk := response.read(1024 * 1024):
                target.write(chunk)
    assert digest(ARCHIVE) == LOCK["source_sha256"]
    with tarfile.open(ARCHIVE) as archive:
        for member, expected in LOCK["source_members"].items():
            file = archive.extractfile(member)
            assert file and sha256(file.read()).hexdigest() == expected, member
        with tempfile.TemporaryDirectory(prefix="parsarium-blukpast-") as work:
            archive.extractall(work, filter="data")
            source = Path(work) / "blukpast-1.0.6"
            binary = Path(work) / "blukpast-ply"
            compiler = os.environ.get("CC", "clang")
            # The published loader is C23 and uses x86 SIMD types in public headers.
            # On Apple Silicon, compile for x86_64 and execute through Rosetta.
            flags = ["-arch", "x86_64"] if platform.system() == "Darwin" else []
            dependency_cflags = shlex.split(run(["pkg-config", "--cflags", "vulkan", "glfw3"]))
            build = [compiler, *flags, "-std=gnu2x", "-O2", "-Wall", "-Wextra",
                     f"-I{source}", *dependency_cflags, str(ADAPTER),
                     str(source / "loaders/bkp_loader_ply.c"), "-o", str(binary)]
            run(build)
            execute = [str(binary), str(CONTROL)]
            output = json.loads(run(execute))
            assert output == PARSER["expected_output"], output
    result = json.loads((DATA / "verification.json").read_text())
    result["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    result.setdefault("local_libraries", {})["blukpast"] = {
        "source_sha256": LOCK["source_sha256"],
        "release_commit": LOCK["release_commit"],
        "adapter_sha256": LOCK["adapter_sha256"],
        "compiler": run([compiler, "--version"]).splitlines()[0],
        "architecture": platform.machine(),
        "build_scope": "Tagged upstream PLY loader linked to a C harness that captures the GPU upload arguments; full Vulkan engine not built.",
    }
    result["third_party"] = [row for row in result["third_party"] if row["package"] != "blukpast"]
    result["third_party"].append({
        "package": "blukpast", "version": "1.0.6", "control": PARSER["control"],
        "build_command": shlex.join(build), "command": shlex.join(execute),
        "output": output, "pass": True,
        "note": "Actual upstream C loader parsed the supplied ASCII PLY; only GPU upload and model storage were replaced by observation functions.",
    })
    (DATA / "verification.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("blukpast@1.0.6: C ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
