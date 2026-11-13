"""Compile the tagged Zathura PDF Poppler callback and parse a local PDF."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/c/pdf/source-lock.json"
CONTROL = ROOT / "controls/pdf/two-page.pdf"


def _fetch(url: str, target: Path, digest: str) -> None:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium Zathura PDF verifier"}), timeout=90) as response:
        target.write_bytes(response.read())
    assert sha256(target.read_bytes()).hexdigest() == digest


def _check_members(archive: Path, members: dict[str, str]) -> None:
    with tarfile.open(archive, "r:xz") as tar:
        for name, digest in members.items():
            member = tar.extractfile(name)
            assert member is not None and sha256(member.read()).hexdigest() == digest, name


def verify(parser=None, source=None, root=ROOT, cache=None, target=None):
    del cache, target
    source = source or json.loads(LOCK.read_text())["zathura-pdf-poppler"]
    parser = parser or {"name": "zathura-pdf-poppler", "version": source["release"],
                        "control": "controls/pdf/two-page.pdf",
                        "expected_output": {"pages": 2, "has_parser_data": True}}
    assert parser["version"] == source["release"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == source["control_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-zathura-poppler-pdf-") as folder:
        temp = Path(folder)
        plugin_archive = temp / "plugin.tar.xz"
        host_archive = temp / "host.tar.xz"
        _fetch(source["source_url"], plugin_archive, source["source_sha256"])
        _fetch(source["host_source_url"], host_archive, source["host_source_sha256"])
        _check_members(plugin_archive, source["source_members"])
        _check_members(host_archive, source["host_source_members"])

        with tarfile.open(host_archive, "r:xz") as tar:
            template = tar.extractfile("zathura-2026.07.18/zathura/version.h.in").read().decode()
            build = tar.extractfile("zathura-2026.07.18/meson.build").read().decode()
        assert "version: '2026.07.18'" in build
        assert "plugin_api_version = '8'" in build
        assert "plugin_abi_version = '9'" in build
        for marker, value in source["host_version_macros"].items():
            template = template.replace("@" + marker + "@", str(value))
        assert "@ZV" not in template
        (temp / "zathura-version.h").write_text(template)

        packages = source["ubuntu_packages"]
        apt_args = " ".join(shlex.quote(f"{name}={version}") for name, version in packages.items())
        checks = []
        for name, digest in source["apt_package_sha256"].items():
            package_version = shlex.quote(f"{name}={packages[name]}")
            checks.append(
                f'test "$(apt-cache show {package_version} | '
                f"awk '/^SHA256: / {{print $2; exit}}')\" = {shlex.quote(digest)}")
        build_command = (
            "cc -std=gnu2x -O2 -Wall -Wextra -Werror "
            "-I/pin -I/work/zathura-2026.07.18 "
            "-I/work/zathura-pdf-poppler-2026.07.18/zathura-pdf-poppler "
            "$(pkg-config --cflags girara poppler-glib cairo) "
            "/work/zathura-pdf-poppler-2026.07.18/zathura-pdf-poppler/document.c "
            "/repo/adapters/c/pdf/zathura_poppler.c "
            "$(pkg-config --libs girara poppler-glib cairo) -o /tmp/zathura-poppler-pdf"
        )
        shell = " && ".join([
            "set -eu",
            "apt-get update -qq >/dev/null",
            *checks,
            "DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends "
            + apt_args + " >/dev/null",
            "mkdir -p /work",
            "tar -xJf /pin/plugin.tar.xz -C /work",
            "tar -xJf /pin/host.tar.xz -C /work",
            build_command,
            "/tmp/zathura-poppler-pdf /repo/controls/pdf/two-page.pdf",
        ])
        command = ["docker", "run", "--rm", "--platform", "linux/arm64",
                   "-v", f"{temp}:/pin:ro", "-v", f"{root}:/repo:ro",
                   source["container_image"], "sh", "-lc", shell]
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=240)
        if result.returncode:
            raise RuntimeError(result.stderr or result.stdout)
        output = json.loads(result.stdout.strip())
        assert output == parser["expected_output"], output
        row = {"package": parser["name"], "version": parser["version"],
               "control": parser["control"], "output": output, "pass": True,
               "command": "python3 scripts/verify_zathura_poppler_c_pdf.py",
               "build_command": build_command,
               "checked_at_utc": datetime.now(timezone.utc).isoformat(),
               "environment": "Ubuntu 26.04 arm64 container; official plugin and matching host source archives; seven direct apt packages pinned by version and SHA-256",
               "underlying_family": "Zathura PDF Poppler plugin over Poppler GLib",
               "scope_limit": "Minimal host shim tests document_open; full viewer registration and rendering were not exercised."}
        library = {"source_sha256": source["source_sha256"],
                   "host_source_sha256": source["host_source_sha256"],
                   "container_image": source["container_image"],
                   "apt_package_sha256": source["apt_package_sha256"]}
        return row, library


if __name__ == "__main__":
    row, _library = verify()
    print(json.dumps(row))
