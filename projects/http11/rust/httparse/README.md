# httparse — HTTP/1.1 / Rust

Pinned release: `1.10.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/httparse/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust httparse
python3 parsarium.py run http11 rust httparse controls/http11/request.http
python3 parsarium.py replay http11 rust httparse CORPUS_DIR runs/http11-httparse-replay
python3 parsarium.py afl build http11 rust httparse
python3 parsarium.py afl prepare http11 rust httparse runs/http11-httparse-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
