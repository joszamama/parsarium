"""Run one pinned Python ZIP API against a supplied valid local control."""

import json
import sys
import tempfile
from pathlib import Path


def result(names, content):
    return {"names": sorted(names), "hello": content.decode("ascii")}


def extracted(extract_func, path):
    with tempfile.TemporaryDirectory() as destination:
        extract_func(path, destination)
        names = [item.relative_to(destination).as_posix()
                 for item in Path(destination).rglob("*") if item.is_file()]
        return result(names, (Path(destination) / "hello.txt").read_bytes())


def run(name: str, path: Path):
    if name == "pyzipper":
        import pyzipper
        with pyzipper.AESZipFile(path) as archive:
            return result(archive.namelist(), archive.read("hello.txt"))
    if name == "zipfile-zstd":
        import zipfile_zstd as zipfile
        with zipfile.ZipFile(path) as archive:
            info = archive.getinfo("hello.txt")
            if info.compress_type != zipfile.ZIP_ZSTANDARD:
                raise ValueError("expected ZIP method 93 Zstandard")
            return result(archive.namelist(), archive.read("hello.txt"))
    if name == "zipp":
        import zipp
        root = zipp.Path(path)
        return result((item.name for item in root.iterdir()),
                      (root / "hello.txt").read_bytes())
    if name == "fsspec":
        import fsspec
        filesystem = fsspec.filesystem("zip", fo=str(path))
        try:
            return result((item["name"] for item in filesystem.ls("", detail=True)),
                          filesystem.open("hello.txt", "rb").read())
        finally:
            filesystem.close()
    if name == "fs":
        from fs.zipfs import ZipFS
        with ZipFS(str(path)) as archive:
            return result(archive.listdir("/"), archive.readbytes("hello.txt"))
    if name == "libarchive-c":
        import libarchive
        with libarchive.file_reader(str(path)) as archive:
            members = [(entry.pathname, b"".join(entry.get_blocks())) for entry in archive]
        return result((name for name, _ in members), dict(members)["hello.txt"])
    if name == "stream-unzip":
        from stream_unzip import stream_unzip
        members = [(name.decode("utf-8"), b"".join(chunks))
                   for name, _size, chunks in stream_unzip([path.read_bytes()])]
        return result((name for name, _ in members), dict(members)["hello.txt"])
    if name == "pyzip":
        from pyzip import PyZip
        archive = PyZip().from_file(str(path))
        return result(archive.zip_content.keys(), archive.zip_content["hello.txt"])
    if name in {"zipfile36", "zipfile37", "zipfile38", "zipfile2"}:
        module = __import__(name)
        with module.ZipFile(str(path)) as archive:
            return result(archive.namelist(), archive.read("hello.txt"))
    if name == "larzarchive":
        from larzarchive import listing, extract
        names = listing(str(path))
        output = extracted(lambda source, dest: extract(source, dest), str(path))
        if sorted(names) != output["names"]:
            raise ValueError("listing and extraction disagree")
        return output
    if name == "python-archive":
        from archive import Archive
        return extracted(lambda source, dest: Archive(source).extract(dest), str(path))
    if name == "omni-archive":
        from omni_archive import Archive
        archive = Archive(str(path))
        try:
            names = [member.name for member in archive.members()]
            with archive.open_member("hello.txt", "rb") as stream:
                return result(names, stream.read())
        finally:
            archive.close()
    if name == "archivey":
        import archivey
        with archivey.open_archive(str(path)) as archive:
            return result((member.name for member in archive.members()),
                          archive.read("hello.txt"))
    if name == "zipmonkey":
        import zipmonkey
        with zipmonkey.open(str(path)) as archive:
            return result(archive.namelist(), archive.read("hello.txt"))
    if name == "archive-path":
        from archive_path import ZipPath
        archive = ZipPath(str(path))
        try:
            return result((member.name for member in archive.iterdir()),
                          (archive / "hello.txt").read_bytes())
        finally:
            archive.close()
    if name == "patool":
        import patoolib
        return extracted(lambda source, dest: patoolib.extract_archive(source,
                         outdir=dest, verbosity=-1), str(path))
    if name == "pyunpack":
        from pyunpack import Archive
        return extracted(lambda source, dest: Archive(source).extractall(dest), str(path))
    raise ValueError(f"unknown package: {name}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: main.py PACKAGE CONTROL_PATH")
    print(json.dumps(run(sys.argv[1], Path(sys.argv[2]))))
