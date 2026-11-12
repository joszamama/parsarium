"""Build pinned C++ PDF readers and record valid-control results."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import base64
import json
import platform
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/pdf"
CONTROL = ROOT / "controls/pdf/one-page.pdf"
CACHE = Path(tempfile.gettempdir()) / "parsarium-cpp-pdf"
TARGET = ROOT / "adapters/cpp/pdf/target"
CONTROL_SHA256 = "9bbfad1ba7ac5d0f4e25dd1d2e00c9f4cc7a493e303034b5884759f42ec5f60a"


def run(command: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def archive(name: str, source: dict) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    suffix = ".tar.xz" if source["source_url"].endswith(".tar.xz") else ".tgz" if source["source_url"].endswith(".tgz") else ".tar.gz"
    target = CACHE / f"{name}-{source['release']}{suffix}"
    if not target.exists() or sha256(target.read_bytes()).hexdigest() != source["source_sha256"]:
        with urlopen(Request(source["source_url"], headers={"User-Agent": "Parsarium C++ PDF verifier"}),
                     timeout=90) as response:
            target.write_bytes(response.read())
    assert sha256(target.read_bytes()).hexdigest() == source["source_sha256"]
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
            assert sha256(header.read_bytes()).hexdigest() == source["local_header_sha256"]
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
            with urlopen(Request(source["upstream_header_url"], headers={"User-Agent": "Parsarium C++ PDF verifier"}),
                         timeout=90) as response:
                upstream_header = base64.b64decode(response.read())
            assert sha256(upstream_header).hexdigest() == source["source_header_sha256"]
        elif name == "pdfwriter":
            source_dir = CACHE / f"PDF-Writer-{source['release']}"
            if not source_dir.exists():
                run(["tar", "-xzf", str(source_archive), "-C", str(CACHE)])
            header = source_dir / "PDFWriter/PDFParser.h"
            build_dir = CACHE / "pdfwriter-build"
            run(["cmake", "-S", str(source_dir), "-B", str(build_dir),
                 "-DCMAKE_BUILD_TYPE=Release", "-DPDFHUMMUS_NO_DCT=TRUE",
                 "-DPDFHUMMUS_NO_TIFF=TRUE", "-DPDFHUMMUS_NO_PNG=TRUE",
                 "-DUSE_BUNDLED=FALSE", "-DUSE_UNBUNDLED_FALLBACK_BUNDLED=TRUE"])
            run(["cmake", "--build", str(build_dir), "--target", "PDFWriter", "-j4"])
            library = build_dir / "PDFWriter/libPDFWriter.a"
        else:
            header = Path(source["local_header"])
            library = Path(source["local_library"])
        assert sha256(header.read_bytes()).hexdigest() == source["local_header_sha256"]
        if name not in ("pdfio", "pdfwriter"):
            assert sha256(library.read_bytes()).hexdigest() == source["local_library_sha256"]
        if name == "poppler":
            assert run(["pkg-config", "--modversion", source["pkg_config"]]) == source["release"]
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", source["pkg_config"]]))
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(TARGET / name)]
        elif name == "podofo":
            assert run(["brew", "list", "--versions", "podofo"]) == "podofo " + source["release"]
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-Wno-unnecessary-virtual-specifier",
                       "-I" + str(header.parents[2]), str(ROOT / parser["adapter"]),
                       str(library), "-o", str(TARGET / name)]
        elif name == "qpdf":
            assert run(["brew", "list", "--versions", "qpdf"]) == "qpdf " + source["installed_revision"]
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parents[1]), str(ROOT / parser["adapter"]),
                       str(library), "-o", str(TARGET / name)]
        elif name == "mupdf":
            assert run(["brew", "list", "--versions", "mupdf"]) == "mupdf " + source["release"]
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parents[1]), str(ROOT / parser["adapter"]),
                       str(library), "-o", str(TARGET / name)]
        elif name == "ghostscript":
            assert run(["brew", "list", "--versions", "ghostscript"]) == "ghostscript " + source["release"]
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parents[1]), str(ROOT / parser["adapter"]),
                       str(library), "-o", str(TARGET / name)]
        elif name == "pdfio":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parent), str(ROOT / parser["adapter"]),
                       str(library), *shlex.split(run(["pkg-config", "--libs", "libpng"])),
                       "-lz", "-o", str(TARGET / name)]
        elif name == "pdfium":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parent), str(ROOT / parser["adapter"]),
                       str(library), "-Wl,-rpath," + str(library.parent),
                       "-o", str(TARGET / name)]
        elif name == "pdfwriter":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parent), str(ROOT / parser["adapter"]),
                       str(library), str(build_dir / "LibAesgm/libLibAesgm.a"),
                       *shlex.split(run(["pkg-config", "--libs", "freetype2"])),
                       "-lz", "-o", str(TARGET / name)]
        else:
            raise AssertionError(name)
        run(command)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(command),
                     "command": shlex.join(execute), "output": output, "pass": True})
        libraries[name] = {"source_sha256": source["source_sha256"],
                           "local_library_sha256": sha256(library.read_bytes()).hexdigest(),
                           "local_header_sha256": source["local_header_sha256"]}
        print(f"{name}@{parser['version']}: C++ PDF passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["c++", "--version"]).splitlines()[0],
              "source_lock": "data/cpp/pdf/source-lock.json",
              "local_libraries": libraries,
              "control": "controls/pdf/one-page.pdf", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
