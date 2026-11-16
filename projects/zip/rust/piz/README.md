# piz — ZIP / Rust

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/piz/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust piz
python3 parsarium.py run zip rust piz controls/zip/hello.zip
python3 parsarium.py replay zip rust piz CORPUS_DIR runs/zip-piz-replay
python3 parsarium.py afl build zip rust piz
python3 parsarium.py afl prepare zip rust piz runs/zip-piz-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
