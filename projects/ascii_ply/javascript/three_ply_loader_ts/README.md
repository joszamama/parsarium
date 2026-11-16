# three-ply-loader-ts — ASCII PLY / JavaScript

Pinned release: `1.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/three-ply-loader-ts/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript three_ply_loader_ts
python3 parsarium.py run ascii_ply javascript three_ply_loader_ts controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript three_ply_loader_ts CORPUS_DIR runs/ascii_ply-three_ply_loader_ts-replay
python3 parsarium.py afl build ascii_ply javascript three_ply_loader_ts
python3 parsarium.py afl prepare ascii_ply javascript three_ply_loader_ts runs/ascii_ply-three_ply_loader_ts-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
