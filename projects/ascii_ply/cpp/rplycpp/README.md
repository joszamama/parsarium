# rplycpp — ASCII PLY / C++

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/rplycpp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp rplycpp
python3 parsarium.py run ascii_ply cpp rplycpp controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp rplycpp CORPUS_DIR runs/ascii_ply-rplycpp-replay
python3 parsarium.py afl build ascii_ply cpp rplycpp
python3 parsarium.py afl prepare ascii_ply cpp rplycpp runs/ascii_ply-rplycpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
