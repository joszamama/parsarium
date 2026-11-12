"""Add the Parsarium control target to pinned Docling Parse v7.25.0 source."""

from pathlib import Path
import shutil
import sys


TARGET = b'''
add_executable(parsarium_control "${TOPLEVEL_PREFIX_PATH}/app/parsarium_control.cpp")
set_property(TARGET parsarium_control PROPERTY CXX_STANDARD 20)
add_dependencies(parsarium_control ${DEPENDENCIES})
target_link_libraries(parsarium_control ${DEPENDENCIES} ${LIB_LINK})
'''


def patch_docling_parse(source_root: Path, adapter: Path) -> None:
    qpdf_cmake = source_root / "cmake/extlib_qpdf_v12.cmake"
    qpdf_original = qpdf_cmake.read_bytes()
    anchor = b"      CMAKE_ARGS " + b"\\" * 2 + b" \n"
    compiler_args = (b"      -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER} " + b"\\" * 2 + b" \n"
                     b"      -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER} " + b"\\" * 2 + b" \n")
    assert qpdf_original.count(anchor) == 1
    qpdf_cmake.write_bytes(qpdf_original.replace(anchor, anchor + compiler_args))

    cmake = source_root / "CMakeLists.txt"
    original = cmake.read_bytes()
    assert b"add_executable(parsarium_control" not in original
    assert b"target_link_libraries(parse.exe ${DEPENDENCIES} ${LIB_LINK})" in original
    cmake.write_bytes(original + TARGET)
    shutil.copyfile(adapter, source_root / "app/parsarium_control.cpp")


if __name__ == "__main__":
    patch_docling_parse(Path(sys.argv[1]), Path(sys.argv[2]))
