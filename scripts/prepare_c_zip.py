"""Fetch and verify the source-built C ZIP parser releases."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePosixPath
from tarfile import open as taropen
from urllib.request import Request, urlopen
import json


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "adapters/c/zip/cache"
LOCK = json.loads((ROOT / "data/c/zip/source-lock.json").read_text())


def prepare(name: str) -> None:
    item = LOCK[name]
    archive_path = CACHE / (name + ".tar.gz")
    if archive_path.exists() and sha256(archive_path.read_bytes()).hexdigest() == item["source_sha256"]:
        data = archive_path.read_bytes()
    else:
        request = Request(item["source_url"], headers={"User-Agent": "Parsarium-Research"})
        with urlopen(request, timeout=45) as response:
            data = response.read()
        assert sha256(data).hexdigest() == item["source_sha256"], name
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_bytes(data)
    with taropen(fileobj=BytesIO(data), mode="r:gz") as archive:
        members = archive.getmembers()
        prefixes = {PurePosixPath(member.name).parts[0] for member in members}
        assert len(prefixes) == 1
        prefix = prefixes.pop()
        for member in members:
            parts = PurePosixPath(member.name).parts
            assert parts and parts[0] == prefix and ".." not in parts
            assert member.isfile() or member.isdir(), member.name
            if not member.isfile():
                continue
            destination = CACHE / "source" / name / Path(*parts[1:])
            destination.parent.mkdir(parents=True, exist_ok=True)
            file = archive.extractfile(member)
            assert file is not None
            destination.write_bytes(file.read())
            destination.chmod(member.mode)


def main() -> None:
    for name in ("kuba-zip", "zziplib", "unarr", "lowzip", "unziplib"):
        prepare(name)
        print(f"{name}: pinned {LOCK[name]['release']} source verified")
    name = "libc7zip"
    prepare(name)
    item = LOCK[name]
    engine_archive = CACHE / "7z2603-src.tar.xz"
    if not (engine_archive.exists() and
            sha256(engine_archive.read_bytes()).hexdigest() == item["engine_source_sha256"]):
        request = Request(item["engine_source_url"], headers={"User-Agent": "Parsarium-Research"})
        with urlopen(request, timeout=45) as response:
            engine = response.read()
        assert sha256(engine).hexdigest() == item["engine_source_sha256"]
        engine_archive.write_bytes(engine)
    cmake = CACHE / "source/libc7zip/vendor/lib7zip/CMakeLists.txt"
    cmake.write_text(cmake.read_text().replace(
        "https://7-zip.org/a/7z2603-src.tar.xz", engine_archive.resolve().as_uri()))
    print(f"{name}: pinned {item['release']} source and 7-Zip {item['engine_release']} source verified")


if __name__ == "__main__":
    main()
