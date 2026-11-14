"""Replay HRConvert2's tagged PHP Model pipeline on a local ASCII PLY."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import os
import platform
import shlex
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER = ROOT / "adapters/php/ascii_ply/hrconvert2.php"
REQ_LOCK = ROOT / "adapters/php/ascii_ply/hrconvert2-requirements.lock"
LOCK = json.loads((DATA / "source-lock.json").read_text())["zelon88/hrconvert2"]
PARSER = next(x for x in json.loads((DATA / "parsers.json").read_text()) if x["name"] == "zelon88/hrconvert2")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], *, environment: dict[str, str] | None = None, timeout: int = 300) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                            env=environment, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def verify() -> None:
    assert platform.system() == "Darwin" and platform.machine() == "arm64"
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    assert digest(ADAPTER) == LOCK["adapter_sha256"]
    assert digest(REQ_LOCK) == LOCK["requirements_lock_sha256"]
    assert run(["brew", "list", "--versions", "assimp"]) == "assimp 6.0.6"
    assimp = Path(run(["brew", "--prefix", "assimp"])) / "bin/assimp"
    assimp_library = assimp.parent.parent / "lib/libassimp.6.0.6.dylib"
    assert digest(assimp) == LOCK["assimp_binary_sha256"]
    assert digest(assimp_library) == LOCK["assimp_library_sha256"]

    with tempfile.TemporaryDirectory(prefix="parsarium-hrconvert2-") as temporary:
        work = Path(temporary)
        source = work / "source"
        for filename, metadata in LOCK["tagged_files"].items():
            path = source / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            with urlopen(Request(metadata["url"], headers={"User-Agent": "Parsarium PHP PLY verifier"}), timeout=120) as response:
                path.write_bytes(response.read())
            assert digest(path) == metadata["sha256"], filename

        venv = work / "venv"
        run(["uv", "venv", "--python", "python3.13", str(venv)])
        run(["uv", "pip", "sync", str(REQ_LOCK), "--python", str(venv / "bin/python"), "--require-hashes"], timeout=600)
        environment = os.environ.copy()
        environment["PATH"] = str(venv / "bin") + os.pathsep + environment["PATH"]
        environment["PARSARIUM_PYTHON"] = str(venv / "bin/python3")
        environment["PARSARIUM_ASSIMP"] = str(assimp)
        pipeline = source / "Resources/Pipelines/Model/pipeline.php"
        output_path = work / "triangle.obj"
        command = ["php", str(ADAPTER), str(pipeline), str(CONTROL), str(output_path)]
        output = json.loads(run(command, environment=environment))
        assert output == PARSER["expected_output"], output
        assert output_path.is_file() and output_path.stat().st_size > 0

    verification_path = DATA / "verification.json"
    results = json.loads(verification_path.read_text())
    checked_at_utc = datetime.now(timezone.utc).isoformat()
    results["checked_at_utc"] = checked_at_utc
    results.setdefault("local_libraries", {})["zelon88/hrconvert2"] = {
        "source_sha256": LOCK["source_sha256"],
        "release_commit": LOCK["release_commit"],
        "adapter_sha256": LOCK["adapter_sha256"],
        "requirements_lock_sha256": LOCK["requirements_lock_sha256"],
        "assimp_binary_sha256": LOCK["assimp_binary_sha256"],
        "assimp_library_sha256": LOCK["assimp_library_sha256"],
        "platform": platform.platform(),
        "php": run(["php", "-v"]).splitlines()[0],
        "build_scope": "Tagged HRConvert2 PHP Model pipeline with standalone host-service shims; real PyMeshLab 2025.7 and Assimp 6.0.6 stages both produced output. Full web server and its sandbox policy were not run."
    }
    results["third_party"] = [x for x in results["third_party"] if x["package"] != "zelon88/hrconvert2"]
    results["third_party"].append({
        "package": "zelon88/hrconvert2", "version": "v4.0.0", "control": PARSER["control"],
        "command": shlex.join(command), "output": output, "pass": True,
        "checked_at_utc": checked_at_utc,
        "note": "Unmodified tagged PHP convertModels pipeline accepted local ASCII PLY and used real PyMeshLab and Assimp stages; standalone host-service shims supplied tool paths and ran commands without the web application's sandbox."
    })
    results["note"] = "Five PHP package paths passed the valid ASCII PLY control; HRConvert2 is a tagged PHP application module over PyMeshLab and Assimp. The PHP standard/runtime inventory remains separate."
    verification_path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    print("zelon88/hrconvert2@v4.0.0: PHP ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
