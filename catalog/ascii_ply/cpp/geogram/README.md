# geogram — ASCII PLY / C++

- **Pinned release:** `1.10.1`
- **License:** BSD-3-Clause AND MIT
- **Parsed scope:** three parsed mesh vertices and one triangle facet with indices
- **Underlying family:** Geogram PLYIOHandler over bundled RPly 1.1.4
- **Local input API:** `GEO::initialize(); GEO::mesh_load(local filename, GEO::Mesh&, MeshIOFlags)`
- **Documentation:** [API reference](<https://github.com/BrunoLevy/geogram/wiki/Mesh>)
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

Geogram v1.10.1 registers PLYIOHandler in mesh_io.cpp and calls bundled RPly 1.1.4. This shares the RPly underlying syntax parser family with standalone RPly and rplycpp, but Geogram exposes its distinct mesh_load API and mesh representation.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/cpp/geogram/README.md)

```sh
python3 parsarium.py build ascii_ply cpp geogram
python3 parsarium.py run ascii_ply cpp geogram controls/ascii_ply/triangle.ply
```
