# oxideav-png — PNG / Rust

Pinned release: `0.1.14`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/oxideav-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust oxideav_png
python3 parsarium.py run png rust oxideav_png controls/png/red-green.png
python3 parsarium.py replay png rust oxideav_png CORPUS_DIR runs/png-oxideav_png-replay
python3 parsarium.py afl build png rust oxideav_png
python3 parsarium.py afl prepare png rust oxideav_png runs/png-oxideav_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
