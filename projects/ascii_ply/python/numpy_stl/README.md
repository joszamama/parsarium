# numpy-stl — ASCII PLY / Python

Pinned release: `4.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/numpy-stl/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python numpy_stl
python3 parsarium.py run ascii_ply python numpy_stl controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python numpy_stl CORPUS_DIR runs/ascii_ply-numpy_stl-replay
python3 parsarium.py afl build ascii_ply python numpy_stl
python3 parsarium.py afl prepare ascii_ply python numpy_stl runs/ascii_ply-numpy_stl-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
