# C × ZIP: verified parser ranking

16 verified third-party package paths; working goal 20, ceiling 30. The metric is GitHub repository stars captured between 2026-11-12T07:50:21.979330+00:00 and 2026-11-12T11:45:39.757179+00:00. The captured Conan Center recipe-name surface provides no comparable per-recipe download counts. Stars are a repository-level adoption proxy, compared only within C, and do not establish a complete most-used set. 3 path(s) lack a metric and remain unranked.

Search hits, unresolved leads, and the C standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [sqlite](https://www.sqlite.org/zipfile.html) | 3.54.1 | 10,998 | entry name and decompressed entry bytes | SQLite Zipfile virtual table with zlib DEFLATE |
| 2 | [libarchive](https://github.com/libarchive/libarchive/blob/v3.8.11/libarchive/archive.h) | 3.8.11 | 3,672 | entry name and decompressed entry bytes | libarchive ZIP reader |
| 3 | [miniz](https://github.com/richgel999/miniz/blob/3.1.2/miniz_zip.h) | 3.1.2 | 2,918 | entry name and decompressed entry bytes | miniz ZIP reader |
| 4 | [kuba-zip](https://github.com/kuba--/zip/blob/v0.3.2/src/zip.h) | 0.3.2 | 1,615 | entry name and decompressed entry bytes | kuba-zip wrapper over bundled miniz |
| 5 | [minizip-ng](https://github.com/zlib-ng/minizip-ng/blob/4.2.2/mz_zip_rw.h) | 4.2.2 | 1,511 | entry name and decompressed entry bytes | MiniZip lineage |
| 6 | [libzip](https://libzip.org/documentation/zip_open/) | 1.12.1 | 1,060 | entry name and decompressed entry bytes | libzip ZIP reader |
| 7 | [physfs](https://github.com/icculus/physfs/blob/release-3.2.0/src/physfs.h) | 3.2.0 | 844 | mounted ZIP entry name and decompressed entry bytes | PhysicsFS ZIP archiver |
| 8 | [unarr](https://github.com/selmf/unarr/blob/v1.2.0/unarr.h.in) | 1.2.0 | 92 | entry name and decompressed entry bytes | unarr ZIP reader |
| 9 | [zziplib](https://github.com/gdraheim/zziplib/blob/v0.13.80/zzip/zzip.h) | 0.13.80 | 70 | entry name and decompressed entry bytes | ZZIPlib ZIP reader |
| 10 | [unziplib](https://github.com/bitbank2/unzipLIB/blob/1.0.0/src/unzip.h) | 1.0.0 | 69 | entry name and decompressed entry bytes | unzipLIB modified classic MiniZip |
| 11 | [junzip](https://github.com/jokkebk/JUnzip/blob/v0.1.1/junzip.h) | v0.1.1 | 63 | entry name and decompressed entry bytes | JUnzip ZIP record reader with zlib DEFLATE |
| 12 | [lowzip](https://github.com/svaarala/lowzip/blob/v1.0.1/README.md) | 1.0.1 | 46 | entry name and decompressed entry bytes | lowzip ZIP reader |
| 13 | [libc7zip](https://github.com/itchio/libc7zip/blob/v1.10.0/include/libc7zip.h) | v1.10.0 | 18 | entry name and decompressed entry bytes | libc7zip → lib7zip → 7-Zip ZIP engine |
| unranked | [infozip-unzip](https://github.com/madler/unzip/blob/master/unzip.h) | 6.0 | unknown | entry name parsed by Info-ZIP listing and decompressed entry bytes from its C API | Info-ZIP UnZip 6.0 engine |
| unranked | [libgsf](https://gnome.pages.gitlab.gnome.org/libgsf/api/gsf-Zip.html) | 1.14.60 | unknown | entry name and decompressed entry bytes | libgsf ZIP reader |
| unranked | [minizip](https://github.com/madler/zlib/blob/v1.4/contrib/minizip/unzip.h) | 1.4 | unknown | entry name and decompressed entry bytes | classic MiniZip |
