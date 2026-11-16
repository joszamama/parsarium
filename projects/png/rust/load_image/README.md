# load_image — PNG / Rust

Pinned release: `3.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/load-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust load_image
python3 parsarium.py run png rust load_image controls/png/red-green.png
python3 parsarium.py replay png rust load_image CORPUS_DIR runs/png-load_image-replay
python3 parsarium.py afl build png rust load_image
python3 parsarium.py afl prepare png rust load_image runs/png-load_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
