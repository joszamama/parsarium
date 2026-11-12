"""Pin Java ASCII PNM releases, resolved Maven classpath, and adoption data."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha1, sha256
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
import json
import os
import subprocess
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/java/ascii_pnm"
ADAPTER = ROOT / "adapters/java/ascii_pnm"
REPOSITORY = Path.home() / ".m2/repository"


def get(url: str) -> bytes:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium Java PNM research"}), timeout=20) as response:
        return response.read()


def release(parser: dict) -> tuple[str, dict]:
    name, group, artifact, version = (parser[key] for key in ("name", "group", "artifact", "version"))
    base = f"https://repo.maven.apache.org/maven2/{group.replace('.', '/')}/{artifact}/{version}/"
    local = REPOSITORY / group.replace(".", "/") / artifact / version
    fields = {}
    for kind in ("jar", "pom"):
        filename = f"{artifact}-{version}.{kind}"
        blob = (local / filename).read_bytes()
        url = base + filename
        assert sha1(blob).hexdigest() == get(url + ".sha1").decode().strip(), (name, kind)
        fields[f"{kind}_url"] = url
        fields[f"{kind}_sha256"] = sha256(blob).hexdigest()
        if kind == "pom":
            ET.fromstring(blob)
    return name, {"group": group, "artifact": artifact, "version": version,
                  "license": parser["license"], **fields}


def metric(parser: dict) -> tuple[str, dict]:
    name, group, artifact, version = (parser[key] for key in ("name", "group", "artifact", "version"))
    package = quote(f"{group}:{artifact}", safe="")
    url = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{package}/versions/{version}:dependents"
    try:
        value = json.loads(get(url))["directDependentCount"]
        if not isinstance(value, int):
            raise ValueError("directDependentCount absent")
        return name, {"direct_dependent_count": value, "url": url}
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
        return name, {"direct_dependent_count": None, "url": url,
                      "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    with ThreadPoolExecutor(max_workers=5) as pool:
        releases = dict(pool.map(release, parsers))
        metrics = dict(pool.map(metric, parsers))
    snapshot["releases"] = releases
    snapshot["popularity_metric"] = {
        "name": "deps.dev version-level directDependentCount",
        "documentation": "https://docs.deps.dev/api/v3alpha/",
        "scope": "Known public direct dependents of the exact Maven release; incomplete coverage and version-age bias",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(), "packages": metrics}
    ffprobe = Path(os.environ.get("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin")) / "ffprobe"
    snapshot["external_tools"] = {"ffprobe": {
        "path": str(ffprobe),
        "version": subprocess.run([str(ffprobe), "-version"], text=True,
                                  capture_output=True, check=True).stdout.splitlines()[0],
        "sha256": sha256(ffprobe.read_bytes()).hexdigest()}}
    (DATA / "registry-snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    total_jars = 0
    for module in sorted({parser.get("adapter_module", "main") for parser in parsers}):
        directory = ADAPTER if module == "main" else ADAPTER / module
        jars = [Path(item) for item in (directory / "target/classpath.txt").read_text().strip().split(":")]
        lock = {"classpath": [{"repository_path": str(jar.relative_to(REPOSITORY)),
                                "sha256": sha256(jar.read_bytes()).hexdigest()} for jar in jars]}
        (directory / "dependencies.lock.json").write_text(json.dumps(lock, indent=2) + "\n")
        total_jars += len(jars)
    print(f"Pinned {len(releases)} releases and {total_jars} classpath JARs")


if __name__ == "__main__":
    main()
