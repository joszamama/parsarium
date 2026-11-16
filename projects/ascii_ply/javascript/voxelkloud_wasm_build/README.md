# @voxelkloud/wasm-build — ASCII PLY / JavaScript

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/voxelkloud-wasm-build/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript voxelkloud_wasm_build
python3 parsarium.py run ascii_ply javascript voxelkloud_wasm_build controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript voxelkloud_wasm_build CORPUS_DIR runs/ascii_ply-voxelkloud_wasm_build-replay
python3 parsarium.py afl build ascii_ply javascript voxelkloud_wasm_build
python3 parsarium.py afl prepare ascii_ply javascript voxelkloud_wasm_build runs/ascii_ply-voxelkloud_wasm_build-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
