# h2o — HTTP/1.1 / C++

Pinned release: `2.2.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/cpp/h2o/README.md)

The harness builds only `deps/picohttpparser` from the H2O 2.2.6 tarball and calls its `phr_parse_request` from C++17. This is the PicoHTTPParser family, shared with [C × HTTP/1.1 picohttpparser](../../c/picohttpparser/README.md), not an independent engine. The bundled copy is an older snapshot than standalone PicoHTTPParser 1.5: `picohttpparser.c` and `picohttpparser.h` differ byte-for-byte (for example, the status-code `PARSE_INT` range checks and `findchar_fast` range tables). [`source-lock.json`](source-lock.json) records both bundled file hashes.

## Run from the repository root

```sh
python3 parsarium.py build http11 cpp h2o
python3 parsarium.py run http11 cpp h2o controls/http11/request.http
python3 parsarium.py replay http11 cpp h2o CORPUS_DIR runs/http11-h2o-replay
python3 parsarium.py afl build http11 cpp h2o
python3 parsarium.py afl prepare http11 cpp h2o runs/http11-h2o-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
