# makepad-zune-png — PNG / Rust

Pinned release: `0.4.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/makepad-zune-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust makepad_zune_png
python3 parsarium.py run png rust makepad_zune_png controls/png/red-green.png
python3 parsarium.py replay png rust makepad_zune_png CORPUS_DIR runs/png-makepad_zune_png-replay
python3 parsarium.py afl build png rust makepad_zune_png
python3 parsarium.py afl prepare png rust makepad_zune_png runs/png-makepad_zune_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
