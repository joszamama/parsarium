# nopng — PNG / Rust

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/nopng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust nopng
python3 parsarium.py run png rust nopng controls/png/red-green.png
python3 parsarium.py replay png rust nopng CORPUS_DIR runs/png-nopng-replay
python3 parsarium.py afl build png rust nopng
python3 parsarium.py afl prepare png rust nopng runs/png-nopng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
