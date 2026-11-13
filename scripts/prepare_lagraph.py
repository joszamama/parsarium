"""Build the pinned LAGraph release against the pinned local GraphBLAS."""

from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import tarfile


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def prepare_lagraph(source: dict, archive: Path, cache: Path) -> tuple[Path, Path, str]:
    assert digest(archive) == source["source_sha256"]
    root = source["archive_root"]
    tree = cache / root
    build = cache / "lagraph-build"
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
    graphblas = Path(source["graphblas_prefix"])
    libomp = Path(source["libomp_prefix"])
    configure = [
        "cmake", "-S", str(tree), "-B", str(build),
        "-DCMAKE_PREFIX_PATH=" + str(graphblas) + ";" + str(libomp),
        "-DCMAKE_BUILD_TYPE=Release", "-DLAGRAPH_USE_OPENMP=OFF",
        "-DBUILD_TESTING=OFF", "-DBUILD_SHARED_LIBS=ON", "-DBUILD_STATIC_LIBS=OFF",
        "-DOpenMP_C_FLAGS=-Xpreprocessor -fopenmp", "-DOpenMP_C_LIB_NAMES=omp",
        "-DOpenMP_omp_LIBRARY=" + str(libomp / "lib/libomp.dylib"),
    ]
    for command in (configure, ["cmake", "--build", str(build), "--target", "LAGraph", "-j", "8"]):
        result = subprocess.run(command, text=True, capture_output=True, timeout=300)
        if result.returncode:
            raise RuntimeError(f"LAGraph build failed: {' '.join(command)}\n{result.stdout}\n{result.stderr}")
    library = build / "src/liblagraph.1.2.2.dylib"
    assert library.is_file()
    return tree / "include", build / "src", digest(library)
