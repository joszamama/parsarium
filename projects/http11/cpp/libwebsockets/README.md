# libwebsockets — HTTP/1.1 / C++

Pinned release: `5.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/cpp/libwebsockets/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 cpp libwebsockets
python3 parsarium.py run http11 cpp libwebsockets controls/http11/request.http
python3 parsarium.py replay http11 cpp libwebsockets CORPUS_DIR runs/http11-libwebsockets-replay
python3 parsarium.py afl build http11 cpp libwebsockets
python3 parsarium.py afl prepare http11 cpp libwebsockets runs/http11-libwebsockets-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

## Status

Staged. The Docker image has not been built and no `verification.json` receipt exists, so this path is not yet counted as runnable.

## Harness notes

- Each input becomes the initial read buffer of a local socketpair adopted with `lws_adopt_socket_vhost_readbuf` on one persistent `CONTEXT_PORT_NO_LISTEN_SERVER` context. Nothing is written to the socket.
- `method`, `path` and `host` are read inside `LWS_CALLBACK_HTTP` from lws's parsed header table. `path` is the URI after lws urldecoding and path normalization, followed by the URI-argument fragments rejoined with `&`.
- Requests that span more than one service chunk are finished with bounded direct `lws_service_fd` calls; a connection still open after that is closed synchronously, so no state carries into the next input.
- The build keeps the plain-TCP HTTP/1 server role only (no TLS, client, HTTP/2, HTTP/3 or Secure Streams) and the library's default header limits. Requests whose stored headers exceed about 4 KB are rejected by lws and produce no output.
