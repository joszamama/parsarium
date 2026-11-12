"""Build pinned C++ PDF readers and record valid-control results."""

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

from patch_pdf4qt_core import patch_pdf4qt_core
from patch_docling_parse import patch_docling_parse


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/pdf"
CONTROL = ROOT / "controls/pdf/one-page.pdf"
CACHE = Path(tempfile.gettempdir()) / "parsarium-cpp-pdf"
TARGET = ROOT / "adapters/cpp/pdf/target"
CONTROL_SHA256 = "9bbfad1ba7ac5d0f4e25dd1d2e00c9f4cc7a493e303034b5884759f42ec5f60a"


def run(command: list[str], cwd: Path = ROOT, timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)
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


def nuget_archive(name: str, version: str, url: str, expected_sha256: str) -> Path:
    target = CACHE / f"{name}-{version}.nupkg"
    if not target.exists() or sha256(target.read_bytes()).hexdigest() != expected_sha256:
        with urlopen(Request(url, headers={"User-Agent": "Parsarium C++ PDF verifier"}), timeout=120) as response:
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
        if name == "qtpdf":
            with urlopen(Request(source["source_header_url"],
                                 headers={"User-Agent": "Parsarium C++ PDF verifier"}), timeout=90) as response:
                upstream_header = response.read()
            assert sha256(upstream_header).hexdigest() == source["source_sha256"]
        else:
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
        elif name == "pdf4qt":
            patch = ROOT / source["patch"]
            assert sha256(patch.read_bytes()).hexdigest() == source["patch_sha256"]
            for formula, revision in source["installed_dependencies"].items():
                assert run(["brew", "list", "--versions", formula]) == f"{formula} {revision}"
            blend = source["build_dependencies"]["blend2d"]
            blend_archive = archive("blend2d", blend)
            blend_source = CACHE / f"blend2d-{blend['release']}"
            if not blend_source.exists():
                run(["tar", "-xzf", str(blend_archive), "-C", str(CACHE)])
            blend_build = CACHE / "blend2d-build"
            blend_install = CACHE / "blend2d-install"
            run(["cmake", "-S", str(blend_source), "-B", str(blend_build),
                 "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_INSTALL_PREFIX=" + str(blend_install),
                 "-DBLEND2D_NO_JIT=ON", "-DBLEND2D_STATIC=ON"])
            run(["cmake", "--build", str(blend_build), "-j4"])
            run(["cmake", "--install", str(blend_build)])
            source_dir = CACHE / f"PDF4QT-{source['release']}"
            if source_dir.exists():
                shutil.rmtree(source_dir)
            run(["tar", "-xzf", str(source_archive), "-C", str(CACHE)])
            patch_pdf4qt_core(source_dir)
            header = source_dir / "Pdf4QtLibCore/sources/pdfdocumentreader.h"
            build_dir = CACHE / "pdf4qt-build"
            run(["cmake", "-S", str(source_dir), "-B", str(build_dir),
                 "-DCMAKE_BUILD_TYPE=Release", "-DPDF4QT_BUILD_ONLY_CORE_LIBRARY=ON",
                 "-DPDF4QT_BUILD_TESTS=OFF", "-DOPENSSL_ROOT_DIR=/opt/homebrew/opt/openssl@3",
                 "-DCMAKE_PREFIX_PATH=" + ";".join([str(blend_install),
                     "/opt/homebrew/opt/openssl@3", "/opt/homebrew"])])
            run(["cmake", "--build", str(build_dir), "--target", "Pdf4QtLibCore", "-j4"])
            library = build_dir / "bin/libPdf4QtLibCore.1.6.0.0.dylib"
        elif name == "qtpdf":
            assert run(["brew", "list", "--versions", "qtwebengine"]) == "qtwebengine " + source["installed_revision"]
            assert run(["pkg-config", "--modversion", "Qt6Pdf"]) == source["pkg_config_version"]
            header = Path(source["local_header"])
            library = Path(source["local_library"])
            assert header.read_bytes() == upstream_header
        elif name == "xpdf":
            source_dir = CACHE / f"xpdf-{source['release']}"
            if not source_dir.exists():
                run(["tar", "-xzf", str(source_archive), "-C", str(CACHE)])
            header = source_dir / "xpdf/PDFDoc.h"
            build_dir = CACHE / "xpdf-build"
            assert run(["brew", "list", "--versions", "fontconfig"]) == "fontconfig " + source["fontconfig_revision"]
            fontconfig = Path(source["fontconfig_library"])
            assert sha256(fontconfig.read_bytes()).hexdigest() == source["fontconfig_sha256"]
            run(["cmake", "-S", str(source_dir), "-B", str(build_dir),
                 "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_POLICY_VERSION_MINIMUM=3.5"])
            run(["cmake", "--build", str(build_dir), "--target", "xpdf_objs", "goo", "fofi", "-j4"])
            library = build_dir / "libxpdf_parsarium.a"
            library.unlink(missing_ok=True)
            objects = sorted((build_dir / "xpdf/CMakeFiles/xpdf_objs.dir").glob("*.o"))
            assert objects
            run(["ar", "rcs", str(library), *(str(obj) for obj in objects)])
        elif name == "pdfmm":
            source_dir = CACHE / f"pdfmm-{source['release']}"
            if not source_dir.exists():
                run(["tar", "-xzf", str(source_archive), "-C", str(CACHE)])
            header = source_dir / "src/pdfmm/base/PdfMemDocument.h"
            for dep in source["installed_dependencies"]:
                path = Path(dep["path"])
                assert sha256(path.read_bytes()).hexdigest() == dep["sha256"]
            build_dir = CACHE / "pdfmm-build"
            run(["cmake", "-S", str(source_dir), "-B", str(build_dir),
                 "-DCMAKE_BUILD_TYPE=Release", "-DPDFMM_BUILD_LIB_ONLY=ON",
                 "-DPDFMM_SHARED=ON", "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
                 "-DOPENSSL_ROOT_DIR=/opt/homebrew/Cellar/openssl@4/4.1.0"])
            run(["cmake", "--build", str(build_dir), "--target", "pdfmm_shared", "-j4"])
            library = build_dir / "src/pdfmm/libpdfmm.0.10.0.dylib"
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
        elif name == "docling_parse":
            patch = ROOT / source["patch"]
            adapter = ROOT / parser["adapter"]
            assert sha256(patch.read_bytes()).hexdigest() == source["patch_sha256"]
            assert sha256(adapter.read_bytes()).hexdigest() == source["adapter_sha256"]
            for program, release in source["installed_dependencies"].items():
                assert run(["brew", "list", "--versions", program]) == f"{program} {release}"
            assert sha256(Path(source["compiler"]).read_bytes()).hexdigest() == source["compiler_sha256"]
            assert sha256(Path(source["pybind11_header"]).read_bytes()).hexdigest() == source["pybind11_header_sha256"]
            source_dir = CACHE / f"docling-parse-{source['release']}"
            build_dir = CACHE / "docling-parse-build"
            if source_dir.exists():
                shutil.rmtree(source_dir)
            if build_dir.exists():
                shutil.rmtree(build_dir)
            run(["tar", "-xzf", str(source_archive), "-C", str(CACHE)])
            patch_docling_parse(source_dir, adapter)
            header = source_dir / "src/parse/pdf_decoders/document.h"
            run(["cmake", "-S", str(source_dir), "-B", str(build_dir),
                 "-DCMAKE_BUILD_TYPE=Release", "-DUSE_SYSTEM_DEPS=OFF",
                 "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
                 "-DCMAKE_C_COMPILER=/opt/homebrew/opt/llvm/bin/clang",
                 "-DCMAKE_CXX_COMPILER=/opt/homebrew/opt/llvm/bin/clang++"], timeout=600)
            library = build_dir / "parsarium_control"
        else:
            header = Path(source["local_header"])
            library = Path(source["local_library"])
        assert sha256(header.read_bytes()).hexdigest() == source["local_header_sha256"]
        if name not in ("pdfio", "pdfwriter", "pdf4qt", "xpdf", "pdfmm", "docling_parse", "tspdf"):
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
        elif name == "pdf4qt":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "Qt6Core", "Qt6Gui", "Qt6Xml", "Qt6Svg"]))
            command = ["c++", "-std=c++20", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parent), "-I" + str(build_dir),
                       str(ROOT / parser["adapter"]), str(library), *flags,
                       "-Wl,-rpath," + str(library.parent), "-o", str(TARGET / name)]
        elif name == "qtpdf":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "Qt6Pdf"]))
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(TARGET / name)]
        elif name == "xpdf":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-Wno-unused-parameter", "-I" + str(source_dir / "xpdf"),
                       "-I" + str(source_dir / "goo"), "-I" + str(build_dir),
                       str(ROOT / parser["adapter"]), str(library),
                       str(build_dir / "goo/libgoo.a"), str(build_dir / "fofi/libfofi.a"),
                       str(fontconfig), "-o", str(TARGET / name)]
        elif name == "pdfmm":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-Wno-unnecessary-virtual-specifier", "-DPDFMM_SHARED=1",
                       "-I" + str(source_dir / "src"), "-I" + str(build_dir / "src/pdfmm"),
                       str(ROOT / parser["adapter"]), str(library),
                       "-Wl,-rpath," + str(library.parent), "-o", str(TARGET / name)]
        elif name == "vanillapdf":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(header.parents[2]), str(ROOT / parser["adapter"]),
                       str(library), "-Wl,-rpath," + str(library.parent),
                       "-o", str(TARGET / name)]
        elif name == "tspdf":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(source_dir / "include"), str(ROOT / parser["adapter"]),
                       str(library), "-o", str(TARGET / name)]
        elif name == "docling_parse":
            command = ["cmake", "--build", str(build_dir), "--target", "parsarium_control", "-j4"]
        else:
            raise AssertionError(name)
        run(command, timeout=1200 if name == "docling_parse" else 180)
        if name == "docling_parse":
            shutil.copy2(library, TARGET / name)
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
