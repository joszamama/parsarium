# C++ × ZIP: verified parser ranking

15 verified third-party package paths; working goal 20, ceiling 30. The metric is GitHub repository stars captured between 2026-11-12T07:50:21.979330+00:00 and 2026-11-12T08:29:12.999248+00:00. The captured Conan Center recipe-name surface provides no comparable per-recipe download counts. Stars are a repository-level adoption proxy, compared only within C++, and do not establish a complete most-used set. 2 path(s) lack a metric and remain unranked.

Search hits, unresolved leads, and the C++ standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [poco](https://github.com/pocoproject/poco/blob/poco-1.15.4-release/Zip/include/Poco/Zip/ZipArchive.h) | 1.15.4 | 9,499 | entry name and decompressed entry bytes | POCO Zip reader |
| 2 | [libarchive](https://github.com/libarchive/libarchive/blob/v3.8.11/libarchive/archive.h) | 3.8.11 | 3,672 | entry name and decompressed entry bytes | libarchive ZIP reader |
| 3 | [miniz](https://github.com/richgel999/miniz/blob/3.1.2/miniz_zip.h) | 3.1.2 | 2,918 | entry name and decompressed entry bytes | miniz ZIP reader |
| 4 | [kuba-zip](https://github.com/kuba--/zip/blob/v0.3.2/src/zip.h) | 0.3.2 | 1,615 | entry name and decompressed entry bytes | kuba-zip wrapper over bundled miniz |
| 5 | [minizip-ng](https://github.com/zlib-ng/minizip-ng/blob/4.2.2/mz_zip_rw.h) | 4.2.2 | 1,511 | entry name and decompressed entry bytes | MiniZip lineage |
| 6 | [libzip](https://libzip.org/documentation/zip_open/) | 1.12.1 | 1,060 | entry name and decompressed entry bytes | libzip ZIP reader |
| 7 | [bit7z](https://github.com/rikyoz/bit7z/blob/v4.1.0/include/bit7z/bitarchivereader.hpp) | 4.1.0 | 858 | entry name and decompressed entry bytes | bit7z wrapper over SevenZip ZIP reader |
| 8 | [libzippp](https://github.com/ctabin/libzippp/blob/libzippp-v7.1-1.10.1/src/libzippp.h) | 7.1-1.10.1 | 465 | entry name and decompressed entry bytes | libzippp wrapper over libzip |
| 9 | [zipper](https://github.com/Lecrapouille/zipper/blob/v4.0.0/include/Zipper/Unzipper.hpp) | 4.0.0 | 99 | entry name and decompressed entry bytes | Zipper wrapper over classic MiniZip fork |
| 10 | [unarr](https://github.com/selmf/unarr/blob/v1.2.0/unarr.h.in) | 1.2.0 | 92 | entry name and decompressed entry bytes | unarr ZIP reader |
| 11 | [zziplib](https://github.com/gdraheim/zziplib/blob/v0.13.80/zzip/zzip.h) | 0.13.80 | 70 | entry name and decompressed entry bytes | ZZIPlib ZIP reader |
| 12 | [zipios](https://github.com/Zipios/Zipios/blob/2.3.4/zipios/zipfile.hpp) | 2.3.4 | 54 | entry name and decompressed entry bytes | Zipios ZIP reader |
| 13 | [troldal-zippy](https://github.com/troldal/KZip/blob/a838de8522f9051df0d1b202473bb6befe648702/library/Zippy/ZipArchive.hpp) | cci.20200622 | 32 | entry name and decompressed entry bytes | Troldal Zippy wrapper over bundled miniz |
| unranked | [libgsf](https://gnome.pages.gitlab.gnome.org/libgsf/api/gsf-Zip.html) | 1.14.60 | unknown | entry name and decompressed entry bytes | libgsf ZIP reader |
| unranked | [minizip](https://github.com/madler/zlib/blob/v1.4/contrib/minizip/unzip.h) | 1.4 | unknown | entry name and decompressed entry bytes | classic MiniZip |
