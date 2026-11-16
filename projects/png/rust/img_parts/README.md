# img-parts — PNG / Rust

Pinned release: `0.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/img-parts/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust img_parts
python3 parsarium.py run png rust img_parts controls/png/red-green.png
python3 parsarium.py replay png rust img_parts CORPUS_DIR runs/png-img_parts-replay
python3 parsarium.py afl build png rust img_parts
python3 parsarium.py afl prepare png rust img_parts runs/png-img_parts-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
