# http-muncher — HTTP/1.1 / Rust

Pinned release: `0.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/http-muncher/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust http_muncher
python3 parsarium.py run http11 rust http_muncher controls/http11/request.http
python3 parsarium.py replay http11 rust http_muncher CORPUS_DIR runs/http11-http_muncher-replay
python3 parsarium.py afl build http11 rust http_muncher
python3 parsarium.py afl prepare http11 rust http_muncher runs/http11-http_muncher-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
