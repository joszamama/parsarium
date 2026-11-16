# blazingly-wire — HTTP/1.1 / Rust

Pinned release: `0.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/blazingly-wire/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust blazingly_wire
python3 parsarium.py run http11 rust blazingly_wire controls/http11/request.http
python3 parsarium.py replay http11 rust blazingly_wire CORPUS_DIR runs/http11-blazingly_wire-replay
python3 parsarium.py afl build http11 rust blazingly_wire
python3 parsarium.py afl prepare http11 rust blazingly_wire runs/http11-blazingly_wire-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
