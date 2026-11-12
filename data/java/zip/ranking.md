# Java × ZIP: verified parser ranking

20 verified third-party Maven package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T03:51:06.661140+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 0 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [commons-compress](https://commons.apache.org/proper/commons-compress/apidocs/org/apache/commons/compress/archivers/zip/ZipFile.html) | org.apache.commons:commons-compress:1.28.0 | 1,402 | ZIP entry name and decompressed content from a local archive | Apache Commons Compress ZIP parser |
| 2 | [ant](https://ant.apache.org/manual/api/org/apache/tools/zip/ZipFile.html) | org.apache.ant:ant:1.10.18 | 124 | ZIP entry name and decompressed content from a local archive | Apache Ant ZIP reader; historically related to Commons Compress |
| 3 | [commons-vfs2](https://commons.apache.org/proper/commons-vfs/filesystems.html) | org.apache.commons:commons-vfs2:2.10.0 | 99 | ZIP entry name and decompressed content from a local archive | Commons VFS ZIP provider over JDK ZipFile |
| 4 | [zip4j](https://github.com/srikanth-lingala/zip4j) | net.lingala.zip4j:zip4j:2.11.6 | 40 | ZIP entry name and decompressed content from a local archive | zip4j ZIP parser |
| 5 | [jarchivelib](https://github.com/thrau/jarchivelib) | org.rauschig:jarchivelib:1.2.0 | 31 | ZIP entry name and decompressed content from a local archive | JArchiveLib wrapper over Commons Compress |
| 6 | [plexus-archiver](https://codehaus-plexus.github.io/plexus-archiver/apidocs/org/codehaus/plexus/archiver/zip/ZipUnArchiver.html) | org.codehaus.plexus:plexus-archiver:4.15.0 | 24 | ZIP entry name and decompressed content from a local archive | Plexus Archiver wrapper over Commons Compress |
| 7 | [truezip-driver-zip](https://christian-schlichtherle.bitbucket.io/truezip/apidocs/de/schlichtherle/truezip/file/TFileInputStream.html) | de.schlichtherle.truezip:truezip-driver-zip:7.7.10 | 18 | ZIP entry name and decompressed content from a local archive | TrueZIP ZIP driver |
| 8 | [zt-zip](https://github.com/zeroturnaround/zt-zip) | org.zeroturnaround:zt-zip:1.18.2 | 6 | ZIP entry name and decompressed content from a local archive | zt-zip wrapper over JDK ZipFile |
| 9 | [truezip-utils](https://www.mojohaus.org/truezip/truezip-utils/apidocs/index-all.html) | org.codehaus.mojo:truezip-utils:1.2 | 5 | ZIP entry name and decompressed content from a local archive | MojoHaus TrueZIP wrapper over TrueZIP ZIP driver |
| 10 | [quarkus-fs-util](https://github.com/quarkusio/quarkus-fs-util) | io.quarkus:quarkus-fs-util:1.4.2 | 4 | ZIP entry name and decompressed content from a local archive | Quarkus read-only ZIP filesystem parser |
| 11 | [tinyzip-core](https://github.com/bitstorm/tiny-zip) | io.github.bitstorm:tinyzip-core:1.0.0 | 2 | ZIP entry name and decompressed content from a local archive | TinyZip wrapper over JDK ZipInputStream |
| 11 | [truevfs-driver-zip](https://truevfs.namespace.global/kick-start/tutorial.html) | net.java.truevfs:truevfs-driver-zip:0.14.0 | 2 | ZIP entry name and decompressed content from a local archive | TrueVFS ZIP driver (TrueZIP successor family) |
| 13 | [commons-archive](https://github.com/deepakdaneva/commons/blob/main/commons-archive/README.md) | io.github.deepakdaneva.commons:commons-archive:1.1.0 | 1 | ZIP entry name and decompressed content from a local archive | Commons Archive wrapper over Apache Commons Compress |
| 13 | [compress4j](https://github.com/hominux/compress4j) | com.hominux:compress4j:5.1.0 | 1 | ZIP entry name and decompressed content from a local archive | Compress4J wrapper over Commons Compress |
| 13 | [tika-parser-pkg-module](https://tika.apache.org/4.2.0/api/org/apache/tika/parser/pkg/ZipParser.html) | org.apache.tika:tika-parser-pkg-module:4.2.0 | 1 | ZIP entry name and decompressed content from a local archive | Apache Tika ZipParser over Commons Compress |
| 16 | [arcana](https://realburst.github.io/arcana/) | io.github.realburst:arcana:1.1.0 | 0 | ZIP entry name and decompressed content from a local archive | Arcana own ZIP parser |
| 16 | [lljzip](https://github.com/Col-E/LL-Java-Zip/blob/2.1.0/README.md) | software.coley:lljzip:2.1.0 | 0 | ZIP entry name and decompressed content from a local archive | LLJZip own ZIP reader |
| 16 | [sevenzipjbinding](https://sevenzipjbind.sourceforge.net/snippets/index.html) | net.sf.sevenzipjbinding:sevenzipjbinding:23.01-2.2 | 0 | ZIP entry name and decompressed content from a local archive | 7-Zip C++ archive parser via JNI |
| 16 | [simplezip](https://256stuff.com/sources/simplezip/docs/simplezip.pdf) | com.j256.simplezip:simplezip:2.2 | 0 | ZIP entry name and decompressed content from a local archive | SimpleZip own ZIP parser |
| 16 | [zip4jvm](https://github.com/oleg-cherednik/zip4jvm) | ru.oleg-cherednik.zip4jvm:zip4jvm:1.13 | 0 | ZIP entry name and decompressed content from a local archive | zip4jvm own ZIP parser |
