# meshlab-ts — ASCII PLY / JavaScript

Pinned release: `2026.8.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/meshlab-ts/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript meshlab_ts
python3 parsarium.py run ascii_ply javascript meshlab_ts controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript meshlab_ts CORPUS_DIR runs/ascii_ply-meshlab_ts-replay
python3 parsarium.py afl build ascii_ply javascript meshlab_ts
python3 parsarium.py afl prepare ascii_ply javascript meshlab_ts runs/ascii_ply-meshlab_ts-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
