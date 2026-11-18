# libagar — ASCII PLY / C

- **Pinned release:** `1.7.1`
- **Upstream:** [source repository](<https://github.com/JulNadeauCA/libagar>)
- **License:** BSD-2-Clause
- **Parsed scope:** three vertices and one triangular facet with parsed vertex ids from ASCII PLY
- **Underlying family:** Agar-SG native PLY loader (sg/sg_load_ply.c)
- **Local input API:** `SG_ObjectNew(NULL, name); SG_ObjectLoadPLY(SG_Object *, local .ply path, 0) after AG_InitCore and SG_InitSubsystem; vertex count from nVtx, facets from facetTbl, first facet vertex ids from its half-edges`
- **Documentation:** [API reference](<https://github.com/JulNadeauCA/libagar/blob/release-1.7.1/sg/SG_Object.3>)
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

Agar's scene-graph library ships its own ASCII and binary PLY header, element and property parser behind SG_ObjectLoadPLY(3); it does not bundle RPly, Greg Turk ply.c or another counted C PLY engine. The library is part of the Agar GUI toolkit; no display driver is opened.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/c/libagar/README.md)

```sh
python3 parsarium.py build ascii_ply c libagar
python3 parsarium.py run ascii_ply c libagar controls/ascii_ply/triangle.ply
```
