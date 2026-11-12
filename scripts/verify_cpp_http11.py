"""Build pinned native C++ HTTP/1.1 readers and record valid-control results."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess
import tarfile
import tempfile
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/http11"
CONTROL = ROOT / "controls/http11/request.http"
CACHE = Path(tempfile.gettempdir()) / "parsarium-cpp-http11"
TARGET = ROOT / "adapters/cpp/http11/target"


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, check=True, text=True,
                          capture_output=True).stdout.strip()


def get_archive(name: str, source: dict) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    archive = CACHE / f"{name}-{source['release']}.tar.gz"
    if not archive.exists() or sha256(archive.read_bytes()).hexdigest() != source["source_sha256"]:
        shared = ROOT / "adapters/cpp/zip/cache/poco.tar.gz"
        if name == "poco" and shared.exists() and sha256(shared.read_bytes()).hexdigest() == source["source_sha256"]:
            archive.write_bytes(shared.read_bytes())
        else:
            with urlopen(source["source_url"], timeout=120) as response:
                archive.write_bytes(response.read())
    assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]
    return archive


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    sources = json.loads((DATA / "source-lock.json").read_text())
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
