# @draco-rust/ply — ASCII PLY / JavaScript

Pinned release: `0.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/draco-rust-ply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript draco_rust_ply
python3 parsarium.py run ascii_ply javascript draco_rust_ply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript draco_rust_ply CORPUS_DIR runs/ascii_ply-draco_rust_ply-replay
python3 parsarium.py afl build ascii_ply javascript draco_rust_ply
python3 parsarium.py afl prepare ascii_ply javascript draco_rust_ply runs/ascii_ply-draco_rust_ply-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
