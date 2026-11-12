# Rust × HTTP/1.1: verified parser ranking

22 verified third-party crate paths; working goal 20, original ceiling 30. The metric is crates.io crate-level recent downloads over 90 days, captured at 2026-11-12T02:11:52.659389+00:00. It includes all releases of each crate name and is compared only within Rust. 0 crate(s) lack a metric and remain unranked; equal counts share a rank.

Search hits, unresolved leads, and the standard-library inventory are separate from this ranking. See `cell.json`, `leads.json`, and `verification.json` in this directory.

| Rank | Crate | Pinned release | 90-day downloads | Scope | Underlying family |
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
| 11 | [sutegi-http](https://docs.rs/sutegi-http/0.13.0/sutegi_http/) | 0.13.0 | 556 | request: method, path, query, version | sutegi-http |
| 12 | [http-net](https://docs.rs/http-net/0.9.2/http_net/) | 0.9.2 | 470 | request head: method, target, version | http-net |
| 13 | [blazingly-wire](https://docs.rs/blazingly-wire/0.1.3/blazingly_wire/) | 0.1.3 | 180 | request head: method, target, connection semantics | httparse core |
| 14 | [request-http-parser](https://docs.rs/request-http-parser/0.1.4/request_http_parser/) | 0.1.4 | 150 | request: method, path, query, headers; does not expose HTTP version | request-http-parser |
| 15 | [xibalba-proto](https://docs.rs/xibalba-proto/0.4.0/xibalba_proto/) | 0.4.0 | 147 | response head: status and fields; body slice after consumed offset | xibalba-proto |
| 16 | [zenith-http1](https://docs.rs/zenith-http1/0.1.1/zenith_http1/) | 0.1.1 | 138 | response: status, fields, body | zenith-http1 |
| 17 | [weida-http-codec](https://docs.rs/weida-http-codec/0.1.0-alpha.14/weida_http_codec/) | 0.1.0-alpha.14 | 120 | request head: method, target, version, fields | weida-http-codec |
| 18 | [stream-httparse](https://docs.rs/stream-httparse/0.2.6/stream_httparse/) | 0.2.6 | 84 | streaming request: method, target, protocol | stream-httparse |
| 19 | [h11r](https://docs.rs/h11r/0.3.1/h11r/) | 0.3.1 | 79 | request event: method, target, version | httparse core |
| 20 | [xocomil](https://docs.rs/xocomil/0.3.0/xocomil/) | 0.3.0 | 8 | request head: method, target, version | xocomil |
| 21 | [thhp](https://docs.rs/thhp/0.2.0/thhp/) | 0.2.0 | 6 | request head: method, target, HTTP minor version, fields | thhp |
| 22 | [saf-httparser](https://docs.rs/saf-httparser/0.1.1/saf_httparser/) | 0.1.1 | 5 | request: method, URI, version | saf-httparser |
