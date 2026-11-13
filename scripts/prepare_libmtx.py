"""Build tagged Libmtx's Matrix Market reader from its pinned C source."""

from hashlib import sha256
from pathlib import Path
import shlex
import shutil
import subprocess
import tarfile


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def execute(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=600)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def prepare_libmtx(source: dict, archive: Path, cache: Path) -> tuple[Path, Path, Path, str]:
    assert digest(archive) == source["source_sha256"]
    root = source["archive_root"]
    work = cache / "libmtx-build"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or not (
                member.name == root or member.name.startswith(root + "/")
            ):
                raise ValueError(f"unsafe Libmtx archive path: {member.name}")
        for member, expected in source["source_members"].items():
            file = tar.extractfile(member)
            assert file is not None and sha256(file.read()).hexdigest() == expected, member
        tar.extractall(work, filter="data")
    tree = work / root
    execute(["sh", "./autogen.sh"], tree)
    build = work / "build"
    build.mkdir()
    install = work / "install"
    openblas = execute(["brew", "--prefix", "openblas"], tree)
    assert Path(openblas).resolve() == Path(source["openblas_prefix"])
    execute([str(tree / "configure"), "--prefix=" + str(install),
             "--without-mpi", "--without-openmp", "--without-zlib",
             "--with-openblas=" + openblas], build)
    execute(["make", "-j4", "libmtx.la"], build)
    execute(["make", "install-libLTLIBRARIES"], build)
    library = install / "lib/libmtx.0.dylib"
    return tree, build, install, digest(library)
