# libsoup — HTTP/1.1 / C

Pinned release: `3.8.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/libsoup/README.md)

This C harness calls `soup_headers_parse_request` from the same pinned libsoup source as the [C++ path](../../cpp/libsoup/README.md). Both paths reach one parser engine, so they count as one libsoup family, not two independent parsers.

The harness finds the end of the request head the way libsoup's HTTP/1 server reader does, and passes the head to libsoup without the final blank line, as the API requires. It rejects heads above libsoup's 100 KiB reader limit. Method, path and Host are copied at their parsed length, with no fixed size limit. Inputs above 1 MiB are rejected before parsing; that cap belongs to the harness, not to libsoup.

The pinned Docker control parsed the request method, target, version, and Host header. LLVM coverage reached 319 libsoup source lines, including 97 in `soup-headers.c`; the AFL++ overlay produced 203 feedback edges.

## Run from the repository root

```sh
python3 parsarium.py build http11 c libsoup
python3 parsarium.py run http11 c libsoup controls/http11/request.http
python3 parsarium.py replay http11 c libsoup CORPUS_DIR runs/http11-libsoup-c-replay
python3 parsarium.py afl build http11 c libsoup
python3 parsarium.py afl prepare http11 c libsoup runs/http11-libsoup-c-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
