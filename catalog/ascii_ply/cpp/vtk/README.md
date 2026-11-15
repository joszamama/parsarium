# vtk — ASCII PLY / C++

- **Pinned release:** `9.7.2`
- **License:** BSD-3-Clause
- **Parsed scope:** three vertices, one polygon and its three indices
- **Underlying family:** VTK vtkPLYReader over bundled vtkPLY syntax parser
- **Local input API:** `vtkPLYReader::SetFileName(local filename); Update; GetOutput`
- **Documentation:** [API reference](<https://examples.vtk.org/site/Cxx/IO/ReadPLY/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_ply/parsers.json) · [control verification](../../../../data/cpp/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "face": [
    0,
    1,
    2
  ]
}
```

VTK bundles vtkPLY; distinct from RPly and the other listed PLY engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
