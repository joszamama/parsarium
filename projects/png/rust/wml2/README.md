# wml2 — PNG / Rust

Pinned release: `0.0.45`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/wml2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust wml2
python3 parsarium.py run png rust wml2 controls/png/red-green.png
python3 parsarium.py replay png rust wml2 CORPUS_DIR runs/png-wml2-replay
python3 parsarium.py afl build png rust wml2
python3 parsarium.py afl prepare png rust wml2 runs/png-wml2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
