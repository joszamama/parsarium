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
    assert len(parsers) == 22
    assert {p["name"] for p in parsers} == set(c_parsers) | set(extra_lock)
    assert set(c_parsers) == set(c_runs)
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    local_libraries = {}
    for parser in parsers:
        name = parser["name"]
        configure = None
        library_build = None
        prerequisite_build_commands = []
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
        elif name == "bit7z":
            item = extra_lock[name]
            assert run(["brew", "list", "--versions", "sevenzip"]) == "sevenzip 26.04"
            library = Path(item["local_library"])
            digest = sha256(library.read_bytes()).hexdigest()
            assert digest == item["local_library_sha256"]
            local_libraries["sevenzip"] = {"release": "26.04", "library": str(library),
                                            "library_sha256": digest}
            source = ADAPTER / "cache/bit7z"
            build = TARGET / "bit7z-build"
            sevenzip_source = ADAPTER / "cache/sevenzip"
            configure = ["cmake", "-S", str(source), "-B", str(build),
                         "-DBIT7Z_CUSTOM_7ZIP_PATH=" + str(sevenzip_source),
                         "-DBIT7Z_BUILD_TESTS=OFF", "-DBIT7Z_BUILD_DOCS=OFF",
                         "-DBIT7Z_USE_PCH=OFF", "-DBIT7Z_7ZIP_VERSION=26.04",
                         "-DCMAKE_BUILD_TYPE=Release"]
            library_build = ["cmake", "--build", str(build), "--target", "bit7z", "-j", "8"]
            run(configure)
            run(library_build)
            command = ["c++", "-std=c++17", "-O2", "-I" + str(source / "include"),
                       str(ROOT / parser["adapter"]), str(source / "lib/arm64/libbit7z64.a"),
                       "-o", str(TARGET / name)]
        elif name in ("quazip", "karchive"):
            item = extra_lock[name]
            library = Path(item["local_library"])
            digest = sha256(library.read_bytes()).hexdigest()
            assert digest == item["local_library_sha256"], name
            package = item["pkg_config"]
            observed = run(["pkg-config", "--modversion", package])
            assert observed == item["release"], (name, observed)
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", package]))
            command = ["c++", "-std=c++17", "-O2", str(ROOT / parser["adapter"]),
                       *flags, "-o", str(TARGET / name)]
            local_libraries[name] = {"pkg_config_version": observed,
                                     "library": str(library), "library_sha256": digest}
        elif name == "qarchive":
            source = ADAPTER / "cache/qarchive"
            build = TARGET / "qarchive-build"
            archive_library = Path(verify_c_zip.DATA / "source-lock.json")
            archive_lock = json.loads(archive_library.read_text())["libarchive"]
            archive_binary = Path(archive_lock["local_library"])
            assert sha256(archive_binary.read_bytes()).hexdigest() == archive_lock["local_library_sha256"]
            configure = ["cmake", "-S", str(source), "-B", str(build),
                         "-DQARCHIVE_QT_VERSION_MAJOR=6",
                         "-DLIBARCHIVE_PKG_CONFIG=" + str(archive_binary.parent / "pkgconfig"),
                         "-DBUILD_TESTS=OFF", "-DBUILD_EXAMPLES=OFF",
                         "-DBUILD_SHARED_LIBS=OFF", "-DCMAKE_BUILD_TYPE=Release"]
            library_build = ["cmake", "--build", str(build), "--target", "QArchive", "-j", "8"]
            run(configure)
            run(library_build)
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "Qt6Core"]))
            command = ["c++", "-std=c++17", "-O2", "-I" + str(source / "include"),
                       "-I" + str(build), str(ROOT / parser["adapter"]),
                       str(build / "libQArchive.a"), str(archive_binary),
                       *flags, "-o", str(TARGET / name)]
        elif name == "sebastiandev-zipper":
            source = ADAPTER / "cache/sebastiandev-zipper"
            build = TARGET / "sebastiandev-zipper-build"
            configure = ["cmake", "-S", str(source), "-B", str(build),
                         "-DBUILD_SHARED_VERSION=OFF", "-DBUILD_STATIC_VERSION=ON",
                         "-DBUILD_TEST=OFF", "-DCMAKE_BUILD_TYPE=Release",
                         "-DCMAKE_POLICY_VERSION_MINIMUM=3.5"]
            library_build = ["cmake", "--build", str(build), "--target", "staticZipper", "-j", "8"]
            run(configure)
            run(library_build)
            command = ["c++", "-std=c++17", "-O2", "-I" + str(source),
                       str(ROOT / parser["adapter"]), str(build / "libZipper.a"),
                       "-lz", "-o", str(TARGET / name)]
        elif name == "unziplib":
            source = ROOT / "adapters/c/zip/cache/source/unziplib/src"
            build = TARGET / "unziplib-build"
            build.mkdir(parents=True, exist_ok=True)
            objects = []
            for stem in ("unzip", "adler32", "crc32", "infback", "inffast",
                         "inflate", "inftrees", "zutil"):
                obj = build / (stem + ".o")
                step = ["cc", "-std=c11", "-O2", "-Wno-deprecated-non-prototype",
                        "-Wno-macro-redefined", "-include", "stdio.h",
                        "-I" + str(source), "-c", str(source / (stem + ".c")),
                        "-o", str(obj)]
                run(step)
                prerequisite_build_commands.append(shlex.join(step))
                objects.append(obj)
            library = build / "libunziplib.a"
            library_build = ["ar", "rcs", str(library), *map(str, objects)]
            run(library_build)
            command = ["c++", "-std=c++17", "-O2", "-I" + str(source),
                       str(ROOT / parser["adapter"]), str(library),
                       "-o", str(TARGET / name)]
        else:
            assert parser["version"] == c_parsers[name]["version"]
            assert parser["expected_output"] == c_parsers[name]["expected_output"]
            command = shlex.split(c_runs[name]["build_command"])
            assert command[0:2] == ["cc", "-std=c11"]
            command[0:2] = ["c++", "-std=c++17"]
            if name == "lowzip":
                command[2:2] = ["-x", "c++"]
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
                     "prerequisite_build_commands": prerequisite_build_commands,
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: C++ passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["c++", "--version"]).splitlines()[0],
              "source_lock": "data/c/zip/source-lock.json",
              "extra_source_lock": "data/cpp/zip/extra-source-lock.json",
              "local_libraries": local_libraries,
              "prerequisite_verifier": "scripts/verify_c_zip.py",
              "control": "controls/zip/hello.zip",
              "control_sha256": verify_c_zip.CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
