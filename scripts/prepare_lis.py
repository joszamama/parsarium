"""Build the pinned official Lis release for Matrix Market control adapters."""

from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile
import shutil
import subprocess


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def prepare_lis(source: dict, archive: Path, cache: Path) -> tuple[Path, str]:
    assert digest(archive) == source["source_sha256"]
    root_name = f"lis-{source['release']}"
    build_root = cache / "lis-build"
    if build_root.exists():
        shutil.rmtree(build_root)
    build_root.mkdir()
    with ZipFile(archive) as zipfile:
        for member in zipfile.namelist():
            parts = Path(member)
            assert not parts.is_absolute() and ".." not in parts.parts
            assert member == root_name + "/" or member.startswith(root_name + "/")
        for member, expected in source["source_members"].items():
            assert sha256(zipfile.read(member)).hexdigest() == expected, member
    extracted = subprocess.run(["unzip", "-oq", str(archive), "-d", str(build_root)],
                               text=True, capture_output=True, timeout=120)
    if extracted.returncode:
        raise RuntimeError(f"Lis extraction failed: {extracted.stderr}")
    tree = build_root / root_name
    install = build_root / "install"
    for command in (["sh", "./configure", "--prefix=" + str(install), "--disable-shared", "--enable-static"],
                    ["make", "-j4"], ["make", "install"]):
        result = subprocess.run(command, cwd=tree, text=True, capture_output=True, timeout=300)
        if result.returncode:
            raise RuntimeError(f"Lis build failed: {' '.join(command)}\n{result.stderr}")
    assert digest(install / "include/lis.h") == source["source_members"][root_name + "/include/lis.h"]
    return install, digest(install / "lib/liblis.a")
