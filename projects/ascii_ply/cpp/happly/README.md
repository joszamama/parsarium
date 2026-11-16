# happly — ASCII PLY / C++

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/happly/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp happly
python3 parsarium.py run ascii_ply cpp happly controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp happly CORPUS_DIR runs/ascii_ply-happly-replay
python3 parsarium.py afl build ascii_ply cpp happly
python3 parsarium.py afl prepare ascii_ply cpp happly runs/ascii_ply-happly-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
