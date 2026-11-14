"""Replay the tagged Providence and Heratio PHP ASCII PLY modules."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import shlex
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
LOCK = json.loads((DATA / "source-lock.json").read_text())
PARSERS = {item["name"]: item for item in json.loads((DATA / "parsers.json").read_text())}
NAMES = ("collectiveaccess/providence", "ahg/3d-model", "collectiveaccess/pawtucket2")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def fetch(url: str, destination: Path, expected: str) -> None:
    if not destination.exists() or digest(destination) != expected:
        with urlopen(Request(url, headers={"User-Agent": "Parsarium ASCII PLY verifier"}), timeout=120) as response:
            destination.write_bytes(response.read())
    assert digest(destination) == expected, destination


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def verify() -> None:
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    records = []
    with tempfile.TemporaryDirectory(prefix="parsarium-php-ply-") as scratch:
        for name in NAMES:
            source = LOCK[name]
            parser = PARSERS[name]
            assert source["release"] == parser["version"]
            assert digest(ROOT / source["adapter"]) == source["adapter_sha256"]
            if "support" in source:
                assert digest(ROOT / source["support"]) == source["support_sha256"]
            source_path = Path(scratch) / (name.replace("/", "-") + ".php")
            fetch(source["source_url"], source_path, source["source_sha256"])
            for label in ("license", "documentation", "manifest"):
                if f"{label}_url" in source:
                    fetch(source[f"{label}_url"], Path(scratch) / f"{name.replace('/', '-')}-{label}", source[f"{label}_sha256"])
            command = ["php", str(ROOT / parser["adapter"]), str(CONTROL), str(source_path)]
            output = json.loads(run(command))
            assert output == parser["expected_output"], (name, output)
            records.append({
                "package": name, "version": parser["version"], "control": parser["control"],
                "source_url": source["source_url"], "source_sha256": source["source_sha256"],
                "release_commit": source["release_commit"], "command": shlex.join(command),
                "output": output, "pass": True,
            })
            print(f"{name}@{parser['version']}: PHP ASCII PLY passed", flush=True)

    path = DATA / "verification.json"
    result = json.loads(path.read_text())
    previous = [row for row in result["third_party"] if row["package"] not in NAMES]
    result["third_party"] = previous + records
    result["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    result["platform"] = platform.platform()
    result["php"] = run(["php", "-v"]).splitlines()[0]
    result["note"] = ("This run reverified the Providence, Pawtucket2 and Heratio modules. Providence and Pawtucket2 "
                      "contain byte-identical PLY-to-STL classes and converted vertex and face rows using a no-op "
                      "Db.php include for an unused legacy dependency. Heratio parsed header element counts only. "
                      "The separately tested magdev/php-assimp 0.6.0 remains excluded.")
    result.setdefault("local_libraries", {}).update({name: {
        "source_sha256": LOCK[name]["source_sha256"],
        "release_commit": LOCK[name]["release_commit"],
    } for name in NAMES})
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    verify()
