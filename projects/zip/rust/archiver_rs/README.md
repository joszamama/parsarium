# archiver-rs — ZIP / Rust

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/archiver-rs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust archiver_rs
python3 parsarium.py run zip rust archiver_rs controls/zip/hello.zip
python3 parsarium.py replay zip rust archiver_rs CORPUS_DIR runs/zip-archiver_rs-replay
python3 parsarium.py afl build zip rust archiver_rs
python3 parsarium.py afl prepare zip rust archiver_rs runs/zip-archiver_rs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
