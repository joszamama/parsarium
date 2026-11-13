"""Build the tagged rustpdf C ABI and parse the valid two-page PDF."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/c/pdf/source-lock.json"
CONTROL = ROOT / "controls/pdf/two-page.pdf"
ADAPTER = ROOT / "adapters/c/pdf/rustpdf.c"


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                            timeout=240, check=True)
    return result.stdout.strip()


def verify(parser=None, source=None, root=ROOT, cache=None, target=None):
    del cache, target
    source = source or json.loads(LOCK.read_text())["rustpdf"]
    parser = parser or {"name": "rustpdf", "version": source["release"],
                        "control": "controls/pdf/two-page.pdf",
                        "expected_output": {"pages": 2}}
    assert sha256(CONTROL.read_bytes()).hexdigest() == source["control_sha256"]
    assert run(["rustc", "--version"], root) == source["rustc_version"]
    assert run(["cargo", "--version"], root) == source["cargo_version"]

    with tempfile.TemporaryDirectory(prefix="parsarium-rustpdf-c-pdf-") as folder:
        temp = Path(folder)
        archive = temp / "source.tar.gz"
        with urlopen(Request(source["source_url"], headers={
                "User-Agent": "Parsarium rustpdf verifier"}), timeout=90) as response:
            archive.write_bytes(response.read())
        assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]
        with tarfile.open(archive, "r:gz") as tar:
            for member_name, expected in source["source_members"].items():
                member = tar.extractfile(member_name)
                assert member is not None and sha256(member.read()).hexdigest() == expected
            for member in tar.getmembers():
                assert member.name == "rustpdf-swift-v0.5.0" or member.name.startswith(
                    "rustpdf-swift-v0.5.0/")
                assert ".." not in Path(member.name).parts
                assert member.isfile() or member.isdir()
            tar.extractall(temp)

        project = temp / "rustpdf-swift-v0.5.0"
        header = project / "include/pdf.h"
        run(["cargo", "build", "-p", "pdf-ffi", "--release", "--locked"], project)
        dylib = project / "target/release" / (
            "libpdf_ffi.dylib" if platform.system() == "Darwin" else "libpdf_ffi.so")
        assert dylib.exists()
        binary = temp / "adapter"
        run(["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
             "-I" + str(header.parent), str(ADAPTER), "-L" + str(dylib.parent),
             "-lpdf_ffi", "-Wl,-rpath," + str(dylib.parent), "-o", str(binary)], root)
        output = json.loads(run([str(binary), str(CONTROL)], root))
        assert output == parser["expected_output"], output
        row = {"package": "rustpdf", "version": parser["version"],
               "control": parser["control"], "output": output, "pass": True,
               "command": "python3 scripts/verify_rustpdf_c_pdf.py",
               "build_command": "cargo build -p pdf-ffi --release --locked; cc -std=c11 -O2 -Wall -Wextra -Werror -Iinclude adapters/c/pdf/rustpdf.c -lpdf_ffi"}
        library = {"source_sha256": source["source_sha256"],
                   "source_commit": source["source_commit"],
                   "cargo_lock_sha256": source["source_members"]["rustpdf-swift-v0.5.0/Cargo.lock"],
                   "built_library_sha256": sha256(dylib.read_bytes()).hexdigest(),
                   "header_sha256": sha256(header.read_bytes()).hexdigest()}
        return row, library


if __name__ == "__main__":
    row, _library = verify()
    print(json.dumps(row))
