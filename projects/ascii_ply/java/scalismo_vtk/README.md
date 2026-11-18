# scalismo-vtk_3 — ASCII PLY / Java

Pinned release: `1.0-RC1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/java/scalismo-vtk-3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply java scalismo_vtk
python3 parsarium.py run ascii_ply java scalismo_vtk controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply java scalismo_vtk CORPUS_DIR runs/ascii_ply-scalismo_vtk-replay
python3 parsarium.py afl build ascii_ply java scalismo_vtk
python3 parsarium.py afl prepare ascii_ply java scalismo_vtk runs/ascii_ply-scalismo_vtk-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
