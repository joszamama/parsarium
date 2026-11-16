# brepkit-io — ASCII PLY / Rust

Pinned release: `4.11.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/brepkit-io/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust brepkit_io
python3 parsarium.py run ascii_ply rust brepkit_io controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply rust brepkit_io CORPUS_DIR runs/ascii_ply-brepkit_io-replay
python3 parsarium.py afl build ascii_ply rust brepkit_io
python3 parsarium.py afl prepare ascii_ply rust brepkit_io runs/ascii_ply-brepkit_io-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
