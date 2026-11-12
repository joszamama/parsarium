"""Verify pinned PHP package paths against the valid ASCII P3 PNM control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/ascii_pnm"
CONTROL = ROOT / "controls/ascii_pnm/red-green.ppm"


def execute(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    locks = sorted({parser["composer_lock"] for parser in parsers})
    locked = {}
    for name in locks:
        path = ROOT / name
        execute(["composer", "install", "--no-interaction", "--no-progress", "--prefer-dist",
                 "--no-plugins", "--no-scripts", "--no-dev"], path.parent)
        locked[name] = {entry["name"]: entry for entry in json.loads(path.read_text())["packages"]}

    rows = []
    for parser in parsers:
        name = parser["name"]
        lock = locked[parser["composer_lock"]][name]
        release = snapshot["releases"][name]
        assert parser["version"] == lock["version"] == release["version"]
        assert lock["source"]["reference"] == release["source_reference"]
        command = ["php", "-d", "ffi.enable=1", "-d", "zend.max_allowed_stack_size=-1",
                   "-d", "display_errors=0", "-d", "log_errors=0", "-d", "error_reporting=8191",
                   str(ROOT / parser["adapter"]), name, str(CONTROL)]
        run = execute(command)
        output = json.loads(run.stdout.strip())
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "composer_lock": parser["composer_lock"],
                     "composer_lock_sha256": sha256((ROOT / parser["composer_lock"]).read_bytes()).hexdigest(),
                     "source_reference": lock["source"]["reference"],
                     "control": parser["control"], "command": " ".join(command),
                     "output": output, "pass": True})
        print(f"{name}@{parser['version']}: passed")

    probe_command = ["php", str(ROOT / "adapters/php/ascii_pnm/runtime_probe.php"), str(CONTROL)]
    probe_output = json.loads(execute(probe_command).stdout)
    assert probe_output == {"getimagesize": False, "getimagesizefromstring": False,
                            "imagecreatefromstring": False}

    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "php_version": execute(["php", "-r", "echo PHP_VERSION;"]).stdout,
              "libvips_version": execute(["php", "-d", "ffi.enable=1", "-r",
                  "require 'adapters/php/ascii_pnm/vendor/autoload.php'; echo \\Jcupitt\\Vips\\Config::version();"]).stdout,
              "composer_version": execute(["composer", "--version"]).stdout.strip(),
              "control": "controls/ascii_pnm/red-green.ppm",
              "control_sha256": sha256(CONTROL.read_bytes()).hexdigest(),
              "composer_locks": [{"path": name, "sha256": sha256((ROOT / name).read_bytes()).hexdigest()}
                                 for name in locks],
              "third_party": rows, "runtime": [],
              "runtime_probe": {"command": " ".join(probe_command),
                                "output": probe_output, "pass": True}}
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(rows)}/{len(parsers)} PHP ASCII PNM paths passed")


if __name__ == "__main__":
    main()
