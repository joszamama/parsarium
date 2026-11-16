# cumulus3d-core — ASCII PLY / Rust

Pinned release: `0.11.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/cumulus3d-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust cumulus3d_core
python3 parsarium.py run ascii_ply rust cumulus3d_core controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply rust cumulus3d_core CORPUS_DIR runs/ascii_ply-cumulus3d_core-replay
python3 parsarium.py afl build ascii_ply rust cumulus3d_core
python3 parsarium.py afl prepare ascii_ply rust cumulus3d_core runs/ascii_ply-cumulus3d_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
