# spng — PNG / Rust

Pinned release: `0.2.0-alpha.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/spng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust spng
python3 parsarium.py run png rust spng controls/png/red-green.png
python3 parsarium.py replay png rust spng CORPUS_DIR runs/png-spng-replay
python3 parsarium.py afl build png rust spng
python3 parsarium.py afl prepare png rust spng runs/png-spng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
