# RUST × HTTP/1.1: selected parsers

10 control-verified third-party paths selected from 22 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

crates.io recent downloads (90 days).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [httparse](https://docs.rs/httparse/1.10.1/httparse/) | 1.10.1 | 230,801,924 | request head: method, target, HTTP minor version, headers | httparse core |
| 2 | [async-h1](https://docs.rs/async-h1/2.3.4/async_h1/) | 2.3.4 | 585,900 | async response: status, body | httparse core |
| 3 | [async-http-codec](https://docs.rs/async-http-codec/0.8.0/async_http_codec/) | 0.8.0 | 277,503 | async request head: method, URI, version, fields | httparse core |
| 4 | [ntex-httparse](https://docs.rs/ntex-httparse/2.4.0/ntex_httparse/) | 2.4.0 | 66,776 | request line: method, target, HTTP minor version | ntex-httparse fork |
| 5 | [http-muncher](https://docs.rs/http-muncher/0.3.2/http_muncher/) | 0.3.2 | 17,242 | streaming request: method, target, version, consumed bytes | node/http-parser C binding |
| 6 | [shiguredo_http11](https://docs.rs/shiguredo_http11/2026.7.0-canary.2/shiguredo_http11/) | 2026.7.0-canary.2 | 9,884 | request head: method, URI, version | shiguredo_http11 |
| 7 | [minihttpse](https://docs.rs/minihttpse/0.1.6/minihttpse/) | 0.1.6 | 2,084 | response: status, reason, body | minihttpse |
| 8 | [http_parser](https://docs.rs/http_parser/0.0.2/http_parser/) | 0.0.2 | 1,823 | streaming request: method, target, version, consumed bytes | node/http-parser Rust port |
| 9 | [http-kit-h1](https://docs.rs/http-kit-h1/0.6.2/http_kit_h1/) | 0.6.2 | 1,462 | request head: method, URI, connection semantics | httparse core |
| 10 | [webparse](https://docs.rs/webparse/0.3.1/webparse/) | 0.3.1 | 801 | request: method, URL, consumed bytes | webparse |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
