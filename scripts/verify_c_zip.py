"""Build the pinned C ZIP adapters and record valid-control observations."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import shlex
import shutil
import subprocess

import prepare_c_zip


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/zip"
ADAPTER = ROOT / "adapters/c/zip"
SOURCE = ADAPTER / "cache/source"
TARGET = ADAPTER / "target"
CONTROL = ROOT / "controls/zip/hello.zip"
CONTROL_SHA256 = "c534fa083d1da92474852ca9168ba0793740c25205f828915a1d862bd78c776b"
EXPECTED = {"entries": 1, "name": "hello.txt", "content": "parsarium\n"}


def run(command: list[str], env: dict[str, str] | None = None) -> str:
    return subprocess.run(command, cwd=ROOT, env=env, check=True,
                          text=True, capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    lock = json.loads((DATA / "source-lock.json").read_text())
    parsers = json.loads((DATA / "parsers.json").read_text())
    cell = json.loads((DATA / "cell.json").read_text())
    assert len(parsers) == cell["verified_third_party_count"]
    assert {p["name"] for p in parsers} == set(lock)
    prepare_c_zip.main()
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    local_libraries = {}
    source_builds = {}
    for parser in parsers:
        name = parser["name"]
        item = lock[name]
        assert parser["version"] == item["release"]
        env = os.environ.copy()
        if name == "kuba-zip":
            source = SOURCE / name / "src"
            command = ["cc", "-std=c11", "-O2", "-I" + str(source),
                       str(ROOT / parser["adapter"]), str(source / "zip.c"),
                       "-o", str(TARGET / name)]
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "build": "compiled pinned src/zip.c with bundled miniz.h"}
        elif name == "zziplib":
            build = TARGET / "zziplib-build"
            configure = ["cmake", "-S", str(SOURCE / name), "-B", str(build),
                         "-DBUILD_SHARED_LIBS=OFF", "-DBUILD_TESTS=OFF",
                         "-DZZIPMMAPPED=OFF", "-DZZIPFSEEKO=OFF",
                         "-DZZIPWRAP=OFF", "-DZZIPSDL=OFF", "-DZZIPBINS=OFF",
                         "-DZZIPTEST=OFF", "-DZZIPDOCS=OFF", "-DCMAKE_BUILD_TYPE=Release"]
            run(configure)
            run(["cmake", "--build", str(build), "-j", "4"])
            command = ["cc", "-std=c11", "-O2", "-I" + str(SOURCE / name),
                       "-I" + str(build), str(ROOT / parser["adapter"]),
                       str(build / "zzip/libzzip.a"), "-lz", "-o", str(TARGET / name)]
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "configure_command": shlex.join(configure),
                                   "zlib_pkg_config_version": run(["pkg-config", "--modversion", "zlib"])}
        elif name == "unarr":
            build = TARGET / "unarr-build"
            configure = ["cmake", "-S", str(SOURCE / name), "-B", str(build),
                         "-DBUILD_SHARED_LIBS=OFF", "-DENABLE_7Z=OFF",
                         "-DUSE_SYSTEM_BZ2=OFF", "-DUSE_SYSTEM_LZMA=OFF",
                         "-DUSE_SYSTEM_ZLIB=ON", "-DBUILD_INTEGRATION_TESTS=OFF",
                         "-DBUILD_UNIT_TESTS=OFF", "-DCMAKE_BUILD_TYPE=Release"]
            run(configure)
            run(["cmake", "--build", str(build), "-j", "4"])
            command = ["cc", "-std=c11", "-O2", "-I" + str(build),
                       str(ROOT / parser["adapter"]), str(build / "libunarr.a"),
                       "-lz", "-o", str(TARGET / name)]
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "configure_command": shlex.join(configure),
                                   "zlib_pkg_config_version": run(["pkg-config", "--modversion", "zlib"])}
        elif name == "lowzip":
            source = SOURCE / name
            command = ["cc", "-std=c11", "-O2", "-I" + str(source),
                       str(ROOT / parser["adapter"]), str(source / "lowzip.c"),
                       "-o", str(TARGET / name)]
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "build": "compiled pinned lowzip.c and adapter"}
        elif name == "unziplib":
            source = SOURCE / name / "src"
            sources = [source / (stem + ".c") for stem in
                       ("unzip", "adler32", "crc32", "infback", "inffast",
                        "inflate", "inftrees", "zutil")]
            command = ["cc", "-std=c11", "-O2", "-Wno-deprecated-non-prototype",
                       "-Wno-macro-redefined", "-include", "stdio.h",
                       "-I" + str(source), str(ROOT / parser["adapter"]),
                       *map(str, sources), "-o", str(TARGET / name)]
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "build": "compiled pinned unzipLIB MiniZip fork and bundled zlib C sources"}
        elif name == "junzip":
            source = SOURCE / name
            command = ["cc", "-std=c11", "-O2", "-I" + str(source),
                       str(ROOT / parser["adapter"]), str(source / "junzip.c"),
                       "-lz", "-o", str(TARGET / name)]
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "build": "compiled pinned junzip.c with zlib for DEFLATE"}
        elif name == "zipc":
            source = SOURCE / name
            command = ["cc", "-std=c11", "-O2", "-DZIPC_ONLY_READ",
                       "-I" + str(source), str(ROOT / parser["adapter"]),
                       str(source / "zipc.c"), "-lz", "-o", str(TARGET / name)]
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "build": "compiled pinned zipc.c read-only with zlib"}
        elif name == "aosp-libzipfile":
            source = SOURCE / name
            command = ["cc", "-std=c11", "-O2", "-I" + str(source / "include"),
                       "-I" + str(source), str(ROOT / parser["adapter"]),
                       str(source / "zipfile.c"), str(source / "centraldir.c"),
                       "-lz", "-o", str(TARGET / name)]
            source_builds[name] = {"release_commit": item["release_commit"],
                                   "file_sha256": {file["name"]: file["sha256"]
                                                   for file in item["files"]},
                                   "build": "compiled pinned AOSP libzipfile ZIP reader with system zlib"}
        elif name == "sqlite":
            library = Path(item["local_library"])
            digest = sha256(library.read_bytes()).hexdigest()
            assert digest == item["local_library_sha256"]
            env["PKG_CONFIG_PATH"] = str(library.parent / "pkgconfig") + os.pathsep + env.get("PKG_CONFIG_PATH", "")
            observed = run(["pkg-config", "--modversion", "sqlite3"], env)
            assert observed == item["release"]
            source = SOURCE / name / "ext/misc/zipfile.c"
            command = ["cc", "-std=c11", "-O2", "-DSQLITE_CORE",
                       "-I" + item["local_include"], str(ROOT / parser["adapter"]),
                       str(source), str(library), "-lz", "-o", str(TARGET / name)]
            local_libraries[name] = {"pkg_config_version": observed,
                                     "library": str(library), "library_sha256": digest}
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "build": "compiled SQLite ext/misc/zipfile.c into application"}
        elif name == "infozip-unzip":
            source = SOURCE / name
            build = ["make", "-C", str(source), "-f", "unix/Makefile", "objsdll",
                     "CC=cc", "CFLAGS=-O2 -fPIC -DDLL -DUNIX -Wno-deprecated-non-prototype -Wno-implicit-function-declaration", "-j4"]
            run(build)
            library = TARGET / "libinfozip_unzip.a"
            objects = sorted(source.glob("*.pic.o"))
            assert len(objects) == 19, len(objects)
            run(["ar", "rcs", str(library), *map(str, objects)])
            command = ["cc", "-std=c11", "-O2", "-DDLL", "-DUNIX",
                       "-I" + str(source), str(ROOT / parser["adapter"]),
                       str(library), "-o", str(TARGET / name)]
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "build_command": shlex.join(build),
                                   "library_sha256": sha256(library.read_bytes()).hexdigest()}
        elif name == "libc7zip":
            assert platform.system() == "Darwin" and platform.machine() == "arm64"
            source = SOURCE / name
            build = TARGET / "libc7zip-build"
            configure = ["cmake", "-S", str(source), "-B", str(build),
                         "-DCMAKE_BUILD_TYPE=Release", "-DBUILD_TESTS=OFF"]
            run(configure)
            run(["cmake", "--build", str(build), "-j", "4"])
            engine_dir = build / "upstream-7zip-src/CPP/7zip/Bundles/Format7zF"
            engine_command = ["make", "-C", str(engine_dir), "-j4", "-f",
                              "../../cmpl_mac_arm64.mak"]
            run(engine_command)
            engine = engine_dir / "b/m_arm64/7z.so"
            shutil.copy2(engine, TARGET / "7z.so")
            library = build / "libc7zip.dylib"
            command = ["cc", "-std=c11", "-O2", "-I" + str(source / "include"),
                       str(ROOT / parser["adapter"]), str(library),
                       "-Wl,-rpath," + str(build), "-o", str(TARGET / name)]
            source_builds[name] = {
                "source_sha256": item["source_sha256"],
                "engine_source_sha256": item["engine_source_sha256"],
                "engine_sha256": sha256(engine.read_bytes()).hexdigest(),
                "library_sha256": sha256(library.read_bytes()).hexdigest(),
                "configure_command": shlex.join(configure),
                "engine_build_command": shlex.join(engine_command),
            }
        elif name == "libtfs":
            assert platform.system() == "Darwin" and platform.machine() == "arm64"
            archive = ADAPTER / "cache/libtfs"
            libtfs_library = archive / "pkg/lib/libtfs.a"
            dependencies = sorted((archive / "deps/lib").glob("*.a"))
            assert len(dependencies) == item["dependency_archive_count"]
            crypto = Path(item["local_crypto_library"])
            crypto_digest = sha256(crypto.read_bytes()).hexdigest()
            assert crypto_digest == item["local_crypto_sha256"]
            assert run(["brew", "list", "--versions", "openssl@3"]) == item["local_crypto_release"]
            object_file = TARGET / "libtfs-adapter.o"
            compile_command = ["cc", "-std=c11", "-O2",
                               "-I" + str(archive / "pkg/include"), "-c",
                               str(ROOT / parser["adapter"]), "-o", str(object_file)]
            run(compile_command)
            command = ["c++", str(object_file), str(libtfs_library),
                       *map(str, dependencies), str(crypto),
                       "-framework", "CoreFoundation", "-framework", "Security",
                       "-framework", "Foundation", "-o", str(TARGET / name)]
            local_libraries[name] = {"openssl_release": item["local_crypto_release"],
                                     "openssl_library": str(crypto),
                                     "openssl_library_sha256": crypto_digest}
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "release_assets": {asset["name"]: asset["sha256"]
                                                      for asset in item["binary_assets"]},
                                   "compile_command": shlex.join(compile_command),
                                   "dependency_archive_count": len(dependencies),
                                   "libtfs_library_sha256": sha256(libtfs_library.read_bytes()).hexdigest()}
        else:
            library = Path(item["local_library"])
            digest = sha256(library.read_bytes()).hexdigest()
            assert digest == item["local_library_sha256"], name
            for dependency in item.get("transitive_local_libraries", []):
                assert sha256(Path(dependency["path"]).read_bytes()).hexdigest() == dependency["sha256"]
            if name == "libarchive":
                directory = str(library.parent / "pkgconfig")
                env["PKG_CONFIG_PATH"] = directory + os.pathsep + env.get("PKG_CONFIG_PATH", "")
            observed = run(["pkg-config", "--modversion", item["pkg_config"]], env)
            assert observed == item["release"], (name, observed)
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", item["pkg_config"]], env))
            command = ["cc", "-std=c11", "-O2", str(ROOT / parser["adapter"]),
                       *flags, "-o", str(TARGET / name)]
            local_libraries[name] = {"pkg_config_version": observed,
                                     "library": str(library), "library_sha256": digest}
        run(command, env)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute, env))
        if name == "zipc":
            assert parser["expected_output"] == {"content": EXPECTED["content"]}
        else:
            assert parser["expected_output"] == EXPECTED
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(command),
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["cc", "--version"]).splitlines()[0],
              "local_libraries": local_libraries, "source_builds": source_builds,
              "control": "controls/zip/hello.zip", "control_sha256": CONTROL_SHA256,
              "expected": EXPECTED, "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
