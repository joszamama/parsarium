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

The documented `lws_adopt_socket_vhost_readbuf` API accepts at most 2048 initial bytes; the harness and replay reject larger inputs before calling libwebsockets. Header and query copy failures reject the parse.
