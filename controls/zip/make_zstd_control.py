"""Generate a deterministic valid ZIP with one Zstandard-compressed member.

Run with the pinned Python ZIP environment from the repository root.
"""

from pathlib import Path
import zipfile_zstd as zipfile

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "controls" / "zip" / "hello-zstd.zip"
info = zipfile.ZipInfo("hello.txt", date_time=(2020, 1, 1, 0, 0, 0))
info.compress_type = zipfile.ZIP_ZSTANDARD
with zipfile.ZipFile(TARGET, "w") as archive:
    archive.writestr(info, b"parsarium\n")
print(f"Wrote {TARGET}")
