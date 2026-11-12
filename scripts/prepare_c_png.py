"""Fetch pinned C PNG source releases and verify every extracted source file."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path
from pathlib import PurePosixPath
from tarfile import open as taropen
from urllib.request import Request, urlopen
from zipfile import ZipFile
import json

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "data/c/png/source-lock.json").read_text())
CACHE = ROOT / "adapters/c/png/cache"


def prepare(name: str) -> None:
    item = LOCK[name]
    suffix = ".zip" if item["source_url"].endswith(".zip") else (".tar.xz" if item["source_url"].endswith(".tar.xz") else ".tar.gz")
    archive_path = CACHE / (name + suffix)
    if archive_path.exists() and sha256(archive_path.read_bytes()).hexdigest() == item["source_sha256"]:
        data = archive_path.read_bytes()
    else:
        request = Request(item["source_url"], headers={"User-Agent": "Parsarium-Research"})
        with urlopen(request, timeout=45) as response:
            data = response.read()
        assert sha256(data).hexdigest() == item["source_sha256"], name
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_bytes(data)
    if name == "libpng":
        with taropen(fileobj=BytesIO(data), mode="r:xz") as archive:
            prefix = f"libpng-{item['release']}"
            for member in archive.getmembers():
                parts = PurePosixPath(member.name).parts
                assert parts and parts[0] == prefix and ".." not in parts
                if not member.isfile():
                    continue
                destination = CACHE / "source/libpng" / Path(*parts[1:])
                destination.parent.mkdir(parents=True, exist_ok=True)
                file = archive.extractfile(member)
                assert file is not None
                destination.write_bytes(file.read())
        return
    if suffix == ".zip":
        with ZipFile(BytesIO(data)) as archive:
            names = archive.namelist()
            read_file = archive.read
            write_files(name, item, names, read_file)
    else:
        with taropen(fileobj=BytesIO(data), mode="r:xz" if suffix == ".tar.xz" else "r:gz") as archive:
            members = {member.name: member for member in archive.getmembers() if member.isfile()}
            def read_file(path: str) -> bytes:
                file = archive.extractfile(members[path])
                assert file is not None
                return file.read()
            write_files(name, item, list(members), read_file)


def write_files(name: str, item: dict, names: list[str], read_file) -> None:
    for expected in item["files"]:
        matches = [path for path in names if path.endswith(expected["archive_suffix"])]
        assert len(matches) == 1, (name, expected["archive_suffix"], matches)
        data = read_file(matches[0])
        assert sha256(data).hexdigest() == expected["sha256"], expected["destination"]
        destination = CACHE / "source" / expected["destination"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)


def main() -> None:
    for name in ("libpng", "stb", "lodepng", "libspng"):
        prepare(name)
        print(f"{name}: pinned {LOCK[name]['release']} source verified")


if __name__ == "__main__":
    main()
