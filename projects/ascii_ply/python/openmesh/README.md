# openmesh — ASCII PLY / Python

Pinned release: `1.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/openmesh/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python openmesh
python3 parsarium.py run ascii_ply python openmesh controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python openmesh CORPUS_DIR runs/ascii_ply-openmesh-replay
python3 parsarium.py afl build ascii_ply python openmesh
python3 parsarium.py afl prepare ascii_ply python openmesh runs/ascii_ply-openmesh-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
