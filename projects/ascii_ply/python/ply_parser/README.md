# ply-parser — ASCII PLY / Python

Pinned release: `3.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/ply-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python ply_parser
python3 parsarium.py run ascii_ply python ply_parser controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python ply_parser CORPUS_DIR runs/ascii_ply-ply_parser-replay
python3 parsarium.py afl build ascii_ply python ply_parser
python3 parsarium.py afl prepare ascii_ply python ply_parser runs/ascii_ply-ply_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
