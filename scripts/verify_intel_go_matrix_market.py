"""Build compatible GraphBLAS 8.0.2 and run Intel's Go Matrix Market reader."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import os
import platform
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/go/matrix_market/intel"
LOCK = ROOT / "data/go/matrix_market/intel-forlagraphgo-lock.json"


def run(command: list[str], cwd: Path, timeout: int = 600, env=None) -> str:
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                            text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{command[0]} failed: {(result.stderr or result.stdout)[-2000:]}")
    return result.stdout.strip()


def verify(parser=None) -> tuple[dict, dict]:
    lock = json.loads(LOCK.read_text())
    parser = parser or {
        "name": lock["package"], "module": lock["module"],
        "version": lock["release"], "control": lock["control"],
        "scope": "Coordinate real matrix dimensions, entries and value",
        "expected_output": {"rows": 2, "cols": 3, "entries": 3, "value_0_2": -2},
    }
    assert parser["name"] == lock["package"]
    assert parser["module"] == lock["module"]
    assert parser["version"] == lock["release"]
    assert parser["control"] == lock["control"]
    assert sha256((ROOT / lock["control"]).read_bytes()).hexdigest() == lock["control_sha256"]
    assert platform.system() == "Darwin" and platform.machine() == "arm64"
    assert run(["go", "version"], ADAPTER) == lock["go_toolchain_observed"]
    assert run(["cmake", "--version"], ROOT).splitlines()[0] == lock["cmake_observed"]
    module = (ADAPTER / "go.mod").read_text()
    sums = (ADAPTER / "go.sum").read_text()
    assert f'{lock["module"]} {lock["release"]}' in module
    assert f'{lock["module"]} {lock["release"]} {lock["module_sum"]}' in sums
    assert f'{lock["module"]} {lock["release"]}/go.mod {lock["go_mod_sum"]}' in sums
    run(["go", "mod", "download"], ADAPTER, timeout=90)
    assert run(["go", "mod", "verify"], ADAPTER) == "all modules verified"
    module_dir = Path(run(["go", "list", "-m", "-f", "{{.Dir}}", lock["module"]], ADAPTER))
    assert sha256((module_dir / "LAGraph/MatrixMarket/read.go").read_bytes()).hexdigest() == lock["reader_source_sha256"]
    assert sha256((module_dir / "LICENSE").read_bytes()).hexdigest() == lock["license_sha256"]

    with tempfile.TemporaryDirectory(prefix="parsarium-intel-mm-") as folder:
        temp = Path(folder)
        archive = temp / "graphblas-v8.0.2.tar.gz"
        with urlopen(Request(lock["graphblas_source_url"], headers={
                "User-Agent": "Parsarium Intel Matrix Market verifier"}), timeout=90) as response:
            archive.write_bytes(response.read())
        assert sha256(archive.read_bytes()).hexdigest() == lock["graphblas_source_sha256"]
        with tarfile.open(archive, "r:gz") as tar:
            for member_name, digest in (
                    (lock["graphblas_header_member"], lock["graphblas_header_sha256"]),
                    (lock["graphblas_license_member"], lock["graphblas_license_sha256"])):
                member = tar.extractfile(member_name)
                assert member is not None and sha256(member.read()).hexdigest() == digest
        run(["tar", "-xzf", str(archive), "-C", str(temp)], ROOT, timeout=90)
        source = temp / "GraphBLAS-8.0.2"
        build = temp / "build"
        install = temp / "install"
        configure = run(["cmake", "-S", str(source), "-B", str(build),
                         *lock["graphblas_build_options"],
                         "-DCMAKE_INSTALL_PREFIX=" + str(install)], ROOT, timeout=90)
        assert "GraphBLAS C API: v2.0" in configure
        run(["cmake", "--build", str(build), "--parallel", "8"], ROOT)
        run(["cmake", "--install", str(build)], ROOT, timeout=90)
        assert sha256((install / "include/GraphBLAS.h").read_bytes()).hexdigest() == lock["graphblas_header_sha256"]
        library = install / "lib/libgraphblas.8.0.2.dylib"
        assert library.exists()
        env = os.environ.copy()
        env["CGO_CFLAGS"] = "-I" + str(install / "include")
        env["CGO_LDFLAGS"] = "-L" + str(install / "lib") + " -Wl,-rpath," + str(install / "lib")
        output = json.loads(run(["go", "run", "-mod=readonly", ".",
                                 str(ROOT / lock["control"])], ADAPTER, timeout=120, env=env))
        assert output == parser["expected_output"], output
        row = {"package": parser["name"], "module": parser["module"],
               "version": parser["version"], "control": parser["control"],
               "scope": parser["scope"], "output": output, "pass": True,
               "error": None, "command": "python3 scripts/verify_intel_go_matrix_market.py",
               "checked_at_utc": datetime.now(timezone.utc).isoformat(),
               "environment": "macOS arm64; GraphBLAS v8.0.2 built from pinned source; Go modules verified by go.sum"}
        evidence = {"graphblas_source_sha256": lock["graphblas_source_sha256"],
                    "graphblas_library_sha256": sha256(library.read_bytes()).hexdigest(),
                    "graphblas_c_api": lock["graphblas_c_api"],
                    "module_sum": lock["module_sum"], "source_commit": lock["source_commit"]}
        return row, evidence


if __name__ == "__main__":
    row, evidence = verify()
    print(json.dumps({"result": row, "library": evidence}, sort_keys=True))
