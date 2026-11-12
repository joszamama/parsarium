# C++ × ZIP: verified parser ranking

27 verified third-party package paths; working goal 20, ceiling 30. The metric is GitHub repository stars captured between 2026-11-12T07:50:21.979330+00:00 and 2026-11-12T11:50:06.305574+00:00. The captured Conan Center recipe-name surface provides no comparable per-recipe download counts. Stars are a repository-level adoption proxy, compared only within C++, and do not establish a complete most-used set. 4 path(s) lack a metric and remain unranked.

Search hits, unresolved leads, and the C++ standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [sqlite](https://www.sqlite.org/zipfile.html) | 3.54.1 | 10,998 | entry name and decompressed entry bytes | SQLite Zipfile virtual table with zlib DEFLATE |
| 2 | [poco](https://github.com/pocoproject/poco/blob/poco-1.15.4-release/Zip/include/Poco/Zip/ZipArchive.h) | 1.15.4 | 9,499 | entry name and decompressed entry bytes | POCO Zip reader |
| 3 | [libarchive](https://github.com/libarchive/libarchive/blob/v3.8.11/libarchive/archive.h) | 3.8.11 | 3,672 | entry name and decompressed entry bytes | libarchive ZIP reader |
| 4 | [miniz](https://github.com/richgel999/miniz/blob/3.1.2/miniz_zip.h) | 3.1.2 | 2,918 | entry name and decompressed entry bytes | miniz ZIP reader |
| 5 | [kuba-zip](https://github.com/kuba--/zip/blob/v0.3.2/src/zip.h) | 0.3.2 | 1,615 | entry name and decompressed entry bytes | kuba-zip wrapper over bundled miniz |
| 6 | [minizip-ng](https://github.com/zlib-ng/minizip-ng/blob/4.2.2/mz_zip_rw.h) | 4.2.2 | 1,511 | entry name and decompressed entry bytes | MiniZip lineage |
| 7 | [libzip](https://libzip.org/documentation/zip_open/) | 1.12.1 | 1,060 | entry name and decompressed entry bytes | libzip ZIP reader |
| 8 | [bit7z](https://github.com/rikyoz/bit7z/blob/v4.1.0/include/bit7z/bitarchivereader.hpp) | 4.1.0 | 858 | entry name and decompressed entry bytes | bit7z wrapper over SevenZip ZIP reader |
| 9 | [physfs](https://github.com/icculus/physfs/blob/release-3.2.0/src/physfs.h) | 3.2.0 | 844 | mounted ZIP entry name and decompressed entry bytes | PhysicsFS ZIP archiver |
| 10 | [quazip](https://github.com/stachenov/quazip/blob/v1.7.2/quazip/quazip.h) | 1.7.2 | 699 | entry name and decompressed entry bytes | QuaZip wrapper over classic MiniZip |
| 11 | [sebastiandev-zipper](https://github.com/sebastiandev/zipper/blob/v1.0.3/README.md) | 1.0.3 | 534 | entry name and decompressed entry bytes | Sebastian Zipper wrapper over classic MiniZip fork |
| 12 | [libzippp](https://github.com/ctabin/libzippp/blob/libzippp-v7.1-1.10.1/src/libzippp.h) | 7.1-1.10.1 | 465 | entry name and decompressed entry bytes | libzippp wrapper over libzip |
| 13 | [zipper](https://github.com/Lecrapouille/zipper/blob/v4.0.0/include/Zipper/Unzipper.hpp) | 4.0.0 | 99 | entry name and decompressed entry bytes | Zipper wrapper over classic MiniZip fork |
| 14 | [qarchive](https://github.com/antony-jr/QArchive/blob/v2.2.8/include/qarchivememoryextractor.hpp) | 2.2.8 | 97 | entry name and decompressed entry bytes | QArchive wrapper over libarchive |
| 15 | [unarr](https://github.com/selmf/unarr/blob/v1.2.0/unarr.h.in) | 1.2.0 | 92 | entry name and decompressed entry bytes | unarr ZIP reader |
| 16 | [zziplib](https://github.com/gdraheim/zziplib/blob/v0.13.80/zzip/zzip.h) | 0.13.80 | 70 | entry name and decompressed entry bytes | ZZIPlib ZIP reader |
| 17 | [unziplib](https://github.com/bitbank2/unzipLIB/blob/1.0.0/src/unzip.h) | 1.0.0 | 69 | entry name and decompressed entry bytes | unzipLIB modified classic MiniZip |
| 18 | [junzip](https://github.com/jokkebk/JUnzip/blob/v0.1.1/junzip.h) | v0.1.1 | 63 | entry name and decompressed entry bytes | JUnzip ZIP record reader with zlib DEFLATE |
| 19 | [zipios](https://github.com/Zipios/Zipios/blob/2.3.4/zipios/zipfile.hpp) | 2.3.4 | 54 | entry name and decompressed entry bytes | Zipios ZIP reader |
| 20 | [lowzip](https://github.com/svaarala/lowzip/blob/v1.0.1/README.md) | 1.0.1 | 46 | entry name and decompressed entry bytes | lowzip ZIP reader |
| 21 | [troldal-zippy](https://github.com/troldal/KZip/blob/a838de8522f9051df0d1b202473bb6befe648702/library/Zippy/ZipArchive.hpp) | cci.20200622 | 32 | entry name and decompressed entry bytes | Troldal Zippy wrapper over bundled miniz |
| 22 | [libc7zip](https://github.com/itchio/libc7zip/blob/v1.10.0/include/libc7zip.h) | v1.10.0 | 18 | entry name and decompressed entry bytes | libc7zip → lib7zip → 7-Zip ZIP engine |
| 23 | [zipc](https://www.msweet.org/zipc/zipc.html) | v1.3 | 13 | decompressed bytes for a known named ZIP entry; no entry enumeration API verified | zipc ZIP container reader with zlib DEFLATE |
| unranked | [infozip-unzip](https://github.com/madler/unzip/blob/master/unzip.h) | 6.0 | unknown | entry name parsed by Info-ZIP listing and decompressed entry bytes from its C API | Info-ZIP UnZip 6.0 engine |
| unranked | [karchive](https://api.kde.org/kzip.html) | 6.31.0 | unknown | entry name and decompressed entry bytes | KArchive KZip reader |
| unranked | [libgsf](https://gnome.pages.gitlab.gnome.org/libgsf/api/gsf-Zip.html) | 1.14.60 | unknown | entry name and decompressed entry bytes | libgsf ZIP reader |
| unranked | [minizip](https://github.com/madler/zlib/blob/v1.4/contrib/minizip/unzip.h) | 1.4 | unknown | entry name and decompressed entry bytes | classic MiniZip |
