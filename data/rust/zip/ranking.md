# RUST × ZIP: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

crates.io recent downloads (90 days).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
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

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
