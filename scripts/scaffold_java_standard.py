"""Stage Java desktop runtime parser APIs with JDK bytecode coverage."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "eclipse-temurin@sha256:06c1f157dacf6b68198bd9a4186dd4c34ef24e65d7bbbe2a0cf8e62571ad38c9"
JMOD_SHA = "a59ed5a74ba89346159fb74216115d34c2ed460126b736f89bce81eac661c160"
ZIPFS_JMOD_SHA = "f6cd4c18337aa25147e14e59c071b8e9171ece8b08bead0139b4667ec39ea185"
BASE_JMOD_SHA = "db87d005701923c8b38d829219b6245bbf022262eb4851be47639fe50aa9a916"
RUNTIME = "Eclipse Temurin OpenJDK 21.0.2 linux/arm64 java.desktop"
JACOCO_AGENT = "3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face"
JACOCO_CLI = "811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c"
JAZZER = "0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f"
TARGETS = {
    "jdk-imageio": ("png", "imageio"),
    "jdk-imagereader": ("png", "imagereader"),
    "jdk-imageicon": ("png", "imageicon"),
    "jdk-toolkit": ("png", "toolkit"),
    "AudioSystem.getAudioFileFormat(File)": ("wav", "audio_file_format"),
    "AudioSystem.getAudioInputStream(File)": ("wav", "audio_input_stream"),
    "jdk-zipfs": ("zip", "zipfs"),
    "jdk-zipfile": ("zip", "zipfile"),
    "jdk-zipinputstream": ("zip", "zipinputstream"),
    "jdk-jarfile": ("zip", "jarfile"),
    "jdk-jarinputstream": ("zip", "jarinputstream"),
}
SLUG = {
    "jdk-imageio": "jdk_imageio", "jdk-imagereader": "jdk_imagereader",
    "jdk-imageicon": "jdk_imageicon", "jdk-toolkit": "jdk_toolkit",
    "AudioSystem.getAudioFileFormat(File)": "jdk_audiofileformat",
    "AudioSystem.getAudioInputStream(File)": "jdk_audioinputstream",
    "jdk-zipfs": "jdk_zipfs",
    "jdk-zipfile": "jdk_zipfile",
    "jdk-zipinputstream": "jdk_zipinputstream",
    "jdk-jarfile": "jdk_jarfile",
    "jdk-jarinputstream": "jdk_jarinputstream",
}


def stage(api: str) -> Path:
    fmt, mode = TARGETS[api]
    module = "jdk.zipfs" if mode == "zipfs" else "java.base" if fmt == "zip" else "java.desktop"
    module_sha = (ZIPFS_JMOD_SHA if mode == "zipfs" else BASE_JMOD_SHA
                  if module == "java.base" else JMOD_SHA)
    runtime = f"Eclipse Temurin OpenJDK 21.0.2 linux/arm64 {module}"
    inventory_path = ROOT / "data/java" / fmt / "standard.json"
    inventory = json.loads(inventory_path.read_text())
    entry, = [item for item in inventory["verified_apis"]
              if (item.get("api") or item.get("name")) == api]
    entry["api"] = api
    entry["runtime"] = runtime
    entry["expected"] = entry["expected_output"]
    inventory["runtime"] = runtime
    inventory_path.write_text(json.dumps(inventory, indent=2) + "\n")
    destination = ROOT / "projects" / fmt / "java" / SLUG[api]
    if destination.exists():
        raise ValueError(f"already staged: {destination}")
    destination.mkdir(parents=True)
    expected = entry["expected_output"]
    control = ROOT / entry["control"]
    harness = '''import java.awt.Image;
import java.awt.Toolkit;
import java.awt.image.BufferedImage;
import java.awt.image.PixelGrabber;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Iterator;
import java.util.Base64;
import java.util.Map;
import java.util.zip.ZipFile;
import java.util.zip.ZipInputStream;
import java.util.zip.ZipEntry;
import java.util.jar.JarFile;
import java.util.jar.JarInputStream;
import java.util.jar.JarEntry;
import javax.imageio.ImageIO;
import javax.imageio.ImageReader;
import javax.imageio.stream.ImageInputStream;
import javax.swing.ImageIcon;
import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;

public final class GenericHarness {
    private static final String MODE = MODE_VALUE;
    private static final String SUFFIX = SUFFIX_VALUE;

    private static String pixels(int width, int height, int first, int second) {
        return String.format("{\\"width\\":%d,\\"height\\":%d,\\"pixels\\":\\"%08x,%08x\\"}",
                             width, height, first, second);
    }

    private static String imageResult(BufferedImage image) throws Exception {
        if (image == null || image.getWidth() < 2 || image.getHeight() < 1)
            throw new IllegalArgumentException("no decoded PNG pixels");
        return pixels(image.getWidth(), image.getHeight(),
                      image.getRGB(0, 0), image.getRGB(1, 0));
    }

    private static String imageResult(Image image) throws Exception {
        if (image == null) throw new IllegalArgumentException("no decoded PNG image");
        int[] argb = new int[2];
        PixelGrabber grabber = new PixelGrabber(image, 0, 0, 2, 1, argb, 0, 2);
        if (!grabber.grabPixels(3000)) throw new IllegalArgumentException("PNG pixel decode timed out");
        int width = image.getWidth(null), height = image.getHeight(null);
        if (width < 2 || height < 1) throw new IllegalArgumentException("no decoded PNG pixels");
        return pixels(width, height, argb[0], argb[1]);
    }

    private static String zipResult(byte[] member) {
        return "{\\"name\\":\\"hello.txt\\",\\"content_base64\\":\\"" +
            Base64.getEncoder().encodeToString(member) + "\\"}";
    }

    private static String parse(byte[] data) throws Exception {
        if (data.length == 0 || data.length > (1 << 20)) return "";
        Path file = Files.createTempFile("parsarium-jdk-", SUFFIX);
        try {
            Files.write(file, data);
            switch (MODE) {
                case "imageio": return imageResult(ImageIO.read(file.toFile()));
                case "imagereader": {
                    Iterator<ImageReader> readers = ImageIO.getImageReadersByFormatName("PNG");
                    if (!readers.hasNext()) throw new IllegalStateException("no JDK PNG reader");
                    ImageReader reader = readers.next();
                    try (ImageInputStream input = ImageIO.createImageInputStream(new ByteArrayInputStream(data))) {
                        reader.setInput(input);
                        return imageResult(reader.read(0));
                    } finally { reader.dispose(); }
                }
                case "imageicon": return imageResult(new ImageIcon(data).getImage());
                case "toolkit": return imageResult(new ImageIcon(Toolkit.getDefaultToolkit().createImage(data)).getImage());
                case "audio_file_format": {
                    AudioFileFormat parsed = AudioSystem.getAudioFileFormat(file.toFile());
                    return String.format("{\\"type\\":\\"%s\\",\\"sample_rate\\":%d,\\"channels\\":%d,\\"frames\\":%d}",
                        parsed.getType(), (int) parsed.getFormat().getSampleRate(),
                        parsed.getFormat().getChannels(), parsed.getFrameLength());
                }
                case "audio_input_stream": {
                    try (AudioInputStream parsed = AudioSystem.getAudioInputStream(file.toFile())) {
                        int sampleBytes = parsed.readNBytes(8).length;
                        return String.format("{\\"sample_rate\\":%d,\\"channels\\":%d,\\"frames\\":%d,\\"sample_bytes\\":%d}",
                            (int) parsed.getFormat().getSampleRate(),
                            parsed.getFormat().getChannels(), parsed.getFrameLength(), sampleBytes);
                    }
                }
                case "zipfs": {
                    try (FileSystem archive = FileSystems.newFileSystem(file, Map.of())) {
                        byte[] member = Files.readAllBytes(archive.getPath("/hello.txt"));
                        return zipResult(member);
                    }
                }
                case "zipfile": {
                    try (ZipFile archive = new ZipFile(file.toFile())) {
                        ZipEntry member = archive.getEntry("hello.txt");
                        if (member == null) throw new IllegalArgumentException("missing ZIP member");
                        return zipResult(archive.getInputStream(member).readAllBytes());
                    }
                }
                case "zipinputstream": {
                    try (ZipInputStream archive = new ZipInputStream(new ByteArrayInputStream(data))) {
                        ZipEntry member = archive.getNextEntry();
                        if (member == null || !member.getName().equals("hello.txt"))
                            throw new IllegalArgumentException("missing ZIP member");
                        return zipResult(archive.readAllBytes());
                    }
                }
                case "jarfile": {
                    try (JarFile archive = new JarFile(file.toFile())) {
                        JarEntry member = archive.getJarEntry("hello.txt");
                        if (member == null) throw new IllegalArgumentException("missing JAR member");
                        return zipResult(archive.getInputStream(member).readAllBytes());
                    }
                }
                case "jarinputstream": {
                    try (JarInputStream archive = new JarInputStream(new ByteArrayInputStream(data))) {
                        JarEntry member = archive.getNextJarEntry();
                        if (member == null || !member.getName().equals("hello.txt"))
                            throw new IllegalArgumentException("missing JAR member");
                        return zipResult(archive.readAllBytes());
                    }
                }
                default: throw new IllegalStateException(MODE);
            }
        } finally { Files.deleteIfExists(file); }
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
'''.replace("MODE_VALUE", json.dumps(mode)).replace("SUFFIX_VALUE", json.dumps(control.suffix))
    (destination / "GenericHarness.java").write_text(harness)
    coverage_packages = (("com/sun/imageio/plugins/png", "sun/awt/image") if fmt == "png"
                         else ("com/sun/media/sound",) if fmt == "wav"
                         else ("jdk/nio/zipfs",) if mode == "zipfs"
                         else ("java/util/zip", "java/util/jar"))
    includes = ("com.sun.imageio.plugins.png.*:sun.awt.image.*:javax.imageio.*"
                if fmt == "png" else "com.sun.media.sound.*:javax.sound.sampled.*"
                if fmt == "wav" else "jdk.nio.zipfs.*" if mode == "zipfs"
                else "java.util.zip.*:java.util.jar.*")
    prepare_classes = "".join(
        f"    && mkdir -p /work/parser-classes/{item.rsplit('/', 1)[0]} \\\n    && cp -a /work/jdk-module/classes/{item} /work/parser-classes/{item} \\\n" for item in coverage_packages)
    docker = f'''FROM --platform=linux/arm64 {BASE} AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN echo '{module_sha}  /opt/java/openjdk/jmods/{module}.jmod' | sha256sum --check \\
    && jmod extract --dir /work/jdk-module /opt/java/openjdk/jmods/{module}.jmod \\
{prepare_classes}    && mkdir /work/parser-sources
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \\
    && echo '{JACOCO_AGENT}  /work/jacocoagent.jar' | sha256sum --check \\
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \\
    && echo '{JACOCO_CLI}  /work/jacococli.jar' | sha256sum --check
RUN curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \\
    && echo '{JAZZER}  /work/jazzer.tar.gz' | sha256sum --check \\
    && tar -xf /work/jazzer.tar.gz -C /work
COPY GenericHarness.java /work/
RUN mkdir /work/classes && javac -d /work/classes /work/GenericHarness.java \\
    && {{ java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; }} > /work/toolchain.txt
FROM --platform=linux/arm64 {BASE}
ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_TOOL_OPTIONS=-Djava.awt.headless=true
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/parser-classes /work/parser-classes
COPY --from=build /work/parser-sources /work/parser-sources
COPY --from=build /work/jacocoagent.jar /work/jacocoagent.jar
COPY --from=build /work/jacococli.jar /work/jacococli.jar
COPY --from=build /work/jazzer /work/jazzer
COPY --from=build /work/jazzer_standalone.jar /work/jazzer_standalone.jar
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
'''
    (destination / "Dockerfile").write_text(docker)
    expected_json = json.dumps(expected, separators=(",", ":"))
    prefixes = ["/work/parser-classes/" + item + "/" for item in coverage_packages]
    script = f'''#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes={includes},inclbootstrapclasses=true \\
  -cp /work/classes GenericHarness /input/control > /coverage/observed.json
java -jar /work/jacococli.jar report /coverage/jacoco.exec \\
  --classfiles /work/parser-classes --sourcefiles /work/parser-sources --xml /coverage/jacoco.xml --quiet
python3 - <<'PY_CHECK'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = json.loads({json.dumps(expected_json)})
if observed != expected:
    raise SystemExit(f'control mismatch: {{observed}}')
root = ET.parse('/coverage/jacoco.xml').getroot()
files = []
for package in root.findall('package'):
    for source in package.findall('sourcefile'):
        executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                          if int(line.attrib['ci']) > 0)
        if not executed: continue
        filename = f"/work/parser-classes/{{package.attrib['name']}}/{{source.attrib['name']}}"
        files.append({{'filename': filename,
                      'summary': {{'lines': {{'covered': len(executed)}}}},
                      'executed_lines': executed}})
prefixes = {prefixes!r}
parser_files = [item for item in files if any(item['filename'].startswith(p) for p in prefixes)]
covered = sum(item['summary']['lines']['covered'] for item in parser_files)
if not parser_files or covered == 0:
    raise SystemExit('no instrumented JDK format reader source lines covered')
coverage = {{'data': [{{'files': parser_files}}]}}
summary = {{'control_pass': True, 'output': observed,
           'parser_source_files': len(parser_files),
           'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}}
Path('/coverage/coverage.json').write_text(json.dumps(coverage, indent=2) + '\\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\\n')
print(json.dumps(summary))
PY_CHECK
'''
    (destination / "run-control.sh").write_text(script)
    lock = {"runtime": runtime, "base_image": BASE, "source_sha256": module_sha}
    (destination / "runtime-lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    manifest = {"schema_version": 1, "kind": "standard", "format": fmt,
                "ecosystem": "java", "package": api, "release": "21.0.2",
                "api": api, "runtime": runtime,
                "standard_inventory": str(inventory_path.relative_to(ROOT)),
                "runtime_lock": "runtime-lock.json", "source_sha256": module_sha,
                "base_image": BASE, "platform": "linux/arm64", "tmpfs_exec": True,
                "control": entry["control"],
                "control_sha256": sha256(control.read_bytes()).hexdigest(),
                "expected_output": expected, "harness": "GenericHarness.java",
                "fuzz_engine": "Jazzer", "fuzz_engine_release": "v0.26.0",
                "fuzz_engine_sha256": JAZZER,
                "fuzz_entry": "GenericHarness.fuzzerTestOneInput",
                "fuzz_smoke_entrypoint": "/work/jazzer",
                "fuzz_smoke_args": ["--cp=/work/classes", "--target_class=GenericHarness", "-help=1"],
                "fuzz_smoke_expect": "Usage:",
                "coverage": f"JaCoCo bytecode coverage of OpenJDK {module} format readers",
                "coverage_subject_prefix": "/work/parser-classes/"}
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return destination


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("api", choices=sorted(TARGETS))
    args = cli.parse_args()
    print(stage(args.api).relative_to(ROOT))
