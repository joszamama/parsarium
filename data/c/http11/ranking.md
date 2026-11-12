# C × HTTP/1.1: verified parser ranking

5 verified package paths; working goal 20, original ceiling 30. GitHub stars are project-level interest signals captured at 2026-11-12T20:49:34.855545+00:00; they are compared only within C. They are not downloads or a measure of actual parser use.

Search hits, unresolved leads, and C standard APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mongoose](https://mongoose.ws/docs/api/http/#mg_http_parse) | 7.23 | 13,131 | HTTP/1.1 GET request method, target, query and version | Mongoose C HTTP request parser; related to CivetWeb and LibHTTP ancestry |
| 2 | [http-parser](https://github.com/nodejs/http-parser#usage) | 2.9.4 | 6,434 | HTTP/1.1 GET request method, target and version after complete header parse | Node http-parser C state machine, predecessor design to llhttp |
| 3 | [picohttpparser](https://github.com/h2o/picohttpparser#phr_parse_request) | 1.5 | 2,114 | HTTP/1.1 GET request method, target and version after complete header parse | PicoHTTPParser C request parser, used by H2O |
| 4 | [llhttp](https://github.com/nodejs/llhttp#usage) | 9.4.3 | 1,955 | HTTP/1.1 GET request method, target and version after complete header parse | llhttp generated HTTP/1 parser, descended from Node http-parser design |
| 5 | [httpp](https://github.com/cebem1nt/httpp#api) | 2.0.0 | 10 | HTTP/1.1 GET request method, target and version | httpp C single-header request parser |
