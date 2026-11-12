"""Fetch and verify the source-built C ZIP parser releases."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePosixPath
from tarfile import open as taropen
from urllib.request import Request, urlopen
import base64
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
            if name == "sqlite" and "/".join(parts[1:]) not in (
                    "ext/misc/zipfile.c", "LICENSE.md"):
                continue
            assert member.isfile() or member.isdir(), member.name
            if not member.isfile():
                continue
            destination = CACHE / "source" / name / Path(*parts[1:])
            destination.parent.mkdir(parents=True, exist_ok=True)
            file = archive.extractfile(member)
            assert file is not None
            destination.write_bytes(file.read())
            destination.chmod(member.mode)


def prepare_libtfs() -> None:
    item = LOCK["libtfs"]
    source_path = CACHE / "libtfs-source.tar.gz"
    sources = [(source_path, item["source_url"], item["source_sha256"])]
    for asset in item["binary_assets"]:
        sources.append((CACHE / asset["name"], asset["url"], asset["sha256"]))
    for path, url, digest in sources:
        if path.exists() and sha256(path.read_bytes()).hexdigest() == digest:
            continue
        request = Request(url, headers={"User-Agent": "Parsarium-Research"})
        with urlopen(request, timeout=45) as response:
            data = response.read()
        assert sha256(data).hexdigest() == digest, url
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    for asset in item["binary_assets"]:
        with taropen(CACHE / asset["name"], mode="r:gz") as archive:
            for member in archive.getmembers():
                parts = PurePosixPath(member.name).parts
                assert parts and ".." not in parts and not member.name.startswith("/")
                assert member.isfile() or member.isdir(), member.name
                if not member.isfile():
                    continue
                destination = CACHE / "libtfs" / asset["destination"] / Path(*parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                file = archive.extractfile(member)
                assert file is not None
                destination.write_bytes(file.read())
                destination.chmod(member.mode)


def prepare_aosp_libzipfile() -> None:
    item = LOCK["aosp-libzipfile"]
    source = CACHE / "source/aosp-libzipfile"
    for file in item["files"]:
        destination = source / file["name"]
        if destination.exists() and sha256(destination.read_bytes()).hexdigest() == file["sha256"]:
            continue
        request = Request(file["url"], headers={"User-Agent": "Parsarium-Research"})
        with urlopen(request, timeout=45) as response:
            data = base64.b64decode(response.read())
        assert sha256(data).hexdigest() == file["sha256"], file["name"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)


def main() -> None:
    for name in ("kuba-zip", "zziplib", "unarr", "lowzip", "unziplib", "infozip-unzip", "junzip", "sqlite", "zipc"):
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
    prepare_libtfs()
    print(f"libtfs: pinned {LOCK['libtfs']['release']} source and macOS arm64 release assets verified")
    prepare_aosp_libzipfile()
    print(f"aosp-libzipfile: pinned {LOCK['aosp-libzipfile']['release']} source and C header verified")


if __name__ == "__main__":
    main()
