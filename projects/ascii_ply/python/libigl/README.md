# libigl — ASCII PLY / Python

Pinned release: `2.6.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/libigl/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python libigl
python3 parsarium.py run ascii_ply python libigl controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python libigl CORPUS_DIR runs/ascii_ply-libigl-replay
python3 parsarium.py afl build ascii_ply python libigl
python3 parsarium.py afl prepare ascii_ply python libigl runs/ascii_ply-libigl-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
