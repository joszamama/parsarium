# threecrate — ASCII PLY / Rust

Pinned release: `0.12.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/threecrate/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust threecrate
python3 parsarium.py run ascii_ply rust threecrate controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply rust threecrate CORPUS_DIR runs/ascii_ply-threecrate-replay
python3 parsarium.py afl build ascii_ply rust threecrate
python3 parsarium.py afl prepare ascii_ply rust threecrate runs/ascii_ply-threecrate-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
