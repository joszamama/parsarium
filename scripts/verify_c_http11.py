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


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True, timeout=120)


def archive(name: str, source: dict) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    target = CACHE / f"{name}-{source['release']}.tar.gz"
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
    assert CONTROL.read_bytes() == expected_control
    control_hash = sha256(expected_control).hexdigest()
    for parser in parsers:
        name = parser["name"]
        assert parser["version"] == lock[name]["release"] == snapshot["releases"][name]["version"]
        assert parser["license"] == snapshot["releases"][name]["license"]
        archive(name, lock[name])
    for name, pkgconfig in (("llhttp", "libllhttp"), ("libmicrohttpd", "libmicrohttpd")):
        installed = lock[name]
        assert run(["pkg-config", "--modversion", pkgconfig]).stdout.strip() == installed["release"]
        for path_key, hash_key in (("system_library", "system_library_sha256"),
                                   ("system_header", "system_header_sha256")):
            assert sha256(Path(installed[path_key]).read_bytes()).hexdigest() == installed[hash_key]
    with tempfile.TemporaryDirectory(prefix="parsarium-c-http11-build-") as temporary:
        build = Path(temporary)
        for name in ("http-parser", "picohttpparser", "mongoose", "httpp", "HTTPParserC"):
            with tarfile.open(archive(name, lock[name])) as tar:
                tar.extractall(build, filter="data")
        llflags = run(["pkg-config", "--cflags", "--libs", "libllhttp"]).stdout.split()
        mhdflags = run(["pkg-config", "--cflags", "--libs", "libmicrohttpd"]).stdout.split()
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
                              *mhdflags, "-o", str(build / "libmicrohttpd-adapter")]}
        rows = []
        for parser in parsers:
            name = parser["name"]
            run(commands[name])
            result = json.loads(run([str(build / f"{name}-adapter"), str(CONTROL)]).stdout)
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
                              "libmicrohttpd_library_sha256": lock["libmicrohttpd"]["system_library_sha256"]},
              "control": "controls/http11/request.http", "control_sha256": control_hash,
              "control_meaning": "Valid HTTP/1.1 GET request with Host, custom, and Connection headers",
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(rows)}/{len(parsers)} C HTTP/1.1 package paths passed")


if __name__ == "__main__":
    main()
