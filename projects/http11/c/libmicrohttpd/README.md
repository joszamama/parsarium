# libmicrohttpd — HTTP/1.1 / C

Pinned release: `1.0.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/libmicrohttpd/README.md)

This path uses the same libmicrohttpd source and parser as the [C++ path](../../cpp/libmicrohttpd/README.md). The two paths are one parser reached from C and from C++, not two independent parsers.

The harness gives each input to a libmicrohttpd daemon over a local socket pair. It reports the method, the decoded path with its query arguments, and the version. Inputs above 1 MiB are rejected, and each input gets at most 5 seconds.

The pinned Docker control parsed the GET method, target, and HTTP version. LLVM coverage reached 3,130 libmicrohttpd source lines, including 1,509 in `connection.c`; AFL++ produced 1,105 feedback edges.

## Run from the repository root

```sh
python3 parsarium.py build http11 c libmicrohttpd
python3 parsarium.py run http11 c libmicrohttpd controls/http11/request.http
python3 parsarium.py replay http11 c libmicrohttpd CORPUS_DIR runs/http11-libmicrohttpd-c-replay
python3 parsarium.py afl build http11 c libmicrohttpd
python3 parsarium.py afl prepare http11 c libmicrohttpd runs/http11-libmicrohttpd-c-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
