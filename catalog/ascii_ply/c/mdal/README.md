# mdal — ASCII PLY / C

- **Pinned release:** `1.3.3`
- **License:** MIT
- **Parsed scope:** Three parsed vertices, one face and face indices
- **Underlying family:** MDAL PLY driver over bundled libplyxx
- **Local input API:** `MDAL_LoadMesh(local path); MDAL_M_vertexCount; MDAL_M_faceCount; MDAL_FI_next`
- **Documentation:** [API reference](<https://github.com/lutraconsulting/MDAL/blob/release-1.3.3/mdal/api/mdal.h>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "indices": [
    0,
    1,
    2
  ]
}
```

MDAL uses its native PLY driver over a fork of libplyxx; distinct package path from the other C PLY readers. The public C ABI is called through pinned C declarations because upstream mdal.h itself is not C11-compatible.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/c/mdal/README.md)

```sh
python3 parsarium.py build ascii_ply c mdal
python3 parsarium.py run ascii_ply c mdal controls/ascii_ply/triangle.ply
```
