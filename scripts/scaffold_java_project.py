"""Stage one Maven parser with JaCoCo, Jazzer, and a pinned source JAR."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "projects/png/java/pngj"
BASE = "eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9"
BASE25 = "eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d"
JACOCO_AGENT = "3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face"
JACOCO_CLI = "811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c"
JAZZER = "0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f"
ADAPTER_CLASSES = {"png": "PngAdapter", "zip": "ZipAdapter", "mp4": "Mp4Adapter",
                   "wav": "WavAdapter", "pdf": "PdfAdapter", "svg": "SvgAdapter",
                   "http11": "Http11Adapter", "ascii_ply": "PlyAdapter",
                   "ascii_pnm": "PnmAdapter", "mp3_id3v2": "Mp3Id3v2Adapter"}


def stage(format_name: str, package: str) -> Path:
    catalog = ROOT / "data/java" / format_name / "parsers.json"
    parser, = [item for item in json.loads(catalog.read_text()) if item["name"] == package]
    for existing in (ROOT / "projects" / format_name / "java").glob("*/manifest.json"):
        if json.loads(existing.read_text()).get("package") == package:
            raise ValueError(f"package already staged: {existing.parent}")
    group, artifact, version = parser["group"], parser["artifact"], parser["version"]
    repository = "https://repo.maven.apache.org/maven2/"
    prefix = f"{group.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}"
    source_url = repository + prefix + "-sources.jar"
    with urllib.request.urlopen(source_url, timeout=30) as response:
        source_sha = sha256(response.read()).hexdigest()
    adapter_root = ROOT / "adapters/java" / format_name
    jar_path = prefix + ".jar"
    locks = sorted(adapter_root.rglob("dependencies.lock.json"),
                   key=lambda path: (len(path.parts), str(path)))
    matches = []
    for candidate in locks:
        candidate_lock = json.loads(candidate.read_text())
        if any(item["repository_path"] == jar_path for item in candidate_lock["classpath"]):
            matches.append((candidate, candidate_lock))
    if not matches:
        raise ValueError(f"no locked JAR for {jar_path}")
    lock_path, lock = matches[0]
    jars = [item for item in lock["classpath"]
            if not (format_name == "wav" and Path(item["repository_path"]).name in {
                "xmpcore-6.1.11.jar", "jvm-2.5.jar", "core-2.5.jar"})
            and not (format_name == "wav" and "junit" in item["repository_path"].lower())]
    target, = [item for item in jars if item["repository_path"] == jar_path]
    if lock_path.parent == adapter_root:
        source = adapter_root / "src/main/java/org/parsarium" / (ADAPTER_CLASSES[format_name] + ".java")
        uses_mode = True
    else:
        java_sources = [path for path in lock_path.parent.rglob("*.java")
                        if "public static void main(" in path.read_text()]
        if len(java_sources) != 1:
            raise ValueError(f"expected one local adapter main in {lock_path.parent}: {java_sources}")
        source = java_sources[0]
        uses_mode = False
    if not source.is_file():
        raise ValueError(f"missing Java adapter: {source}")
    slug = re.sub(r"[^a-z0-9]+", "_", package.lower()).strip("_")
    destination = ROOT / "projects" / format_name / "java" / slug
    if destination.exists():
        raise ValueError(f"project exists: {destination}")
    destination.mkdir(parents=True)
    adapter_text = source.read_text()
    adapter_text = adapter_text.replace("/opt/homebrew/bin", "/usr/bin")
    if format_name == "wav" and uses_mode:
        start = adapter_text.index('            case "tarsos" -> {')
        end = adapter_text.index('            case "musicg" -> {', start)
        adapter_text = adapter_text[:start] + adapter_text[end:]
    (destination / source.name).write_text(adapter_text)
    label = parser.get("adapter_label", package)
    if format_name == "wav":
        label = {"jhove-modules": "jhove", "tika-audiovideo": "tika"}.get(label, label)
    class_name = "org.parsarium." + source.stem
    control = ROOT / parser["control"]
    harness = '''import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.lang.reflect.InvocationTargetException;
import java.nio.file.Files;
import java.nio.file.Path;

public final class GenericHarness {
    private static final String ADAPTER = ADAPTER_CLASS;
    private static final String LABEL = ADAPTER_LABEL;
    private static final String SUFFIX = INPUT_SUFFIX;

    private static String parse(byte[] data) throws Exception {
        if (data.length == 0 || data.length > (1 << 20)) return "";
        Path input = Files.createTempFile("parsarium-java-", SUFFIX);
        PrintStream original = System.out;
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        try {
            Files.write(input, data);
            System.setOut(new PrintStream(output, true, "UTF-8"));
            try {
                Class.forName(ADAPTER).getMethod("main", String[].class)
                     .invoke(null, (Object) INPUT_ARGUMENTS);
            } catch (InvocationTargetException error) {
                Throwable cause = error.getCause();
                if (cause instanceof Exception checked) throw checked;
                if (cause instanceof Error failure) throw failure;
                throw error;
            }
        } finally {
            System.setOut(original);
            Files.deleteIfExists(input);
        }
        String[] lines = output.toString("UTF-8").trim().split("\\r?\\n");
        return lines[lines.length - 1];
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (RuntimeException error) { throw error; }
        catch (Exception ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one input path required");
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
'''
    arguments = "new String[]{LABEL, input.toString()}" if uses_mode else "new String[]{input.toString()}"
    harness = (harness.replace("ADAPTER_CLASS", json.dumps(class_name))
              .replace("ADAPTER_LABEL", json.dumps(label))
              .replace("INPUT_SUFFIX", json.dumps(control.suffix))
              .replace("INPUT_ARGUMENTS", arguments))
    (destination / "GenericHarness.java").write_text(harness)
    (destination / "source-lock.json").write_text(json.dumps({package: {
        "release": version, "source_sha256": source_sha,
        "jar_sha256": target["sha256"], "source_url": source_url}}, indent=2) + "\n")
    downloads = []
    for item in jars:
        name = Path(item["repository_path"]).name
        downloads.extend([f"    && curl --fail --location --retry 3 {repository + item['repository_path']} -o /work/lib/{name} \\",
                          f"    && echo '{item['sha256']}  /work/lib/{name}' | sha256sum --check \\"])
    downloads[-1] = downloads[-1].removesuffix(" \\")
    base_image = BASE25 if format_name in {"mp3_id3v2", "pdf"} else BASE
    runtime_packages = (" ffmpeg" if re.search(r"ffprobe|ffmpeg|FFprobe|FFmpeg", adapter_text) else "")
    runtime_packages += (" imagemagick" if re.search(r"ImageMagick|magick|convert", adapter_text) else "")
    docker = f'''FROM --platform=linux/arm64 {base_image} AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/lib \\
{chr(10).join(downloads)}
RUN curl --fail --location --retry 3 {source_url} -o /work/parser-sources.jar \\
    && echo '{source_sha}  /work/parser-sources.jar' | sha256sum --check \\
    && mkdir /work/parser-source && unzip -qo /work/parser-sources.jar -d /work/parser-source
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \\
    && echo '{JACOCO_AGENT}  /work/jacocoagent.jar' | sha256sum --check \\
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \\
    && echo '{JACOCO_CLI}  /work/jacococli.jar' | sha256sum --check \\
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \\
    && echo '{JAZZER}  /work/jazzer.tar.gz' | sha256sum --check \\
    && tar -xf /work/jazzer.tar.gz -C /work
COPY {source.name} GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \\
    && {{ java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; }} > /work/toolchain.txt

FROM --platform=linux/arm64 {base_image}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3{runtime_packages} \\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
'''
    (destination / "Dockerfile").write_text(docker)
    expected = json.dumps(parser["expected_output"], separators=(",", ":"))
    run_control = f'''#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=* \\
  -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \\
  --classfiles /work/lib/{Path(jar_path).name} --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text()
observed = json.loads(raw.strip().splitlines()[-1])
expected = json.loads({json.dumps(expected)})
if observed != expected:
    raise SystemExit(f'control mismatch: {{observed}}')
root = ET.parse('/coverage/jacoco.xml').getroot()
files = []
for package in root.findall('package'):
    for source in package.findall('sourcefile'):
        executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                          if int(line.attrib['ci']) > 0)
        if executed:
            filename = f"/work/parser-source/{{package.attrib['name']}}/{{source.attrib['name']}}"
            files.append({{'filename': filename,
                          'summary': {{'lines': {{'covered': len(executed)}}}},
                          'executed_lines': executed}})
covered = sum(f['summary']['lines']['covered'] for f in files)
if covered == 0:
    raise SystemExit('no parser package source lines covered')
summary = {{'control_pass': True, 'output': observed,
           'parser_source_files': len(files), 'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\\n')
Path('/coverage/coverage.json').write_text(json.dumps({{'data': [{{'files': files}}]}}, indent=2) + '\\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\\n')
print(json.dumps(summary))
PYRUN
'''
    (destination / "run-control.sh").write_text(run_control)
    manifest = json.loads((TEMPLATE / "manifest.json").read_text())
    manifest.pop("format_specific_coverage_file_suffix", None)
    manifest.update({"format": format_name, "package": package, "release": version,
                     "base_image": base_image, "runtime_base_image": base_image,
                     "catalog_parser": str(catalog.relative_to(ROOT)),
                     "source_lock": str((destination / "source-lock.json").relative_to(ROOT)),
                     "source_sha256": source_sha, "control": parser["control"],
                     "control_sha256": sha256(control.read_bytes()).hexdigest(),
                     "expected_output": parser["expected_output"],
                     "harness": "GenericHarness.java", "fuzz_entry": "GenericHarness.fuzzerTestOneInput",
                     "fuzz_smoke_args": ["--cp=/work/classes:" + ":".join(
                         "/work/lib/" + Path(item["repository_path"]).name for item in jars),
                         "--target_class=GenericHarness", "-help=1"],
                     "coverage": f"JaCoCo bytecode coverage of {group}:{artifact}:{version} during valid-control replay; Jazzer fuzz entry",
                     "coverage_subject_prefix": "/work/parser-source/"})
    if package == "netty-codec-http":
        # Jazzer's UnsafeSanitizer conflicts with Netty's shaded JCTools queue
        # initializer on the pinned control; parser instrumentation remains on.
        manifest["fuzz_smoke_args"].insert(-1,
            "--disabled_hooks=com.code_intelligence.jazzer.sanitizers.UnsafeSanitizer")
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return destination


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("package")
    args = cli.parse_args()
    print(stage(args.format, args.package).relative_to(ROOT))
