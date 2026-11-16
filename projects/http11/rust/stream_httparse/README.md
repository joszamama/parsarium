# stream-httparse — HTTP/1.1 / Rust

Pinned release: `0.2.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/stream-httparse/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust stream_httparse
python3 parsarium.py run http11 rust stream_httparse controls/http11/request.http
python3 parsarium.py replay http11 rust stream_httparse CORPUS_DIR runs/http11-stream_httparse-replay
python3 parsarium.py afl build http11 rust stream_httparse
python3 parsarium.py afl prepare http11 rust stream_httparse runs/http11-stream_httparse-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
