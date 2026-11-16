# @meshioplusplus/wasm — ASCII PLY / JavaScript

Pinned release: `20.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/meshioplusplus-wasm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript meshioplusplus_wasm
python3 parsarium.py run ascii_ply javascript meshioplusplus_wasm controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript meshioplusplus_wasm CORPUS_DIR runs/ascii_ply-meshioplusplus_wasm-replay
python3 parsarium.py afl build ascii_ply javascript meshioplusplus_wasm
python3 parsarium.py afl prepare ascii_ply javascript meshioplusplus_wasm runs/ascii_ply-meshioplusplus_wasm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
