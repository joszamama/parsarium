"""Replay pinned Java ASCII PNM adapters on a valid P3 PPM control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/ascii_pnm"
DATA = ROOT / "data/java/ascii_pnm"
CONTROL = ROOT / "controls/ascii_pnm/red-green.ppm"
REPOSITORY = Path.home() / ".m2/repository"


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True, timeout=120)


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    assert CONTROL.read_text() == "P3\n2 1\n255\n255 0 0  0 255 0\n"
    control_hash = sha256(CONTROL.read_bytes()).hexdigest()
    ffprobe = Path(os.environ.get("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin")) / "ffprobe"
    if any(parser.get("adapter_module") in {"jaffree", "bramp", "v47", "imagic"} for parser in parsers):
        tool = snapshot["external_tools"]["ffprobe"]
        assert sha256(ffprobe.read_bytes()).hexdigest() == tool["sha256"]
        assert run([str(ffprobe), "-version"]).stdout.splitlines()[0] == tool["version"]
    identify = Path(os.environ.get("PARSARIUM_IMAGEMAGICK_DIR", "/opt/homebrew/bin")) / "identify"
    if any(parser.get("adapter_module") == "im4java" for parser in parsers):
        tool = snapshot["external_tools"]["imagemagick_identify"]
        assert sha256(identify.read_bytes()).hexdigest() == tool["sha256"]
        assert run([str(identify), "-version"]).stdout.splitlines()[0] == tool["version"]
        os.environ["PATH"] = str(identify.parent) + os.pathsep + os.environ.get("PATH", "")

    module_jars = {}
    for module in sorted({parser.get("adapter_module", "main") for parser in parsers}):
        directory = ADAPTER if module == "main" else ADAPTER / module
        run(["mvn", "-q", "-DskipTests", "package",
             "org.apache.maven.plugins:maven-dependency-plugin:3.8.1:build-classpath",
             "-Dmdep.outputFile=target/classpath.txt"], directory)
        jars = [Path(item) for item in (directory / "target/classpath.txt").read_text().strip().split(":")]
        actual = [{"repository_path": str(jar.relative_to(REPOSITORY)),
                   "sha256": sha256(jar.read_bytes()).hexdigest()} for jar in jars]
        assert actual == json.loads((directory / "dependencies.lock.json").read_text())["classpath"]
        module_jars[module] = jars
    java27 = Path(os.environ.get("PARSARIUM_JAVA27_HOME", "/opt/homebrew/opt/openjdk")) / "bin"
    native_classes = ADAPTER / "native/target"
    native_classes.mkdir(parents=True, exist_ok=True)
    run([str(java27 / "javac"), "--release", "26", "-d", str(native_classes),
         str(ADAPTER / "native/PnmNativeAdapter.java")])
    for parser in parsers:
        release = snapshot["releases"][parser["name"]]
        assert (release["group"], release["artifact"], release["version"]) == (
            parser["group"], parser["artifact"], parser["version"])
        stem = f"{parser['artifact']}-{parser['version']}"
        path = f"{parser['group'].replace('.', '/')}/{parser['artifact']}/{parser['version']}/{stem}.jar"
        jars = module_jars[parser.get("adapter_module", "main")]
        by_path = {str(jar.relative_to(REPOSITORY)): sha256(jar.read_bytes()).hexdigest() for jar in jars}
        assert by_path[path] == release["jar_sha256"]
        pom = REPOSITORY / path.replace(".jar", ".pom")
        assert sha256(pom.read_bytes()).hexdigest() == release["pom_sha256"]

    rows = []
    for parser in parsers:
        label = parser["adapter_label"]
        module = parser.get("adapter_module", "main")
        if module == "main":
            classpath = str(ADAPTER / "target/classes") + ":" + ":".join(str(jar) for jar in module_jars[module])
            command = ["java", "-Djava.awt.headless=true", "-cp", classpath,
                       "org.parsarium.PnmAdapter", label, str(CONTROL)]
            display = f"java -Djava.awt.headless=true -cp <locked main classpath> org.parsarium.PnmAdapter {label} {parser['control']}"
        elif module == "ffmpeg":
            classpath = str(ADAPTER / module / "target/classes") + ":" + ":".join(str(jar) for jar in module_jars[module])
            command = ["java", "-Djava.awt.headless=true", "-cp", classpath,
                       "org.parsarium.FfmpegPnmAdapter", label, str(CONTROL)]
            display = f"java -Djava.awt.headless=true -cp <locked {module} classpath> org.parsarium.FfmpegPnmAdapter {label} {parser['control']}"
        elif module in {"jaffree", "bramp", "v47", "imagic", "jave", "lafa", "ijp", "im4java"}:
            classes = {"jaffree": "JaffreePnmAdapter", "bramp": "BrampPnmAdapter",
                       "v47": "V47PnmAdapter", "imagic": "ImagicPnmAdapter",
                       "jave": "JavePnmAdapter", "lafa": "LafaPnmAdapter",
                       "ijp": "IjpPnmAdapter", "im4java": "Im4javaPnmAdapter"}
            classpath = str(ADAPTER / module / "target/classes") + ":" + ":".join(str(jar) for jar in module_jars[module])
            command = ["java", "-Djava.awt.headless=true", "-cp", classpath,
                       f"org.parsarium.{classes[module]}", str(CONTROL)]
            display = f"java -Djava.awt.headless=true -cp <locked {module} classpath> org.parsarium.{classes[module]} {parser['control']}"
        else:
            classpath = str(native_classes) + ":" + ":".join(str(jar) for jar in module_jars[module])
            command = [str(java27 / "java"), "--enable-native-access=ALL-UNNAMED",
                       "-Djava.awt.headless=true", "-cp", classpath,
                       "PnmNativeAdapter", str(CONTROL)]
            display = f"{java27 / 'java'} --enable-native-access=ALL-UNNAMED -Djava.awt.headless=true -cp <locked {module} classpath> PnmNativeAdapter {parser['control']}"
        output = json.loads(run(command).stdout.strip())
        assert output == parser["expected_output"], (label, output)
        rows.append({"package": parser["name"], "version": parser["version"],
                     "control": parser["control"], "output": output, "pass": True,
                     "command": display})
        print(f"{label}: passed")

    runtime = ADAPTER / "target/runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    run(["javac", "--release", "21", "-d", str(runtime),
         str(ADAPTER / "runtime/JdkPnmProbe.java")])
    runtime_output = json.loads(run(["java", "-cp", str(runtime), "JdkPnmProbe", str(CONTROL)]).stdout.strip())
    assert runtime_output == {"pnm_readers": 0, "imageio_result": None}
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "environment": {"java": run(["java", "-version"]).stderr.strip(),
                              "maven": run(["mvn", "-version"]).stdout.splitlines()[0],
                              "platform": platform.platform(),
                              "classpath_jars": {module: len(jars) for module, jars in module_jars.items()},
                              "libvips": run(["vips", "--version"]).stdout.strip(),
                              "imagemagick": run(["magick", "-version"]).stdout.splitlines()[0],
                              "ffprobe": run([str(ffprobe), "-version"]).stdout.splitlines()[0],
                              "imagemagick_identify": run([str(identify), "-version"]).stdout.splitlines()[0]},
              "control": "controls/ascii_pnm/red-green.ppm", "control_sha256": control_hash,
              "control_meaning": "Valid ASCII P3 PPM with two red/green pixels",
              "third_party": rows, "runtime": [],
              "runtime_probe": {"output": runtime_output, "pass": True,
                                "command": "java -cp <bare JDK runtime probe> JdkPnmProbe controls/ascii_pnm/red-green.ppm"}}
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(rows)}/{len(parsers)} Java ASCII PNM package paths passed; no bundled JDK PNM reader")


if __name__ == "__main__":
    main()
