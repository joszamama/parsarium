# gegl — ASCII PNM / C

- **Pinned release:** `0.4.72`
- **License:** LGPL-3.0-or-later AND GPL-3.0-or-later AND BSD-3-Clause AND MIT
- **Parsed scope:** P3 dimensions and two decoded RGB pixels
- **Underlying family:** GEGL PPM loader
- **Local input API:** `gegl_node_new_child(operation=gegl:ppm-load,path=local path); gegl_node_blit`
- **Documentation:** [API reference](<https://www.gegl.org/operations/gegl-ppm-load.html>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_pnm/parsers.json) · [control verification](../../../../data/c/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

GEGL ppm-load is a separate plugin; its dylib is pinned along with the core library.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/c/gegl/README.md)

```sh
python3 parsarium.py build ascii_pnm c gegl
python3 parsarium.py run ascii_pnm c gegl controls/ascii_pnm/red-green.ppm
```
