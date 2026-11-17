"""Stage a pinned Python wheel and locked dependencies as an individual Docker target.

This creates a candidate only. Run ``parsarium.py build`` and ``afl build`` before
counting it; failing candidates must be fixed or removed. The wheel hash must
already occur in the cell's committed requirements lock.
"""

import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import shutil
import tarfile
import urllib.request
import zipfile

from pip._vendor.packaging.markers import default_environment
from pip._vendor.packaging.requirements import Requirement


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "projects/png/python/imagesize"
SYSTEM_PACKAGES = {
    "cairosvg": "libcairo2", "pyvips": "libvips42t64", "audiofile": "libsndfile1", "soundfile": "libsndfile1",
    "ffmpeg-python": "ffmpeg", "ffmpegio": "ffmpeg",
    "pdf2image": "poppler-utils", "mahotas": "libfreeimage3",
    "pydub": "ffmpeg", "audioread": "ffmpeg", "pycord": "ffmpeg", "imageio": "ffmpeg", "pyqt6": "libglib2.0-0 libgl1 libegl1 libxkbcommon0 libfreetype6 libglib2.0-0 libfontconfig1 libx11-6 libxcb1 libxrender1 libxext6 libsm6 libice6",
    "pyside6": "libglib2.0-0 libgl1 libegl1 libxkbcommon0 libfreetype6 libglib2.0-0 libfontconfig1 libx11-6 libxcb1 libxrender1 libxext6 libsm6 libice6", "pyqt5": "libgl1 libegl1 libxkbcommon0 libfreetype6 libglib2.0-0 libfontconfig1 libx11-6 libxcb1 libxrender1 libxext6 libsm6 libice6",
    "librosa": "libsndfile1", "audiolab": "libsndfile1",
    "mpl-simple-svg-parser": "libcairo2", "pymeshlab": "libgl1", "pyassimp": "libassimp6=6.0.4+ds-1build1", "open3d": "libgl1 libegl1 libxkbcommon0 libfreetype6 libglib2.0-0 libfontconfig1 libx11-6 libxcb1 libxrender1 libxext6 libsm6 libice6",
}
EXTRA_DEPENDENCIES = {
    "pydub": ["audioop-lts"], "markitdown": ["pdfminer-six", "pdfplumber"],
    "pgm-reader": ["numpy", "matplotlib"], "resvglite": ["Pillow"], "av": ["numpy"],
    "assimp-py": ["numpy"], "pyassimp": ["numpy", "setuptools"], "imageio": ["imageio-ffmpeg"], "resvg-py": ["Pillow"], "mpl-simple-svg-parser": ["skia-python"],
    "music-tag": ["mutagen"], "scour": ["six", "lxml"],
    "pdfquery": ["chardet", "pdfminer-six", "pyquery", "six"], "pymp4": ["construct"],
}
WHEEL_URL = ("https://files.pythonhosted.org/packages/01/f9/"
             "575c8d760eae1fc99651b7cc5efd96ad5379ca4d6b53750b0fb4fe983f34/"
             "imagesize-2.0.1-py3-none-any.whl")
WHEEL_SHA = "ea0c9a0384df69ed86a943a15cde37d0360b82491b3910dc2215e202e62b5b02"


def normalized(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def locked_versions(text: str) -> dict[str, str]:
    return {normalized(name): version for name, version in
            re.findall(r"(?m)^([A-Za-z0-9_.-]+)==([^\s\\]+)", text)}


def pypi_release(name: str, version: str, lock_text: str) -> tuple[dict, list[str], list[str]]:
    address = f"https://pypi.org/pypi/{name}/{version}/json"
    with urllib.request.urlopen(address, timeout=20) as response:
        info = json.load(response)
    def compatible(item: dict) -> bool:
        filename = item["filename"]
        if not filename.endswith(".whl"):
            return False
        python_tag, abi, platform = filename[:-4].split("-")[-3:]
        python_ok = any((tag in {"py3", "py2.py3"} and abi == "none") or
                        (tag == "cp314" and abi == "cp314") or
                        (tag.startswith("cp3") and abi == "abi3" and int(tag[2:]) <= 314)
                        for tag in python_tag.split("."))
        platform_ok = platform == "any" or ("manylinux" in platform and "x86_64" in platform)
        return python_ok and platform_ok and item["digests"]["sha256"] in lock_text

    wheels = sorted((item for item in info["urls"] if compatible(item)),
                    key=lambda item: (not item["filename"].endswith("-none-any.whl"), item["filename"]))
    if not wheels:
        wheels = [item for item in info["urls"] if item["packagetype"] == "sdist"
                  and item["digests"]["sha256"] in lock_text]
    if not wheels:
        raise ValueError(f"no locked compatible Linux wheel or source archive for {name}=={version}")
    wheel = wheels[0]
    with urllib.request.urlopen(wheel["url"], timeout=30) as response:
        data = response.read()
    if sha256(data).hexdigest() != wheel["digests"]["sha256"]:
        raise ValueError("wheel digest differs from PyPI release metadata")
    if wheel["filename"].endswith(".whl"):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            metadata = next(path for path in archive.namelist() if path.endswith(".dist-info/METADATA"))
            dependencies = [line[15:] for line in archive.read(metadata).decode().splitlines()
                            if line.startswith("Requires-Dist: ")]
            modules = sorted({path.split("/")[0] for path in archive.namelist()
                              if path.endswith(".py") and ".dist-info/" not in path})
    else:
        dependencies = info["info"].get("requires_dist") or []
        if wheel["filename"].endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                names = archive.namelist()
        else:
            with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as archive:
                names = archive.getnames()
        candidates = []
        for path in names:
            parts = path.split("/")[1:]
            if not path.endswith(".py") or not parts:
                continue
            if parts[0] == "src":
                parts = parts[1:]
            if parts:
                candidates.append(parts[0])
        modules = sorted(set(candidates))
    environment = default_environment()
    environment.update({"extra": "", "python_version": "3.14",
                        "python_full_version": "3.14.4", "sys_platform": "linux",
                        "platform_system": "Linux", "platform_machine": "x86_64"})
    runtime_dependencies = [item for item in dependencies
                            if (Requirement(item).marker is None or
                                Requirement(item).marker.evaluate(environment))]
    return wheel, modules, runtime_dependencies


def stage(format_name: str, package: str) -> Path:
    catalog_path = ROOT / "data/python" / format_name / "parsers.json"
    parser, = [item for item in json.loads(catalog_path.read_text())
               if item["name"] == package]
    if "expected_output" not in parser:
        raise ValueError("this parser has no direct expected_output in the catalog")
    lock_path = ROOT / parser.get("environment_lock", f"adapters/python/{format_name}/requirements.lock")
    lock_text = lock_path.read_text()
    versions = locked_versions(lock_text)
    wheel, modules, requirements = pypi_release(package, parser["version"], lock_text)
    module_alias = {"pdfminer-six": "pdfminer", "python-archive": "archive"}.get(normalized(package))
    matches = [item for item in modules if normalized(item.removesuffix(".py")) == normalized(module_alias or package)]
    module = matches[0] if matches else (modules[0] if len(modules) == 1 else None)
    if module is None:
        raise ValueError(f"cannot infer parser source root: {modules}")
    digest = wheel["digests"]["sha256"]
    if versions.get(normalized(package)) != parser["version"] or digest not in lock_text:
        raise ValueError(f"wheel digest not in committed source lock: {package}")
    dependencies = {}
    pending = list(requirements) + EXTRA_DEPENDENCIES.get(normalized(package), [])
    while pending:
        requirement = Requirement(pending.pop())
        key = normalized(requirement.name)
        if key == normalized(package) or key in dependencies:
            continue
        version = versions.get(key)
        if not version or (requirement.specifier and not requirement.specifier.contains(version)):
            raise ValueError(f"dependency not resolved by committed lock: {requirement}")
        dependency_wheel, _, child_requirements = pypi_release(requirement.name, version, lock_text)
        dependency_sha = dependency_wheel["digests"]["sha256"]
        if dependency_sha not in lock_text:
            raise ValueError(f"dependency wheel digest absent from lock: {requirement.name}")
        dependencies[key] = (version, dependency_wheel)
        pending.extend(child_requirements)
    slug = re.sub(r"[^a-z0-9]+", "_", package.lower()).strip("_")
    destination = ROOT / "projects" / format_name / "python" / slug
    if destination.exists():
        raise ValueError(f"project exists: {destination}")
    control = ROOT / parser["control"]
    if not control.is_file():
        raise ValueError(f"missing control: {control}")
    adapter = ROOT / parser.get("adapter", f"adapters/python/{format_name}/main.py")
    if not adapter.is_file():
        raise ValueError(f"missing cell adapter: {adapter}")
    destination.mkdir(parents=True)
    for name in ("run-control.py", "fuzz.py"):
        shutil.copyfile(BASE / name, destination / name)
    (destination / "run-control.py").write_text(
        (destination / "run-control.py").read_text().replace("parse_png", "parse_data"))
    shutil.copyfile(adapter, destination / "adapter.py")
    docker = (BASE / "Dockerfile").read_text()
    docker = (docker.replace(WHEEL_URL, wheel["url"])
             .replace("imagesize-2.0.1-py3-none-any.whl", wheel["filename"])
             .replace(WHEEL_SHA, digest)
             .replace("pip show imagesize atheris", f"pip show {package} atheris")
             .replace("COPY harness.py fuzz.py run-control.py target.json /work/",
                      "COPY adapter.py harness.py fuzz.py run-control.py target.json /work/"))
    dependency_sdists = [item["filename"] for _, item in dependencies.values()
                         if not item["filename"].endswith(".whl")]
    if not wheel["filename"].endswith(".whl") or dependency_sdists:
        docker = docker.replace("ca-certificates curl python3 python3-venv \\",
                                "ca-certificates curl python3 python3-venv python3-setuptools python3-wheel \\")
        docker = docker.replace("python3 -m venv /opt/venv", "python3 -m venv --system-site-packages /opt/venv")
    if dependency_sdists:
        installer = " \\\n".join(
            f"    && /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps /work/wheels/{name}"
            for name in dependency_sdists)
        docker = docker.replace("/opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl",
                                "/opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \\\n" + installer)
    if not wheel["filename"].endswith(".whl"):
        docker = docker.replace("/opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl",
                                f"/opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \\\n    && /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps /work/wheels/{wheel['filename']}")
    if normalized(package) in SYSTEM_PACKAGES:
        docker = docker.replace("libstdc++6 python3 && rm -rf /var/lib/apt/lists/*",
                                f"libstdc++6 python3 {SYSTEM_PACKAGES[normalized(package)]} && rm -rf /var/lib/apt/lists/*")
    if dependencies:
        lines = []
        for key, (_, item) in sorted(dependencies.items()):
            name = item["filename"]
            lines += [f"    && curl --fail --location --retry 3 {item['url']} --output /work/wheels/{name} \\",
                      f"    && echo '{item['digests']['sha256']}  /work/wheels/{name}' | sha256sum --check \\"]
        marker = ("    && python3 -m venv " + ("--system-site-packages " if not wheel["filename"].endswith(".whl") or dependency_sdists else "") + "/opt/venv " + chr(92) + "\n")
        if marker not in docker:
            raise ValueError("base Dockerfile install marker changed")
        docker = docker.replace(marker, "\n".join(lines) + "\n" + marker)
    if normalized(package) == "librosa":
        docker = docker.replace("WORKDIR /work", "ENV NUMBA_CACHE_DIR=/tmp/numba-cache NUMBA_DISABLE_JIT=1\nWORKDIR /work")
    (destination / "Dockerfile").write_text(docker)
    entry = ("adapter.run" if format_name in {"png", "zip", "wav", "ascii_pnm"}
             else "adapter.parse")
    argument = ("data" if format_name == "http11" else
                "source.name" if normalized(package) in {"audiomath", "pyntcloud", "assimp-py", "pymeshlab", "pyassimp"} else "Path(source.name)")
    body = f'''"""Byte-input harness for {package} {parser['version']} on {format_name}."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix="{control.suffix}") as source:
        source.write(data)
        source.flush()
        return {entry}({package!r}, {argument})


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
'''
    (destination / "harness.py").write_text(body)
    prefix = f"/opt/venv/lib/python3.14/site-packages/{module}"
    if not module.endswith(".py"):
        prefix += "/"
    manifest = json.loads((BASE / "manifest.json").read_text())
    manifest.update({"format": format_name, "package": package,
                     "release": parser["version"],
                     "catalog_parser": str(catalog_path.relative_to(ROOT)),
                     "source_lock": str(lock_path.relative_to(ROOT)),
                     "source_sha256": digest, "control": parser["control"],
                     "control_sha256": sha256(control.read_bytes()).hexdigest(),
                     "expected_output": parser["expected_output"],
                     "coverage_subject_prefix": prefix})
    if dependencies:
        manifest["dependencies"] = [
            {"package": key, "release": version,
             "sha256": item["digests"]["sha256"]}
            for key, (version, item) in sorted(dependencies.items())]
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (destination / "target.json").write_text(json.dumps({
        "expected_output": manifest["expected_output"],
        "coverage_subject_prefix": prefix}, indent=2) + "\n")
    return destination


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("package")
    args = cli.parse_args()
    print(stage(args.format, args.package).relative_to(ROOT))
