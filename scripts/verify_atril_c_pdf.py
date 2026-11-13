"""Verify Atril's tagged C document library against a valid local PDF."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE_LOCK = ROOT / "data/c/pdf/source-lock.json"
ADAPTER = ROOT / "adapters/c/pdf/atril.c"
CONTROL = ROOT / "controls/pdf/two-page.pdf"


def verify(parser=None, source=None, root=ROOT, cache=None, target=None):
    """Return the same result shape as the other C PDF verifiers."""
    del cache, target
    source = source or json.loads(SOURCE_LOCK.read_text())["atril"]
    parser = parser or {"name": "atril", "version": source["release"],
                        "control": "controls/pdf/two-page.pdf",
                        "expected_output": {"pages": 2}}
    assert sha256(CONTROL.read_bytes()).hexdigest() == source["control_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-atril-pdf-") as folder:
        archive = Path(folder) / "atril.tar.gz"
        with urlopen(Request(source["source_url"], headers={
                "User-Agent": "Parsarium Atril verifier"}), timeout=90) as response:
            archive.write_bytes(response.read())
        assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]
        with tarfile.open(archive, "r:gz") as tar:
            for member_name, expected in source["source_members"].items():
                member = tar.extractfile(member_name)
                assert member is not None and sha256(member.read()).hexdigest() == expected

        image = source["container_image"]
        packages = source["ubuntu_packages"]
        apt_args = " ".join(shlex.quote(f"{name}={version}") for name, version in
                            packages.items())
        checks = []
        for name, digest in source["apt_package_sha256"].items():
            package_version = f"{name}={packages[name]}"
            checks.append(
                f'test "$(apt-cache show {shlex.quote(package_version)} | '
                f"awk '/^SHA256: / {{print $2; exit}}')\" = {shlex.quote(digest)}")
        binary_checks = [
            f'test "$(sha256sum {shlex.quote(path)} | cut -d" " -f1)" = '
            f'{shlex.quote(digest)}'
            for path, digest in source["binary_sha256"].items()
        ]
        shell = " && ".join([
            "set -eu",
            "apt-get update -qq >/dev/null",
            *checks,
            "DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends "
            f"gcc pkg-config {apt_args} >/dev/null",
            *binary_checks,
            f'test "$(sha256sum {source["local_header"]} | cut -d" " -f1)" = '
            f'{source["local_header_sha256"]}',
            f'test "$(pkg-config --modversion {source["pkg_config"]})" = '
            f'{source["release"]}',
            f'gcc -std=c11 -O2 -Wall -Wextra -Werror '
            f'/src/{ADAPTER.relative_to(root)} -o /tmp/atril-pdf '
            f'$(pkg-config --cflags --libs {source["pkg_config"]})',
            f'/tmp/atril-pdf /src/{CONTROL.relative_to(root)}',
        ])
        command = ["docker", "run", "--rm", "--platform", "linux/arm64",
                   "-v", f"{root}:/src:ro", "-w", "/src", image,
                   "sh", "-lc", shell]
        result = subprocess.run(command, cwd=root, capture_output=True,
                                text=True, timeout=240, check=True)
        output = json.loads(result.stdout.strip())
        assert output == parser["expected_output"], output
        row = {"package": "atril", "version": parser["version"],
               "control": parser["control"], "output": output, "pass": True,
               "command": "python3 scripts/verify_atril_c_pdf.py",
               "build_command": "gcc -std=c11 -O2 -Wall -Wextra -Werror /src/adapters/c/pdf/atril.c -o /tmp/atril-pdf $(pkg-config --cflags --libs atril-document-1.5.0)"}
        library = {"source_sha256": source["source_sha256"],
                   "local_library_sha256": source["binary_sha256"][source["local_library"]],
                   "local_header_sha256": source["local_header_sha256"],
                   "pdf_backend_sha256": source["binary_sha256"][source["pdf_backend"]],
                   "container_image": image}
        return row, library


if __name__ == "__main__":
    row, _library = verify()
    print(json.dumps(row))
