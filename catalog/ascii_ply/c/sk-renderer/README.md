# sk_renderer — ASCII PLY / C

- **Pinned release:** `v2026.11.3`
- **License:** MIT OR Unlicense
- **Parsed scope:** One valid ASCII PLY triangle; parsed vertex and face element counts and second X coordinate from converted vertex body
- **Underlying family:** micro_ply standalone C parser by Nick Klingensmith
- **Local input API:** `Read local PLY file into bytes; ply_read(bytes, length, ply_file_t*); ply_convert(vertex element, position properties, output)`
- **Documentation:** [API reference](<https://github.com/StereoKit/sk_renderer/blob/v2026.11.3/README.md>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "converted": 3,
  "second_x": 1.0
}
```

Released sk_renderer package publishes the same micro_ply.h bytes as the author’s unversioned maluoi/header-libs repository. This is one parser family, not two independent engines. Renderer GPU APIs are not involved in this standalone reader control.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
