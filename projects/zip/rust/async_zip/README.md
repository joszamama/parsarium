# async_zip — ZIP / Rust

Pinned release: `0.0.19`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/async-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust async_zip
python3 parsarium.py run zip rust async_zip controls/zip/hello.zip
python3 parsarium.py replay zip rust async_zip CORPUS_DIR runs/zip-async_zip-replay
python3 parsarium.py afl build zip rust async_zip
python3 parsarium.py afl prepare zip rust async_zip runs/zip-async_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
