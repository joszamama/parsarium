"""Read ZIP entries from bytes through fsspec's ZIP filesystem."""

from io import BytesIO
import zipfile

from fsspec.implementations.zip import ZipFileSystem


def parse_zip(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    filesystem = ZipFileSystem(fo=BytesIO(data))
    try:
        names = sorted(item["name"] for item in filesystem.ls("", detail=True)
                       if item.get("type") == "file")
        if not names:
            return None
        with filesystem.open(names[0], "rb") as member:
            contents = member.read((1 << 20) + 1)
        if names == ["hello.txt"]:
            return {"names": names, "hello": contents.decode("utf-8", "replace")}
        return {"names": names, "first_member_bytes": len(contents)}
    finally:
        filesystem.close()


def fuzz_one_input(data: bytes):
    try:
        parse_zip(data)
    except (zipfile.BadZipFile, EOFError, ValueError):
        pass
