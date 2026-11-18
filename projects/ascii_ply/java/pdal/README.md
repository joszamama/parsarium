# pdal_2.13 — ASCII PLY / Java

Pinned release: `2.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/java/pdal-2-13/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply java pdal
python3 parsarium.py run ascii_ply java pdal controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply java pdal CORPUS_DIR runs/ascii_ply-pdal-replay
python3 parsarium.py afl build ascii_ply java pdal
python3 parsarium.py afl prepare ascii_ply java pdal runs/ascii_ply-pdal-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
