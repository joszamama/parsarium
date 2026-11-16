"""Emit AFL++ features from a Java wrapper and its pinned underlying JAR."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(2)
    with tempfile.TemporaryDirectory(prefix="parsarium-java-dual-") as temporary:
        work = Path(temporary)
        execution = work / "jacoco.exec"
        result = subprocess.run(
            ["java", f"-javaagent:/work/jacocoagent.jar=destfile={execution},append=false,includes={os.environ['PARSARIUM_JACOCO_INCLUDES']}",
             "-cp", "/work/afl-java-classes:" + os.environ["PARSARIUM_JAVA_CLASSPATH"],
             "JavaCase", sys.argv[1]],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode:
            raise RuntimeError(result.stdout[-1000:] + result.stderr[-1000:])
        with open(sys.argv[2], "w", encoding="utf-8") as output:
            for label, jar, sources in (
                ("wrapper", os.environ["PARSARIUM_PARSER_JAR"], os.environ["PARSARIUM_PARSER_SOURCES"]),
                ("core", os.environ["PARSARIUM_UNDERLYING_JAR"], os.environ["PARSARIUM_UNDERLYING_SOURCES"]),
            ):
                report = work / f"{label}.xml"
                subprocess.run(
                    ["java", "-jar", "/work/jacococli.jar", "report", str(execution),
                     "--classfiles", jar, "--sourcefiles", sources,
                     "--xml", str(report), "--quiet"],
                    check=True, capture_output=True, text=True, timeout=30,
                )
                for package in ET.parse(report).getroot().findall("package"):
                    for source in package.findall("sourcefile"):
                        filename = f"{label}/{package.attrib['name']}/{source.attrib['name']}"
                        for line in source.findall("line"):
                            if int(line.attrib["ci"]) > 0:
                                output.write(f"{filename}:{line.attrib['nr']}\n")


if __name__ == "__main__":
    main()
