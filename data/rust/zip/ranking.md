# Rust × ZIP: verified parser ranking

20 verified third-party crate paths; working goal 20, original ceiling 30. The metric is crates.io crate-level recent downloads over 90 days, captured at 2026-11-12T00:50:18.278018+00:00. It includes all releases of each crate name and is compared only within Rust. 0 crate(s) lack a metric and remain unranked; equal counts share a rank.

Search hits, unresolved leads, and the standard-library inventory are separate from this ranking. See `cell.json`, `leads.json`, and `verification.json` in this directory.

| Rank | Crate | Pinned release | 90-day downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [zip](https://docs.rs/zip/9.5.1/zip/) | 9.5.1 | 102,480,927 | Entry name and decompressed text | zip-rs lineage |
| 2 | [async_zip](https://docs.rs/async_zip/0.0.19/async_zip/) | 0.0.19 | 2,587,792 | Entry name and decompressed text via deprecated memory API | rs-async-zip lineage |
| 3 | [eazip](https://docs.rs/crate/eazip/0.2.7/source/src/lib.rs) | 0.2.7 | 1,162,159 | Entry name and decompressed text | eazip engine |
| 4 | [astral_async_zip](https://docs.rs/astral_async_zip/0.0.22/async_zip/) | 0.0.22 | 872,021 | Entry name and decompressed text | rs-async-zip lineage |
| 5 | [rc-zip-sync](https://docs.rs/rc-zip-sync/4.4.2/rc_zip_sync/) | 4.4.2 | 657,483 | Entry name and decompressed text | rc-zip engine |
| 6 | [rawzip](https://docs.rs/rawzip/0.5.2/rawzip/) | 0.5.2 | 469,819 | Entry name and externally DEFLATE-decoded text | rawzip engine |
| 7 | [zip-extract](https://docs.rs/zip-extract/0.4.1/zip_extract/) | 0.4.1 | 411,375 | Extracted entry name and text | zip-rs lineage |
| 8 | [zip_structs](https://docs.rs/zip_structs/0.2.1/zip_structs/zip_local_file_header/) | 0.2.1 | 229,632 | ZIP local-header entry name and declared size | zip_structs header reader |
| 9 | [tinyzip](https://docs.rs/tinyzip/0.4.0/tinyzip/) | 0.4.0 | 200,657 | Entry name and externally DEFLATE-decoded text | tinyzip engine |
| 10 | [zip-extensions](https://docs.rs/zip-extensions/0.14.1/zip_extensions/) | 0.14.1 | 121,691 | Decompressed named ZIP entry | zip-rs lineage |
| 11 | [piz](https://docs.rs/piz/0.5.1/piz/) | 0.5.1 | 16,466 | Entry name and decompressed text | piz engine |
| 12 | [libarchive2](https://docs.rs/libarchive2/0.2.1/libarchive2/) | 0.2.1 | 15,462 | ZIP entry name and decompressed text | libarchive native engine |
| 13 | [archiver-rs](https://docs.rs/archiver-rs/0.5.1/archiver_rs/struct.Zip.html) | 0.5.1 | 13,231 | ZIP entry name and count | zip-rs lineage |
| 14 | [openpack](https://docs.rs/openpack/0.2.7/openpack/) | 0.2.7 | 12,593 | Entry name and decompressed text | zip-rs lineage |
| 15 | [zip-forensic-core](https://docs.rs/zip-forensic-core/0.2.3/zip_core/) | 0.2.3 | 12,319 | ZIP entry name and decompressed text | zip-forensic-core engine |
| 16 | [oxiarc-archive](https://docs.rs/oxiarc-archive/0.4.2/oxiarc_archive/) | 0.4.2 | 7,355 | Entry name and decompressed text | OxiArc ZIP engine |
| 17 | [archive-core](https://docs.rs/archive-core/0.1.6/archive_core/) | 0.1.6 | 6,149 | ZIP entry name and decompressed text | zip-forensic-core engine |
| 18 | [s-zip](https://docs.rs/s-zip/0.15.0/s_zip/) | 0.15.0 | 4,188 | Entry name and decompressed text | s-zip engine |
| 19 | [zip_next](https://docs.rs/zip_next/1.1.1/zip_next/) | 1.1.1 | 3,805 | Entry name and decompressed text | zip-rs lineage |
| 20 | [zip-lzma](https://docs.rs/zip-lzma/0.6.3/zip_lzma/) | 0.6.3 | 2,296 | Entry name and decompressed text | zip-rs lineage |
