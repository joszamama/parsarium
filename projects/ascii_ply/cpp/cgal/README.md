# cgal — ASCII PLY / C++

Pinned release: `6.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/cgal/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp cgal
python3 parsarium.py run ascii_ply cpp cgal controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp cgal CORPUS_DIR runs/ascii_ply-cgal-replay
python3 parsarium.py afl build ascii_ply cpp cgal
python3 parsarium.py afl prepare ascii_ply cpp cgal runs/ascii_ply-cgal-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
