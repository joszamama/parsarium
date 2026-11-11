"""Create a deterministic, valid DEFLATE-compressed ZIP with one text entry."""

from pathlib import Path
import zipfile


def main() -> None:
    path = Path(__file__).with_name("hello.zip")
    info = zipfile.ZipInfo("hello.txt", date_time=(2020, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o644 << 16
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(info, b"parsarium\n")
    print(f"{path}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
