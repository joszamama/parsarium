"""Replay the pinned PHP Assimp 0.3.2 ASCII PLY control."""

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
DATA = ROOT / "data/php/ascii_ply"
ADAPTER_DIR = ROOT / "adapters/php/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
SOURCE = json.loads((DATA / "source-lock.json").read_text())["magdev/php-assimp"]
PARSER = json.loads((DATA / "parsers.json").read_text())[0]
ARCHIVE = Path(os.environ.get("PARSARIUM_PHP_ASSIMP_ARCHIVE", str(Path(tempfile.gettempdir()) / "parsarium-php-assimp-0.3.2.tar.gz")))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def verify() -> None:
    assert digest(CONTROL) == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    assert digest(ADAPTER_DIR / "composer.json") == SOURCE["composer_json_sha256"]
    assert digest(ADAPTER_DIR / "composer.lock") == SOURCE["composer_lock_sha256"]
    locked = json.loads((ADAPTER_DIR / "composer.lock").read_text())["packages"]
    assert len(locked) == 1 and locked[0]["name"] == "magdev/php-assimp"
    assert locked[0]["version"] == SOURCE["release"]
    assert locked[0]["source"]["reference"] == SOURCE["release_commit"]
    if not ARCHIVE.exists() or digest(ARCHIVE) != SOURCE["source_sha256"]:
        with urlopen(Request(SOURCE["source_url"], headers={"User-Agent": "Parsarium ASCII PLY verifier"}), timeout=120) as response, ARCHIVE.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
    assert digest(ARCHIVE) == SOURCE["source_sha256"]
    with tarfile.open(ARCHIVE) as archive:
        for member, expected in SOURCE["source_members"].items():
            file = archive.extractfile(member)
            assert file is not None and sha256(file.read()).hexdigest() == expected, member
    install = ["composer", "install", f"--working-dir={ADAPTER_DIR}",
               "--no-dev", "--no-interaction", "--prefer-dist", "--no-progress"]
    run(install)
    vendor = ADAPTER_DIR / "vendor/magdev/php-assimp"
    for member, expected in SOURCE["source_members"].items():
        relative = member.removeprefix("php-assimp-0.3.2/")
        assert digest(vendor / relative) == expected, relative
    binary = Path(os.environ.get("PARSARIUM_ASSIMP_BIN", SOURCE["underlying_parser"]["installed_binary"]))
    assert digest(binary) == SOURCE["underlying_parser"]["binary_sha256"]
    execute = ["php", str(ROOT / PARSER["adapter"]), str(CONTROL)]
    output = json.loads(run(execute))
    assert output == PARSER["expected_output"], output
    result = json.loads((DATA / "verification.json").read_text())
    result.update({
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(), "php": run(["php", "-v"]).splitlines()[0],
        "composer": run(["composer", "--version"]).splitlines()[0],
        "source_lock": "data/php/ascii_ply/source-lock.json",
        "local_libraries": {"magdev/php-assimp": {
            "source_sha256": SOURCE["source_sha256"],
            "release_commit": SOURCE["release_commit"],
            "assimp_binary_sha256": SOURCE["underlying_parser"]["binary_sha256"]}},
        "third_party": [{"package": PARSER["name"], "version": PARSER["version"],
                         "control": PARSER["control"], "install_command": shlex.join(install),
                         "command": shlex.join(execute), "output": output, "pass": True}],
        "note": "The 0.3.2 PHP package passed through its local InfoVerb API over Assimp 6.0.6; the separately tested 0.6.0 release remains excluded."})
    (DATA / "verification.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("magdev/php-assimp@0.3.2: PHP ASCII PLY passed", flush=True)


if __name__ == "__main__":
    verify()
