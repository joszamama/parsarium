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
import urllib.request
import zipfile

from pip._vendor.packaging.markers import default_environment
from pip._vendor.packaging.requirements import Requirement


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "projects/png/python/imagesize"
WHEEL_URL = ("https://files.pythonhosted.org/packages/01/f9/"
             "575c8d760eae1fc99651b7cc5efd96ad5379ca4d6b53750b0fb4fe983f34/"
             "imagesize-2.0.1-py3-none-any.whl")
WHEEL_SHA = "ea0c9a0384df69ed86a943a15cde37d0360b82491b3910dc2215e202e62b5b02"


def normalized(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def locked_versions(text: str) -> dict[str, str]:
    return {normalized(name): version for name, version in
            re.findall(r"(?m)^([A-Za-z0-9_.-]+)==([^\s\\]+)", text)}


def pypi_release(name: str, version: str) -> tuple[dict, list[str], list[str]]:
    address = f"https://pypi.org/pypi/{name}/{version}/json"
    with urllib.request.urlopen(address, timeout=20) as response:
        info = json.load(response)
    universal = [item for item in info["urls"] if item["filename"].endswith(
        ("-py3-none-any.whl", "-py2.py3-none-any.whl"))]
    linux = [item for item in info["urls"] if item["filename"].endswith(".whl")
             and "-cp314-cp314-" in item["filename"] and "manylinux" in item["filename"]
             and "x86_64" in item["filename"]]
    wheels = universal or linux
    if len(wheels) != 1:
        raise ValueError(f"expected one compatible wheel for {name}=={version}, found {len(wheels)}")
    wheel = wheels[0]
    if wheel["size"] > 30_000_000:
        raise ValueError(f"wheel exceeds 30 MB staging limit: {wheel['filename']}")
    with urllib.request.urlopen(wheel["url"], timeout=30) as response:
        data = response.read()
    if sha256(data).hexdigest() != wheel["digests"]["sha256"]:
        raise ValueError("wheel digest differs from PyPI release metadata")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        metadata = next(path for path in archive.namelist() if path.endswith(".dist-info/METADATA"))
        dependencies = [line[15:] for line in archive.read(metadata).decode().splitlines()
                        if line.startswith("Requires-Dist: ")]
        environment = default_environment()
        environment.update({"extra": "", "python_version": "3.14",
                            "python_full_version": "3.14.4", "sys_platform": "linux",
                            "platform_system": "Linux", "platform_machine": "x86_64"})
        runtime_dependencies = [item for item in dependencies
                                if (Requirement(item).marker is None or
                                    Requirement(item).marker.evaluate(environment))]
        modules = sorted({path.split("/")[0] for path in archive.namelist()
                          if path.endswith(".py") and ".dist-info/" not in path})
    return wheel, modules, runtime_dependencies


def stage(format_name: str, package: str) -> Path:
    catalog_path = ROOT / "data/python" / format_name / "parsers.json"
    parser, = [item for item in json.loads(catalog_path.read_text())
               if item["name"] == package]
    if "expected_output" not in parser:
        raise ValueError("this parser has no direct expected_output in the catalog")
    lock_path = ROOT / "adapters/python" / format_name / "requirements.lock"
    lock_text = lock_path.read_text()
    versions = locked_versions(lock_text)
    wheel, modules, requirements = pypi_release(package, parser["version"])
    if len(modules) != 1:
        raise ValueError(f"cannot infer one parser source root: {modules}")
    module = modules[0]
    digest = wheel["digests"]["sha256"]
    if versions.get(normalized(package)) != parser["version"] or digest not in lock_text:
        raise ValueError(f"wheel digest not in committed source lock: {package}")
    dependencies = {}
    pending = list(requirements)
    while pending:
        requirement = Requirement(pending.pop())
        key = normalized(requirement.name)
        if key == normalized(package) or key in dependencies:
            continue
        version = versions.get(key)
        if not version or (requirement.specifier and not requirement.specifier.contains(version)):
            raise ValueError(f"dependency not resolved by committed lock: {requirement}")
        dependency_wheel, _, child_requirements = pypi_release(requirement.name, version)
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
    adapter = ROOT / "adapters/python" / format_name / "main.py"
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
    if dependencies:
        lines = []
        for key, (_, item) in sorted(dependencies.items()):
            name = item["filename"]
            lines += [f"    && curl --fail --location --retry 3 {item['url']} --output /work/wheels/{name} \\",
                      f"    && echo '{item['digests']['sha256']}  /work/wheels/{name}' | sha256sum --check \\"]
        marker = "    && python3 -m venv /opt/venv \\\n"
        if marker not in docker:
            raise ValueError("base Dockerfile install marker changed")
        docker = docker.replace(marker, "\n".join(lines) + "\n" + marker)
    (destination / "Dockerfile").write_text(docker)
    entry = ("adapter.run" if format_name in {"png", "zip", "wav", "ascii_pnm"}
             else "adapter.parse")
    argument = "data" if format_name == "http11" else "Path(source.name)"
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
