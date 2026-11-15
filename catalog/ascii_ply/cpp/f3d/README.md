# f3d — ASCII PLY / C++

- **Pinned release:** `4.0.1`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII triangle produced three parsed points and one cell
- **Underlying family:** F3D native PLY plugin over VTK vtkPLYReader
- **Local input API:** `f3d::scene::add(local filename); getSceneInfo`
- **Documentation:** [API reference](<https://github.com/f3d-app/f3d/blob/v4.0.1/library/public/scene.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_ply/parsers.json) · [control verification](../../../../data/cpp/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_ply/ranking.md)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
