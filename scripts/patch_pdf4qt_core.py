"""Apply the small macOS core-only compatibility patch to PDF4QT 1.6.0.0."""

from pathlib import Path
import sys


def replace_exact(path: Path, original: bytes, replacement: bytes, count: int = 1) -> None:
    contents = path.read_bytes()
    assert contents.count(original) == count, (path, original)
    path.write_bytes(contents.replace(original, replacement))


def patch_pdf4qt_core(root: Path) -> None:
    cmake = root / "CMakeLists.txt"
    replace_exact(cmake,
                  b"qt_add_translations(TARGETS Pdf4QtEditor",
                  b"if(NOT PDF4QT_BUILD_ONLY_CORE_LIBRARY)\r\nqt_add_translations(TARGETS Pdf4QtEditor")
    end = b"                    QM_FILES_OUTPUT_VARIABLE PDF4QT_QM_FILES)"
    replace_exact(cmake, end, end + b"\r\nendif()")

    sources = root / "Pdf4QtLibCore/sources"
    replace_exact(sources / "pdfexecutionpolicy.h",
                  b"std::for_each(std::execution::seq,", b"std::for_each(")
    replace_exact(sources / "pdfexecutionpolicy.h",
                  b"std::sort(std::execution::seq,", b"std::sort(")
    replace_exact(sources / "pdfvisitor.h",
                  b"std::for_each(std::execution::par,", b"std::for_each(", 2)
    replace_exact(sources / "pdfvisitor.h",
                  b"std::for_each(std::execution::seq,", b"std::for_each(")

    core_cmake = root / "Pdf4QtLibCore/CMakeLists.txt"
    freetype = b"target_link_libraries(Pdf4QtLibCore PRIVATE Freetype::Freetype)"
    replace_exact(core_cmake, freetype,
                  freetype + b"\r\nfind_package(Fontconfig REQUIRED)\r\n"
                             b"target_link_libraries(Pdf4QtLibCore PRIVATE Fontconfig::Fontconfig)")


if __name__ == "__main__":
    patch_pdf4qt_core(Path(sys.argv[1]))
