"""Rebuild and run SHA-locked Java PDF adapters on the valid one-page control.

Requires JDK 25, Maven 3.9+, macOS arm64, and network access on first run for
PDF Clown's pinned SourceForge release. JDK 25 runs the two FFM PDFium bindings
and the current SAMBox release. The adapter observes only control page count.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import json
import os
import platform
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/pdf"
DATA = ROOT / "data/java/pdf"
CONTROL = ROOT / "controls/pdf/one-page.pdf"
CONTROL_SHA256 = "9bbfad1ba7ac5d0f4e25dd1d2e00c9f4cc7a493e303034b5884759f42ec5f60a"
JAVA_HOME = Path(os.environ.get("PARSARIUM_JAVA25_HOME", "/opt/homebrew/opt/openjdk@25"))
MODULES = ("main", "icepdf8", "jpod_original", "ffm", "jpdfium")


def read(path: Path):
    return json.loads(path.read_text())


def version(command: list[str], env: dict[str, str] | None = None) -> str:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=True, env=env).stdout.strip()


def check_control() -> None:
    encoded = CONTROL.read_bytes()
    assert sha256(encoded).hexdigest() == CONTROL_SHA256
    assert encoded.startswith(b"%PDF-1.4\n") and encoded.endswith(b"%%EOF\n")
    assert b"/Type /Pages /Kids [3 0 R] /Count 1" in encoded
    assert b"(Parsarium) Tj" in encoded
    xref = int(encoded.split(b"startxref\n")[-1].split(b"\n")[0])
    assert encoded[xref:xref+5] == b"xref\n"


def build_module(name: str) -> tuple[str, int]:
    module = ADAPTER / (name if name != "main" else "")
    env = java25_environment()
    result = subprocess.run([
        "mvn", "-q", "-DskipTests", "package",
        "org.apache.maven.plugins:maven-dependency-plugin:3.8.1:build-classpath",
        "-Dmdep.outputFile=target/classpath.txt",
    ], cwd=module, env=env, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"Maven build failed for {name}:\n{result.stdout}\n{result.stderr}")
    repository = Path.home() / ".m2/repository"
    jars = [Path(item) for item in (module / "target/classpath.txt").read_text().strip().split(":")]
    actual = [{"repository_path": str(jar.relative_to(repository)),
               "sha256": sha256(jar.read_bytes()).hexdigest()} for jar in jars]
    lock = read(module / "dependencies.lock.json")["classpath"]
    if actual != lock:
        raise AssertionError(f"Resolved classpath differs from SHA lock: {name}")
    return str(module / "target/classes") + ":" + ":".join(str(jar) for jar in jars), len(jars)


def java25_environment() -> dict[str, str]:
    return {**os.environ, "JAVA_HOME": str(JAVA_HOME),
            "PATH": str(JAVA_HOME / "bin") + os.pathsep + os.environ["PATH"]}


def check_releases(snapshot: dict) -> None:
    repository = Path.home() / ".m2/repository"
    for name, release in {**snapshot["releases"], **snapshot["native_releases"]}.items():
        group, artifact, ver = (release[k] for k in ("group", "artifact", "version"))
        base = repository / group.replace(".", "/") / artifact / ver
        stem = f"{artifact}-{ver}" + (f"-{release['classifier']}" if release["classifier"] else "")
        assert sha256((base / f"{stem}.jar").read_bytes()).hexdigest() == release["jar_sha256"], name
        assert sha256((base / f"{artifact}-{ver}.pom").read_bytes()).hexdigest() == release["pom_sha256"], name


def fetch_pdfclown(snapshot: dict) -> str:
    release = snapshot["non_maven_release"]["pdfclown"]
    cache = Path.home() / ".cache/parsarium/java/pdf/pdfclown"
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / "PDFClown-0.1.2-Beta.zip"
    if not archive.exists() or sha256(archive.read_bytes()).hexdigest() != release["archive_sha256"]:
        with urlopen(release["url"], timeout=120) as response:
            archive.write_bytes(response.read())
    assert sha256(archive.read_bytes()).hexdigest() == release["archive_sha256"]
    jar = cache / "pdfclown.jar"
    with ZipFile(BytesIO(archive.read_bytes())) as zipped:
        jar.write_bytes(zipped.read(release["jar_entry"]))
    assert sha256(jar.read_bytes()).hexdigest() == release["jar_sha256"]
    classes = ADAPTER / "pdfclown/target/classes"
    classes.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(JAVA_HOME / "bin/javac"), "-cp", str(jar), "-d", str(classes),
                    str(ADAPTER / "pdfclown/PdfClownAdapter.java")], check=True)
    return str(classes) + ":" + str(jar)


def main() -> None:
    parsers = read(DATA / "parsers.json")
    snapshot = read(DATA / "registry-snapshot.json")
    assert len(parsers) == 20 and len({(p["group"], p["artifact"]) for p in parsers}) == 20
    assert platform.system() == "Darwin" and platform.machine() == "arm64"
    check_control()
    classpaths, counts = {}, {}
    for name in MODULES:
        classpaths[name], counts[name] = build_module(name)
    check_releases(snapshot)
    classpaths["pdfclown"] = fetch_pdfclown(snapshot)
    java = str(JAVA_HOME / "bin/java")
    classes = {"main": "org.parsarium.PdfAdapter", "ffm": "org.parsarium.FfmPdfAdapter",
               "jpdfium": "org.parsarium.JPdfiumAdapter", "icepdf8": "org.parsarium.IcePdf8Adapter",
               "jpod_original": "org.parsarium.JPodOriginalAdapter",
               "pdfclown": "org.parsarium.PdfClownAdapter"}
    third_party = []
    for parser in parsers:
        name, module = parser["name"], parser["adapter_module"]
        flags = (["--enable-preview", "--enable-native-access=ALL-UNNAMED"]
                 if module in ("ffm", "jpdfium") else [])
        args = ([name] if module in ("main", "ffm") else [])
        command = [java, "-Djava.awt.headless=true", *flags, "-cp", classpaths[module],
                   classes[module], *args, str(CONTROL)]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        try:
            output = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            output = None
        passed = result.returncode == 0 and output == parser["expected_output"]
        row = {"package": name, "version": parser["version"],
               "adapter_module": module, "control": parser["control"],
               "output": output, "pass": passed, "exit_code": result.returncode,
               "command": f"java -Djava.awt.headless=true {' '.join(flags)} -cp <locked {module} classpath> {classes[module]} {' '.join(args)} {parser['control']}".replace("  ", " ")}
        if result.stderr and not passed:
            row["stderr"] = result.stderr[-2000:]
        third_party.append(row)
    results = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"java": version([java, "-version"]),
                        "maven": version(["mvn", "-version"], env=java25_environment()),
                        "os": platform.platform(), "arch": platform.machine(),
                        "locked_classpath_jars_by_module": counts},
        "control_sha256": CONTROL_SHA256,
        "control_meaning": "Valid one-page PDF 1.4 with Helvetica Parsarium text, page tree count 1, xref, trailer and EOF",
        "third_party": third_party,
        "runtime": [],
    }
    (DATA / "verification.json").write_text(json.dumps(results, indent=2) + "\n")
    passed = sum(row["pass"] for row in third_party)
    print(f"{passed}/{len(third_party)} Java PDF packages passed; 0 documented JDK parser APIs")
    if passed != len(third_party):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
