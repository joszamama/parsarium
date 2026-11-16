# png-decoder — PNG / Rust

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/png-decoder/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust png_decoder
python3 parsarium.py run png rust png_decoder controls/png/red-green.png
python3 parsarium.py replay png rust png_decoder CORPUS_DIR runs/png-png_decoder-replay
python3 parsarium.py afl build png rust png_decoder
python3 parsarium.py afl prepare png rust png_decoder runs/png-png_decoder-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
