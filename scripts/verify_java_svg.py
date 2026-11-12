"""Replay pinned Java SVG adapters on the valid red/green local control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import os
import json
import platform
import subprocess
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/svg"
DATA = ROOT / "data/java/svg"
CONTROL = ROOT / "controls/svg/red-green.svg"


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True, timeout=120)


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    root = ET.parse(CONTROL).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    assert root.tag == ns + "svg" and root.attrib["width"] == "2" and root.attrib["height"] == "1"
    assert [r.attrib["fill"] for r in root.findall(ns + "rect")] == ["#ff0000", "#00ff00"]
    control_sha256 = sha256(CONTROL.read_bytes()).hexdigest()

    repository = Path.home() / ".m2/repository"
    module_jars = {}
    module_paths = {parser.get("adapter_module", "main") for parser in parsers}
    for module in sorted(module_paths):
        directory = ADAPTER if module == "main" else ADAPTER / module
        run(["mvn", "-q", "-DskipTests", "package",
             "org.apache.maven.plugins:maven-dependency-plugin:3.8.1:build-classpath",
             "-Dmdep.outputFile=target/classpath.txt"], directory)
        lock = json.loads((directory / "dependencies.lock.json").read_text())["classpath"]
        jars = [Path(item) for item in (directory / "target/classpath.txt").read_text().strip().split(":")]
        actual = [{"repository_path": str(jar.relative_to(repository)),
                   "sha256": sha256(jar.read_bytes()).hexdigest()} for jar in jars]
        assert actual == lock, f"Resolved Maven {module} classpath differs from lock"
        module_jars[module] = jars
    for parser in parsers:
        release = snapshot["releases"][parser["name"]]
        assert (parser["group"], parser["artifact"], parser["version"]) == (
            release["group"], release["artifact"], release["version"])
        stem = f"{parser['artifact']}-{parser['version']}"
        path = f"{parser['group'].replace('.', '/')}/{parser['artifact']}/{parser['version']}/{stem}.jar"
        jars = module_jars[parser.get("adapter_module", "main")]
        by_path = {str(jar.relative_to(repository)): sha256(jar.read_bytes()).hexdigest() for jar in jars}
        assert by_path[path] == release["jar_sha256"]
        pom = repository / path.replace(".jar", ".pom")
        assert sha256(pom.read_bytes()).hexdigest() == release["pom_sha256"]

    rows = []
    for parser in parsers:
        label = parser["adapter_label"]
        module = parser.get("adapter_module", "main")
        directory = ADAPTER if module == "main" else ADAPTER / module
        classpath = str(directory / "target/classes") + ":" + ":".join(str(jar) for jar in module_jars[module])
        if module == "jairo":
            java25 = Path(os.environ.get("PARSARIUM_JAVA25_HOME", "/opt/homebrew/opt/openjdk@25")) / "bin/java"
            command = [str(java25), "-Djava.awt.headless=true", "-cp", classpath,
                       "org.parsarium.JairoSvgAdapter", str(CONTROL)]
            display = f"{java25} -Djava.awt.headless=true -cp <locked jairo classpath> org.parsarium.JairoSvgAdapter {parser['control']}"
        elif module == "vips":
            java27 = Path(os.environ.get("PARSARIUM_JAVA27_HOME", "/opt/homebrew/opt/openjdk")) / "bin/java"
            command = [str(java27), "--enable-native-access=ALL-UNNAMED",
                       "-Djava.awt.headless=true", "-cp", classpath,
                       "org.parsarium.VipsSvgAdapter", str(CONTROL)]
            display = f"{java27} --enable-native-access=ALL-UNNAMED -Djava.awt.headless=true -cp <locked vips classpath> org.parsarium.VipsSvgAdapter {parser['control']}"
        elif module == "echosvg":
            command = ["java", "-Djava.awt.headless=true", "-cp", classpath,
                       "org.parsarium.EchoSvgAdapter", label, str(CONTROL)]
            display = f"java -Djava.awt.headless=true -cp <locked echosvg classpath> org.parsarium.EchoSvgAdapter {label} {parser['control']}"
        else:
            command = ["java", "-Djava.awt.headless=true", "-cp", classpath,
                       "org.parsarium.SvgAdapter", label, str(CONTROL)]
            display = f"java -Djava.awt.headless=true -cp <locked classpath> org.parsarium.SvgAdapter {label} {parser['control']}"
        result = run(command)
        output = json.loads(result.stdout.strip())
        assert output == parser["expected_output"], (label, output)
        rows.append({"package": parser["name"], "version": parser["version"],
                     "control": parser["control"], "output": output, "pass": True,
                     "command": display})
        print(f"{label}: passed")

    target = ADAPTER / "target/runtime"
    target.mkdir(parents=True, exist_ok=True)
    run(["javac", "--release", "21", "-d", str(target),
         str(ADAPTER / "runtime/JdkSvgProbe.java")])
    command = ["java", "-Djava.awt.headless=true", "-cp", str(target),
               "JdkSvgProbe", str(CONTROL)]
    runtime_output = json.loads(run(command).stdout.strip())
    assert runtime_output == {"svg_readers": 0, "imageio_result": None}
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "environment": {"java": run(["java", "-version"]).stderr.strip(),
                              "maven": run(["mvn", "-version"]).stdout.splitlines()[0],
                              "platform": platform.platform(),
                              "classpath_jars": {module: len(jars) for module, jars in module_jars.items()}},
              "control": "controls/svg/red-green.svg", "control_sha256": control_sha256,
              "control_meaning": "Valid 2x1 SVG with red and green unit rectangles",
              "third_party": rows, "runtime": [],
              "runtime_probe": {"output": runtime_output, "pass": True,
                                "command": "java -cp <bare JDK runtime probe> JdkSvgProbe controls/svg/red-green.svg"}}
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(rows)}/{len(parsers)} Java SVG package paths passed; no bundled JDK SVG reader")


if __name__ == "__main__":
    main()
