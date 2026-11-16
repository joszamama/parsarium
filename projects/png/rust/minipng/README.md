# minipng — PNG / Rust

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/minipng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust minipng
python3 parsarium.py run png rust minipng controls/png/red-green.png
python3 parsarium.py replay png rust minipng CORPUS_DIR runs/png-minipng-replay
python3 parsarium.py afl build png rust minipng
python3 parsarium.py afl prepare png rust minipng runs/png-minipng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
