"""Rebuild and replay pinned C HTTP/1.1 request parsers on a valid control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/http11"
ADAPTER = ROOT / "adapters/c/http11"
CONTROL = ROOT / "controls/http11/request.http"
CACHE = Path(tempfile.gettempdir()) / "parsarium-c-http11"


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True, timeout=120)


def archive(name: str, source: dict) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    suffix = next(ext for ext in (".tar.xz", ".tar.bz2", ".tar.gz")
                  if source["source_url"].endswith(ext))
    target = CACHE / f"{name}-{source['release']}{suffix}"
    if not target.exists() or sha256(target.read_bytes()).hexdigest() != source["source_sha256"]:
        with urlopen(Request(source["source_url"], headers={"User-Agent": "Parsarium C HTTP verifier"}), timeout=30) as response:
            target.write_bytes(response.read())
    assert sha256(target.read_bytes()).hexdigest() == source["source_sha256"]
    return target


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    lock = json.loads((DATA / "source-lock.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    expected_control = b"GET /parsarium?x=1 HTTP/1.1\r\nHost: example.test\r\nX-Parsarium: yes\r\nConnection: close\r\n\r\n"
    expected_response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 2\r\n\r\nOK"
    assert CONTROL.read_bytes() == expected_control
    response_control = ROOT / "controls/http11/response_serf.http"
    assert response_control.read_bytes() == expected_response
    control_hashes = {"controls/http11/request.http": sha256(expected_control).hexdigest(),
                      "controls/http11/response_serf.http": sha256(expected_response).hexdigest()}
    for parser in parsers:
        name = parser["name"]
        assert parser["version"] == lock[name]["release"] == snapshot["releases"][name]["version"]
        assert parser["license"] == snapshot["releases"][name]["license"]
        archive(name, lock[name])
    for name, pkgconfig in (("llhttp", "libllhttp"), ("libmicrohttpd", "libmicrohttpd"),
                            ("libsoup", "libsoup-3.0")):
        installed = lock[name]
        assert run(["pkg-config", "--modversion", pkgconfig]).stdout.strip() == installed["release"]
        for path_key, hash_key in (("system_library", "system_library_sha256"),
                                   ("system_header", "system_header_sha256")):
            assert sha256(Path(installed[path_key]).read_bytes()).hexdigest() == installed[hash_key]
    websockets = lock["libwebsockets"]
    assert run(["pkg-config", "--modversion", "libwebsockets"]).stdout.strip() == websockets["pkg_config_version"]
    for path_key, hash_key in (("system_library", "system_library_sha256"),
                               ("system_header", "system_header_sha256")):
        assert sha256(Path(websockets[path_key]).read_bytes()).hexdigest() == websockets[hash_key]
    libev = lock["libonion"]["build_dependency"]
    libev_prefix = Path(run(["brew", "--prefix", "libev"]).stdout.strip()).resolve()
    assert libev_prefix.name == libev["release"]
    libev_library = libev_prefix / "lib/libev.dylib"
    libev_header = libev_prefix / "include/ev.h"
    assert sha256(libev_library.read_bytes()).hexdigest() == libev["library_sha256"]
    assert sha256(libev_header.read_bytes()).hexdigest() == libev["header_sha256"]
    serf_build_dependencies = lock["serf"]["build_dependencies"]
    for formula, version in serf_build_dependencies.items():
        assert run(["brew", "list", "--versions", formula]).stdout.strip() == f"{formula} {version}"
    with tempfile.TemporaryDirectory(prefix="parsarium-c-http11-build-") as temporary:
        build = Path(temporary)
        for name in ("http-parser", "picohttpparser", "mongoose", "httpp", "HTTPParserC", "libevhtp", "libhtp", "libonion", "serf"):
            with tarfile.open(archive(name, lock[name])) as tar:
                tar.extractall(build, filter="data")
        libhtp_source = build / "libhtp-0.5.53"
        run(["./autogen.sh"], cwd=libhtp_source)
        run(["./configure", "--disable-shared", "--enable-static"], cwd=libhtp_source)
        run(["make", "-j4"], cwd=libhtp_source)
        libonion_source = build / "onion-0.8"
        poller = libonion_source / "src/onion/poller_libev.c"
        original = "void onion_poller_slot_set_type(onion_poller_slot *el, int type){"
        updated = "void onion_poller_slot_set_type(onion_poller_slot *el, onion_poller_slot_type_e type){"
        poller_text = poller.read_text()
        assert poller_text.count(original) == 1
        poller.write_text(poller_text.replace(original, updated))
        libonion_build = build / "libonion-build"
        run(["cmake", "-S", str(libonion_source), "-B", str(libonion_build),
             "-DONION_USE_PAM=OFF", "-DONION_USE_JPEG=OFF", "-DONION_USE_SSL=OFF",
             "-DONION_USE_PNG=OFF", "-DONION_USE_XML2=OFF", "-DONION_USE_SQLITE3=OFF",
             "-DONION_USE_REDIS=OFF", "-DONION_USE_SYSTEMD=OFF", "-DONION_EXAMPLES=OFF",
             "-DONION_USE_BINDINGS_CPP=OFF", "-DCMAKE_BUILD_TYPE=Release",
             "-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DLIBEV_LIB=" + str(libev_library),
             "-DLIBEV_HEADER=" + str(libev_prefix / "include"),
             "-DCMAKE_C_FLAGS=-include " + str(ADAPTER / "libonion_macos_compat.h")])
        run(["cmake", "--build", str(libonion_build), "--target", "onion_static", "-j4"])
        serf_source = build / "serf-1.3.10"
        sconstruct = serf_source / "SConstruct"
        original = "SOURCES = Glob('*.c') + Glob('buckets/*.c') + Glob('auth/*.c')"
        updated = "SOURCES = Glob('*.c') + [x for x in Glob('buckets/*.c') if not str(x).endswith('ssl_buckets.c')] + Glob('auth/*.c')"
        build_text = sconstruct.read_text()
        assert build_text.count(original) == 1
        sconstruct.write_text(build_text.replace(original, updated))
        apr_prefix = Path(run(["brew", "--prefix", "apr"]).stdout.strip())
        apu_prefix = Path(run(["brew", "--prefix", "apr-util"]).stdout.strip())
        openssl_prefix = Path(run(["brew", "--prefix", "openssl@3"]).stdout.strip())
        run(["scons", "-j4", "APR=" + str(apr_prefix), "APU=" + str(apu_prefix),
             "OPENSSL=" + str(openssl_prefix), "PREFIX=" + str(build / "serf-install"),
             "libserf-1.a"], cwd=serf_source)
        apr_config = apr_prefix / "bin/apr-1-config"
        apu_config = apu_prefix / "bin/apu-1-config"
        apr_includes = run([str(apr_config), "--includes"]).stdout.split()
        apu_includes = run([str(apu_config), "--includes"]).stdout.split()
        apr_link = run([str(apr_config), "--link-ld", "--libs"]).stdout.split()
        apu_link = run([str(apu_config), "--link-ld", "--libs"]).stdout.split()
        llflags = run(["pkg-config", "--cflags", "--libs", "libllhttp"]).stdout.split()
        mhdflags = run(["pkg-config", "--cflags", "--libs", "libmicrohttpd"]).stdout.split()
        soupflags = run(["pkg-config", "--cflags", "--libs", "libsoup-3.0"]).stdout.split()
        lws_cflags = run(["pkg-config", "--cflags", "openssl", "libwebsockets"]).stdout.split()
        lws_libs = run(["pkg-config", "--libs", "libwebsockets"]).stdout.split()
        commands = {
            "llhttp": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(ADAPTER), str(ADAPTER / "llhttp.c"), *llflags,
                       "-o", str(build / "llhttp-adapter")],
            "http-parser": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                            "-I" + str(ADAPTER), "-I" + str(build / "http-parser-2.9.4"),
                            str(ADAPTER / "http_parser.c"),
                            str(build / "http-parser-2.9.4/http_parser.c"),
                            "-o", str(build / "http-parser-adapter")],
            "picohttpparser": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                               "-I" + str(ADAPTER), "-I" + str(build / "picohttpparser-1.5"),
                               str(ADAPTER / "picohttpparser.c"),
                               str(build / "picohttpparser-1.5/picohttpparser.c"),
                               "-o", str(build / "picohttpparser-adapter")],
            "mongoose": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                         "-I" + str(ADAPTER), "-I" + str(build / "mongoose-7.23"),
                         str(ADAPTER / "mongoose.c"), str(build / "mongoose-7.23/mongoose.c"),
                         "-o", str(build / "mongoose-adapter")],
            "httpp": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                      "-I" + str(ADAPTER), "-I" + str(build / "httpp-2.0.0"),
                      str(ADAPTER / "httpp.c"), "-o", str(build / "httpp-adapter")],
            "HTTPParserC": ["cc", "-std=c11", "-Wall", "-Wextra", "-Wno-unused-parameter", "-Werror",
                            "-I" + str(ADAPTER), "-I" + str(build / "HTTPParserC-9.2.0/Sources"),
                            str(ADAPTER / "HTTPParserC.c"),
                            *[str(build / f"HTTPParserC-9.2.0/Sources/{file}")
                              for file in ("llhttp.c", "http.c", "api.c")],
                            "-o", str(build / "HTTPParserC-adapter")],
            "libmicrohttpd": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                              "-I" + str(ADAPTER), str(ADAPTER / "libmicrohttpd.c"),
                              *mhdflags, "-o", str(build / "libmicrohttpd-adapter")],
            "libevhtp": ["cc", "-std=c11", "-Wall", "-Wextra", "-Wno-sign-compare",
                         "-Wno-unused-function", "-Werror", "-I" + str(ADAPTER),
                         "-I" + str(build / "libevhtp-1.2.9/htparse"),
                         str(ADAPTER / "libevhtp.c"),
                         str(build / "libevhtp-1.2.9/htparse/htparse.c"),
                         "-o", str(build / "libevhtp-adapter")],
            "libhtp": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(ADAPTER), "-I" + str(libhtp_source),
                       str(ADAPTER / "libhtp.c"),
                       str(libhtp_source / "htp/.libs/libhtp.a"), "-lz",
                       "-o", str(build / "libhtp-adapter")],
            "libwebsockets": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                              "-I" + str(ADAPTER), str(ADAPTER / "libwebsockets.c"),
                              *lws_cflags, *lws_libs,
                              "-o", str(build / "libwebsockets-adapter")],
            "libonion": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                         "-I" + str(ADAPTER), "-I" + str(libonion_source / "src"),
                         "-I" + str(libonion_build / "src"), str(ADAPTER / "libonion.c"),
                         str(libonion_build / "src/onion/libonion_static.a"),
                         "-L" + str(libev_prefix / "lib"), "-lev",
                         "-o", str(build / "libonion-adapter")],
            "libsoup": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                        "-I" + str(ADAPTER), str(ADAPTER / "libsoup.c"),
                        *soupflags, "-o", str(build / "libsoup-adapter")],
            "serf": ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                     "-I" + str(ADAPTER), "-I" + str(serf_source),
                     *apr_includes, *apu_includes, str(ADAPTER / "serf.c"),
                     str(serf_source / "libserf-1.a"), *apr_link, *apu_link,
                     "-L" + str(openssl_prefix / "lib"), "-lssl", "-lcrypto", "-lz",
                     "-o", str(build / "serf-adapter")]}
        rows = []
        for parser in parsers:
            name = parser["name"]
            run(commands[name])
            result = json.loads(run([str(build / f"{name}-adapter"),
                                     str(ROOT / parser["control"])]).stdout)
            assert result == parser["expected_output"], (name, result)
            rows.append({"package": name, "version": parser["version"],
                         "control": parser["control"], "output": result,
                         "pass": True, "command": f"build pinned {name}; {name}-adapter {parser['control']}"})
            print(f"{name}: passed")
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "environment": {"platform": platform.platform(),
                              "compiler": run(["cc", "--version"]).stdout.splitlines()[0],
                              "llhttp_version": lock["llhttp"]["release"],
                              "llhttp_library_sha256": lock["llhttp"]["system_library_sha256"],
                              "libmicrohttpd_version": lock["libmicrohttpd"]["release"],
                              "libmicrohttpd_library_sha256": lock["libmicrohttpd"]["system_library_sha256"],
                              "libwebsockets_version": websockets["release"],
                              "libwebsockets_library_sha256": websockets["system_library_sha256"],
                              "libonion_build_dependency": "libev " + libev["release"],
                              "libonion_compatibility": "macOS preinclude plus poller parameter type correction in temporary source",
                              "libsoup_version": lock["libsoup"]["release"],
                              "libsoup_library_sha256": lock["libsoup"]["system_library_sha256"],
                              "serf_build_dependencies": serf_build_dependencies,
                              "serf_build_scope": "static library without SSL bucket object; response parser unmodified"},
              "controls": control_hashes,
              "control_meaning": "Valid HTTP/1.1 GET request and 200 response controls",
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(rows)}/{len(parsers)} C HTTP/1.1 package paths passed")


if __name__ == "__main__":
    main()
