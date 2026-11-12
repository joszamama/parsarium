"""Replay pinned PHP SVG adapters and bundled PHP 8.5 SVG size APIs."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import subprocess
from build_php_imagick import build as build_imagick


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/svg"
CONTROL = ROOT / "controls/svg/red-green.svg"
PHP = os.environ.get("PARSARIUM_PHP85", "php")
PHP74 = os.environ.get("PARSARIUM_PHP74", "/opt/homebrew/opt/php@7.4/bin/php")


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
    if any(p["name"] == "choowx/rasterize-svg" for p in parsers):
        expected_sharp = json.loads((ROOT / "package-lock.json").read_text())["packages"]["node_modules/sharp"]["version"]
        sharp_file = ROOT / "node_modules/sharp/package.json"
        if not sharp_file.is_file() or json.loads(sharp_file.read_text())["version"] != expected_sharp:
            run(["npm", "ci"])
    imagick_extension = build_imagick() if any(
        p["name"] == "bitandblack/image-information" for p in parsers) else None
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
        executable = PHP74 if name == "t3g/svg-sanitize-elts7" else PHP
        command = [executable, "-d", "display_errors=0", "-d", "log_errors=0"]
        if name == "bitandblack/image-information":
            command += ["-d", f"extension={imagick_extension}"]
        command += [str(ROOT / parser["adapter"])]
        if name != "t3g/svg-sanitize-elts7":
            command += [name]
        command += [str(ROOT / parser["control"])]
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
        "legacy_php_version": run([PHP74, "-r", "echo PHP_VERSION;"]),
        "composer_version": run(["composer", "--version"]),
        "rsvg_convert_version": run(["rsvg-convert", "--version"]).splitlines()[0],
        "sharp_version": json.loads((ROOT / "node_modules/sharp/package.json").read_text())["version"],
        "imagick_extension_source_lock": "data/php/ascii_pnm/pecl-imagick-lock.json",
        "imagick_extension_sha256": sha256(imagick_extension.read_bytes()).hexdigest() if imagick_extension else None,
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
