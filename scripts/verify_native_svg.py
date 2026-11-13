"""Verify pinned C or C++ SVG readers on a valid two-rectangle SVG."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import shlex
import shutil
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "controls/svg/red-green.svg"
CONTROL_SHA256 = "ba543b92d6a2c405691fce177270bd55fa13d9866a4128495c3dc93ed7bfd3d2"


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], cwd: Path = ROOT, timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def verify(ecosystem: str) -> None:
    assert ecosystem in ("c", "cpp")
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    data = ROOT / "data" / ecosystem / "svg"
    cache = Path(tempfile.gettempdir()) / f"parsarium-{ecosystem}-svg"
    target = ROOT / "adapters" / ecosystem / "svg/target"
    cache.mkdir(parents=True, exist_ok=True)
    target.mkdir(parents=True, exist_ok=True)
    parsers = json.loads((data / "parsers.json").read_text())
    lock = json.loads((data / "source-lock.json").read_text())
    assert len(parsers) == json.loads((data / "cell.json").read_text())["verified_third_party_count"]
    rows = []
    libraries = {}
    for parser in parsers:
        name = parser["name"]
        source = lock[name]
        suffix = ".tar.xz" if source["source_url"].endswith(".tar.xz") else (
            ".tar.bz2" if source["source_url"].endswith(".tar.bz2") else ".tar.gz")
        archive = cache / f"{name}-{source['release']}{suffix}"
        if not archive.exists() or file_sha256(archive) != source["source_sha256"]:
            partial = archive.with_suffix(archive.suffix + ".part")
            with urlopen(Request(source["source_url"], headers={"User-Agent": "Parsarium SVG verifier"}), timeout=120) as response:
                with partial.open("wb") as output:
                    shutil.copyfileobj(response, output, length=1024 * 1024)
            partial.replace(archive)
        assert file_sha256(archive) == source["source_sha256"]
        with tarfile.open(archive) as tar:
            member = tar.extractfile(source["source_header_member"])
            assert member is not None
            assert sha256(member.read()).hexdigest() == source["local_header_sha256"]
            if "license_member" in source:
                license_member = tar.extractfile(source["license_member"])
                assert license_member is not None
                assert sha256(license_member.read()).hexdigest() == source["license_sha256"]
            if "source_engine_member" in source:
                engine_member = tar.extractfile(source["source_engine_member"])
                assert engine_member is not None
                assert sha256(engine_member.read()).hexdigest() == source["source_engine_sha256"]
            for engine in source.get("source_engine_members", []):
                engine_member = tar.extractfile(engine["member"])
                assert engine_member is not None
                assert sha256(engine_member.read()).hexdigest() == engine["sha256"]
        formula = "vips" if name == "libvips" else ("gtk+3" if name == "gtk3" else name)
        source_build = None
        juce_binary = None
        juce_build_command = None
        imlib2_build_command = None
        if name == "nanosvg":
            source_dir = cache / source["archive_root"]
            if source_dir.exists():
                shutil.rmtree(source_dir)
            source_build = ["tar", "-xzf", str(archive), "-C", str(cache)]
            run(source_build)
            header = source_dir / "src/nanosvg.h"
            library = None
        elif name == "novasvg":
            source_dir = cache / f"novasvg-{source['release']}"
            if source_dir.exists():
                shutil.rmtree(source_dir)
            run(["tar", "-xzf", str(archive), "-C", str(cache)])
            header = source_dir / "include/novasvg/novasvg.h"
            library = None
            source_build = ["tar", "-xzf", str(archive), "-C", str(cache)]
        elif name == "juce":
            source_dir = cache / f"JUCE-{source['release']}"
            if source_dir.exists():
                shutil.rmtree(source_dir)
            run(["tar", "-xzf", str(archive), "-C", str(cache)])
            header = source_dir / "modules/juce_graphics/drawables/juce_Drawable.h"
            library = None
            build_dir = cache / "juce-svg-build"
            configure = ["cmake", "-S", str(ROOT / "adapters/cpp/svg/juce"), "-B", str(build_dir),
                         "-DJUCE_SOURCE_DIR=" + str(source_dir), "-DCMAKE_BUILD_TYPE=Release",
                         "-DCMAKE_OSX_ARCHITECTURES=arm64"]
            build = ["cmake", "--build", str(build_dir), "--target", "parsarium_juce_svg", "-j8"]
            run(configure, timeout=600)
            run(build, timeout=900)
            juce_binary = build_dir / "parsarium_juce_svg_artefacts/Release/parsarium_juce_svg"
            source_build = configure
            juce_build_command = shlex.join(configure) + " && " + shlex.join(build)
        elif name == "resvg":
            source_dir = cache / f"resvg-{source['release']}"
            if source_dir.exists():
                shutil.rmtree(source_dir)
            run(["tar", "-xzf", str(archive), "-C", str(cache)])
            header = source_dir / "crates/c-api/resvg.h"
            assert sha256((source_dir / "Cargo.lock").read_bytes()).hexdigest() == source["cargo_lock_sha256"]
            source_build = ["cargo", "build", "--release", "--locked", "-p", "resvg-capi"]
            run(source_build, cwd=source_dir, timeout=900)
            library = source_dir / "target/release/libresvg.dylib"
        elif name == "imlib2":
            source_dir = cache / f"imlib2-{source['release']}"
            build_dir = cache / "imlib2-svg-build"
            install_dir = cache / "imlib2-svg-install"
            for directory in (source_dir, build_dir, install_dir):
                if directory.exists():
                    shutil.rmtree(directory)
            run(["tar", "-xf", str(archive), "-C", str(cache)])
            build_dir.mkdir()
            install_dir.mkdir()
            configure = [str(source_dir / "configure"), "--prefix=" + str(install_dir),
                         "--with-svg", "--without-x", "--without-raw"]
            build = ["make", "-j8"]
            install = ["make", "install"]
            run(configure, cwd=build_dir, timeout=600)
            run(build, cwd=build_dir, timeout=600)
            run(install, cwd=build_dir, timeout=600)
            source_build = configure
            imlib2_build_command = " && ".join(map(shlex.join, (configure, build, install)))
            header = install_dir / "include/Imlib2.h"
            library = install_dir / "lib/libImlib2.1.dylib"
            svg_loader = install_dir / "lib/imlib2/loaders/svg.so"
            assert svg_loader.is_file()
            for dependency in source.get("installed_dependencies", []):
                assert dependency["revision"] in run(["brew", "list", "--versions", dependency["formula"]]).split()
                assert file_sha256(Path(dependency["path"])) == dependency["sha256"]
        else:
            assert source["installed_revision"] in run(["brew", "list", "--versions", formula]).split()
            if name == "wxwidgets":
                assert run(["wx-config", "--version"]) == source["release"]
            elif source.get("pkg_config"):
                assert run(["pkg-config", "--modversion", source["pkg_config"]]) == source.get("pkg_config_version", source["release"])
            header = Path(source["local_header"])
            library = Path(source["local_library"])
            assert file_sha256(library) == source["local_library_sha256"]
            for dependency in source.get("installed_dependencies", []):
                if "formula" in dependency:
                    assert dependency["revision"] in run(["brew", "list", "--versions", dependency["formula"]]).split()
                assert file_sha256(Path(dependency["path"])) == dependency["sha256"]
        assert file_sha256(header) == source["local_header_sha256"]
        compiler = "c++" if ecosystem == "cpp" else "cc"
        std = "-std=c++17" if ecosystem == "cpp" else "-std=c11"
        if name == "juce":
            command = source_build
        elif name == "wxwidgets":
            flags = shlex.split(run(["wx-config", "--cxxflags", "--libs", "core,base"]))
            command = [compiler, std, "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        elif name == "nanosvg":
            command = [compiler, std, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parent), str(ROOT / parser["adapter"]),
                       "-lm", "-o", str(target / name)]
        elif name == "mupdf":
            command = [compiler, std, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(header.parent.parent), str(ROOT / parser["adapter"]),
                       "-L" + str(library.parent), "-lmupdf", "-o", str(target / name)]
        elif name == "novasvg":
            command = [compiler, std, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(header.parent.parent), str(ROOT / parser["adapter"]),
                       "-o", str(target / name)]
        elif name == "resvg":
            command = [compiler, std, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parent), str(ROOT / parser["adapter"]),
                       str(library), "-Wl,-rpath," + str(library.parent), "-o", str(target / name)]
        elif name == "imlib2":
            x11_flags = shlex.split(run(["pkg-config", "--cflags", "x11"]))
            command = [compiler, std, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parent), *x11_flags, str(ROOT / parser["adapter"]),
                       "-L" + str(library.parent), "-lImlib2",
                       "-Wl,-rpath," + str(library.parent), "-o", str(target / name)]
        else:
            if name in ("libsvg", "libsvg-cairo"):
                # These old .pc files require -lpng/-ljpeg without their Homebrew
                # library paths. Their dylibs already link those dependencies.
                flags = shlex.split(run(["pkg-config", "--cflags", source["pkg_config"]]))
                flags += ["-L" + str(library.parent), "-l" + name.removeprefix("lib")]
                if name == "libsvg-cairo":
                    svg_library = next(Path(item["path"]) for item in source["installed_dependencies"]
                                       if item.get("formula") == "libsvg")
                    flags += ["-L" + str(svg_library.parent), "-lsvg"]
                    flags += shlex.split(run(["pkg-config", "--libs", "cairo"]))
            else:
                flags = shlex.split(run(["pkg-config", "--cflags", "--libs", source["pkg_config"], *(["cairo"] if name == "librsvg" else [])]))
            command = [compiler, std, "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        if name != "juce":
            run(command)
        execute = [str(juce_binary if juce_binary is not None else target / name), str(CONTROL)]
        if name in ("qtdeclarative", "qtwebengine"):
            execute = ["env", "QT_QPA_PLATFORM=offscreen", *execute]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        row = {"package": name, "version": parser["version"], "control": parser["control"],
                     "build_command": juce_build_command or shlex.join(command), "command": shlex.join(execute),
                     "output": output, "pass": True}
        if source_build is not None:
            row["source_build_command"] = juce_build_command or imlib2_build_command or shlex.join(source_build)
        rows.append(row)
        libraries[name] = {"source_sha256": source["source_sha256"],
                           "local_header_sha256": source["local_header_sha256"]}
        if library is not None:
            libraries[name]["local_library_sha256"] = file_sha256(library)
        if name == "imlib2":
            libraries[name]["svg_loader_sha256"] = file_sha256(svg_loader)
        if juce_binary is not None:
            libraries[name]["built_executable_sha256"] = file_sha256(juce_binary)
        print(f"{name}@{parser['version']}: {ecosystem} SVG passed", flush=True)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["c++" if ecosystem == "cpp" else "cc", "--version"]).splitlines()[0],
              "source_lock": f"data/{ecosystem}/svg/source-lock.json", "local_libraries": libraries,
              "control": "controls/svg/red-green.svg", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (data / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
