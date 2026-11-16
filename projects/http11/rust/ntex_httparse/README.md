# ntex-httparse — HTTP/1.1 / Rust

Pinned release: `2.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/ntex-httparse/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust ntex_httparse
python3 parsarium.py run http11 rust ntex_httparse controls/http11/request.http
python3 parsarium.py replay http11 rust ntex_httparse CORPUS_DIR runs/http11-ntex_httparse-replay
python3 parsarium.py afl build http11 rust ntex_httparse
python3 parsarium.py afl prepare http11 rust ntex_httparse runs/http11-ntex_httparse-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
