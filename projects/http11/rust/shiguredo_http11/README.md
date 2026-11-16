# shiguredo_http11 — HTTP/1.1 / Rust

Pinned release: `2026.7.0-canary.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/shiguredo-http11/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust shiguredo_http11
python3 parsarium.py run http11 rust shiguredo_http11 controls/http11/request.http
python3 parsarium.py replay http11 rust shiguredo_http11 CORPUS_DIR runs/http11-shiguredo_http11-replay
python3 parsarium.py afl build http11 rust shiguredo_http11
python3 parsarium.py afl prepare http11 rust shiguredo_http11 runs/http11-shiguredo_http11-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
