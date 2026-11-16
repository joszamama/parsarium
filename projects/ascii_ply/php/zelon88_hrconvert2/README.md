# zelon88/hrconvert2 — ASCII PLY / PHP

Pinned release: `v4.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/php/zelon88-hrconvert2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply php zelon88_hrconvert2
python3 parsarium.py run ascii_ply php zelon88_hrconvert2 controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply php zelon88_hrconvert2 CORPUS_DIR runs/ascii_ply-zelon88_hrconvert2-replay
python3 parsarium.py afl build ascii_ply php zelon88_hrconvert2
python3 parsarium.py afl prepare ascii_ply php zelon88_hrconvert2 runs/ascii_ply-zelon88_hrconvert2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
