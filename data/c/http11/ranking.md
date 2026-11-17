# C × HTTP/1.1: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

GitHub stargazers_count of primary upstream repository.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mongoose](https://mongoose.ws/docs/api/http/#mg_http_parse) | 7.23 | 13,131 | HTTP/1.1 GET request method, target, query and version | Mongoose C HTTP request parser; related to CivetWeb and LibHTTP ancestry |
| 2 | [h2o](https://github.com/h2o/h2o/blob/v2.2.6/deps/picohttpparser/README.md) | 2.2.6 | 11,568 | HTTP/1.1 GET request method, target, version and headers from local byte buffer via H2O-bundled parser | H2O 2.2.6 bundles PicoHTTPParser as its HTTP/1 parser; separate tagged H2O package distribution but same underlying parser family as h2o/picohttpparser 1.5, not an independent engine |
| 3 | [libhv](https://github.com/ithewei/libhv/blob/v1.3.1/http/http_parser.h) | 1.3.1 | 7,575 | HTTP/1.1 GET request method, target and version after complete header parse from local bytes | libhv bundles a modified Node http-parser 2.9.1 C engine; separate tagged library distribution but shared parser family with Node http-parser 2.9.4, not an independent engine |
| 4 | [http-parser](https://github.com/nodejs/http-parser#usage) | 2.9.4 | 6,434 | HTTP/1.1 GET request method, target and version after complete header parse | Node http-parser C state machine, predecessor design to llhttp |
| 5 | [libwebsockets](https://github.com/warmcat/libwebsockets/blob/v5.0.0/include/libwebsockets/lws-adopt.h) | 5.0.0 | 5,352 | HTTP/1.1 GET request method, path, query argument and Host header from local read buffer | libwebsockets C HTTP/1 parser in the server adoption path; independent from llhttp and LibHTP |
| 6 | [facil-legacy](https://github.com/boazsegev/facil.io/blob/0.7.6/lib/facil/http/parsers/http1_parser.h) | 0.7.6 | 2,415 | HTTP/1.1 GET request method, path, query, version and Host header after complete local-byte parse | facil.io 0.7 HTTP/1 parser, earlier distinct distribution and API of the facil.io family later developed as C STL 0.8; these two package paths share lineage |
| 7 | [picohttpparser](https://github.com/h2o/picohttpparser#phr_parse_request) | 1.5 | 2,114 | HTTP/1.1 GET request method, target and version after complete header parse | PicoHTTPParser C request parser, used by H2O |

## Supplemental numeric evidence

These paths lack a positive primary metric. Their figures are reported separately and are not compared numerically with the table above.

| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | [libsoup](https://libsoup.gnome.org/libsoup-3.0/func.headers_parse_request.html) | 3.8.1 | [Debian source installed count](https://sources.debian.org/src/libsoup/) | 137,466 | HTTP/1.1 GET request-head method, target, version and Host header from local byte buffer | GNOME libsoup 3 HTTP/1 request-head parser, independent from llhttp and PicoHTTPParser |
| 2 | [serf](https://github.com/apache/serf/blob/1.3.10/serf_bucket_types.h) | 1.3.10 | [Debian source installed count](https://sources.debian.org/src/serf/) | 19,931 | HTTP/1.1 response status, reason, Content-Type, Content-Length and body from local byte buffer | Apache Serf C HTTP/1 response bucket state machine; independent from libsoup and llhttp |
| 3 | [libmicrohttpd](https://www.gnu.org/software/libmicrohttpd/manual/libmicrohttpd.pdf) | 1.0.10 | [Debian source installed count](https://sources.debian.org/src/libmicrohttpd/) | 5,678 | HTTP/1.1 GET request method, path, query argument and version from local socket stream | GNU libmicrohttpd HTTP/1 request parser in an embedded C server, separate from llhttp and PicoHTTPParser |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
