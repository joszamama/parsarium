# image — PNG / Rust

Pinned release: `0.25.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust image
python3 parsarium.py run png rust image controls/png/red-green.png
python3 parsarium.py replay png rust image CORPUS_DIR runs/png-image-replay
python3 parsarium.py afl build png rust image
python3 parsarium.py afl prepare png rust image runs/png-image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
