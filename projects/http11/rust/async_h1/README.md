# async-h1 — HTTP/1.1 / Rust

Pinned release: `2.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/async-h1/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust async_h1
python3 parsarium.py run http11 rust async_h1 controls/http11/response.http
python3 parsarium.py replay http11 rust async_h1 CORPUS_DIR runs/http11-async_h1-replay
python3 parsarium.py afl build http11 rust async_h1
python3 parsarium.py afl prepare http11 rust async_h1 runs/http11-async_h1-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
