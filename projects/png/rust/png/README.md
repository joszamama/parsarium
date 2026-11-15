# png — PNG / Rust

Pinned release: `0.18.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust png
python3 parsarium.py run png rust png controls/png/red-green.png
python3 parsarium.py replay png rust png CORPUS_DIR runs/png-png-replay
python3 parsarium.py afl build png rust png
python3 parsarium.py afl prepare png rust png runs/png-png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
