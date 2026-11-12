"""Replay pinned PHP MP3/ID3v2 package adapters on the valid tagged control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/mp3_id3v2"
CONTROL = ROOT / "controls/mp3_id3v2/tone-tags.mp3"
LOCK = ROOT / "adapters/php/mp3_id3v2/composer.lock"


def execute(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    execute(["composer", "install", "--no-interaction", "--no-progress", "--prefer-dist",
             "--no-plugins", "--no-scripts", "--no-dev"], LOCK.parent)
    locked = {package["name"]: package for package in json.loads(LOCK.read_text())["packages"]}
    lock_sha = sha256(LOCK.read_bytes()).hexdigest()
    rows = []
    for parser in parsers:
        name = parser["name"]
        release = snapshot["releases"][name]
        package = locked[name]
        assert parser["version"] == release["version"] == package["version"]
        assert package["source"]["reference"] == release["source_reference"]
        command = ["php", "-d", "display_errors=0", "-d", "log_errors=0",
                   str(ROOT / parser["adapter"]), name, str(ROOT / parser["control"])]
        output = json.loads(execute(command).stdout.strip())
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "composer_lock": parser["composer_lock"], "composer_lock_sha256": lock_sha,
                     "source_reference": release["source_reference"],
                     "control": parser["control"], "command": " ".join(command),
                     "output": output, "pass": True})
        print(f"{name}@{parser['version']}: passed")

    probe_command = ["php", str(ROOT / "adapters/php/mp3_id3v2/runtime_probe.php"), str(CONTROL)]
    probe = json.loads(execute(probe_command).stdout.strip())
    assert probe == {"id3_extension_loaded": False, "id3_get_tag_exists": False,
                     "fileinfo_mime": "audio/mpeg"}
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "php_version": execute(["php", "-r", "echo PHP_VERSION;"]).stdout,
              "composer_version": execute(["composer", "--version"]).stdout.strip(),
              "control": "controls/mp3_id3v2/tone-tags.mp3",
              "control_sha256": sha256(CONTROL.read_bytes()).hexdigest(),
              "composer_lock": "adapters/php/mp3_id3v2/composer.lock",
              "composer_lock_sha256": lock_sha,
              "third_party": rows, "runtime": [],
              "runtime_probe": {"command": " ".join(probe_command),
                                "output": probe, "pass": True}}
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(rows)}/{len(parsers)} PHP MP3/ID3v2 paths passed")


if __name__ == "__main__":
    main()
