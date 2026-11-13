"""Verify pinned C and C++ MP4 readers on a valid two-track local file."""

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
CONTROL = ROOT / "controls/mp4/red-av.mp4"
CONTROL_SHA256 = "10086c39c7226726579924794cd7c0bbafe65de38021bd0f38f6da9d23d24643"


def run(command: list[str], timeout: int = 180, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout,
                            env={**os.environ, **(env or {})})
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def build_bento4(archive: Path, cache: Path, ecosystem: str) -> tuple[list[str], list[str], dict[str, str]]:
    """Build the pinned AP4 core and its separate C binding from source."""
    source_dir = cache / "Bento4-1.6.0-641"
    if not source_dir.exists():
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                path = Path(member.name)
                if path.is_absolute() or ".." in path.parts or not (member.name == "Bento4-1.6.0-641" or member.name.startswith("Bento4-1.6.0-641/")):
                    raise ValueError(f"unsafe Bento4 archive path: {member.name}")
            tar.extractall(cache, filter="data")
    build_dir = cache / "bento4-build"
    run(["cmake", "-S", str(source_dir), "-B", str(build_dir), "-DBUILD_APPS=OFF",
         "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_OSX_ARCHITECTURES=arm64"], timeout=300)
    run(["cmake", "--build", str(build_dir), "--target", "ap4", "-j8"], timeout=600)
    include_dirs = [source_dir / "Source/C++" / part for part in ("Core", "Codecs", "Crypto", "MetaData")]
    run(["c++", "-std=c++17", "-O2", *(f"-I{path}" for path in include_dirs), "-c",
         str(source_dir / "Source/C++/CApi/Bento4C.cpp"), "-o", str(build_dir / "Bento4C.o")], timeout=300)
    run(["ar", "rcs", str(build_dir / "libbento4c.a"), str(build_dir / "Bento4C.o")])
    flags = ["-I" + str(source_dir / "Source/C++/CApi"), "-I" + str(include_dirs[0])]
    libs = [str(build_dir / "libbento4c.a"), str(build_dir / "libap4.a")]
    hashes = {"source_header_sha256": sha256((source_dir / "Source/C++/CApi/Bento4C.h").read_bytes()).hexdigest(),
              "local_library_sha256": sha256((build_dir / "libap4.a").read_bytes()).hexdigest(),
              "c_binding_library_sha256": sha256((build_dir / "libbento4c.a").read_bytes()).hexdigest()}
    return flags, libs, hashes


def build_libmp4tag(archive: Path, cache: Path) -> tuple[list[str], list[str], dict[str, str]]:
    """Build the pinned C library and generated public header from its release."""
    source_dir = cache / "libmp4tag-2.0.4"
    if not source_dir.exists():
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                path = Path(member.name)
                if path.is_absolute() or ".." in path.parts or not (
                    member.name == "libmp4tag-2.0.4" or member.name.startswith("libmp4tag-2.0.4/")
                ):
                    raise ValueError(f"unsafe libmp4tag archive path: {member.name}")
            tar.extractall(cache, filter="data")
    build_dir = cache / "libmp4tag-build"
    run(["cmake", "-S", str(source_dir), "-B", str(build_dir),
         "-DCMAKE_BUILD_TYPE=Release", "-DBUILD_SHARED_LIBS=OFF",
         "-DCMAKE_INSTALL_PREFIX=" + str(cache / "libmp4tag-install")], timeout=300)
    run(["cmake", "--build", str(build_dir), "--target", "libmp4tag", "-j4"], timeout=300)
    library = build_dir / "libmp4tag.a"
    header = build_dir / "libmp4tag.h"
    return (["-I" + str(build_dir)], [str(library)],
            {"generated_header_sha256": sha256(header.read_bytes()).hexdigest(),
             "local_library_sha256": sha256(library.read_bytes()).hexdigest()})


def build_avcpp(archive: Path, cache: Path, compiler: str) -> tuple[list[str], list[str], dict[str, str]]:
    """Build the pinned C++ FFmpeg wrapper with a C++20 ranges-capable toolchain."""
    source_dir = cache / "avcpp-3.0.1"
    if not source_dir.exists():
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                path = Path(member.name)
                if path.is_absolute() or ".." in path.parts or not (
                    member.name == "avcpp-3.0.1" or member.name.startswith("avcpp-3.0.1/")
                ):
                    raise ValueError(f"unsafe AvCpp archive path: {member.name}")
            tar.extractall(cache, filter="data")
    build_dir = cache / "avcpp-build"
    run(["cmake", "-S", str(source_dir), "-B", str(build_dir),
         "-DCMAKE_CXX_COMPILER=" + compiler, "-DCMAKE_CXX_STANDARD=20",
         "-DCMAKE_BUILD_TYPE=Release", "-DAV_BUILD_EXAMPLES=OFF",
         "-DAV_BUILD_TESTS=OFF", "-DAV_ENABLE_SHARED=OFF",
         "-DAV_ENABLE_STATIC=ON", "-DAV_DISABLE_AVFILTER=ON"], timeout=300)
    run(["cmake", "--build", str(build_dir), "--target", "avcpp", "-j6"], timeout=600)
    components = ["libavformat", "libavcodec", "libavutil", "libswscale", "libswresample"]
    library = build_dir / "src/libavcpp.a"
    generated_header = build_dir / "src/avcpp/avconfig.h"
    flags = ["-I" + str(source_dir / "src"), "-I" + str(build_dir / "src")]
    flags.extend(shlex.split(run(["pkg-config", "--cflags", *components])))
    libraries = [str(library), *shlex.split(run(["pkg-config", "--libs", *components]))]
    return flags, libraries, {
        "generated_header_sha256": sha256(generated_header.read_bytes()).hexdigest(),
        "local_library_sha256": sha256(library.read_bytes()).hexdigest(),
    }


def build_ireader_media_server(archive: Path, cache: Path) -> tuple[list[str], list[str], dict[str, str]]:
    """Build the tagged libmov C parser and its upstream FILE callback adapter."""
    source_dir = cache / "media-server-1.0.0"
    if not source_dir.exists():
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                path = Path(member.name)
                if path.is_absolute() or ".." in path.parts or not (
                    member.name == "media-server-1.0.0" or member.name.startswith("media-server-1.0.0/")
                ):
                    raise ValueError(f"unsafe media-server archive path: {member.name}")
            tar.extractall(cache, filter="data")
    build_dir = cache / "media-server-build"
    build_dir.mkdir(exist_ok=True)
    sources = sorted((source_dir / "libmov/source").glob("*.c"))
    sources.append(source_dir / "libmov/test/mov-file-buffer.c")
    objects = []
    for index, source in enumerate(sources):
        object_path = build_dir / f"{index:02d}-{source.stem}.o"
        run(["cc", "-std=c11", "-O2", "-I" + str(source_dir / "libmov/include"),
             "-I" + str(source_dir / "libmov/test"), "-c", str(source),
             "-o", str(object_path)])
        objects.append(object_path)
    library = build_dir / "libmov.a"
    run(["ar", "rcs", str(library), *(str(obj) for obj in objects)])
    return (["-I" + str(source_dir / "libmov/include"),
             "-I" + str(source_dir / "libmov/test")],
            [str(library), "-lm"],
            {"local_library_sha256": sha256(library.read_bytes()).hexdigest()})


def build_shiguredo_mp4(archive: Path, cache: Path, expected_lock_sha256: str) -> tuple[list[str], list[str], dict[str, str]]:
    """Build the pinned Rust MP4 demuxer and published C API from Cargo.lock."""
    source_dir = cache / "mp4-rs-2026.3.0"
    if not source_dir.exists():
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                path = Path(member.name)
                if path.is_absolute() or ".." in path.parts or not (
                    member.name == "mp4-rs-2026.3.0" or member.name.startswith("mp4-rs-2026.3.0/")
                ):
                    raise ValueError(f"unsafe shiguredo/mp4-rs archive path: {member.name}")
            tar.extractall(cache, filter="data")
    lockfile = source_dir / "Cargo.lock"
    assert sha256(lockfile.read_bytes()).hexdigest() == expected_lock_sha256
    run(["cargo", "build", "--release", "--locked", "-p", "c-api",
         "--manifest-path", str(source_dir / "Cargo.toml")], timeout=600)
    library = source_dir / "target/release/libmp4.a"
    return (["-I" + str(source_dir / "crates/c-api/include")], [str(library)],
            {"cargo_lock_sha256": sha256(lockfile.read_bytes()).hexdigest(),
             "local_library_sha256": sha256(library.read_bytes()).hexdigest()})


def verify(ecosystem: str) -> None:
    assert ecosystem in ("c", "cpp")
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    data = ROOT / "data" / ecosystem / "mp4"
    parsers = json.loads((data / "parsers.json").read_text())
    lock = json.loads((data / "source-lock.json").read_text())
    assert len(parsers) == json.loads((data / "cell.json").read_text())["verified_third_party_count"]
    cache = Path(tempfile.gettempdir()) / f"parsarium-{ecosystem}-mp4"
    cache.mkdir(parents=True, exist_ok=True)
    target = ROOT / "adapters" / ecosystem / "mp4/target"
    target.mkdir(parents=True, exist_ok=True)
    rows = []
    libraries = {}
    for parser in parsers:
        name = parser["name"]
        source = lock[name]
        suffix = next(s for s in (".tar.gz", ".tar.xz", ".tar.bz2") if source["source_url"].endswith(s))
        archive = cache / f"{name}-{source['release']}{suffix}"
        if not archive.exists() or sha256(archive.read_bytes()).hexdigest() != source["source_sha256"]:
            with urlopen(Request(source["source_url"], headers={"User-Agent": "Parsarium MP4 verifier"}), timeout=120) as response:
                archive.write_bytes(response.read())
        assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]
        with tarfile.open(archive) as tar:
            member = tar.extractfile(source["source_header_member"])
            assert member is not None
            header_bytes = member.read()
            assert sha256(header_bytes).hexdigest() == source.get("source_header_sha256", source.get("local_header_sha256"))
            member = tar.extractfile(source["license_member"])
            assert member is not None
            assert sha256(member.read()).hexdigest() == source["license_sha256"]
            if "source_engine_member" in source:
                member = tar.extractfile(source["source_engine_member"])
                assert member is not None
                assert sha256(member.read()).hexdigest() == source["source_engine_sha256"]
            for engine in source.get("source_engine_members", []):
                member = tar.extractfile(engine["member"])
                assert member is not None
                assert sha256(member.read()).hexdigest() == engine["sha256"]
        built_libraries = []
        built_hashes = {}
        if source.get("source_build") == "bento4":
            flags, built_libraries, built_hashes = build_bento4(archive, cache, ecosystem)
        elif source.get("source_build") == "libmp4tag":
            flags, built_libraries, built_hashes = build_libmp4tag(archive, cache)
        elif source.get("source_build") == "avcpp":
            assert source["compiler_revision"] in run(["brew", "list", "--versions", "gcc"]).split()
            flags, built_libraries, built_hashes = build_avcpp(archive, cache, source["compiler"])
        elif source.get("source_build") == "ireader_media_server":
            flags, built_libraries, built_hashes = build_ireader_media_server(archive, cache)
        elif source.get("source_build") == "shiguredo_mp4":
            flags, built_libraries, built_hashes = build_shiguredo_mp4(
                archive, cache, source["cargo_lock_sha256"])
        elif source.get("header_only"):
            include_dir = cache / f"{name}-{source['release']}-include"
            include_dir.mkdir(exist_ok=True)
            (include_dir / "dr_mp3.h").write_bytes(header_bytes)
            flags = ["-I" + str(include_dir), "-lm"]
        else:
            if source.get("cask"):
                assert source["installed_revision"] in run(["brew", "list", "--cask", "--versions", source["cask"]]).split()
                cask_archive = Path(run(["brew", "--cache", "--cask", source["cask"]]))
                assert sha256(cask_archive.read_bytes()).hexdigest() == source["cask_sha256"]
            else:
                assert source["installed_revision"] in run(["brew", "list", "--versions", source["formula"]]).split()
            if source.get("pkg_config"):
                assert run(["pkg-config", "--modversion", source["pkg_config"]]) == source.get("pkg_config_version", source["release"])
            header = Path(source["local_header"])
            library = Path(source["local_library"])
            assert sha256(header.read_bytes()).hexdigest() == source["local_header_sha256"]
            assert sha256(library.read_bytes()).hexdigest() == source["local_library_sha256"]
            if source.get("pkg_config"):
                flags = shlex.split(run(["pkg-config", "--cflags", "--libs", source["pkg_config"]]))
            else:
                flags = ["-isystem", source["include_dir"], "-L" + str(library.parent), "-l" + source["link_name"]]
            flags.extend(source.get("extra_linker_flags", []))
        for dependency in source.get("installed_dependencies", []):
            assert sha256(Path(dependency["path"]).read_bytes()).hexdigest() == dependency["sha256"]
        compiler = source.get("compiler", "c++" if ecosystem == "cpp" else "cc")
        standard = source.get("language_standard", "-std=c++17" if ecosystem == "cpp" else "-std=c11")
        if source.get("source_build") == "bento4" and ecosystem == "c":
            object_path = target / "bento4.o"
            compile_command = ["cc", standard, "-O2", "-Wall", "-Wextra", "-Werror",
                               *flags, "-c", str(ROOT / parser["adapter"]), "-o", str(object_path)]
            run(compile_command)
            command = ["c++", str(object_path), *built_libraries, "-o", str(target / name)]
            run(command)
            build_command = shlex.join(compile_command) + " && " + shlex.join(command)
        else:
            command = [compiler, standard, "-O2", "-Wall", "-Wextra", "-Werror",
                       *flags, str(ROOT / parser["adapter"]), *built_libraries,
                       "-o", str(target / name)]
            run(command)
            build_command = shlex.join(command)
        execute = [str(target / name), str(CONTROL)]
        runtime_env = source.get("runtime_env", {})
        output = json.loads(run(execute, env=runtime_env))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"], "control": parser["control"],
                     "build_command": build_command,
                     "command": shlex.join(["env", *(f"{key}={value}" for key, value in runtime_env.items()), *execute]) if runtime_env else shlex.join(execute),
                     "output": output, "pass": True})
        libraries[name] = {"source_sha256": source["source_sha256"]}
        if built_libraries:
            libraries[name].update(built_hashes)
        elif source.get("header_only"):
            libraries[name]["source_header_sha256"] = source["source_header_sha256"]
        else:
            libraries[name]["local_header_sha256"] = source["local_header_sha256"]
            libraries[name]["local_library_sha256"] = source["local_library_sha256"]
        print(f"{name}@{parser['version']}: {ecosystem} MP4 passed", flush=True)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["c++" if ecosystem == "cpp" else "cc", "--version"]).splitlines()[0],
              "source_lock": f"data/{ecosystem}/mp4/source-lock.json", "local_libraries": libraries,
              "control": "controls/mp4/red-av.mp4", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (data / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
