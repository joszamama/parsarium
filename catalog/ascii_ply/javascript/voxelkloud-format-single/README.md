# @voxelkloud/format-single — ASCII PLY / JavaScript

- **Pinned release:** `0.5.1`
- **License:** MIT
- **Parsed scope:** vertex records only
- **Underlying family:** voxelkloud WASM builder
- **Local input API:** `loadSingleFileSource(name, {bytes: localBytes, worker: false})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@voxelkloud/format-single/v/0.5.1>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/javascript/voxelkloud_format_single/README.md)

```sh
python3 parsarium.py build ascii_ply javascript voxelkloud_format_single
python3 parsarium.py run ascii_ply javascript voxelkloud_format_single controls/ascii_ply/triangle.ply
```
