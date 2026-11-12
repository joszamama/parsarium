"""Build C++17 ZIP parser call sites and record valid-control results."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess

import prepare_cpp_zip
import verify_c_zip


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/zip"
ADAPTER = ROOT / "adapters/cpp/zip"
TARGET = ADAPTER / "target"
CONTROL = ROOT / "controls/zip/hello.zip"


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, check=True, text=True,
                          capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == verify_c_zip.CONTROL_SHA256
    # The C verifier checks every shared source archive and local binary pin.
    verify_c_zip.main()
    prepare_cpp_zip.main()
    c_parsers = {p["name"]: p for p in json.loads((ROOT / "data/c/zip/parsers.json").read_text())}
    c_runs = {r["package"]: r for r in json.loads((ROOT / "data/c/zip/verification.json").read_text())["third_party"]}
    parsers = json.loads((DATA / "parsers.json").read_text())
    extra_lock = json.loads((DATA / "extra-source-lock.json").read_text())
    assert len(parsers) == 14
    assert {p["name"] for p in parsers} == set(c_parsers) | set(extra_lock)
    assert set(c_parsers) == set(c_runs)
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    for parser in parsers:
        name = parser["name"]
        configure = None
        library_build = None
        if name == "libzippp":
            source = ADAPTER / "cache/libzippp/src"
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "libzip"]))
            command = ["c++", "-std=c++17", "-O2", "-I" + str(source),
                       str(ROOT / parser["adapter"]), str(source / "libzippp.cpp"),
                       *flags, "-o", str(TARGET / name)]
        elif name == "troldal-zippy":
            source = ADAPTER / "cache/troldal-zippy/library"
            command = ["c++", "-std=c++17", "-O2", "-I" + str(source),
                       str(ROOT / parser["adapter"]), "-o", str(TARGET / name)]
        elif name == "poco":
            source = ADAPTER / "cache/poco"
            build = TARGET / "poco-build"
            configure = ["cmake", "-S", str(source), "-B", str(build),
                         "-DPOCO_MINIMAL_BUILD=ON", "-DENABLE_ZIP=ON",
                         "-DBUILD_SHARED_LIBS=OFF", "-DENABLE_FASTLOGGER=OFF",
                         "-DENABLE_TESTS=OFF", "-DENABLE_SAMPLES=OFF",
                         "-DCMAKE_BUILD_TYPE=Release"]
            library_build = ["cmake", "--build", str(build), "--target", "Zip", "-j", "8"]
            run(configure)
            run(library_build)
            command = ["c++", "-std=c++20", "-O2", "-I" + str(source / "Zip/include"),
                       "-I" + str(source / "Foundation/include"),
                       str(ROOT / parser["adapter"]),
                       str(build / "lib/libPocoZip.a"), str(build / "lib/libPocoFoundation.a"),
                       "-o", str(TARGET / name)]
        elif name == "zipios":
            source = ADAPTER / "cache/zipios"
            build = TARGET / "zipios-build"
            configure = ["cmake", "-S", str(source), "-B", str(build),
                         "-DBUILD_SHARED_LIBS=OFF", "-DBUILD_DOCUMENTATION=OFF",
                         "-DBUILD_ZIPIOS_TESTS=OFF", "-DCMAKE_BUILD_TYPE=Release"]
            library_build = ["cmake", "--build", str(build), "--target", "zipios", "-j", "8"]
            run(configure)
            run(library_build)
            command = ["c++", "-std=c++17", "-O2", "-I" + str(source), "-I" + str(build),
                       str(ROOT / parser["adapter"]), str(build / "src/libzipios.a"),
                       "-lz", "-o", str(TARGET / name)]
        elif name == "zipper":
            source = ADAPTER / "cache/zipper"
            build = TARGET / "zipper-build"
            configure = ["cmake", "-S", str(source), "-B", str(build),
                         "-DZIPPER_BUILD_DEMOS=OFF", "-DZIPPER_BUILD_TESTS=OFF",
                         "-DUSE_AES=OFF", "-DCMAKE_SKIP_INSTALL_RULES=ON",
                         "-DCMAKE_BUILD_TYPE=Release"]
            library_build = ["cmake", "--build", str(build), "--target", "zipper", "-j", "8"]
            run(configure)
            run(library_build)
            command = ["c++", "-std=c++17", "-O2", "-I" + str(source / "include"),
                       str(ROOT / parser["adapter"]), str(build / "libzipper.a"),
                       str(build / "external/minizip/libminizip.a"),
                       str(build / "external/zlib-ng/libz.a"),
                       "-o", str(TARGET / name)]
        else:
            assert parser["version"] == c_parsers[name]["version"]
            assert parser["expected_output"] == c_parsers[name]["expected_output"]
            command = shlex.split(c_runs[name]["build_command"])
            assert command[0:2] == ["cc", "-std=c11"]
            command[0:2] = ["c++", "-std=c++17"]
            c_adapter = str(ROOT / c_parsers[name]["adapter"])
            command[command.index(c_adapter)] = str(ROOT / parser["adapter"])
            assert command[-2] == "-o"
            command[-1] = str(TARGET / name)
        run(command)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(command),
                     "configure_command": shlex.join(configure) if configure else None,
                     "library_build_command": shlex.join(library_build) if library_build else None,
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: C++ passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["c++", "--version"]).splitlines()[0],
              "source_lock": "data/c/zip/source-lock.json",
              "extra_source_lock": "data/cpp/zip/extra-source-lock.json",
              "prerequisite_verifier": "scripts/verify_c_zip.py",
              "control": "controls/zip/hello.zip",
              "control_sha256": verify_c_zip.CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
