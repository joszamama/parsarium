"""Build the pinned unpdf C ABI and exercise its local PDF file parser."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import shlex
import subprocess
import tarfile


def _run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=900)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def verify(parser: dict, source: dict, root: Path, cache: Path, target: Path) -> tuple[dict, dict]:
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / f"unpdf-{source['release']}.crate"
    if not archive.exists() or sha256(archive.read_bytes()).hexdigest() != source["source_sha256"]:
        request = Request(source["source_url"], headers={"User-Agent": "Parsarium C PDF verifier"})
        with urlopen(request, timeout=90) as response:
            archive.write_bytes(response.read())
    assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]

    source_dir = cache / f"unpdf-{source['release']}"
    if not source_dir.exists():
        with tarfile.open(archive) as tar:
            tar.extractall(cache)
    for relative, expected in source["source_members"].items():
        assert sha256((source_dir / relative).read_bytes()).hexdigest() == expected

    cargo = ["cargo", "build", "--release", "--locked", "--no-default-features", "--features", "ffi"]
    _run(cargo, source_dir)
    library = source_dir / "target/release/libunpdf.dylib"
    assert library.is_file()

    build = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
             str(root / parser["adapter"]), "-L" + str(library.parent), "-lunpdf",
             "-Wl,-rpath," + str(library.parent), "-o", str(target / "unpdf")]
    _run(build, root)
    control = root / parser["control"]
    assert sha256(control.read_bytes()).hexdigest() == source["control_sha256"]
    execute = [str(target / "unpdf"), str(control)]
    output = json.loads(_run(execute, root))
    assert output == parser["expected_output"], output
    row = {"package": "unpdf", "version": parser["version"], "control": parser["control"],
           "cargo_build_command": shlex.join(cargo), "cargo_build_cwd": str(source_dir),
           "build_command": shlex.join(build), "command": shlex.join(execute),
           "output": output, "pass": True}
    evidence = {"source_sha256": source["source_sha256"],
                "ffi_source_sha256": source["source_members"]["src/ffi.rs"],
                "cargo_lock_sha256": source["source_members"]["Cargo.lock"],
                "local_library_sha256": sha256(library.read_bytes()).hexdigest()}
    return row, evidence
