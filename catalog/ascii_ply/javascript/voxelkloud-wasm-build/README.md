# @voxelkloud/wasm-build — ASCII PLY / JavaScript

- **Pinned release:** `0.5.1`
- **License:** MIT
- **Parsed scope:** vertex records only
- **Underlying family:** voxelkloud WASM builder
- **Local input API:** `initBuilder(); buildFromFile(localBytes)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@voxelkloud/wasm-build/v/0.5.1>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_ply/parsers.json) · [control verification](../../../../data/javascript/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "pointCount": 3,
  "nodeCount": 1,
  "recordBytes": 60
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/voxelkloud_wasm_build/README.md)

```sh
python3 parsarium.py build ascii_ply javascript voxelkloud_wasm_build
python3 parsarium.py run ascii_ply javascript voxelkloud_wasm_build controls/ascii_ply/triangle.ply
```
