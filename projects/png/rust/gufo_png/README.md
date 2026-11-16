# gufo-png — PNG / Rust

Pinned release: `0.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/gufo-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust gufo_png
python3 parsarium.py run png rust gufo_png controls/png/red-green-title.png
python3 parsarium.py replay png rust gufo_png CORPUS_DIR runs/png-gufo_png-replay
python3 parsarium.py afl build png rust gufo_png
python3 parsarium.py afl prepare png rust gufo_png runs/png-gufo_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
