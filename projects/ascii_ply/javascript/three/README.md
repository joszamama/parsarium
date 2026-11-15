# three — ASCII PLY / JavaScript

Pinned release: `0.187.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/three/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript three
python3 parsarium.py run ascii_ply javascript three controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript three CORPUS_DIR runs/ascii_ply-three-replay
python3 parsarium.py afl build ascii_ply javascript three
python3 parsarium.py afl prepare ascii_ply javascript three runs/ascii_ply-three-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
