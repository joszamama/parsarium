"""Build tagged Xreader libdocument and parse a valid local PDF through C."""

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
ADAPTER = ROOT / "adapters/c/pdf/xreader.c"


def verify(parser=None, source=None, root=ROOT, cache=None, target=None):
    del cache, target
    source = source or json.loads(LOCK.read_text())["xreader"]
    parser = parser or {"name": "xreader", "version": source["release"],
                        "control": "controls/pdf/two-page.pdf",
                        "expected_output": {"pages": 2}}
    assert sha256(CONTROL.read_bytes()).hexdigest() == source["control_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-xreader-pdf-") as folder:
        temp = Path(folder)
        archive = temp / "source.tar.gz"
        with urlopen(Request(source["source_url"], headers={
                "User-Agent": "Parsarium Xreader verifier"}), timeout=90) as response:
            archive.write_bytes(response.read())
        assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]
        with tarfile.open(archive, "r:gz") as tar:
            for member_name, expected in source["source_members"].items():
                member = tar.extractfile(member_name)
                assert member is not None and sha256(member.read()).hexdigest() == expected

        packages = source["build_dependency_versions"]
        apt_args = " ".join(shlex.quote(f"{name}={version}") for name, version in
                            packages.items())
        checks = []
        for name, digest in source["build_dependency_package_sha256"].items():
            package_version = f"{name}={packages[name]}"
            checks.append(
                f'test "$(apt-cache show {shlex.quote(package_version)} | '
                f"awk '/^SHA256: / {{print $2; exit}}')\" = {shlex.quote(digest)}")
        build_options = ["--prefix=/usr", "-Dps=false", "-Dtiff=false",
                         "-Dxps=false", "-Dkeyring=false", "-Dgtk_unix_print=false",
                         "-Dpreviewer=false", "-Dthumbnailer=false",
                         "-Dhelp_files=false", "-Dintrospection=false",
                         "-Denable_dbus=false"]
        shell = " && ".join([
            "set -eu",
            "apt-get update -qq >/dev/null",
            *checks,
            "DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends "
            f"{apt_args} >/dev/null",
            "mkdir -p /work",
            "tar -xzf /pin/source.tar.gz -C /work",
            "meson setup /build /work/xreader-master.mint27 "
            + " ".join(build_options) + " >/tmp/meson.log 2>&1",
            "meson compile -C /build -j4 >/tmp/build.log 2>&1",
            "meson install -C /build >/tmp/install.log 2>&1",
            f'test "$(pkg-config --modversion xreader-document-1.5)" = '
            f'{source["release"]}',
            f'gcc -std=c11 -O2 -Wall -Wextra -Werror '
            f'/repo/{ADAPTER.relative_to(root)} -o /tmp/xreader-pdf '
            '$(pkg-config --cflags --libs xreader-document-1.5)',
            f'/tmp/xreader-pdf /repo/{CONTROL.relative_to(root)}',
        ])
        command = ["docker", "run", "--rm", "--platform", "linux/arm64",
                   "-v", f"{temp}:/pin:ro", "-v", f"{root}:/repo:ro",
                   source["container_image"], "sh", "-lc", shell]
        result = subprocess.run(command, cwd=root, capture_output=True,
                                text=True, timeout=360, check=True)
        output = json.loads(result.stdout.strip())
        assert output == parser["expected_output"], output
        row = {"package": "xreader", "version": parser["version"],
               "control": parser["control"], "output": output, "pass": True,
               "command": "python3 scripts/verify_xreader_c_pdf.py",
               "build_command": "meson setup /build /work/xreader-master.mint27 --prefix=/usr -Dps=false -Dtiff=false -Dxps=false -Dkeyring=false -Dgtk_unix_print=false -Dpreviewer=false -Dthumbnailer=false -Dhelp_files=false -Dintrospection=false -Denable_dbus=false && meson compile -C /build -j4 && meson install -C /build && gcc -std=c11 -O2 -Wall -Wextra -Werror /repo/adapters/c/pdf/xreader.c -o /tmp/xreader-pdf $(pkg-config --cflags --libs xreader-document-1.5)"}
        library = {"source_sha256": source["source_sha256"],
                   "container_image": source["container_image"],
                   "source_commit": source["source_commit"],
                   "build_dependency_package_sha256": source["build_dependency_package_sha256"]}
        return row, library


if __name__ == "__main__":
    row, _library = verify()
    print(json.dumps(row))
