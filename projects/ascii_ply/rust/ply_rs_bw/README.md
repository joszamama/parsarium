# ply-rs-bw — ASCII PLY / Rust

Pinned release: `4.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/ply-rs-bw/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust ply_rs_bw
python3 parsarium.py run ascii_ply rust ply_rs_bw controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply rust ply_rs_bw CORPUS_DIR runs/ascii_ply-ply_rs_bw-replay
python3 parsarium.py afl build ascii_ply rust ply_rs_bw
python3 parsarium.py afl prepare ascii_ply rust ply_rs_bw runs/ascii_ply-ply_rs_bw-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
