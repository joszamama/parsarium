# CPP × ZIP: selected parsers

10 control-verified third-party paths selected from 27 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

GitHub stars of primary upstream repository, where package-specific and available.

| Rank | Package | Release | GitHub stars | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [sqlite](https://www.sqlite.org/zipfile.html) | 3.54.1 | 10,998 | entry name and decompressed entry bytes | SQLite Zipfile virtual table with zlib DEFLATE |
| 2 | [poco](https://github.com/pocoproject/poco/blob/poco-1.15.4-release/Zip/include/Poco/Zip/ZipArchive.h) | 1.15.4 | 9,499 | entry name and decompressed entry bytes | POCO Zip reader |
| 3 | [libarchive](https://github.com/libarchive/libarchive/blob/v3.8.11/libarchive/archive.h) | 3.8.11 | 3,672 | entry name and decompressed entry bytes | libarchive ZIP reader |
| 4 | [miniz](https://github.com/richgel999/miniz/blob/3.1.2/miniz_zip.h) | 3.1.2 | 2,918 | entry name and decompressed entry bytes | miniz ZIP reader |
| 5 | [kuba-zip](https://github.com/kuba--/zip/blob/v0.3.2/src/zip.h) | 0.3.2 | 1,615 | entry name and decompressed entry bytes | kuba-zip wrapper over bundled miniz |
| 6 | [minizip-ng](https://github.com/zlib-ng/minizip-ng/blob/4.2.2/mz_zip_rw.h) | 4.2.2 | 1,511 | entry name and decompressed entry bytes | MiniZip lineage |
| 7 | [libzip](https://libzip.org/documentation/zip_open/) | 1.12.1 | 1,060 | entry name and decompressed entry bytes | libzip ZIP reader |
| 8 | [bit7z](https://github.com/rikyoz/bit7z/blob/v4.1.0/include/bit7z/bitarchivereader.hpp) | 4.1.0 | 858 | entry name and decompressed entry bytes | bit7z wrapper over SevenZip ZIP reader |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [libgsf](https://gnome.pages.gitlab.gnome.org/libgsf/api/gsf-Zip.html) | 1.14.60 | [Debian installations (popcon)](https://sources.debian.org/src/libgsf/) | 86,949 | entry name and decompressed entry bytes | libgsf ZIP reader |
| 2 | [karchive](https://api.kde.org/kzip.html) | 6.31.0 | [Debian installations (popcon)](https://sources.debian.org/src/karchive/) | 44,046 | entry name and decompressed entry bytes | KArchive KZip reader |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
