"""Build pinned F3D 4.0.1 and check its C, C++, or Java PLY input API."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import shlex
import subprocess
import sys
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(tempfile.gettempdir()) / "parsarium-f3d-4.0.1"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
CONTROL_HASH = "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
EXPECTED = {"files": 1, "actors": 1, "points": 3, "cells": 1}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout[-3000:]}\n{result.stderr[-3000:]}")
    return result.stdout.strip()


def prepare() -> tuple[dict, Path, Path]:
    lock = json.loads((ROOT / "data/c/ascii_ply/source-lock.json").read_text())["f3d"]
    assert digest(CONTROL) == CONTROL_HASH
    for formula, version in lock["build_dependencies"].items():
        installed = run(["brew", "list", "--versions", formula]).split()
        assert version in installed, (formula, installed)
    for path, expected in lock["installed_files"].items():
        assert digest(Path(path)) == expected, path
    assert run([lock["cxx_compiler"], "--version"]).splitlines()[0] == lock["cxx_version"]
    CACHE.mkdir(exist_ok=True)
    archive = CACHE / "source.tar.gz"
    if not archive.exists() or digest(archive) != lock["source_sha256"]:
        request = Request(lock["source_url"], headers={"User-Agent": "Parsarium F3D verifier"})
        with urlopen(request, timeout=120) as response, archive.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
    assert digest(archive) == lock["source_sha256"]
    source = CACHE / "f3d-4.0.1"
    if not (source / "CMakeLists.txt").exists():
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                parts = Path(member.name).parts
                assert parts and parts[0] == "f3d-4.0.1" and ".." not in parts
            tar.extractall(CACHE, filter="data")
    for member, expected in lock["source_members"].items():
        assert digest(CACHE / member) == expected, member
    java_home = Path(run(["/usr/libexec/java_home", "-v", "21"]))
    assert run([str(java_home / "bin/javac"), "-version"]) == lock["javac_version"]
    build = CACHE / "build-llvm"
    configure = ["cmake", "-S", str(source), "-B", str(build),
                 "-DCMAKE_C_COMPILER=" + lock["c_compiler"],
                 "-DCMAKE_CXX_COMPILER=" + lock["cxx_compiler"],
                 "-DCMAKE_CXX_FLAGS=-include algorithm -include vector",
                 "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_PREFIX_PATH=/opt/homebrew",
                 "-DF3D_BUILD_APPLICATION=OFF", "-DF3D_BINDINGS_JAVA=ON",
                 "-DF3D_BINDINGS_C=ON", "-DF3D_MODULE_UI=OFF",
                 "-DF3D_MODULE_DMON=OFF", "-DF3D_MODULE_CLIP=OFF",
                 "-DF3D_MODULE_TINYFILEDIALOGS=OFF", "-DBUILD_TESTING=OFF",
                 "-DJAVA_INCLUDE_PATH=" + str(java_home / "include"),
                 "-DJAVA_INCLUDE_PATH2=" + str(java_home / "include/darwin"),
                 "-DJAVA_AWT_INCLUDE_PATH=" + str(java_home / "include"),
                 "-DJAVA_AWT_LIBRARY=" + str(java_home / "lib/libjawt.dylib"),
                 "-DJAVA_JVM_LIBRARY=" + str(java_home / "lib/server/libjvm.dylib")]
    run(configure, timeout=240)
    run(["cmake", "--build", str(build), "--parallel", "8"], timeout=1200)
    for artifact in ("lib/libf3d.dylib", "lib/libf3d_c_api.dylib",
                     "lib/libf3d-java.dylib", "java/f3d.jar"):
        assert (build / artifact).exists(), artifact
    return lock, source, build


def verify_native(ecosystem: str) -> tuple[dict, dict]:
    assert ecosystem in ("c", "cpp")
    lock, source, build = prepare()
    source_file = ROOT / f"adapters/{ecosystem}/ascii_ply/f3d.{ 'c' if ecosystem == 'c' else 'cpp' }"
    executable = CACHE / f"f3d-{ecosystem}-ply"
    library = build / "lib"
    if ecosystem == "c":
        command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                   "-I" + str(source / "c"), "-I" + str(build / "library/public"),
                   str(source_file), "-L" + str(library), "-Wl,-rpath," + str(library),
                   "-lf3d_c_api", "-o", str(executable)]
    else:
        command = [lock["cxx_compiler"], "-std=c++20", "-O2", "-Wall", "-Wextra",
                   "-Werror", "-I" + str(source / "library/public"),
                   "-I" + str(build / "library/public"), str(source_file),
                   "-L" + str(library), "-Wl,-rpath," + str(library),
                   "-lf3d", "-o", str(executable)]
    run(command)
    execute = [str(executable), str(CONTROL)]
    output = json.loads(run(execute).splitlines()[-1])
    assert output == EXPECTED, output
    row = {"package": "f3d", "version": "4.0.1", "control": "controls/ascii_ply/triangle.ply",
           "build_command": shlex.join(command), "command": shlex.join(execute),
           "output": output, "pass": True}
    local = {"source_sha256": lock["source_sha256"],
             "installed_files": lock["installed_files"],
             "underlying_family": "F3D native plugin over VTK vtkPLYReader"}
    return row, local


def verify_java() -> dict:
    lock, _, build = prepare()
    classes = CACHE / "classes"
    classes.mkdir(exist_ok=True)
    jar = build / "java/f3d.jar"
    source_file = ROOT / "adapters/java/ascii_ply/f3d/src/main/java/org/parsarium/F3DPlyAdapter.java"
    command = ["javac", "--release", "21", "-cp", str(jar), "-d", str(classes), str(source_file)]
    run(command)
    execute = ["java", "-Djava.library.path=" + str(build / "lib"),
               "-cp", f"{classes}:{jar}", "org.parsarium.F3DPlyAdapter", str(CONTROL)]
    output = json.loads(run(execute).splitlines()[-1])
    assert output == EXPECTED, output
    return {"package": "f3d", "version": "4.0.1", "control": "controls/ascii_ply/triangle.ply",
            "build_command": shlex.join(command), "command": shlex.join(execute),
            "output": output, "pass": True,
            "source_sha256": lock["source_sha256"],
            "underlying_family": "F3D native plugin over VTK vtkPLYReader"}


def record_java() -> None:
    row = verify_java()
    path = ROOT / "data/java/ascii_ply/verification.json"
    data = json.loads(path.read_text())
    data["third_party"] = [entry for entry in data["third_party"] if entry["package"] != "f3d"] + [row]
    data["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    data["environment"]["f3d"] = "F3D 4.0.1 source built with LLVM 23.1.4, VTK 9.7.2, JDK 21.0.2 on macOS 27.2 arm64"
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(row))


if __name__ == "__main__":
    if sys.argv[1:] == ["java"]:
        record_java()
    elif len(sys.argv) == 2 and sys.argv[1] in ("c", "cpp"):
        print(json.dumps(verify_native(sys.argv[1])[0]))
    else:
        raise SystemExit("usage: python3 scripts/verify_f3d_ascii_ply.py c|cpp|java")
