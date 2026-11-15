# blukpast — ASCII PLY / C

- **Pinned release:** `1.0.6`
- **License:** LGPL-2.1
- **Parsed scope:** One valid ASCII PLY triangle with three parsed positions and face indices; upstream syntax parser with GPU upload replaced by observation harness
- **Underlying family:** Blukpast native C PLY loader
- **Local input API:** `bkpLoadPly(GPU adapter, local PLY path, BkpModel output, scratch group); harness captures parsed geometry at GPU upload boundary`
- **Documentation:** [API reference](<https://github.com/wypifu/blukpast/blob/v1.0.6/loaders/include/bkp_loaders.h>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "indices": 3,
  "meshes": 1,
  "face": [
    0,
    1,
    2
  ],
  "second_x": 1.0
}
```

Distinct tagged C package with native PLY syntax parsing. The harness replaces only GPU upload and model storage calls; no full Vulkan engine is built. This row is a source-level C API replay, not a GPU integration test.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
