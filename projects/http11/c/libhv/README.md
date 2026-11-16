# libhv — HTTP/1.1 / C

Pinned release: `1.3.1`. [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/libhv/README.md)

This harness calls the C HTTP parser bundled in libhv: `http_parser_init(HTTP_REQUEST)`, `http_parser_execute` with `on_url` and `on_headers_complete` callbacks, and `http_method_str`. It reads local bytes only. A parse counts only if every byte is consumed, the parser reports no error, and headers are complete.

The harness accepts at most 1 MiB per input and allocates target storage to match the input length, so callback fragments are joined without a fixed path-length limit.

The parser is not libhv's own engine. libhv 1.3.1 ships a modified copy of Node/Joyent http-parser 2.9.1 (MIT) in `http/http_parser.c`. libhv moved `http_method_str` into `http/httpdef.c`. That makes it the same parser family as [Node http-parser 2.9.4](../http-parser/README.md). The two are separate builds of one engine, not two independent parsers. The libhv wrapper code is BSD-3-Clause.

The Docker build checks the pinned release archive and the SHA-256 of each bundled file it compiles.

The pinned Docker control parsed `GET /parsarium?x=1 HTTP/1.1`, covered 398 lines under libhv's bundled HTTP parser sources, and produced 272 AFL++ feedback edges.

## Run from the repository root

```sh
python3 parsarium.py build http11 c libhv
python3 parsarium.py run http11 c libhv controls/http11/request.http
python3 parsarium.py replay http11 c libhv CORPUS_DIR runs/http11-libhv-c-replay
python3 parsarium.py afl build http11 c libhv
python3 parsarium.py afl prepare http11 c libhv runs/http11-libhv-c-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
