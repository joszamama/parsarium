"""Build pinned C PDF readers and verify a valid one-page local PDF."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import base64
import json
import platform
import shutil
import shlex
import subprocess
import tarfile
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/pdf"
CONTROL = ROOT / "controls/pdf/one-page.pdf"
CACHE = Path(tempfile.gettempdir()) / "parsarium-c-pdf"
TARGET = ROOT / "adapters/c/pdf/target"
CONTROL_SHA256 = "9bbfad1ba7ac5d0f4e25dd1d2e00c9f4cc7a493e303034b5884759f42ec5f60a"


def run(command: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def archive(name: str, source: dict) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    url = source["source_url"]
    suffix = ".tar.xz" if url.endswith(".tar.xz") else ".tgz" if url.endswith(".tgz") else ".tar.gz"
    target = CACHE / f"{name}-{source['release']}{suffix}"
    if not target.exists() or sha256(target.read_bytes()).hexdigest() != source["source_sha256"]:
        with urlopen(Request(url, headers={"User-Agent": "Parsarium C PDF verifier"}), timeout=90) as response:
            target.write_bytes(response.read())
    assert sha256(target.read_bytes()).hexdigest() == source["source_sha256"]
    return target


def nuget_archive(name: str, version: str, url: str, expected_sha256: str) -> Path:
    target = CACHE / f"{name}-{version}.nupkg"
    if not target.exists() or sha256(target.read_bytes()).hexdigest() != expected_sha256:
        with urlopen(Request(url, headers={"User-Agent": "Parsarium C PDF verifier"}), timeout=120) as response:
            target.write_bytes(response.read())
    assert sha256(target.read_bytes()).hexdigest() == expected_sha256
    return target


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    parsers = json.loads((DATA / "parsers.json").read_text())
    lock = json.loads((DATA / "source-lock.json").read_text())
    assert len(parsers) == json.loads((DATA / "cell.json").read_text())["verified_third_party_count"]
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    libraries = {}
    for parser in parsers:
        name = parser["name"]
        source = lock[name]
        source_archive = archive(name, source)
        with tarfile.open(source_archive) as tar:
            member = tar.extractfile(source["source_header_member"])
            assert member is not None
            assert sha256(member.read()).hexdigest() == source.get("source_header_sha256", source["local_header_sha256"])
        if name == "pdfio":
            source_dir = CACHE / f"pdfio-{source['release']}"
            if not source_dir.exists():
                run(["tar", "-xzf", str(source_archive), "-C", str(CACHE)])
            header = source_dir / "pdfio.h"
            library = source_dir / "libpdfio.a"
            run(["./configure", "--prefix=" + str(CACHE / "pdfio-install")], cwd=source_dir)
            run(["make", "clean"], cwd=source_dir)
            optim = "-O2 -arch " + platform.machine() if platform.system() == "Darwin" else "-O2"
            run(["make", "-j4", "OPTIM=" + optim], cwd=source_dir)
        elif name == "pdfium":
            source_dir = CACHE / f"pdfium-{source['release']}"
            if not (source_dir / "VERSION").exists():
                source_dir.mkdir(parents=True, exist_ok=True)
                run(["tar", "-xzf", str(source_archive), "-C", str(source_dir)])
            header = source_dir / "include/fpdfview.h"
            library = source_dir / "lib/libpdfium.dylib"
            assert (source_dir / "VERSION").read_text().strip().splitlines() == [
                "MAJOR=159", "MINOR=0", "BUILD=8152", "PATCH=0"]
            with urlopen(Request(source["upstream_header_url"], headers={"User-Agent": "Parsarium C PDF verifier"}),
                         timeout=90) as response:
                upstream_header = base64.b64decode(response.read())
            assert sha256(upstream_header).hexdigest() == source["source_header_sha256"]
        elif name == "vanillapdf":
            headers_package = source["nuget_headers"]
            runtime_package = source["nuget_runtime"]
            headers_archive = nuget_archive("vanillapdf-headers", source["release"],
                                            headers_package["url"], headers_package["sha256"])
            runtime_archive = nuget_archive("vanillapdf-runtime", source["release"],
                                            runtime_package["url"], runtime_package["sha256"])
            source_dir = CACHE / "vanillapdf-2.3.0"
            source_dir.mkdir(exist_ok=True)
            with zipfile.ZipFile(headers_archive) as package:
                package.extractall(source_dir)
            with zipfile.ZipFile(runtime_archive) as package:
                package.extractall(source_dir)
            header = source_dir / headers_package["header_member"]
            library = source_dir / runtime_package["library_member"]
        elif name == "tspdf":
            source_dir = CACHE / f"tspdf-{source['release']}"
            if source_dir.exists():
                shutil.rmtree(source_dir)
            run(["tar", "-xzf", str(source_archive), "-C", str(CACHE)])
            header = source_dir / "src/reader/tspr.h"
            run(["make", "lib", "-j4"], cwd=source_dir)
            library = source_dir / "build/libtspdf.a"
        elif name in ("imagemagick", "graphicsmagick"):
            assert source["installed_revision"] in run(["brew", "list", "--versions", name]).split()
            assert run(["pkg-config", "--modversion", source["pkg_config"]]) == source["pkg_config_version"]
            header = Path(source["local_header"])
            library = Path(source["local_library"])
            for dependency in source["installed_dependencies"]:
                assert sha256(Path(dependency["path"]).read_bytes()).hexdigest() == dependency["sha256"]
        elif name == "libvips":
            assert source["installed_revision"] in run(["brew", "list", "--versions", "vips"]).split()
            assert run(["pkg-config", "--modversion", source["pkg_config"]]) == source["release"]
            header = Path(source["local_header"])
            library = Path(source["local_library"])
            for dependency in source["installed_dependencies"]:
                assert sha256(Path(dependency["path"]).read_bytes()).hexdigest() == dependency["sha256"]
        else:
            header = Path(source["local_header"])
            library = Path(source["local_library"])
        assert sha256(header.read_bytes()).hexdigest() == source["local_header_sha256"]
        if name not in ("pdfio", "tspdf"):
            assert sha256(library.read_bytes()).hexdigest() == source["local_library_sha256"]
        adapter = str(ROOT / parser["adapter"])
        base = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror"]
        extra_build = None
        if name == "poppler-glib":
            assert run(["pkg-config", "--modversion", "poppler-glib"]) == source["release"]
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "poppler-glib"]))
            command = [*base, adapter, *flags, "-o", str(TARGET / name)]
        elif name == "qpdf":
            assert run(["brew", "list", "--versions", "qpdf"]) == "qpdf " + source["installed_revision"]
            object_file = TARGET / "qpdf.o"
            command = [*base, "-I" + str(header.parents[1]), adapter, "-c", "-o", str(object_file)]
            extra_build = ["c++", str(object_file), str(library), "-o", str(TARGET / name)]
        elif name == "pdfio":
            command = [*base, "-I" + str(header.parent), adapter, str(library),
                       *shlex.split(run(["pkg-config", "--libs", "libpng"])),
                       "-lz", "-o", str(TARGET / name)]
        elif name == "pdfium":
            command = [*base, "-I" + str(header.parent), adapter, str(library),
                       "-Wl,-rpath," + str(library.parent), "-o", str(TARGET / name)]
        elif name == "vanillapdf":
            command = [*base, "-I" + str(header.parents[2]), adapter, str(library),
                       "-Wl,-rpath," + str(library.parent), "-o", str(TARGET / name)]
        elif name == "tspdf":
            command = [*base, "-I" + str(source_dir / "include"), adapter,
                       str(library), "-o", str(TARGET / name)]
        elif name in ("imagemagick", "graphicsmagick"):
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", source["pkg_config"]]))
            command = [*base, adapter, *flags, "-o", str(TARGET / name)]
        elif name == "libvips":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", source["pkg_config"]]))
            command = [*base, adapter, *flags, "-o", str(TARGET / name)]
        elif name in ("mupdf", "ghostscript"):
            assert run(["brew", "list", "--versions", name]) == name + " " + source["release"]
            command = [*base, "-I" + str(header.parents[1]), adapter, str(library),
                       "-o", str(TARGET / name)]
        else:
            raise AssertionError(name)
        run(command)
        if extra_build is not None:
            run(extra_build)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        row = {"package": name, "version": parser["version"], "control": parser["control"],
               "build_command": shlex.join(command), "command": shlex.join(execute),
               "output": output, "pass": True}
        if extra_build is not None:
            row["link_command"] = shlex.join(extra_build)
        rows.append(row)
        libraries[name] = {"source_sha256": source["source_sha256"],
                           "local_library_sha256": sha256(library.read_bytes()).hexdigest(),
                           "local_header_sha256": source["local_header_sha256"]}
        print(f"{name}@{parser['version']}: C PDF passed")
    runtime_build = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                     str(ROOT / "adapters/c/pdf/coregraphics.c"),
                     "-framework", "CoreGraphics", "-framework", "CoreFoundation",
                     "-o", str(TARGET / "coregraphics")]
    run(runtime_build)
    runtime_execute = [str(TARGET / "coregraphics"), str(CONTROL)]
    runtime_output = json.loads(run(runtime_execute))
    assert runtime_output == {"pages": 1}
    runtime = [{"name": "macOS Core Graphics CGPDFDocument", "control": "controls/pdf/one-page.pdf",
                "build_command": shlex.join(runtime_build), "command": shlex.join(runtime_execute),
                "output": runtime_output, "pass": True}]
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["cc", "--version"]).splitlines()[0],
              "source_lock": "data/c/pdf/source-lock.json", "local_libraries": libraries,
              "control": "controls/pdf/one-page.pdf", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": runtime}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
