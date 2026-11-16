# easy3d — ASCII PLY / C++

Pinned release: `2.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/easy3d/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp easy3d
python3 parsarium.py run ascii_ply cpp easy3d controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp easy3d CORPUS_DIR runs/ascii_ply-easy3d-replay
python3 parsarium.py afl build ascii_ply cpp easy3d
python3 parsarium.py afl prepare ascii_ply cpp easy3d runs/ascii_ply-easy3d-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
