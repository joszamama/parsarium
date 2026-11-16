# @voxelkloud/format-single — ASCII PLY / JavaScript

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/voxelkloud-format-single/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript voxelkloud_format_single
python3 parsarium.py run ascii_ply javascript voxelkloud_format_single controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript voxelkloud_format_single CORPUS_DIR runs/ascii_ply-voxelkloud_format_single-replay
python3 parsarium.py afl build ascii_ply javascript voxelkloud_format_single
python3 parsarium.py afl prepare ascii_ply javascript voxelkloud_format_single runs/ascii_ply-voxelkloud_format_single-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
