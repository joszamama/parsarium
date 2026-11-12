# C × HTTP/1.1: verified parser ranking

7 verified package paths; working goal 20, original ceiling 30. GitHub stars are project-level interest signals captured at 2026-11-12T20:57:01.563112+00:00; they are compared only within C. They are not downloads or a measure of actual parser use. GNU libmicrohttpd has no primary GitHub repository and remains unranked.

Search hits, unresolved leads, and C standard APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mongoose](https://mongoose.ws/docs/api/http/#mg_http_parse) | 7.23 | 13,131 | HTTP/1.1 GET request method, target, query and version | Mongoose C HTTP request parser; related to CivetWeb and LibHTTP ancestry |
| 2 | [http-parser](https://github.com/nodejs/http-parser#usage) | 2.9.4 | 6,434 | HTTP/1.1 GET request method, target and version after complete header parse | Node http-parser C state machine, predecessor design to llhttp |
| 3 | [picohttpparser](https://github.com/h2o/picohttpparser#phr_parse_request) | 1.5 | 2,114 | HTTP/1.1 GET request method, target and version after complete header parse | PicoHTTPParser C request parser, used by H2O |
| 4 | [llhttp](https://github.com/nodejs/llhttp#usage) | 9.4.3 | 1,955 | HTTP/1.1 GET request method, target and version after complete header parse | llhttp generated HTTP/1 parser, descended from Node http-parser design |
| 5 | [HTTPParserC](https://github.com/Building42/HTTPParserC#documentation) | 9.2.0 | 31 | HTTP/1.1 GET request method, target and version after complete header parse | Building42 packaged llhttp 9.2.0 generated C source; shares the llhttp engine and is a separate versioned distribution |
| 6 | [httpp](https://github.com/cebem1nt/httpp#api) | 2.0.0 | 10 | HTTP/1.1 GET request method, target and version | httpp C single-header request parser |
| unranked | [libmicrohttpd](https://www.gnu.org/software/libmicrohttpd/manual/libmicrohttpd.pdf) | 1.0.10 | n/a | HTTP/1.1 GET request method, path, query argument and version from local socket stream | GNU libmicrohttpd HTTP/1 request parser in an embedded C server, separate from llhttp and PicoHTTPParser |
