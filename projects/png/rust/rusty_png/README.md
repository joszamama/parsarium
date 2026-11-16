# rusty_png — PNG / Rust

Pinned release: `0.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/rusty-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust rusty_png
python3 parsarium.py run png rust rusty_png controls/png/red-green.png
python3 parsarium.py replay png rust rusty_png CORPUS_DIR runs/png-rusty_png-replay
python3 parsarium.py afl build png rust rusty_png
python3 parsarium.py afl prepare png rust rusty_png runs/png-rusty_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
