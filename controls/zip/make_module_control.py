"""Create a deterministic ZIP containing one Python source module for zipimport."""

from pathlib import Path
import zipfile

TARGET = Path(__file__).with_name("hello-module.zip")
info = zipfile.ZipInfo("hello.py", date_time=(2020, 1, 1, 0, 0, 0))
info.compress_type = zipfile.ZIP_DEFLATED
info.create_system = 3
info.external_attr = 0o644 << 16
with zipfile.ZipFile(TARGET, "w") as archive:
    archive.writestr(info, b"message = 'parsarium'\n")
print(f"Wrote {TARGET}")
