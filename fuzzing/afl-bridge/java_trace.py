"""Run one Java fuzz input under JaCoCo and emit covered parser source lines."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(2)
    with tempfile.TemporaryDirectory(prefix="parsarium-java-") as temporary:
        work = Path(temporary)
        execution = work / "jacoco.exec"
        report = work / "jacoco.xml"
        result = subprocess.run(
            ["java", f"-javaagent:/work/jacocoagent.jar=destfile={execution},append=false,includes={os.environ['PARSARIUM_JACOCO_INCLUDES']}",
             "-cp", "/work/afl-java-classes:" + os.environ["PARSARIUM_JAVA_CLASSPATH"],
             "JavaCase", sys.argv[1]],
            capture_output=True, text=True, timeout=30,
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
