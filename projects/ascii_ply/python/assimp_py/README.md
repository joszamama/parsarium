# assimp-py — ASCII PLY / Python

Pinned release: `1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/assimp-py/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python assimp_py
python3 parsarium.py run ascii_ply python assimp_py controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python assimp_py CORPUS_DIR runs/ascii_ply-assimp_py-replay
python3 parsarium.py afl build ascii_ply python assimp_py
python3 parsarium.py afl prepare ascii_ply python assimp_py runs/ascii_ply-assimp_py-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
