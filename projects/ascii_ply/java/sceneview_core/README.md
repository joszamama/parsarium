# sceneview-core — ASCII PLY / Java

Pinned release: `4.69.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/java/sceneview-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply java sceneview_core
python3 parsarium.py run ascii_ply java sceneview_core controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply java sceneview_core CORPUS_DIR runs/ascii_ply-sceneview_core-replay
python3 parsarium.py afl build ascii_ply java sceneview_core
python3 parsarium.py afl prepare ascii_ply java sceneview_core runs/ascii_ply-sceneview_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
