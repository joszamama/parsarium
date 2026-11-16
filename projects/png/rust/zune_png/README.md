# zune-png — PNG / Rust

Pinned release: `0.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/zune-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust zune_png
python3 parsarium.py run png rust zune_png controls/png/red-green.png
python3 parsarium.py replay png rust zune_png CORPUS_DIR runs/png-zune_png-replay
python3 parsarium.py afl build png rust zune_png
python3 parsarium.py afl prepare png rust zune_png runs/png-zune_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
