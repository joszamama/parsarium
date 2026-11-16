package org.parsarium;

import java.io.File;
import java.io.InputStream;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Base64;
import java.util.Map;
import java.util.jar.JarFile;
import java.util.jar.JarInputStream;
import java.util.zip.ZipFile;
import java.util.zip.ZipInputStream;

public final class ZipAdapter {
    private ZipAdapter() {}

    private record Parsed(String name, byte[] content) {}

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            throw new IllegalArgumentException("usage: ZipAdapter PACKAGE CONTROL.zip");
        }
        Path path = Path.of(args[1]);
        Parsed parsed = switch (args[0]) {
            case "jdk-zipfile" -> {
                try (ZipFile zip = new ZipFile(path.toFile())) {
                    var entry = zip.getEntry("hello.txt");
                    try (InputStream input = zip.getInputStream(entry)) {
                        yield new Parsed(entry.getName(), input.readAllBytes());
                    }
                }
            }
            case "jdk-zipinputstream" -> {
                try (ZipInputStream zip = new ZipInputStream(Files.newInputStream(path))) {
                    var entry = zip.getNextEntry();
                    yield new Parsed(entry.getName(), zip.readAllBytes());
                }
            }
            case "jdk-jarfile" -> {
                try (JarFile jar = new JarFile(path.toFile())) {
                    var entry = jar.getJarEntry("hello.txt");
                    try (InputStream input = jar.getInputStream(entry)) {
                        yield new Parsed(entry.getName(), input.readAllBytes());
                    }
                }
            }
            case "jdk-jarinputstream" -> {
                try (JarInputStream jar = new JarInputStream(Files.newInputStream(path))) {
                    var entry = jar.getNextJarEntry();
                    yield new Parsed(entry.getName(), jar.readAllBytes());
                }
            }
            case "jdk-zipfs" -> {
                try (var zipfs = FileSystems.newFileSystem(path, Map.of())) {
                    yield new Parsed("hello.txt", Files.readAllBytes(zipfs.getPath("/hello.txt")));
                }
            }
            case "commons-compress" -> {
                try (var zip = org.apache.commons.compress.archivers.zip.ZipFile.builder()
                        .setPath(path).get()) {
                    var entry = zip.getEntry("hello.txt");
                    try (InputStream input = zip.getInputStream(entry)) {
                        yield new Parsed(entry.getName(), input.readAllBytes());
                    }
                }
            }
            case "zip4j" -> {
                var zip = new net.lingala.zip4j.ZipFile(path.toFile());
                var entry = zip.getFileHeader("hello.txt");
                try (InputStream input = zip.getInputStream(entry)) {
                    yield new Parsed(entry.getFileName(), input.readAllBytes());
                }
            }
            case "zt-zip" -> {
                Parsed[] found = new Parsed[1];
                org.zeroturnaround.zip.ZipUtil.iterate(path.toFile(), (input, entry) -> {
                    if (entry.getName().equals("hello.txt")) {
                        found[0] = new Parsed(entry.getName(), input.readAllBytes());
                    }
                });
                if (found[0] == null) throw new IllegalStateException("hello.txt not found");
                yield found[0];
            }
            case "lljzip" -> {
                try (var archive = software.coley.lljzip.ZipIO.readJvm(path)) {
                    var entry = archive.getLocalFileByName("hello.txt");
                    var data = software.coley.lljzip.format.compression.ZipCompressions.decompress(entry);
                    byte[] content = new byte[Math.toIntExact(data.length())];
                    data.get(0, content, 0, content.length);
                    yield new Parsed(entry.getFileNameAsString(), content);
                }
            }
            case "ant" -> {
                try (var zip = new org.apache.tools.zip.ZipFile(path.toFile())) {
                    var entry = zip.getEntry("hello.txt");
                    try (InputStream input = zip.getInputStream(entry)) {
                        yield new Parsed(entry.getName(), input.readAllBytes());
                    }
                }
            }
            case "commons-vfs2" -> {
                var file = org.apache.commons.vfs2.VFS.getManager()
                        .resolveFile("zip:" + path.toAbsolutePath().toUri() + "!/hello.txt");
                try (InputStream input = file.getContent().getInputStream()) {
                    yield new Parsed(file.getName().getBaseName(), input.readAllBytes());
                } finally {
                    file.close();
                }
            }
            case "zip4jvm" -> {
                try (InputStream input = ru.olegcherednik.zip4jvm.UnzipIt.zip(path).stream("hello.txt")) {
                    yield new Parsed("hello.txt", input.readAllBytes());
                }
            }
            case "quarkus-fs-util" -> {
                try (var fs = io.quarkus.fs.util.ZipUtils.openReadOnly(path)) {
                    var entry = fs.getPath("/hello.txt");
                    yield new Parsed(entry.getFileName().toString(), Files.readAllBytes(entry));
                }
            }
            case "jarchivelib" -> {
                var archiver = org.rauschig.jarchivelib.ArchiverFactory
                        .createArchiver(org.rauschig.jarchivelib.ArchiveFormat.ZIP);
                try (var stream = archiver.stream(path.toFile())) {
                    var entry = stream.getNextEntry();
                    yield new Parsed(entry.getName(), stream.readAllBytes());
                }
            }
            case "compress4j" -> {
                try (var extractor = com.hominux.compress4j.archivers.zip.ZipArchiveExtractor
                        .builder(path).build(); var items = extractor.stream()) {
                    var item = items.findFirst().orElseThrow();
                    try (InputStream input = item.content()) {
                        yield new Parsed(item.entry().name(), input.readAllBytes());
                    }
                }
            }
            case "arcana" -> {
                try (var reader = be.stef.arcana.Arcana.read(path.toFile())) {
                    var item = reader.iterator().next();
                    try (InputStream input = item.openStream()) {
                        yield new Parsed(item.getEntry().getName(), input.readAllBytes());
                    }
                }
            }
            case "tika-parser-pkg-module" -> {
                Parsed[] found = new Parsed[1];
                var context = new org.apache.tika.parser.ParseContext();
                context.set(org.apache.tika.extractor.EmbeddedDocumentExtractor.class,
                        new org.apache.tika.extractor.EmbeddedDocumentExtractor() {
                            public boolean shouldParseEmbedded(org.apache.tika.metadata.Metadata metadata,
                                                               org.apache.tika.parser.ParseContext ignored) {
                                return true;
                            }
                            public void parseEmbedded(org.apache.tika.io.TikaInputStream input,
                                                      org.xml.sax.ContentHandler handler,
                                                      org.apache.tika.metadata.Metadata metadata,
                                                      org.apache.tika.parser.ParseContext ignored,
                                                      boolean outputHtml) throws java.io.IOException {
                                found[0] = new Parsed(metadata.get(
                                        org.apache.tika.metadata.TikaCoreProperties.RESOURCE_NAME_KEY),
                                        input.readAllBytes());
                            }
                        });
                try (var input = org.apache.tika.io.TikaInputStream.get(path)) {
                    new org.apache.tika.parser.pkg.ZipParser().parse(input,
                            new org.xml.sax.helpers.DefaultHandler(),
                            new org.apache.tika.metadata.Metadata(), context);
                }
                if (found[0] == null) throw new IllegalStateException("ZIP entry not parsed");
                yield found[0];
            }
            case "truezip-driver-zip" -> {
                var entry = new de.schlichtherle.truezip.file.TFile(path.toFile(), "hello.txt");
                try (InputStream input = new de.schlichtherle.truezip.file.TFileInputStream(entry)) {
                    yield new Parsed(entry.getName(), input.readAllBytes());
                }
            }
            case "commons-archive" -> {
                try (InputStream source = Files.newInputStream(path);
                     var archive = io.github.deepakdaneva.commons.archive.ArchiveUtil
                             .getArchiveInputStream(source, "application/zip")) {
                    var entry = archive.getNextEntry();
                    try (InputStream input = io.github.deepakdaneva.commons.archive.ArchiveUtil
                            .getEntryInputStream(archive)) {
                        yield new Parsed(entry.getName(), input.readAllBytes());
                    }
                }
            }
            case "truezip-utils" -> {
                var set = new org.codehaus.mojo.truezip.TrueZipFileSet();
                set.setDirectory(path.toAbsolutePath().toString());
                var files = new org.codehaus.mojo.truezip.internal.DefaultTrueZip().list(set);
                var entry = files.stream().filter(file -> file.getName().equals("hello.txt"))
                        .findFirst().orElseThrow();
                try (InputStream input = new de.schlichtherle.truezip.file.TFileInputStream(entry)) {
                    yield new Parsed(entry.getName(), input.readAllBytes());
                }
            }
            case "simplezip" -> {
                try (var zip = new com.j256.simplezip.ZipFileInput(path.toFile());
                     var output = new java.io.ByteArrayOutputStream()) {
                    var entry = zip.readFileHeader();
                    zip.readFileData(output);
                    yield new Parsed(entry.getFileName(), output.toByteArray());
                }
            }
            case "tinyzip-core" -> {
                Path destination = Files.createTempDirectory("parsarium-tinyzip-");
                try {
                    org.tinyzip.TinyZip.unzip(path, destination);
                    yield new Parsed("hello.txt", Files.readAllBytes(destination.resolve("hello.txt")));
                } finally {
                    Files.deleteIfExists(destination.resolve("hello.txt"));
                    Files.deleteIfExists(destination);
                }
            }
            case "sevenzipjbinding" -> {
                try (var file = new java.io.RandomAccessFile(path.toFile(), "r");
                     var archive = net.sf.sevenzipjbinding.SevenZip.openInArchive(
                             net.sf.sevenzipjbinding.ArchiveFormat.ZIP,
                             new net.sf.sevenzipjbinding.impl.RandomAccessFileInStream(file));
                     var output = new java.io.ByteArrayOutputStream()) {
                    var item = archive.getSimpleInterface().getArchiveItems()[0];
                    var result = item.extractSlow(data -> {
                        output.write(data, 0, data.length);
                        return data.length;
                    });
                    if (result != net.sf.sevenzipjbinding.ExtractOperationResult.OK) {
                        throw new IllegalStateException("7-Zip extraction failed: " + result);
                    }
                    yield new Parsed(item.getPath(), output.toByteArray());
                }
            }
            case "truevfs-driver-zip" -> {
                var entry = new net.java.truevfs.access.TFile(path.toFile(), "hello.txt");
                try (InputStream input = new net.java.truevfs.access.TFileInputStream(entry)) {
                    yield new Parsed(entry.getName(), input.readAllBytes());
                } finally {
                    net.java.truevfs.access.TVFS.umount();
                }
            }
            case "plexus-archiver" -> {
                Path destination = Files.createTempDirectory("parsarium-plexus-zip-");
                try {
                    var archiver = new org.codehaus.plexus.archiver.zip.ZipUnArchiver(path.toFile());
                    archiver.setDestDirectory(destination.toFile());
                    archiver.extract();
                    yield new Parsed("hello.txt", Files.readAllBytes(destination.resolve("hello.txt")));
                } finally {
                    Files.deleteIfExists(destination.resolve("hello.txt"));
                    Files.deleteIfExists(destination);
                }
            }
            default -> throw new IllegalArgumentException("unknown API: " + args[0]);
        };
        System.out.println("{\"name\":\"" + parsed.name + "\",\"content_base64\":\""
                + Base64.getEncoder().encodeToString(parsed.content) + "\"}");
    }
}
