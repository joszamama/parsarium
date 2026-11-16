# threejs-ply-loader — ASCII PLY / JavaScript

Pinned release: `1.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/threejs-ply-loader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript threejs_ply_loader
python3 parsarium.py run ascii_ply javascript threejs_ply_loader controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript threejs_ply_loader CORPUS_DIR runs/ascii_ply-threejs_ply_loader-replay
python3 parsarium.py afl build ascii_ply javascript threejs_ply_loader
python3 parsarium.py afl prepare ascii_ply javascript threejs_ply_loader runs/ascii_ply-threejs_ply_loader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
