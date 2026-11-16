# imagesize — ASCII PNM / Rust

Pinned release: `0.15.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/rust/imagesize/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm rust imagesize
python3 parsarium.py run ascii_pnm rust imagesize controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm rust imagesize CORPUS_DIR runs/ascii_pnm-imagesize-replay
python3 parsarium.py afl build ascii_pnm rust imagesize
python3 parsarium.py afl prepare ascii_pnm rust imagesize runs/ascii_pnm-imagesize-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
