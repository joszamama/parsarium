# threecrate-io — ASCII PLY / Rust

Pinned release: `0.12.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/threecrate-io/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust threecrate_io
python3 parsarium.py run ascii_ply rust threecrate_io controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply rust threecrate_io CORPUS_DIR runs/ascii_ply-threecrate_io-replay
python3 parsarium.py afl build ascii_ply rust threecrate_io
python3 parsarium.py afl prepare ascii_ply rust threecrate_io runs/ascii_ply-threecrate_io-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
