"""Replay the PCC 0.1.0 public C point-cloud API on the ASCII PLY control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import os
import platform
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER = ROOT / "adapters/c/ascii_ply/pcc.c"
LOCK = json.loads((DATA / "source-lock.json").read_text())["pcc"]
PARSER = next(p for p in json.loads((DATA / "parsers.json").read_text()) if p["name"] == "pcc")
ARCHIVE = Path(os.environ.get("PARSARIUM_PCC_ARCHIVE", str(Path(tempfile.gettempdir()) / "parsarium-pcc-v0.1.0.tar.gz")))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def verify() -> None:
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    assert digest(ADAPTER) == LOCK["adapter_sha256"]
    if not ARCHIVE.exists() or digest(ARCHIVE) != LOCK["source_sha256"]:
        with urlopen(Request(LOCK["source_url"], headers={"User-Agent": "Parsarium C ASCII PLY verifier"}), timeout=120) as response:
            ARCHIVE.write_bytes(response.read())
    assert digest(ARCHIVE) == LOCK["source_sha256"]
    with tarfile.open(ARCHIVE) as archive:
        for member, expected in LOCK["source_members"].items():
            item = archive.extractfile(member)
            assert item is not None and sha256(item.read()).hexdigest() == expected, member
        with tempfile.TemporaryDirectory(prefix="parsarium-pcc-") as scratch:
            archive.extractall(scratch)
            source = Path(scratch) / "pcc-0.1.0"
            build = Path(scratch) / "build"
            run(["cmake", "-S", str(source), "-B", str(build), "-DUSE_ZSTD=OFF", "-DBUILD_EXAMPLES=OFF"])
            include = ["-I", str(source / "include"), "-I", str(build / "export"),
                       "-I", str(source / "source/internal")]
            cc, cxx = os.getenv("CC", "cc"), os.getenv("CXX", "c++")
            objects = []
            commands = []
            for filename in ("point_cloud.c", "octree.c", "ply.cpp", "miniply.cpp"):
                compiler = cxx if filename.endswith(".cpp") else cc
                language = "-std=c++17" if filename.endswith(".cpp") else "-std=c17"
                obj = build / (filename + ".o")
                command = [compiler, language, *include, "-c", str(source / "source" / filename), "-o", str(obj)]
                run(command)
                objects.append(str(obj))
                commands.append(shlex.join(command))
            adapter_obj = build / "pcc-adapter.o"
            command = [cc, "-std=c17", *include, "-c", str(ADAPTER), "-o", str(adapter_obj)]
            run(command)
            commands.append(shlex.join(command))
            binary = build / "pcc-ply-control"
            command = [cxx, str(adapter_obj), *objects, "-o", str(binary)]
            run(command)
            commands.append(shlex.join(command))
            execute = [str(binary), str(CONTROL)]
            output = json.loads(run(execute))
            assert output == PARSER["expected_output"], output

    path = DATA / "verification.json"
    result = json.loads(path.read_text())
    result["third_party"] = [row for row in result["third_party"] if row["package"] != "pcc"] + [{
        "package": "pcc", "version": PARSER["version"], "control": PARSER["control"],
        "build_commands": commands, "command": shlex.join(execute), "output": output, "pass": True,
        "note": "Public C point-cloud API read the valid local ASCII PLY through bundled miniply; only three vertices and the second X coordinate are claimed.",
    }]
    result["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    result["platform"] = platform.platform()
    result.setdefault("local_libraries", {})["pcc"] = {
        "source_sha256": LOCK["source_sha256"], "release_commit": LOCK["release_commit"],
        "adapter_sha256": LOCK["adapter_sha256"],
    }
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("pcc@0.1.0: C ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
