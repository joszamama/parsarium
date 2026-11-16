# libviprs — ASCII PNM / Rust

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/rust/libviprs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm rust libviprs
python3 parsarium.py run ascii_pnm rust libviprs controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm rust libviprs CORPUS_DIR runs/ascii_pnm-libviprs-replay
python3 parsarium.py afl build ascii_pnm rust libviprs
python3 parsarium.py afl prepare ascii_pnm rust libviprs runs/ascii_pnm-libviprs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
