"""Replay pinned PHP SVG adapters and bundled PHP 8.5 SVG size APIs."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/svg"
CONTROL = ROOT / "controls/svg/red-green.svg"
PHP = os.environ.get("PARSARIUM_PHP85", "php")


def run(command: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def installed_matches(lock_path: Path) -> bool:
    installed_path = lock_path.parent / "vendor/composer/installed.json"
    if not installed_path.is_file() or not (lock_path.parent / "vendor/autoload.php").is_file():
        return False
    installed = {p["name"]: p for p in json.loads(installed_path.read_text())["packages"]}
    for package in json.loads(lock_path.read_text())["packages"]:
        current = installed.get(package["name"])
        if current is None or current["version"] != package["version"]:
            return False
        if current["source"]["reference"] != package["source"]["reference"]:
            return False
    return True


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    standard = json.loads((DATA / "standard.json").read_text())
    locks = {}
    for name in sorted({parser["composer_lock"] for parser in parsers}):
        path = ROOT / name
        if not installed_matches(path):
            run(["composer", "install", "--no-interaction", "--no-progress",
                 "--prefer-dist", "--no-plugins", "--no-scripts", "--no-dev"], path.parent)
        locks[name] = {"sha256": sha256(path.read_bytes()).hexdigest(),
                       "packages": {p["name"]: p for p in json.loads(path.read_text())["packages"]}}

    rows = []
    for parser in parsers:
        name = parser["name"]
        lock = locks[parser["composer_lock"]]
        package = lock["packages"][name]
        assert package["version"] == parser["version"] == snapshot["releases"][name]["version"]
        assert package["source"]["reference"] == snapshot["releases"][name]["source_reference"]
        command = [PHP, "-d", "display_errors=0", "-d", "log_errors=0",
                   str(ROOT / parser["adapter"]), name, str(ROOT / parser["control"])]
        output = json.loads(run(command))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "composer_lock": parser["composer_lock"], "composer_lock_sha256": lock["sha256"],
                     "source_reference": package["source"]["reference"],
                     "control": parser["control"], "control_sha256": sha256(CONTROL.read_bytes()).hexdigest(),
                     "command": " ".join(command), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: passed")

    probe_command = [PHP, str(ROOT / "adapters/php/svg/runtime_probe.php"), str(CONTROL)]
    probe = json.loads(run(probe_command))
    assert probe["generic_xml_loaded"] is True and probe["generic_xml_node_type"] == "DOMElement"
    assert probe["gd_decoded"] is False
    runtime = []
    for name, key in [("getimagesize", "file_size"), ("getimagesizefromstring", "byte_size")]:
        api = next(api for api in standard["verified_apis"] if api["name"] == name)
        assert probe[key] == api["expected_output"], (name, probe[key])
        runtime.append({"name": name, "control": api["control"],
                        "command": " ".join(probe_command), "output": probe[key], "pass": True})
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "php_version": run([PHP, "-r", "echo PHP_VERSION;"]),
        "composer_version": run(["composer", "--version"]),
        "control": str(CONTROL.relative_to(ROOT)),
        "control_sha256": sha256(CONTROL.read_bytes()).hexdigest(),
        "composer_locks": [{"path": name, "sha256": lock["sha256"]} for name, lock in locks.items()],
        "third_party": rows,
        "runtime": runtime,
        "runtime_probe": {"command": " ".join(probe_command), "output": probe, "pass": True},
    }
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(rows)} third-party SVG paths and {len(runtime)} bundled PHP APIs passed")


if __name__ == "__main__":
    main()
