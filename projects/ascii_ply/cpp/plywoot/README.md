# plywoot — ASCII PLY / C++

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/plywoot/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp plywoot
python3 parsarium.py run ascii_ply cpp plywoot controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp plywoot CORPUS_DIR runs/ascii_ply-plywoot-replay
python3 parsarium.py afl build ascii_ply cpp plywoot
python3 parsarium.py afl prepare ascii_ply cpp plywoot runs/ascii_ply-plywoot-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
