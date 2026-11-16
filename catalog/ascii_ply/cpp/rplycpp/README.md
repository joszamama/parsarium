# rplycpp — ASCII PLY / C++

- **Pinned release:** `1.1.0`
- **License:** MIT
- **Parsed scope:** three parsed vertices and one triangle face with indices from ASCII PLY
- **Underlying family:** rplycpp wrapper over bundled RPly
- **Local input API:** `rplycpp::PLYReader::Open(local filename); GetElements; Read(handlers)`
- **Documentation:** [API reference](<https://github.com/manlito/rplycpp/blob/v1.1.0/README.md>)
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

Tagged rplycpp v1.1.0 exposes a distinct C++ callback API but bundles RPly; it shares the RPly parser family with the standalone rply C and C++ paths.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/cpp/rplycpp/README.md)

```sh
python3 parsarium.py build ascii_ply cpp rplycpp
python3 parsarium.py run ascii_ply cpp rplycpp controls/ascii_ply/triangle.ply
```
