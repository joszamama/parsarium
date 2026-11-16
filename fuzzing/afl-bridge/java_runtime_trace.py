"""Map JDK parser bytecode lines exercised by one input into AFL++ feedback."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(2)
    with tempfile.TemporaryDirectory(prefix="parsarium-jdk-") as temporary:
        work = Path(temporary)
        execution = work / "jacoco.exec"
        report = work / "jacoco.xml"
        if "PARSARIUM_JAVA_PATCH" in os.environ:
            coverage_args = [
                "--patch-module", f"java.base={os.environ['PARSARIUM_JAVA_PATCH']}",
                "--add-reads", "java.base=ALL-UNNAMED",
                f"-Xbootclasspath/a:{os.environ['PARSARIUM_JAVA_BOOTPATH']}",
                f"-Djacoco-agent.destfile={execution}",
            ]
        else:
            agent = (f"-javaagent:/work/jacocoagent.jar=destfile={execution},append=false,"
                     f"includes={os.environ['PARSARIUM_JACOCO_INCLUDES']},inclbootstrapclasses=true")
            coverage_args = [agent]
        result = subprocess.run(
            ["java", *coverage_args, "-cp", "/work/afl-java-classes:" +
             os.environ["PARSARIUM_JAVA_CLASSPATH"], "JavaCase", sys.argv[1]],
            capture_output=True, text=True, errors="replace", timeout=30,
        )
        if result.returncode:
            raise RuntimeError(result.stdout[-1000:] + result.stderr[-1000:])
        subprocess.run(
            ["java", "-jar", "/work/jacococli.jar", "report", str(execution),
             "--classfiles", os.environ["PARSARIUM_PARSER_JAR"],
             "--sourcefiles", os.environ["PARSARIUM_PARSER_SOURCES"],
             "--xml", str(report), "--quiet"],
            check=True, capture_output=True, text=True, timeout=30,
        )
        root = ET.parse(report).getroot()
        with open(sys.argv[2], "w", encoding="utf-8") as output:
            for package in root.findall("package"):
                for source in package.findall("sourcefile"):
                    filename = f"{package.attrib['name']}/{source.attrib['name']}"
                    for line in source.findall("line"):
                        if int(line.attrib["ci"]) > 0:
                            output.write(f"{filename}:{line.attrib['nr']}\n")


if __name__ == "__main__":
    main()
