# thhp — HTTP/1.1 / Rust

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/thhp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust thhp
python3 parsarium.py run http11 rust thhp controls/http11/request.http
python3 parsarium.py replay http11 rust thhp CORPUS_DIR runs/http11-thhp-replay
python3 parsarium.py afl build http11 rust thhp
python3 parsarium.py afl prepare http11 rust thhp runs/http11-thhp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
