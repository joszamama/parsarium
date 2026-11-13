"""Verify LibreOfficeKit's C PDF import from a pinned official macOS release."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import shlex
import subprocess
import tempfile


def digest(path: Path) -> str:
    check = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            check.update(chunk)
    return check.hexdigest()


def run(command: list[str], timeout: int = 240) -> str:
    result = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def download(url: str, path: Path, expected: str) -> None:
    if not path.exists() or digest(path) != expected:
        path.parent.mkdir(parents=True, exist_ok=True)
        partial = path.with_suffix(path.suffix + ".part")
        with urlopen(Request(url, headers={"User-Agent": "Parsarium LibreOfficeKit PDF verifier"}), timeout=180) as source, partial.open("wb") as output:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                output.write(chunk)
        assert digest(partial) == expected, url
        partial.replace(path)
    assert digest(path) == expected, path


def verify(parser: dict, source: dict, root: Path, cache: Path, target: Path) -> tuple[dict, dict]:
    assert platform.system() == "Darwin" and platform.machine() == "arm64"
    control = root / parser["control"]
    assert digest(control) == source["control_sha256"]
    distribution = cache / "libreofficekit-26.8.3.dmg"
    download(source["distribution_url"], distribution, source["distribution_sha256"])

    include = cache / "libreofficekit-26.8.3.1-include" / "LibreOfficeKit"
    for name, expected in source["headers"].items():
        download(source["header_base_url"] + name, include / name, expected)

    target.mkdir(parents=True, exist_ok=True)
    build = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
             "-I" + str(include.parent), str(root / parser["adapter"]),
             "-ldl", "-o", str(target / "libreofficekit")]
    run(build)
    with tempfile.TemporaryDirectory(prefix="parsarium-lok-pdf-") as temporary:
        temporary_path = Path(temporary)
        mountpoint = temporary_path / "mount"
        mountpoint.mkdir()
        run(["hdiutil", "attach", "-readonly", "-nobrowse", "-mountpoint",
             str(mountpoint), str(distribution)])
        try:
            app = mountpoint / "LibreOffice.app" / "Contents"
            binary = app / "MacOS" / "soffice"
            assert run([str(binary), "--version"]) == source["binary_version_string"]
            library = app / "Frameworks" / "libmergedlo.dylib"
            assert digest(library) == source["library_sha256"]
            assert digest(app / "MacOS" / "xpdfimport") == source["xpdfimport_sha256"]
            profile = temporary_path / "profile"
            execute = [str(target / "libreofficekit"), str(control),
                       str(app / "Frameworks"), profile.as_uri()]
            output = json.loads(run(execute))
            assert output == parser["expected_output"], output
        finally:
            run(["hdiutil", "detach", str(mountpoint)])
    row = {"package": parser["name"], "version": parser["version"],
           "control": parser["control"], "build_command": shlex.join(build),
           "command": shlex.join(execute), "output": output, "pass": True}
    library_record = {"distribution_sha256": source["distribution_sha256"],
                      "source_commit": source["source_commit"],
                      "library_sha256": source["library_sha256"],
                      "xpdfimport_sha256": source["xpdfimport_sha256"],
                      "header_sha256": source["headers"],
                      "control_sha256": source["control_sha256"]}
    return row, library_record
