"""Read a valid local ZIP with CPython's documented zipfile API."""

import json
import shutil
import sys
import tempfile
import zipfile
import zipimport
from pathlib import Path


def main(api, path):
    if api == "zipfile.ZipFile":
        with zipfile.ZipFile(path) as archive:
            return {"names": archive.namelist(),
                    "hello": archive.read("hello.txt").decode("ascii")}
    if api == "zipfile.Path":
        root = zipfile.Path(path)
        return {"names": sorted(item.name for item in root.iterdir()),
                "hello": (root / "hello.txt").read_text()}
    if api == "shutil.unpack_archive":
        with tempfile.TemporaryDirectory() as destination:
            shutil.unpack_archive(path, destination)
            return {"names": sorted(item.name for item in Path(destination).iterdir()),
                    "hello": (Path(destination) / "hello.txt").read_text()}
    if api == "zipimport.zipimporter":
        importer = zipimport.zipimporter(path)
        return {"source": importer.get_source("hello")}
    raise ValueError(f"unknown standard API: {api}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: standard.py API CONTROL_PATH")
    print(json.dumps(main(sys.argv[1], sys.argv[2])))
