# JAVA × ZIP: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

deps.dev version-level directDependentCount.

| Rank | Package | Release | Direct dependents (deps.dev) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [commons-compress](https://commons.apache.org/proper/commons-compress/apidocs/org/apache/commons/compress/archivers/zip/ZipFile.html) | 1.28.0 | 1,402 | ZIP entry name and decompressed content from a local archive | Apache Commons Compress ZIP parser |
| 2 | [ant](https://ant.apache.org/manual/api/org/apache/tools/zip/ZipFile.html) | 1.10.18 | 124 | ZIP entry name and decompressed content from a local archive | Apache Ant ZIP reader; historically related to Commons Compress |
| 3 | [commons-vfs2](https://commons.apache.org/proper/commons-vfs/filesystems.html) | 2.10.0 | 99 | ZIP entry name and decompressed content from a local archive | Commons VFS ZIP provider over JDK ZipFile |
| 4 | [zip4j](https://github.com/srikanth-lingala/zip4j) | 2.11.6 | 40 | ZIP entry name and decompressed content from a local archive | zip4j ZIP parser |
| 5 | [jarchivelib](https://github.com/thrau/jarchivelib) | 1.2.0 | 31 | ZIP entry name and decompressed content from a local archive | JArchiveLib wrapper over Commons Compress |
| 6 | [plexus-archiver](https://codehaus-plexus.github.io/plexus-archiver/apidocs/org/codehaus/plexus/archiver/zip/ZipUnArchiver.html) | 4.15.0 | 24 | ZIP entry name and decompressed content from a local archive | Plexus Archiver wrapper over Commons Compress |
| 7 | [truezip-driver-zip](https://christian-schlichtherle.bitbucket.io/truezip/apidocs/de/schlichtherle/truezip/file/TFileInputStream.html) | 7.7.10 | 18 | ZIP entry name and decompressed content from a local archive | TrueZIP ZIP driver |
| 8 | [zt-zip](https://github.com/zeroturnaround/zt-zip) | 1.18.2 | 6 | ZIP entry name and decompressed content from a local archive | zt-zip wrapper over JDK ZipFile |
| 9 | [truezip-utils](https://www.mojohaus.org/truezip/truezip-utils/apidocs/index-all.html) | 1.2 | 5 | ZIP entry name and decompressed content from a local archive | MojoHaus TrueZIP wrapper over TrueZIP ZIP driver |
| 10 | [quarkus-fs-util](https://github.com/quarkusio/quarkus-fs-util) | 1.4.2 | 4 | ZIP entry name and decompressed content from a local archive | Quarkus read-only ZIP filesystem parser |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
