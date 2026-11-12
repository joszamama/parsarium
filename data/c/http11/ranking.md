# C × HTTP/1.1: verified parser ranking

9 verified package paths; working goal 20, original ceiling 30. GitHub stars are project-level interest signals captured at 2026-11-12T21:06:06.160603+00:00 for the first eight and 2026-11-12T21:09:27+00:00 for libhtp; they are compared only within C. The libhtp count came from the primary repository HTML when the GitHub API was rate limited. Stars are not downloads or a measure of actual parser use. Packages without a primary GitHub repository remain unranked.

Search hits, unresolved leads, and C standard APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mongoose](https://mongoose.ws/docs/api/http/#mg_http_parse) | 7.23 | 13,131 | HTTP/1.1 GET request method, target, query and version | Mongoose C HTTP request parser; related to CivetWeb and LibHTTP ancestry |
| 2 | [http-parser](https://github.com/nodejs/http-parser#usage) | 2.9.4 | 6,434 | HTTP/1.1 GET request method, target and version after complete header parse | Node http-parser C state machine, predecessor design to llhttp |
| 3 | [picohttpparser](https://github.com/h2o/picohttpparser#phr_parse_request) | 1.5 | 2,114 | HTTP/1.1 GET request method, target and version after complete header parse | PicoHTTPParser C request parser, used by H2O |
| 4 | [llhttp](https://github.com/nodejs/llhttp#usage) | 9.4.3 | 1,955 | HTTP/1.1 GET request method, target and version after complete header parse | llhttp generated HTTP/1 parser, descended from Node http-parser design |
| 5 | [libhtp](https://github.com/OISF/libhtp/blob/0.5.53/docs/QUICK_START) | 0.5.53 | 306 | HTTP/1.1 GET request method, target, version and parsed header table from local byte buffer | OISF LibHTP independent C HTTP request/response stream parser |
| 6 | [libevhtp](https://github.com/ellzey/libevhtp/blob/1.2.9/htparse/htparse.h) | 1.2.9 | 42 | HTTP/1.1 GET request method, path, query and version after complete headers | libevhtp bundled htparse C HTTP/1 request scanner; source distributed and header installed by libevhtp |
| 7 | [HTTPParserC](https://github.com/Building42/HTTPParserC#documentation) | 9.2.0 | 31 | HTTP/1.1 GET request method, target and version after complete header parse | Building42 packaged llhttp 9.2.0 generated C source; shares the llhttp engine and is a separate versioned distribution |
| 8 | [httpp](https://github.com/cebem1nt/httpp#api) | 2.0.0 | 10 | HTTP/1.1 GET request method, target and version | httpp C single-header request parser |
| unranked | [libmicrohttpd](https://www.gnu.org/software/libmicrohttpd/manual/libmicrohttpd.pdf) | 1.0.10 | n/a | HTTP/1.1 GET request method, path, query argument and version from local socket stream | GNU libmicrohttpd HTTP/1 request parser in an embedded C server, separate from llhttp and PicoHTTPParser |
