"""Replay sk_renderer's tagged, standalone C micro_ply parser."""

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
DATA = ROOT / "data/c/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER = ROOT / "adapters/c/ascii_ply/sk_renderer.c"
LOCK = json.loads((DATA / "source-lock.json").read_text())["sk_renderer"]
PARSER = next(x for x in json.loads((DATA / "parsers.json").read_text()) if x["name"] == "sk_renderer")


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
    with tempfile.TemporaryDirectory(prefix="parsarium-sk-renderer-") as work:
        work = Path(work)
        for filename, metadata in LOCK["tagged_files"].items():
            path = work / filename
            with urlopen(Request(metadata["url"], headers={"User-Agent": "Parsarium C PLY verifier"}), timeout=120) as response:
                path.write_bytes(response.read())
            assert digest(path) == metadata["sha256"], filename
        cc = os.environ.get("CC", "clang")
        binary = work / "sk-renderer-ply-control"
        build = [cc, "-std=c11", "-O2", "-Wall", "-Wextra", "-I", str(work),
                 str(ADAPTER), "-o", str(binary)]
        run(build)
        execute = [str(binary), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == PARSER["expected_output"], output

    results = json.loads((DATA / "verification.json").read_text())
    results["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    results.setdefault("local_libraries", {})["sk_renderer"] = {
        "source_sha256": LOCK["source_sha256"],
        "release_commit": LOCK["release_commit"],
        "adapter_sha256": LOCK["adapter_sha256"],
        "compiler": run([cc, "--version"]).splitlines()[0],
        "platform": platform.platform(),
        "build_scope": "Tag-pinned standalone micro_ply.h from sk_renderer; no graphics runtime linked. The file is identical to the author's header-libs copy, so this is one shared parser family.",
    }
    results["third_party"] = [x for x in results["third_party"] if x["package"] != "sk_renderer"]
    results["third_party"].append({
        "package": "sk_renderer", "version": "v2026.11.3", "control": PARSER["control"],
        "build_command": shlex.join(build), "command": shlex.join(execute),
        "output": output, "pass": True,
        "note": "Tagged C micro_ply parser read local ASCII PLY bytes and converted the second vertex X coordinate; full renderer was not built.",
    })
    (DATA / "verification.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    print("sk_renderer@v2026.11.3: C ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
