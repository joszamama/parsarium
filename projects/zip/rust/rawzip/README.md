# rawzip — ZIP / Rust

Pinned release: `0.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/rawzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust rawzip
python3 parsarium.py run zip rust rawzip controls/zip/hello.zip
python3 parsarium.py replay zip rust rawzip CORPUS_DIR runs/zip-rawzip-replay
python3 parsarium.py afl build zip rust rawzip
python3 parsarium.py afl prepare zip rust rawzip runs/zip-rawzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
