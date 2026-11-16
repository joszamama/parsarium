# imageun — ASCII PNM / Rust

Pinned release: `0.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/rust/imageun/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm rust imageun
python3 parsarium.py run ascii_pnm rust imageun controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm rust imageun CORPUS_DIR runs/ascii_pnm-imageun-replay
python3 parsarium.py afl build ascii_pnm rust imageun
python3 parsarium.py afl prepare ascii_pnm rust imageun runs/ascii_pnm-imageun-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
