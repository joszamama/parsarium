"""Build the pinned official librsb release for Matrix Market adapters."""

from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import tarfile


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def prepare_librsb(source: dict, archive: Path, cache: Path) -> tuple[Path, str]:
    assert digest(archive) == source["source_sha256"]
    root = source["archive_root"]
    work = cache / "librsb-build"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            path = Path(member.name)
            assert not path.is_absolute() and ".." not in path.parts
            assert member.name == root or member.name.startswith(root + "/")
        for member, expected in source["source_members"].items():
            file = tar.extractfile(member)
            assert file is not None and sha256(file.read()).hexdigest() == expected, member
        tar.extractall(work, filter="data")
    tree = work / root
    install = work / "install"
    for command in (
        ["sh", "./configure", "--prefix=" + str(install), "--disable-openmp",
         "--disable-shared", "--enable-static"],
        ["gmake", "-j8"],
        ["gmake", "install"],
    ):
        result = subprocess.run(command, cwd=tree, text=True, capture_output=True, timeout=600)
        if result.returncode:
            raise RuntimeError(f"librsb build failed: {' '.join(command)}\n{result.stderr}")
    assert digest(install / "include/rsb.h") == source["source_members"][root + "/rsb.h"]
    return install, digest(install / "lib/librsb.a")
