"""Stage one npm parser as a pinned, coverage-traced Docker candidate.

The staged target is counted only after the container, AFL++ overlay, and
replay/feedback checks pass. The existing cell adapter supplies the parse API.
"""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "projects/pdf/javascript/pdf_lib"
BASE_IMAGE = "node@sha256:af02d57b57719b9657a45199a79264a9437940cd55b3c7b3fc99615654f124a0"


def registry_release(name: str, version: str) -> tuple[str, str, str]:
    encoded = urllib.parse.quote(name, safe="")
    with urllib.request.urlopen(f"https://registry.npmjs.org/{encoded}/{version}", timeout=20) as response:
        metadata = json.load(response)
    dist = metadata["dist"]
    url = dist["tarball"]
    with urllib.request.urlopen(url, timeout=30) as response:
        digest = sha256(response.read()).hexdigest()
    return url, digest, dist["integrity"]


def adapted_source(source: str) -> str:
    start = re.search(r"const \[name, (path|control)\] = process\.argv\.slice\(2\);", source)
    ending = re.search(r"console\.log\(JSON\.stringify\((result|output)\)\);\s*$", source)
    if not start or not ending:
        raise ValueError("cell adapter does not have the expected CLI shape")
    parameter = start.group(1)
    prefix = source[:start.start()]
    body = source[start.end():ending.start()]
    body = body.replace("join(process.cwd(), path)", "path")
    body = body.replace("../../node_modules/", "./node_modules/")
    return prefix + f"export async function parse(name, {parameter}) {{\n" + body + f"return {ending.group(1)};\n}}\n"


def stage(format_name: str, package: str) -> Path:
    parser_path = ROOT / "data/javascript" / format_name / "parsers.json"
    parser, = [entry for entry in json.loads(parser_path.read_text()) if entry["name"] == package]
    verification = json.loads((parser_path.parent / "verification.json").read_text())
    expected = parser.get("expected_output")
    if expected is None:
        records = verification.get("third_party", verification.get("results", []))
        record = next((item for item in records if item.get("package") == package), None)
        expected = record.get("output") if record and record.get("pass") else None
    if expected is None:
        raise ValueError("no saved expected output for package")
    records = verification.get("third_party", verification.get("results", []))
    record = next((item for item in records if item.get("package") == package), None)
    control = parser.get("control") or verification.get("control")
    if control is None and record and "controls" in verification:
        control = verification["controls"].get(record.get("scope"))
    if isinstance(control, dict):
        control = next(iter(control.values()))
    if not control or not (ROOT / control).is_file():
        raise ValueError("no saved valid control")
    slug = re.sub(r"[^a-z0-9]+", "_", package.lower()).strip("_")
    destination = ROOT / "projects" / format_name / "javascript" / slug
    if destination.exists() and json.loads((destination / "manifest.json").read_text()).get("package") != package:
        slug = "scoped_" + slug
        destination = ROOT / "projects" / format_name / "javascript" / slug
    if destination.exists():
        raise ValueError(f"project exists: {destination}")
    source = ROOT / "adapters/javascript" / f"{format_name}.mjs"
    adapter = adapted_source(source.read_text())
    url, source_sha, integrity = registry_release(package, parser["version"])
    releases = json.loads((parser_path.parent / "registry-snapshot.json").read_text())["releases"]
    if releases[package]["integrity"] != integrity:
        raise ValueError("npm release differs from saved registry snapshot")
    destination.mkdir(parents=True)
    (destination / "adapter.mjs").write_text(adapter)
    package_json = {"name": f"parsarium-{slug}-target", "private": True, "version": "0.1.0",
                    "dependencies": {package: parser["version"], "@jazzer.js/core": "4.0.0"}}
    (destination / "package.json").write_text(json.dumps(package_json, indent=2) + "\n")
    lock_command = ["docker", "run", "--rm", "--platform", "linux/arm64",
                    "--user", f"{os.getuid()}:{os.getgid()}", "-e", "NPM_CONFIG_CACHE=/tmp/npm-cache",
                    "-v", f"{destination}:/work", "-w", "/work", "--entrypoint", "npm",
                    "parsarium/png-javascript-pngjs:local", "install", "--package-lock-only",
                    "--ignore-scripts", "--no-audit", "--no-fund"]
    installed = subprocess.run(lock_command, capture_output=True, text=True, timeout=180)
    if installed.returncode:
        raise RuntimeError(f"npm lock failed: {installed.stderr[-1000:]}")
    lock = json.loads((destination / "package-lock.json").read_text())
    package_lock = lock["packages"][f"node_modules/{package}"]
    if package_lock["version"] != parser["version"] or package_lock["integrity"] != integrity:
        raise ValueError("npm lock differs from saved release")
    (destination / "source-lock.json").write_text(json.dumps({package: {
        "release": parser["version"], "source_sha256": source_sha,
        "npm_integrity": integrity}}, indent=2) + "\n")
    harness = f'''// Byte input reaches the documented {package} adapter branch.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {{ pathToFileURL }} = require('node:url');

async function parseData(data) {{
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20))
    throw new Error('input outside harness limit');
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'parsarium-'));
  const source = path.join(directory, 'input{Path(control).suffix}');
  try {{
    fs.writeFileSync(source, data);
    const {{ parse }} = await import(pathToFileURL('/work/adapter.mjs'));
    return await parse({json.dumps(package)}, source);
  }} finally {{ fs.rmSync(directory, {{ recursive: true, force: true }}); }}
}}
module.exports = {{ parseData }};
'''
    (destination / "harness.js").write_text(harness)
    (destination / "replay.js").write_text(
        "const fs = require('node:fs');\nconst { parseData } = require('./harness');\n"
        "parseData(fs.readFileSync(process.argv[2])).then(value => console.log(JSON.stringify(value)))\n"
        "  .catch(error => { console.error(error); process.exitCode = 1; });\n")
    (destination / "fuzz.js").write_text(
        "const { parseData } = require('./harness');\n"
        "module.exports.fuzz = async function fuzz(data) {\n"
        "  try { await parseData(data); }\n"
        "  catch (error) { if (!(error instanceof Error)) throw error; }\n"
        "};\n")
    control_script = (TEMPLATE / "run-control.js").read_text()
    control_script = re.sub(r"const expected = .*;", lambda _: "const expected = " + json.dumps(expected) + ";", control_script)
    control_script = control_script.replace("file:///work/node_modules/pdf-lib/cjs/",
                                            f"file:///work/node_modules/{package}/")
    control_script = control_script.replace("no pdf-lib package source lines covered",
                                            "no parser package source lines covered")
    control_script = control_script.replace("JSON.parse(child.stdout.trim())",
                                            "JSON.parse(child.stdout.trim().split('\\n').at(-1))")
    (destination / "run-control.js").write_text(control_script)
    docker = f'''FROM --platform=linux/arm64 {BASE_IMAGE} AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \\
    && curl --fail --location --retry 3 {url} --output /work/source.tgz \\
    && echo '{source_sha}  /work/source.tgz' | sha256sum --check
RUN {{ node --version; npm --version; npm ls {package} @jazzer.js/core --depth=0; }} > /work/toolchain.txt

FROM --platform=linux/arm64 {BASE_IMAGE}
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
'''
    (destination / "Dockerfile").write_text(docker)
    manifest = json.loads((TEMPLATE / "manifest.json").read_text())
    manifest.update({"format": format_name, "package": package, "release": parser["version"],
                     "catalog_parser": str(parser_path.relative_to(ROOT)),
                     "source_lock": str((destination / "source-lock.json").relative_to(ROOT)),
                     "source_sha256": source_sha, "control": control,
                     "control_sha256": sha256((ROOT / control).read_bytes()).hexdigest(),
                     "expected_output": expected, "coverage_subject_prefix": f"/work/node_modules/{package}/",
                     "coverage": "Node V8 source-range coverage of package files during valid-control replay; Jazzer.js instrumentation for fuzz entry",
                     "fuzz_smoke_args": ["/work/node_modules/@jazzer.js/core/dist/cli.js", "/work/fuzz.js",
                                         "--includes", f"/work/node_modules/{package}/", "--", "-help=1"],
                     "fuzz_smoke_expect": "Usage:"})
    manifest.pop("format_specific_coverage_file_suffix", None)
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return destination


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("package")
    args = cli.parse_args()
    print(stage(args.format, args.package).relative_to(ROOT))
