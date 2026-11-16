# xibalba-proto — HTTP/1.1 / Rust

Pinned release: `0.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/xibalba-proto/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust xibalba_proto
python3 parsarium.py run http11 rust xibalba_proto controls/http11/response.http
python3 parsarium.py replay http11 rust xibalba_proto CORPUS_DIR runs/http11-xibalba_proto-replay
python3 parsarium.py afl build http11 rust xibalba_proto
python3 parsarium.py afl prepare http11 rust xibalba_proto runs/http11-xibalba_proto-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
