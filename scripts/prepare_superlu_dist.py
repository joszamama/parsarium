"""Build the pinned SuperLU_DIST release for Matrix Market adapters."""

from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import tarfile


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def prepare_superlu_dist(source: dict, archive: Path, cache: Path) -> tuple[Path, Path, str]:
    assert digest(archive) == source["source_sha256"]
    root = source["archive_root"]
    tree = cache / root
    build = cache / "superlu-dist-build"
    if tree.exists():
        shutil.rmtree(tree)
    if build.exists():
        shutil.rmtree(build)
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            path = Path(member.name)
            assert not path.is_absolute() and ".." not in path.parts
            assert member.name == root or member.name.startswith(root + "/")
        for member, expected in source["source_members"].items():
            file = tar.extractfile(member)
            assert file is not None and sha256(file.read()).hexdigest() == expected, member
        tar.extractall(cache, filter="data")
    configure = [
        "cmake", "-S", str(tree), "-B", str(build),
        "-DCMAKE_C_COMPILER=mpicc", "-DCMAKE_CXX_COMPILER=mpic++",
        "-DCMAKE_BUILD_TYPE=Release", "-DXSDK_ENABLE_Fortran=OFF",
        "-Denable_python=OFF", "-Denable_tests=OFF", "-Denable_examples=OFF",
        "-Denable_single=OFF", "-Denable_complex16=OFF",
        "-DTPL_ENABLE_PARMETISLIB=OFF", "-DTPL_ENABLE_INTERNAL_BLASLIB=OFF",
        "-DTPL_BLAS_LIBRARIES=" + str(Path(source["openblas_prefix"]) / "lib/libopenblas.dylib"),
        "-DBUILD_SHARED_LIBS=ON",
    ]
    for command in (configure,
                    ["cmake", "--build", str(build), "--target", "superlu_dist", "-j8"]):
        result = subprocess.run(command, text=True, capture_output=True, timeout=300)
        if result.returncode:
            raise RuntimeError(f"SuperLU_DIST build failed: {' '.join(command)}\n{result.stdout}\n{result.stderr}")
    library = build / "SRC/libsuperlu_dist.9.3.0.dylib"
    assert library.is_file()
    return tree / "SRC/include", build / "SRC", digest(library)
