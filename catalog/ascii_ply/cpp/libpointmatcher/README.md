# libpointmatcher — ASCII PLY / C++

- **Pinned release:** `1.4.4`
- **Upstream:** [source repository](<https://github.com/norlab-ulaval/libpointmatcher>)
- **License:** BSD-3-Clause
- **Parsed scope:** three parsed point-cloud vertices with x/y/z coordinate sums from ASCII PLY
- **Underlying family:** libpointmatcher native PLY point-cloud parser
- **Local input API:** `PointMatcherIO<double>::loadPLY(local filename); DataPoints::features`
- **Documentation:** [API reference](<https://github.com/norlab-ulaval/libpointmatcher/blob/1.4.4/pointmatcher/IO.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_ply/parsers.json) · [control verification](../../../../data/cpp/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "points": 3,
  "x_sum": 1,
  "y_sum": 1,
  "z_sum": 0
}
```

Its pointmatcher/IO.cpp implements ASCII PLY parsing directly and does not delegate to RPly; it ignores the mesh face because the API returns point-cloud DataPoints.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/cpp/libpointmatcher/README.md)

```sh
python3 parsarium.py build ascii_ply cpp libpointmatcher
python3 parsarium.py run ascii_ply cpp libpointmatcher controls/ascii_ply/triangle.ply
```
