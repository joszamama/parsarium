# plyparser — ASCII PLY / JavaScript

Pinned release: `6.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/plyparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript plyparser
python3 parsarium.py run ascii_ply javascript plyparser controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript plyparser CORPUS_DIR runs/ascii_ply-plyparser-replay
python3 parsarium.py afl build ascii_ply javascript plyparser
python3 parsarium.py afl prepare ascii_ply javascript plyparser runs/ascii_ply-plyparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
