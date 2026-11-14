"""Build C++ call sites for pinned PNG libraries and record valid-control results."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess

import verify_c_png


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/png"
ADAPTER = ROOT / "adapters/cpp/png"
TARGET = ADAPTER / "target"
CONTROL = ROOT / "controls/png/red-green.png"


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, check=True, text=True,
                          capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == verify_c_png.CONTROL_SHA256
    # This checks every source and local binary pin before using the same packages from C++.
    verify_c_png.main()
    c_parsers = {p["name"]: p for p in json.loads((ROOT / "data/c/png/parsers.json").read_text())}
    c_runs = {r["package"]: r for r in json.loads((ROOT / "data/c/png/verification.json").read_text())["third_party"]}
    parsers = json.loads((DATA / "parsers.json").read_text())
    extra_lock = json.loads((DATA / "extra-source-lock.json").read_text())
    assert len(parsers) == 24 and {p["name"] for p in parsers} == set(c_parsers) | {"sfml", "opencv", "openimageio", "wxwidgets"}
    assert set(c_parsers) == set(c_runs) and set(extra_lock) == {"sfml", "opencv", "openimageio", "wxwidgets"}
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    local_libraries = {}
    for parser in parsers:
        name = parser["name"]
        prebuild_command = None
        if name == "wxwidgets":
            item = extra_lock[name]
            assert parser["version"] == item["release"]
            assert platform.system() == "Darwin" and platform.machine() == "arm64"
            assert run(["brew", "list", "--versions", name]) == f"{name} {item['release']}"
            assert run(["wx-config", "--version"]) == item["release"]
            assert sha256(Path(run(["brew", "--cache", name])).read_bytes()).hexdigest() == item["bottle_sha256"]
            prefix = Path(run(["brew", "--prefix", name]))
            headers = {header: prefix / header for header in item["installed_headers"]}
            assert all(sha256(path.read_bytes()).hexdigest() == item["installed_headers"][header]
                       for header, path in headers.items())
            libraries = {library: prefix / "lib" / library for library in item["installed_libraries"]}
            assert all(sha256(path.read_bytes()).hexdigest() == item["installed_libraries"][library]
                       for library, path in libraries.items())
            libpng = Path(item["linked_libpng"])
            assert sha256(libpng.read_bytes()).hexdigest() == item["linked_libpng_sha256"]
            assert str(libpng) in run(["otool", "-L", str(libraries["libwx_osx_cocoau_core-3.3.4.0.0.dylib"])])
            flags = shlex.split(run(["wx-config", "--cxxflags"])) + shlex.split(run(["wx-config", "--libs", "base,core"]))
            command = ["c++", "-std=c++17", "-O2", str(ROOT / parser["adapter"]),
                       *flags, "-o", str(TARGET / name)]
            local_libraries[name] = {"bottle_sha256": item["bottle_sha256"],
                                     "header_sha256": item["installed_headers"],
                                     "library_sha256": item["installed_libraries"],
                                     "linked_libpng_sha256": item["linked_libpng_sha256"]}
        elif name == "openimageio":
            item = extra_lock[name]
            assert parser["version"] == item["release"]
            assert platform.system() == "Darwin" and platform.machine() == "arm64"
            assert run(["brew", "list", "--versions", name]) == f"{name} {item['bottle_release']}"
            assert sha256(Path(run(["brew", "--cache", name])).read_bytes()).hexdigest() == item["bottle_sha256"]
            prefix = Path(run(["brew", "--prefix", name]))
            header = prefix / item["installed_header"]
            assert sha256(header.read_bytes()).hexdigest() == item["installed_header_sha256"]
            libraries = {library: prefix / "lib" / library for library in item["installed_libraries"]}
            assert all(sha256(path.read_bytes()).hexdigest() == item["installed_libraries"][library]
                       for library, path in libraries.items())
            libpng = Path(item["linked_libpng"])
            assert sha256(libpng.read_bytes()).hexdigest() == item["linked_libpng_sha256"]
            assert str(libpng) in run(["otool", "-L", str(libraries["libOpenImageIO.3.2.2.dylib"])])
            assert run(["pkg-config", "--modversion", "fmt"]) == item["fmt_release"]
            fmt_prefix = Path(run(["brew", "--prefix", "fmt"]))
            fmt_header = fmt_prefix / "include/fmt/format.h"
            assert sha256(fmt_header.read_bytes()).hexdigest() == item["fmt_header_sha256"]
            fmt_library = fmt_prefix / "lib/libfmt.12.2.1.dylib"
            assert sha256(fmt_library.read_bytes()).hexdigest() == item["fmt_library_sha256"]
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "OpenImageIO", "fmt"]))
            command = ["c++", "-std=c++17", "-O2", str(ROOT / parser["adapter"]),
                       *flags, "-Wl,-rpath," + str(prefix / "lib"), "-o", str(TARGET / name)]
            local_libraries[name] = {"bottle_sha256": item["bottle_sha256"],
                                     "header_sha256": item["installed_header_sha256"],
                                     "library_sha256": item["installed_libraries"],
                                     "linked_libpng_sha256": item["linked_libpng_sha256"],
                                     "fmt_header_sha256": item["fmt_header_sha256"],
                                     "fmt_library_sha256": item["fmt_library_sha256"]}
        elif name == "opencv":
            item = extra_lock[name]
            assert parser["version"] == item["release"]
            assert platform.system() == "Darwin" and platform.machine() == "arm64"
            assert run(["brew", "list", "--versions", name]) == f"{name} {item['release']}"
            assert sha256(Path(run(["brew", "--cache", name])).read_bytes()).hexdigest() == item["bottle_sha256"]
            prefix = Path(run(["brew", "--prefix", name]))
            header = prefix / item["installed_header"]
            assert sha256(header.read_bytes()).hexdigest() == item["installed_header_sha256"]
            libraries = {library: prefix / "lib" / library for library in item["installed_libraries"]}
            assert all(sha256(path.read_bytes()).hexdigest() == item["installed_libraries"][library]
                       for library, path in libraries.items())
            libpng = Path(item["linked_libpng"])
            assert sha256(libpng.read_bytes()).hexdigest() == item["linked_libpng_sha256"]
            assert str(libpng) in run(["otool", "-L", str(libraries["libopencv_imgcodecs.5.1.0.dylib"])])
            command = ["c++", "-std=c++17", "-O2", str(ROOT / parser["adapter"]),
                       "-I" + str(prefix / "include/opencv5"), "-L" + str(prefix / "lib"),
                       "-Wl,-rpath," + str(prefix / "lib"), "-lopencv_imgcodecs", "-lopencv_core",
                       "-o", str(TARGET / name)]
            local_libraries[name] = {"bottle_sha256": item["bottle_sha256"],
                                     "header_sha256": item["installed_header_sha256"],
                                     "library_sha256": item["installed_libraries"],
                                     "linked_libpng_sha256": item["linked_libpng_sha256"]}
        elif name == "sfml":
            item = extra_lock[name]
            assert parser["version"] == item["release"]
            assert run(["pkg-config", "--modversion", item["pkg_config"]]) == item["release"]
            library = Path(item["local_library"])
            digest = sha256(library.read_bytes()).hexdigest()
            assert digest == item["local_library_sha256"]
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", item["pkg_config"]]))
            command = ["c++", "-std=c++17", "-O2", str(ROOT / parser["adapter"]),
                       *flags, "-o", str(TARGET / name)]
            local_libraries[name] = {"pkg_config_version": item["release"],
                                     "library": str(library), "library_sha256": digest}
        else:
            assert parser["version"] == c_parsers[name]["version"]
            assert parser["expected_output"] == c_parsers[name]["expected_output"]
            command = shlex.split(c_runs[name]["build_command"])
            assert command[0] == "cc" and command[1] == "-std=c11"
            command[0:2] = ["c++", "-std=c++17"]
            c_adapter = str(ROOT / c_parsers[name]["adapter"])
            command[command.index(c_adapter)] = str(ROOT / parser["adapter"])
            assert command[-2] == "-o"
            command[-1] = str(TARGET / name)
            if name == "libspng":
                source = ROOT / "adapters/c/png/cache/source/libspng/spng.c"
                object_file = TARGET / "spng.o"
                prebuild_command = ["cc", "-std=c11", "-O2", "-I" + str(source.parent),
                                    "-c", str(source), "-o", str(object_file)]
                run(prebuild_command)
                command[command.index(str(source))] = str(object_file)
        run(command)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(command),
                     "prebuild_command": shlex.join(prebuild_command) if prebuild_command else None,
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: C++ passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["c++", "--version"]).splitlines()[0],
              "source_lock": "data/c/png/source-lock.json",
              "extra_source_lock": "data/cpp/png/extra-source-lock.json",
              "local_libraries": local_libraries,
              "prerequisite_verifier": "scripts/verify_c_png.py",
              "control": "controls/png/red-green.png",
              "control_sha256": verify_c_png.CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
