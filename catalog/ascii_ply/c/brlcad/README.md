# brlcad — ASCII PLY / C

- **Pinned release:** `7.46.0`
- **License:** LGPL-2.1-only AND MIT
- **Parsed scope:** three vertices, one face, triangle indices and BRL-CAD default scaled coordinate from local ASCII PLY
- **Underlying family:** BRL-CAD gcv-ply plugin over bundled RPly 1.1.4
- **Local input API:** `gcv_context_init; find_filter(GCV_FILTER_READ, BU_MIME_MODEL_PLY, local filename); gcv_execute; rt_db_get_internal`
- **Documentation:** [API reference](<https://brlcad.org/docs/html/articles/gcv.html>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "second_x": 1000.0,
  "face": [
    0,
    1,
    2
  ]
}
```

Distinct BRL-CAD library package and import API; bundled RPly is the underlying syntax parser family already represented by standalone RPly and SPly.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/c/brlcad/README.md)

```sh
python3 parsarium.py build ascii_ply c brlcad
python3 parsarium.py run ascii_ply c brlcad controls/ascii_ply/triangle.ply
```
