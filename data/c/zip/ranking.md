# C × ZIP: verified parser ranking

10 verified third-party package paths; working goal 20, ceiling 30. The metric is GitHub repository stars captured at 2026-11-12T07:50:21.979330+00:00. The captured Conan Center recipe-name surface provides no comparable per-recipe download counts. Stars are a repository-level adoption proxy, compared only within C, and do not establish a complete most-used set. 2 path(s) lack a metric and remain unranked.

Search hits, unresolved leads, and the C standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [libarchive](https://github.com/libarchive/libarchive/blob/v3.8.11/libarchive/archive.h) | 3.8.11 | 3,672 | entry name and decompressed entry bytes | libarchive ZIP reader |
| 2 | [miniz](https://github.com/richgel999/miniz/blob/3.1.2/miniz_zip.h) | 3.1.2 | 2,918 | entry name and decompressed entry bytes | miniz ZIP reader |
| 3 | [kuba-zip](https://github.com/kuba--/zip/blob/v0.3.2/src/zip.h) | 0.3.2 | 1,615 | entry name and decompressed entry bytes | kuba-zip wrapper over bundled miniz |
| 4 | [minizip-ng](https://github.com/zlib-ng/minizip-ng/blob/4.2.2/mz_zip_rw.h) | 4.2.2 | 1,511 | entry name and decompressed entry bytes | MiniZip lineage |
| 5 | [libzip](https://libzip.org/documentation/zip_open/) | 1.12.1 | 1,060 | entry name and decompressed entry bytes | libzip ZIP reader |
| 6 | [physfs](https://github.com/icculus/physfs/blob/release-3.2.0/src/physfs.h) | 3.2.0 | 844 | mounted ZIP entry name and decompressed entry bytes | PhysicsFS ZIP archiver |
| 7 | [unarr](https://github.com/selmf/unarr/blob/v1.2.0/unarr.h.in) | 1.2.0 | 92 | entry name and decompressed entry bytes | unarr ZIP reader |
| 8 | [zziplib](https://github.com/gdraheim/zziplib/blob/v0.13.80/zzip/zzip.h) | 0.13.80 | 70 | entry name and decompressed entry bytes | ZZIPlib ZIP reader |
| unranked | [libgsf](https://gnome.pages.gitlab.gnome.org/libgsf/api/gsf-Zip.html) | 1.14.60 | unknown | entry name and decompressed entry bytes | libgsf ZIP reader |
| unranked | [minizip](https://github.com/madler/zlib/blob/v1.4/contrib/minizip/unzip.h) | 1.4 | unknown | entry name and decompressed entry bytes | classic MiniZip |
