# lodepng — PNG / Rust

Pinned release: `3.12.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/lodepng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust lodepng
python3 parsarium.py run png rust lodepng controls/png/red-green.png
python3 parsarium.py replay png rust lodepng CORPUS_DIR runs/png-lodepng-replay
python3 parsarium.py afl build png rust lodepng
python3 parsarium.py afl prepare png rust lodepng runs/png-lodepng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
