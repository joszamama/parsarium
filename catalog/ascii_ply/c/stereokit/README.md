# stereokit — ASCII PLY / C

- **Pinned release:** `v0.3.11`
- **License:** MIT
- **Parsed scope:** One valid ASCII PLY triangle through the full native C ABI in offscreen Mesa mode; vertices and face indices observed
- **Underlying family:** StereoKit model PLY loader over bundled micro_ply
- **Local input API:** `model_create_file(local .ply path, shader); model_subset_count; model_get_mesh; mesh_get_verts; mesh_get_inds`
- **Documentation:** [API reference](<https://stereokit.net/Pages/StereoKit/Model.html>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "subsets": 1,
  "vertices": 3,
  "indices": 3,
  "face": [
    0,
    1,
    2
  ],
  "second_x": 1.0
}
```

A separate released library and public C package path over the micro_ply syntax parser family also present in sk_renderer. The public header has one unguarded C++ default argument; replay uses a one-line generated C compatibility copy without changing library source.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
