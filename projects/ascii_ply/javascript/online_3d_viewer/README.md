# online-3d-viewer — ASCII PLY / JavaScript

Pinned release: `0.18.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/online-3d-viewer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript online_3d_viewer
python3 parsarium.py run ascii_ply javascript online_3d_viewer controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript online_3d_viewer CORPUS_DIR runs/ascii_ply-online_3d_viewer-replay
python3 parsarium.py afl build ascii_ply javascript online_3d_viewer
python3 parsarium.py afl prepare ascii_ply javascript online_3d_viewer runs/ascii_ply-online_3d_viewer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
