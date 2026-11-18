# f3d — ASCII PLY / C

- **Pinned release:** `4.0.1`
- **Upstream:** [source repository](<https://github.com/f3d-app/f3d>)
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII triangle produced three parsed points and one cell
- **Underlying family:** F3D native PLY plugin over VTK vtkPLYReader
- **Local input API:** `f3d_scene_add(scene, local filename); f3d_scene_get_scene_info`
- **Documentation:** [API reference](<https://github.com/f3d-app/f3d/blob/v4.0.1/c/scene_c_api.h>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "files": 1,
  "actors": 1,
  "points": 3,
  "cells": 1
}
```

C, C++, and Java F3D 4.0.1 bindings share the F3D native plugin and VTK 9.7.2 vtkPLYReader syntax parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/c/f3d/README.md)

```sh
python3 parsarium.py build ascii_ply c f3d
python3 parsarium.py run ascii_ply c f3d controls/ascii_ply/triangle.ply
```
