# trimesh — ASCII PLY / Python

Pinned release: `5.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/trimesh/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python trimesh
python3 parsarium.py run ascii_ply python trimesh controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python trimesh CORPUS_DIR runs/ascii_ply-trimesh-replay
python3 parsarium.py afl build ascii_ply python trimesh
python3 parsarium.py afl prepare ascii_ply python trimesh runs/ascii_ply-trimesh-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
