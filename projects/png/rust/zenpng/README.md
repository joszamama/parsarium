# zenpng — PNG / Rust

Pinned release: `0.1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/zenpng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust zenpng
python3 parsarium.py run png rust zenpng controls/png/red-green.png
python3 parsarium.py replay png rust zenpng CORPUS_DIR runs/png-zenpng-replay
python3 parsarium.py afl build png rust zenpng
python3 parsarium.py afl prepare png rust zenpng runs/png-zenpng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
