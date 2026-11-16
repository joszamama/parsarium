# ahg/3d-model — ASCII PLY / PHP

Pinned release: `1.165.35`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/php/ahg-3d-model/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply php ahg_3d_model
python3 parsarium.py run ascii_ply php ahg_3d_model controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply php ahg_3d_model CORPUS_DIR runs/ascii_ply-ahg_3d_model-replay
python3 parsarium.py afl build ascii_ply php ahg_3d_model
python3 parsarium.py afl prepare ascii_ply php ahg_3d_model runs/ascii_ply-ahg_3d_model-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
