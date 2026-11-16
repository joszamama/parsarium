# tinyply — ASCII PLY / C++

Pinned release: `3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/tinyply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp tinyply
python3 parsarium.py run ascii_ply cpp tinyply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp tinyply CORPUS_DIR runs/ascii_ply-tinyply-replay
python3 parsarium.py afl build ascii_ply cpp tinyply
python3 parsarium.py afl prepare ascii_ply cpp tinyply runs/ascii_ply-tinyply-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
