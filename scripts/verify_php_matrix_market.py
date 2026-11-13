"""Verify the tagged Tessero PHP Matrix Market reader on a valid local control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/matrix_market"
ADAPTER_DIR = ROOT / "adapters/php/matrix_market"
CONTROL = ROOT / "controls/matrix_market/real-general.mtx"


def run(command: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def main() -> None:
    parser, = json.loads((DATA / "parsers.json").read_text())
    source = json.loads((DATA / "source-lock.json").read_text())[parser["name"]]
    lock = json.loads((ADAPTER_DIR / "composer.lock").read_text())
    locked, = [item for item in lock["packages"] if item["name"] == parser["name"]]
    assert locked["version"] == parser["version"]
    assert locked["source"]["reference"] == source["source_reference"]
    assert locked["license"] == [parser["license"]]

    archive = Path(tempfile.gettempdir()) / "parsarium-tessero-v0.3.0.tar.gz"
    if not archive.exists() or sha256(archive.read_bytes()).hexdigest() != source["source_sha256"]:
        request = Request(source["source_url"], headers={"User-Agent": "Parsarium PHP Matrix Market verifier"})
        with urlopen(request, timeout=90) as response:
            archive.write_bytes(response.read())
    assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]
    with tarfile.open(archive) as tar:
        for member, expected in source["source_members"].items():
            file = tar.extractfile("tessero-0.3.0/" + member)
            assert file is not None and sha256(file.read()).hexdigest() == expected

    install = ["composer", "install", "--no-dev", "--prefer-dist", "--no-interaction", "--no-progress"]
    run(install, ADAPTER_DIR)
    for member, expected in source["source_members"].items():
        installed = ADAPTER_DIR / "vendor/tessero/tessero" / member
        if member.startswith("src/") or member == "composer.json" or member == "LICENSE":
            assert sha256(installed.read_bytes()).hexdigest() == expected

    assert sha256(CONTROL.read_bytes()).hexdigest() == source["control_sha256"]
    execute = ["php", str(ADAPTER_DIR / "tessero.php"), str(CONTROL)]
    output = json.loads(run(execute))
    assert output == parser["expected_output"], output
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"platform": platform.platform(), "php": run(["php", "-v"]).splitlines()[0],
                        "composer": run(["composer", "--version"]).splitlines()[0]},
        "control": parser["control"], "control_sha256": source["control_sha256"],
        "source_lock": "data/php/matrix_market/source-lock.json",
        "third_party": [{"package": parser["name"], "version": parser["version"],
                         "control": parser["control"], "install_command": shlex.join(install),
                         "command": shlex.join(execute), "output": output, "pass": True}],
        "runtime": [],
    }
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["third_party"][0]))


if __name__ == "__main__":
    main()
