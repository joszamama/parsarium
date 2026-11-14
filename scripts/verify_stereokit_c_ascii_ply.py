"""Build the tagged StereoKit C ABI and replay a valid local ASCII PLY control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import shutil
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER = ROOT / "adapters/c/ascii_ply/stereokit.c"
LOCK = json.loads((DATA / "source-lock.json").read_text())["stereokit"]
PARSER = next(x for x in json.loads((DATA / "parsers.json").read_text()) if x["name"] == "stereokit")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int = 1200) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{' '.join(command)}\n{result.stdout[-6000:]}\n{result.stderr[-6000:]}")
    return result.stdout


def verify() -> None:
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    assert digest(ADAPTER) == LOCK["adapter_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-stereokit-") as temporary:
        work = Path(temporary)
        archive = work / "source.tar.gz"
        with urlopen(Request(LOCK["source_url"], headers={"User-Agent": "Parsarium PLY verifier"}), timeout=120) as response:
            archive.write_bytes(response.read())
        assert digest(archive) == LOCK["source_sha256"]
        with tarfile.open(archive) as tar:
            tar.extractall(work / "extracted", filter="data")
        source = next((work / "extracted").iterdir())
        for filename, expected in LOCK["source_files_sha256"].items():
            assert digest(source / filename) == expected, filename

        header = (source / "StereoKitC/stereokit.h").read_text()
        old = "quit_reason_ quitReason = quit_reason_user"
        assert header.count(old) == 1
        (source / "stereokit_c_compat.h").write_text(header.replace(old, "quit_reason_ quitReason"))
        shutil.copy2(ADAPTER, source / "stereokit.c")
        shutil.copy2(CONTROL, source / "triangle.ply")

        replay = source / "replay.sh"
        replay.write_text("""#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq >/src/apt.log 2>&1
apt-get install -y -qq build-essential cmake ninja-build git curl ca-certificates libegl1-mesa-dev libgbm-dev libx11-dev libxfixes-dev libfontconfig1-dev libxrandr-dev libxinerama-dev libxcursor-dev >/src/apt.log 2>&1
cmake -S /src -B /src/build -G Ninja -DSK_BUILD_TESTS=OFF -DSK_PHYSICS=OFF -DSK_BUILD_SHARED_LIBS=ON >/src/configure.log 2>&1
cmake --build /src/build --target StereoKitC -j4 >/src/build.log 2>&1
cc -std=c11 -O2 -Wno-unused-variable -I /src /src/stereokit.c -L /src/build -Wl,-rpath,/src/build -lStereoKitC -o /src/stereokit-ply-control
/src/stereokit-ply-control /src/triangle.ply
""")
        command = ["docker", "run", "--rm", "-v", f"{source}:/src", "-w", "/src",
                   LOCK["docker_image"], "bash", "/src/replay.sh"]
        stdout = run(command)
        outputs = [json.loads(line) for line in stdout.splitlines() if line.startswith("{")]
        assert outputs == [PARSER["expected_output"]], outputs
        output = outputs[0]

    results = json.loads((DATA / "verification.json").read_text())
    results["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    results.setdefault("local_libraries", {})["stereokit"] = {
        "source_sha256": LOCK["source_sha256"],
        "release_commit": LOCK["release_commit"],
        "adapter_sha256": LOCK["adapter_sha256"],
        "docker_image": LOCK["docker_image"],
        "host_platform": platform.platform(),
        "build_scope": "Full tagged StereoKitC shared library in Ubuntu 24.04 arm64; C11 adapter uses a one-line header compatibility copy for an unguarded C++ default argument. Offscreen Mesa EGL initialization and model file loading passed."
    }
    results["third_party"] = [x for x in results["third_party"] if x["package"] != "stereokit"]
    results["third_party"].append({
        "package": "stereokit", "version": "v0.3.11", "control": PARSER["control"],
        "build_command": "cmake -S /src -B /src/build -G Ninja -DSK_BUILD_TESTS=OFF -DSK_PHYSICS=OFF -DSK_BUILD_SHARED_LIBS=ON; cmake --build /src/build --target StereoKitC -j4; cc -std=c11 -O2 -I /src /src/stereokit.c -L /src/build -Wl,-rpath,/src/build -lStereoKitC -o /src/stereokit-ply-control",
        "command": "/src/stereokit-ply-control /src/triangle.ply",
        "output": output, "pass": True,
        "note": "Full StereoKit C ABI parsed a local PLY file, returning one mesh subset, three vertex coordinates, and triangle indices. C header compatibility copy removes an invalid C++ default argument only. Shares the micro_ply parser family."
    })
    (DATA / "verification.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    print("StereoKit@v0.3.11: C ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
