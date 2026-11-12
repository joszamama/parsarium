"""Build pinned native C++ HTTP/1.1 readers and record valid-control results."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import shutil
import subprocess
import tarfile
import tempfile
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/http11"
CONTROL = ROOT / "controls/http11/request.http"
CACHE = Path(tempfile.gettempdir()) / "parsarium-cpp-http11"
TARGET = ROOT / "adapters/cpp/http11/target"


def run(command: list[str], cwd: Path = ROOT) -> str:
    return subprocess.run(command, cwd=cwd, check=True, text=True,
                          capture_output=True, timeout=600).stdout.strip()


def get_archive(name: str, source: dict) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    suffix = next(ext for ext in (".tar.xz", ".tar.bz2", ".tar.gz")
                  if source["source_url"].endswith(ext))
    archive = CACHE / f"{name}-{source['release']}{suffix}"
    if not archive.exists() or sha256(archive.read_bytes()).hexdigest() != source["source_sha256"]:
        shared = ROOT / "adapters/cpp/zip/cache/poco.tar.gz"
        if name == "poco" and shared.exists() and sha256(shared.read_bytes()).hexdigest() == source["source_sha256"]:
            archive.write_bytes(shared.read_bytes())
        else:
            c_cache = Path(tempfile.gettempdir()) / "parsarium-c-http11"
            match = next((path for path in (c_cache.iterdir() if c_cache.exists() else ())
                          if path.is_file() and path.name.endswith(suffix)
                          and sha256(path.read_bytes()).hexdigest() == source["source_sha256"]), None)
            if match is not None:
                archive.write_bytes(match.read_bytes())
            else:
                with urlopen(source["source_url"], timeout=120) as response:
                    archive.write_bytes(response.read())
    assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]
    return archive


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    sources = json.loads((DATA / "source-lock.json").read_text())
    shared_sources = json.loads((DATA / "extra-source-lock.json").read_text())
    assert len(parsers) == json.loads((DATA / "cell.json").read_text())["verified_third_party_count"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == "0af539fa6b7007346b95c960cbf2e0f9d34e0d53ce732e25ba44aaadaf92b7fe"
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    local_sources = {}

    beast = sources["boost_beast"]
    beast_archive = get_archive("boost_beast", beast)
    with tarfile.open(beast_archive) as archive:
        member = archive.extractfile("beast-boost-1.92.0/include/boost/beast/http/basic_parser.hpp")
        assert member is not None
        assert sha256(member.read()).hexdigest() == beast["local_header_sha256"]
    header = Path(beast["local_header"])
    assert sha256(header.read_bytes()).hexdigest() == beast["local_header_sha256"]
    include = header.parents[3]
    assert "BOOST_LIB_VERSION \"1_92\"" in (include / "boost/version.hpp").read_text()
    local_sources["boost_beast"] = {"source_sha256": beast["source_sha256"],
                                    "local_header": str(header),
                                    "local_header_sha256": beast["local_header_sha256"]}

    poco = sources["poco"]
    poco_archive = get_archive("poco", poco)
    poco_source = CACHE / "poco-poco-1.15.4-release"
    if not (poco_source / "Net/include/Poco/Net/HTTPRequest.h").exists():
        with tarfile.open(poco_archive) as archive:
            archive.extractall(CACHE, filter="data")
    poco_build = CACHE / "poco-build"
    configure = ["cmake", "-S", str(poco_source), "-B", str(poco_build),
                 "-DPOCO_MINIMAL_BUILD=ON", "-DENABLE_NET=ON",
                 "-DBUILD_SHARED_LIBS=OFF", "-DENABLE_FASTLOGGER=OFF",
                 "-DENABLE_TESTS=OFF", "-DENABLE_SAMPLES=OFF",
                 "-DCMAKE_BUILD_TYPE=Release"]
    run(configure)
    build = ["cmake", "--build", str(poco_build), "--target", "Net", "-j4"]
    run(build)
    local_sources["poco"] = {"source_sha256": poco["source_sha256"],
                              "configure_command": shlex.join(configure),
                              "build_command": shlex.join(build)}

    for parser in parsers:
        name = parser["name"]
        if name in shared_sources:
            continue
        adapter = ROOT / parser["adapter"]
        if name == "boost_beast":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(include), str(adapter), "-o", str(TARGET / name)]
        elif name == "poco":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(poco_source / "Net/include"),
                       "-I" + str(poco_source / "Foundation/include"), str(adapter),
                       str(poco_build / "lib/libPocoNet.a"),
                       str(poco_build / "lib/libPocoFoundation.a"),
                       "-o", str(TARGET / name)]
        else:
            raise AssertionError(name)
        run(command)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(command),
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: C++ passed")

    c_source_files = {"http-parser": ["http_parser.c"],
                      "picohttpparser": ["picohttpparser.c"],
                      "mongoose": ["mongoose.c"],
                      "h2o": ["deps/picohttpparser/picohttpparser.c"],
                      "samsung-http-parser": ["http_parser.c"],
                      "libhv": ["http/http_parser.c", "http/httpdef.c"],
                      "libparsehttp": ["src/libparsehttp/libparsehttp.c"],
                      "libevhtp": ["htparse/htparse.c"],
                      "HTTPParserC": ["Sources/llhttp.c", "Sources/http.c", "Sources/api.c"]}
    source_roots = {"http-parser": "http-parser-2.9.4",
                    "picohttpparser": "picohttpparser-1.5",
                    "mongoose": "mongoose-7.23", "httpp": "httpp-2.0.0",
                    "h2o": "h2o-2.2.6", "samsung-http-parser": "http-parser-2.5.0",
                    "libhv": "libhv-1.3.1", "libparsehttp": "libparsehttp-0.06",
                    "libevhtp": "libevhtp-1.2.9", "HTTPParserC": "HTTPParserC-9.2.0",
                    "libhtp": "libhtp-0.5.53", "libonion": "onion-0.8",
                    "serf": "serf-1.3.10"}
    for parser in parsers:
        name = parser["name"]
        if name not in shared_sources:
            continue
        source = shared_sources[name]
        archive = get_archive(name, source)
        prerequisites = []
        if name in ("llhttp", "libmicrohttpd", "libsoup", "libwebsockets"):
            pkg = {"llhttp": "libllhttp", "libmicrohttpd": "libmicrohttpd",
                   "libsoup": "libsoup-3.0", "libwebsockets": "libwebsockets"}[name]
            assert run(["pkg-config", "--modversion", pkg]) == source.get("pkg_config_version", source["release"])
            for path_key, hash_key in (("system_library", "system_library_sha256"),
                                       ("system_header", "system_header_sha256")):
                assert sha256(Path(source[path_key]).read_bytes()).hexdigest() == source[hash_key]
            packages = [pkg, "openssl"] if name == "libwebsockets" else [pkg]
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", *packages]))
            local_sources[name] = {"source_sha256": source["source_sha256"],
                                   "system_library_sha256": source["system_library_sha256"],
                                   "system_header_sha256": source["system_header_sha256"]}
            extra = flags
        elif name == "finwo-http-parser":
            root = CACHE / source["root"]
            if not root.exists():
                with tarfile.open(archive) as tar:
                    tar.extractall(CACHE, filter="data")
            deps = source["build_dependencies"]
            for dep_name, dep in deps.items():
                dep_archive = get_archive(dep_name, dep)
                dep_root = CACHE / dep["root"]
                if not dep_root.exists():
                    with tarfile.open(dep_archive) as tar:
                        tar.extractall(CACHE, filter="data")
            inc = CACHE / "finwo-include"
            (inc / "finwo").mkdir(parents=True, exist_ok=True)
            (inc / "tidwall").mkdir(exist_ok=True)
            for dep_name, from_path, to_path in (
                ("finwo-asprintf", "src/asprintf.h", "finwo/asprintf.h"),
                ("finwo-mindex", "src/mindex.h", "finwo/mindex.h"),
                ("finwo-strextra", "src/strnstr.h", "finwo/strnstr.h"),
                ("tidwall-buf", "buf.h", "tidwall/buf.h"),
            ):
                shutil.copyfile(CACHE / deps[dep_name]["root"] / from_path, inc / to_path)
            files = [root / "src/http-parser.c",
                     CACHE / deps["finwo-asprintf"]["root"] / "src/asprintf.c",
                     CACHE / deps["finwo-mindex"]["root"] / "src/mindex.c",
                     CACHE / deps["finwo-strextra"]["root"] / "src/strnstr.c",
                     CACHE / deps["tidwall-buf"]["root"] / "buf.c"]
            objects = []
            for index, c_file in enumerate(files):
                obj = TARGET / f"finwo-{index}.o"
                c_command = ["cc", "-std=c11", "-O2", "-Wno-unused-parameter",
                             "-Wno-sign-compare", "-I" + str(inc),
                             "-I" + str(root / "src"), "-c", str(c_file), "-o", str(obj)]
                run(c_command)
                prerequisites.append(shlex.join(c_command))
                objects.append(str(obj))
            extra = ["-I" + str(inc), "-I" + str(root / "src"), *objects]
            local_sources[name] = {"source_sha256": source["source_sha256"],
                                   "dependency_sha256": {k: v["source_sha256"] for k, v in deps.items()}}
        else:
            root = CACHE / source_roots[name]
            if not root.exists():
                with tarfile.open(archive) as tar:
                    if name == "h2o":
                        for member in tar.getmembers():
                            if member.name.startswith("h2o-2.2.6/deps/picohttpparser/"):
                                tar.extract(member, CACHE, filter="data")
                    else:
                        tar.extractall(CACHE, filter="data")
            assert root.exists()
            extra = ["-I" + str(root)]
            if name == "h2o":
                extra.append("-I" + str(root / "deps/picohttpparser"))
            elif name == "libhv":
                extra.append("-I" + str(root / "http"))
            elif name == "libparsehttp":
                extra.append("-I" + str(root / "src/libparsehttp"))
            elif name == "libevhtp":
                extra.append("-I" + str(root / "htparse"))
            elif name == "HTTPParserC":
                extra.append("-I" + str(root / "Sources"))
            if name in c_source_files:
                for index, relative in enumerate(c_source_files[name]):
                    c_file = root / relative
                    obj = TARGET / f"{name}-{index}.o"
                    c_command = ["cc", "-std=c11", "-O2", *[x for x in extra if x.startswith("-I")],
                                 "-c", str(c_file), "-o", str(obj)]
                    run(c_command)
                    prerequisites.append(shlex.join(c_command))
                    extra.append(str(obj))
                local_sources[name] = {"source_sha256": source["source_sha256"],
                                       "c_build_commands": prerequisites}
            elif name == "libhtp":
                run(["./autogen.sh"], cwd=root)
                run(["./configure", "--disable-shared", "--enable-static"], cwd=root)
                run(["make", "-j4"], cwd=root)
                extra.extend([str(root / "htp/.libs/libhtp.a"), "-lz"])
                local_sources[name] = {"source_sha256": source["source_sha256"],
                                       "source_build": "autogen.sh; configure --disable-shared --enable-static; make -j4"}
            elif name == "libonion":
                poller = root / "src/onion/poller_libev.c"
                original = "void onion_poller_slot_set_type(onion_poller_slot *el, int type){"
                updated = "void onion_poller_slot_set_type(onion_poller_slot *el, onion_poller_slot_type_e type){"
                content = poller.read_text()
                if original in content:
                    assert content.count(original) == 1
                    poller.write_text(content.replace(original, updated))
                else:
                    assert updated in content
                libev = source["build_dependency"]
                libev_prefix = Path(run(["brew", "--prefix", "libev"])).resolve()
                assert libev_prefix.name == libev["release"]
                assert sha256((libev_prefix / "lib/libev.dylib").read_bytes()).hexdigest() == libev["library_sha256"]
                assert sha256((libev_prefix / "include/ev.h").read_bytes()).hexdigest() == libev["header_sha256"]
                build_dir = CACHE / "onion-build"
                configure = ["cmake", "-S", str(root), "-B", str(build_dir),
                             "-DONION_USE_PAM=OFF", "-DONION_USE_JPEG=OFF", "-DONION_USE_SSL=OFF",
                             "-DONION_USE_PNG=OFF", "-DONION_USE_XML2=OFF", "-DONION_USE_SQLITE3=OFF",
                             "-DONION_USE_REDIS=OFF", "-DONION_USE_SYSTEMD=OFF", "-DONION_EXAMPLES=OFF",
                             "-DONION_USE_BINDINGS_CPP=OFF", "-DCMAKE_BUILD_TYPE=Release",
                             "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
                             "-DLIBEV_LIB=" + str(libev_prefix / "lib/libev.dylib"),
                             "-DLIBEV_HEADER=" + str(libev_prefix / "include"),
                             "-DCMAKE_C_FLAGS=-include " + str(ROOT / "adapters/c/http11/libonion_macos_compat.h")]
                run(configure)
                build_command = ["cmake", "--build", str(build_dir), "--target", "onion_static", "-j4"]
                run(build_command)
                extra.extend(["-I" + str(root / "src"), "-I" + str(build_dir / "src"),
                              str(build_dir / "src/onion/libonion_static.a"),
                              "-L" + str(libev_prefix / "lib"), "-lev"])
                local_sources[name] = {"source_sha256": source["source_sha256"],
                                       "configure_command": shlex.join(configure),
                                       "build_command": shlex.join(build_command)}
            elif name == "serf":
                construct = root / "SConstruct"
                original = "SOURCES = Glob('*.c') + Glob('buckets/*.c') + Glob('auth/*.c')"
                updated = "SOURCES = Glob('*.c') + [x for x in Glob('buckets/*.c') if not str(x).endswith('ssl_buckets.c')] + Glob('auth/*.c')"
                content = construct.read_text()
                if original in content:
                    assert content.count(original) == 1
                    construct.write_text(content.replace(original, updated))
                else:
                    assert updated in content
                for formula, version in source["build_dependencies"].items():
                    assert run(["brew", "list", "--versions", formula]) == f"{formula} {version}"
                apr = Path(run(["brew", "--prefix", "apr"]))
                apu = Path(run(["brew", "--prefix", "apr-util"]))
                openssl = Path(run(["brew", "--prefix", "openssl@3"]))
                build_command = ["scons", "-j4", "APR=" + str(apr), "APU=" + str(apu),
                                 "OPENSSL=" + str(openssl),
                                 "PREFIX=" + str(CACHE / "serf-install"), "libserf-1.a"]
                run(build_command, cwd=root)
                extra.extend(shlex.split(run([str(apr / "bin/apr-1-config"), "--includes"])))
                extra.extend(shlex.split(run([str(apu / "bin/apu-1-config"), "--includes"])))
                extra.append(str(root / "libserf-1.a"))
                extra.extend(shlex.split(run([str(apr / "bin/apr-1-config"), "--link-ld", "--libs"])))
                extra.extend(shlex.split(run([str(apu / "bin/apu-1-config"), "--link-ld", "--libs"])))
                extra.extend(["-L" + str(openssl / "lib"), "-lssl", "-lcrypto", "-lz"])
                local_sources[name] = {"source_sha256": source["source_sha256"],
                                       "build_command": shlex.join(build_command),
                                       "build_scope": "static library without unrelated SSL bucket object"}
            else:
                local_sources[name] = {"source_sha256": source["source_sha256"]}
        adapter = ROOT / parser["adapter"]
        suppress = ["-Wno-sign-compare", "-Wno-unused-function"] if name == "libevhtp" else []
        suppress += ["-Wno-unused-parameter", "-Wno-sign-compare"] if name == "finwo-http-parser" else []
        command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror", *suppress,
                   "-I" + str(ROOT / "adapters/c/http11"),
                   str(adapter), *extra, "-o", str(TARGET / name)]
        run(command)
        control = ROOT / parser["control"]
        execute = [str(TARGET / name), str(control)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "prerequisite_build_commands": prerequisites,
                     "build_command": shlex.join(command),
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: C++ passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["c++", "--version"]).splitlines()[0],
              "source_lock": "data/cpp/http11/source-lock.json",
              "local_sources": local_sources,
              "control": "controls/http11/request.http",
              "control_sha256": sha256(CONTROL.read_bytes()).hexdigest(),
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
