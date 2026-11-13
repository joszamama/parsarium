"""Apply the v1.0.1 missing-include fix needed by Apple clang/libc++."""

from pathlib import Path


def patch_aspose_pdf_foss(source_dir: Path) -> None:
    path = source_dir / "src/internal/asciihex.cpp"
    original = path.read_text()
    needle = "#include <cctype>\n"
    assert original.count(needle) == 1
    assert "#include <stdexcept>" not in original
    assert "#include <string>" not in original
    path.write_text(original.replace(needle, needle + "#include <stdexcept>\n#include <string>\n"))
