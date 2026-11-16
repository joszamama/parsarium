# sply — ASCII PLY / C

Pinned release: `1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/sply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c sply
python3 parsarium.py run ascii_ply c sply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c sply CORPUS_DIR runs/ascii_ply-sply-replay
python3 parsarium.py afl build ascii_ply c sply
python3 parsarium.py afl prepare ascii_ply c sply runs/ascii_ply-sply-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
