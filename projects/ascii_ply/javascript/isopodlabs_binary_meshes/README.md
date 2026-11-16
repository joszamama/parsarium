# @isopodlabs/binary_meshes — ASCII PLY / JavaScript

Pinned release: `0.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/isopodlabs-binary-meshes/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript isopodlabs_binary_meshes
python3 parsarium.py run ascii_ply javascript isopodlabs_binary_meshes controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript isopodlabs_binary_meshes CORPUS_DIR runs/ascii_ply-isopodlabs_binary_meshes-replay
python3 parsarium.py afl build ascii_ply javascript isopodlabs_binary_meshes
python3 parsarium.py afl prepare ascii_ply javascript isopodlabs_binary_meshes runs/ascii_ply-isopodlabs_binary_meshes-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
