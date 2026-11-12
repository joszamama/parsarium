"""Rebuild pinned C PNG adapters and record valid-control observations."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess

import prepare_c_png


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/png"
ADAPTER = ROOT / "adapters/c/png"
SOURCE = ADAPTER / "cache/source"
TARGET = ADAPTER / "target"
CONTROL = ROOT / "controls/png/red-green.png"
CONTROL_SHA256 = "5a852fbaaaecaf4cd14c01e150c7f881c5c5894b0a1e3c53be7e007c58374ee6"
EXPECTED = {"width": 2, "height": 1, "first": [255, 0, 0, 255], "second": [0, 255, 0, 255]}


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    prepare_c_png.main()
    lock = json.loads((DATA / "source-lock.json").read_text())
    parsers = json.loads((DATA / "parsers.json").read_text())
    assert len(parsers) == 12
    zlib_version = run(["pkg-config", "--modversion", "zlib"])
    assert zlib_version == "1.2.12"
    TARGET.mkdir(parents=True, exist_ok=True)
    build = TARGET / "libpng-build"
    run(["cmake", "-S", str(SOURCE / "libpng"), "-B", str(build),
         "-DPNG_SHARED=OFF", "-DPNG_STATIC=ON", "-DPNG_TESTS=OFF", "-DCMAKE_BUILD_TYPE=Release"])
    run(["cmake", "--build", str(build), "--target", "png_static", "-j", "4"])
    commands = {
        "libpng": ["cc", "-std=c11", "-O2", "-I" + str(SOURCE / "libpng"),
                   "-I" + str(build), str(ADAPTER / "libpng.c"),
                   str(build / "libpng16.a"), "-lz", "-lm", "-o", str(TARGET / "libpng")],
        "stb": ["cc", "-std=c11", "-O2", "-I" + str(SOURCE / "stb"), str(ADAPTER / "stb.c"), "-lm", "-o", str(TARGET / "stb")],
        "lodepng": ["cc", "-std=c11", "-O2", "-I" + str(SOURCE / "lodepng"), str(ADAPTER / "lodepng_adapter.c"), str(SOURCE / "lodepng/lodepng.c"), "-o", str(TARGET / "lodepng")],
        "libspng": ["cc", "-std=c11", "-O2", "-I" + str(SOURCE / "libspng"), str(ADAPTER / "libspng_adapter.c"), str(SOURCE / "libspng/spng.c"), "-lz", "-o", str(TARGET / "libspng")],
        "pngle": ["cc", "-std=c11", "-O2", "-I" + str(SOURCE / "pngle"),
                  str(ADAPTER / "pngle.c"), str(SOURCE / "pngle/pngle.c"),
                  str(SOURCE / "pngle/miniz.c"), "-lm", "-o", str(TARGET / "pngle")],
    }
    local_libraries = {}
    for name, adapter_name in (("imagemagick", "imagemagick"),
                               ("gdk-pixbuf", "gdk_pixbuf"), ("vips", "vips"),
                               ("sdl3", "sdl3"), ("sdl3_image", "sdl3_image"),
                               ("sdl2_image", "sdl2_image")):
        item = lock[name]
        observed = run(["pkg-config", "--modversion", item["pkg_config"]])
        if name == "imagemagick":
            assert observed == item["release"].rsplit("-", 1)[0]
            assert item["release"] in run(["magick", "-version"])
        else:
            assert observed == item["release"]
        library = Path(item["local_library"])
        digest = sha256(library.read_bytes()).hexdigest()
        assert digest == item["local_library_sha256"]
        local_libraries[name] = {"pkg_config_version": observed, "library": str(library),
                                 "library_sha256": digest}
        flags = shlex.split(run(["pkg-config", "--cflags", "--libs", item["pkg_config"]]))
        commands[name] = ["cc", "-std=c11", "-O2", str(ADAPTER / (adapter_name + ".c")),
                          *flags, "-o", str(TARGET / name)]
    freeimage = lock["freeimage"]
    library = Path(freeimage["local_library"])
    digest = sha256(library.read_bytes()).hexdigest()
    assert digest == freeimage["local_library_sha256"]
    local_libraries["freeimage"] = {"release": freeimage["release"],
                                    "library": str(library), "library_sha256": digest}
    prefix = library.parents[1]
    commands["freeimage"] = ["cc", "-std=c11", "-O2", "-I" + str(prefix / "include"),
                              str(ADAPTER / "freeimage.c"), "-L" + str(prefix / "lib"),
                              "-lfreeimage", "-o", str(TARGET / "freeimage")]
    rows = []
    for parser in parsers:
        name = parser["name"]
        assert parser["version"] == lock[name]["release"]
        run(commands[name])
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == EXPECTED == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(commands[name]),
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["cc", "--version"]).splitlines()[0],
              "libpng_source_sha256": lock["libpng"]["source_sha256"],
              "libpng_build": "CMake static png_static from pinned libpng 1.6.59 archive",
              "zlib_pkg_config_version": zlib_version,
              "local_libraries": local_libraries,
              "control": "controls/png/red-green.png", "control_sha256": CONTROL_SHA256,
              "expected": EXPECTED, "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
