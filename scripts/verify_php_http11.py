"""Replay pinned PHP HTTP/1.1 parsers and the bundled CLI server on a valid request."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import socket
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/http11"
CONTROL = ROOT / "controls/http11/request.http"


def execute(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)


def lock_is_installed(path: Path, packages: list[dict]) -> bool:
    installed_path = path.parent / "vendor/composer/installed.json"
    autoload_path = path.parent / "vendor/autoload.php"
    if not installed_path.is_file() or not autoload_path.is_file():
        return False
    installed = {item["name"]: item for item in json.loads(installed_path.read_text())["packages"]}
    return all(
        (item := installed.get(package["name"])) is not None
        and item["version"] == package["version"]
        and item["source"]["reference"] == package["source"]["reference"]
        and (path.parent / "vendor" / package["name"]).is_dir()
        for package in packages
    )


def probe_cli_server() -> dict:
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    command = ["php", "-S", f"127.0.0.1:{port}",
               "adapters/php/http11/runtime_router.php"]
    process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
    try:
        response = b""
        for attempt in range(50):
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=2) as connection:
                    connection.sendall(CONTROL.read_bytes())
                    while chunk := connection.recv(8192):
                        response += chunk
                break
            except OSError:
                if attempt == 49:
                    raise
                time.sleep(0.05)
        head, separator, body = response.partition(b"\r\n\r\n")
        assert separator and head.startswith(b"HTTP/1.1 200 "), head
        return json.loads(body)
    finally:
        process.terminate()
        process.wait(timeout=5)


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    standard = json.loads((DATA / "standard.json").read_text())
    locks = {}
    for name in sorted({parser["composer_lock"] for parser in parsers}):
        path = ROOT / name
        packages = json.loads(path.read_text())["packages"]
        if not lock_is_installed(path, packages):
            execute(["composer", "install", "--no-interaction", "--no-progress", "--prefer-dist",
                     "--no-plugins", "--no-scripts", "--no-dev"], path.parent)
        locks[name] = {
            "packages": {package["name"]: package for package in packages},
            "sha256": sha256(path.read_bytes()).hexdigest(),
        }

    rows = []
    for parser in parsers:
        name = parser["name"]
        release = snapshot["releases"][name]
        lock = locks[parser["composer_lock"]]
        package = lock["packages"][name]
        assert parser["version"] == release["version"] == package["version"]
        assert package["source"]["reference"] == release["source_reference"]
        command = ["php", "-d", "display_errors=0", "-d", "log_errors=0",
                   str(ROOT / parser["adapter"]), name, str(ROOT / parser["control"])]
        output = json.loads(execute(command).stdout.strip())
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "composer_lock": parser["composer_lock"], "composer_lock_sha256": lock["sha256"],
                     "source_reference": release["source_reference"],
                     "control": parser["control"],
                     "control_sha256": sha256((ROOT / parser["control"]).read_bytes()).hexdigest(),
                     "command": " ".join(command), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: passed")

    runtime_api = standard["verified_apis"][0]
    runtime_output = probe_cli_server()
    assert runtime_output == runtime_api["expected_output"], runtime_output
    runtime = [{"name": runtime_api["name"], "control": runtime_api["control"],
                "control_sha256": sha256(CONTROL.read_bytes()).hexdigest(),
                "command": "php -S 127.0.0.1:<ephemeral-port> adapters/php/http11/runtime_router.php; send controls/http11/request.http on loopback socket",
                "output": runtime_output, "pass": True}]
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "php_version": execute(["php", "-r", "echo PHP_VERSION;"]).stdout,
              "composer_version": execute(["composer", "--version"]).stdout.strip(),
              "controls": [{"path": str(CONTROL.relative_to(ROOT)),
                            "sha256": sha256(CONTROL.read_bytes()).hexdigest()}],
              "composer_locks": [{"path": name, "sha256": lock["sha256"]}
                                 for name, lock in locks.items()],
              "third_party": rows, "runtime": runtime}
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(rows)}/{len(parsers)} PHP HTTP/1.1 paths passed; bundled server passed")


if __name__ == "__main__":
    main()
