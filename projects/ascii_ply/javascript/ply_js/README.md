# ply-js — ASCII PLY / JavaScript

Pinned release: `0.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/ply-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript ply_js
python3 parsarium.py run ascii_ply javascript ply_js controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript ply_js CORPUS_DIR runs/ascii_ply-ply_js-replay
python3 parsarium.py afl build ascii_ply javascript ply_js
python3 parsarium.py afl prepare ascii_ply javascript ply_js runs/ascii_ply-ply_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
