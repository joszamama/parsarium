# wblidar — ASCII PLY / Rust

Pinned release: `0.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/wblidar/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust wblidar
python3 parsarium.py run ascii_ply rust wblidar controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply rust wblidar CORPUS_DIR runs/ascii_ply-wblidar-replay
python3 parsarium.py afl build ascii_ply rust wblidar
python3 parsarium.py afl prepare ascii_ply rust wblidar runs/ascii_ply-wblidar-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
