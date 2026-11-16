# zenith-http1 — HTTP/1.1 / Rust

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/zenith-http1/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust zenith_http1
python3 parsarium.py run http11 rust zenith_http1 controls/http11/response.http
python3 parsarium.py replay http11 rust zenith_http1 CORPUS_DIR runs/http11-zenith_http1-replay
python3 parsarium.py afl build http11 rust zenith_http1
python3 parsarium.py afl prepare http11 rust zenith_http1 runs/http11-zenith_http1-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
