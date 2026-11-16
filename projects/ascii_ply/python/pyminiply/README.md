# pyminiply — ASCII PLY / Python

Pinned release: `0.2.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/pyminiply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python pyminiply
python3 parsarium.py run ascii_ply python pyminiply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python pyminiply CORPUS_DIR runs/ascii_ply-pyminiply-replay
python3 parsarium.py afl build ascii_ply python pyminiply
python3 parsarium.py afl prepare ascii_ply python pyminiply runs/ascii_ply-pyminiply-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
