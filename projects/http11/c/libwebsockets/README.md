# libwebsockets — HTTP/1.1 / C

Pinned release: `5.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/libwebsockets/README.md)

The pinned Docker control parsed the GET method, target, and Host header. LLVM coverage reached 3,142 libwebsockets source lines, including 478 in `roles/http/parsers.c`; AFL++ produced 1,862 feedback edges.

## Parser family

This is the same libwebsockets HTTP/1 parser as [the C++ path](../../cpp/libwebsockets/README.md). Both build the same pinned source with the same options. Count them as one parser engine reached from two harness languages, not two independent engines.

## What the harness does

`harness.c` is C11 and is compiled with clang. It creates one libwebsockets context in no-listen server mode. For each input it opens a local `AF_UNIX` socketpair and passes one end, together with the input bytes, to `lws_adopt_socket_vhost_readbuf`. lws parses the bytes as the connection's first read. In `LWS_CALLBACK_HTTP` the harness reads back:

- the method, from the first request-line token that is set (`GET`, `POST`, `OPTIONS`, `PUT`, `PATCH`, `DELETE`, `CONNECT`, `HEAD`);
- the path lws passes to the callback (urldecoded and normalized), followed by `?` and the query arguments joined with `&`;
- the `Host` header.

A missing value is printed as an empty string. No network socket is opened and nothing is written to the socketpair.

## Harness caps

- Inputs larger than 2048 bytes are rejected before parsing, matching the documented limit for `lws_adopt_socket_vhost_readbuf`.
- If a request is not finished during adoption, the peer end is shut down and lws gets at most 64 service calls to finish or close it.
- `fd_limit_per_thread` is 16, so lws does not size its fd table from `ulimit -n`.
- One input is parsed at a time. Each call closes its connection before it returns, whatever the outcome.
- lws's own header-table limits stay at their defaults.

## Run from the repository root

```sh
python3 parsarium.py build http11 c libwebsockets
python3 parsarium.py run http11 c libwebsockets controls/http11/request.http
python3 parsarium.py replay http11 c libwebsockets CORPUS_DIR runs/http11-libwebsockets-c-replay
python3 parsarium.py afl build http11 c libwebsockets
python3 parsarium.py afl prepare http11 c libwebsockets runs/http11-libwebsockets-c-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
