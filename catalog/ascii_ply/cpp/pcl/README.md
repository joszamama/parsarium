# pcl — ASCII PLY / C++

- **Pinned release:** `1.15.1`
- **Upstream:** [source repository](<https://github.com/PointCloudLibrary/pcl>) · [Debian](<https://tracker.debian.org/pkg/pcl>)
- **License:** BSD-3-Clause
- **Parsed scope:** three vertices, one polygon and its three indices
- **Underlying family:** PCL PLYReader native implementation
- **Local input API:** `pcl::PLYReader::read(local filename, PolygonMesh)`
- **Documentation:** [API reference](<https://pointclouds.org/documentation/classpcl_1_1_p_l_y_reader.html>)
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

PCL has its own PLY reader implementation.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/cpp/pcl/README.md)

```sh
python3 parsarium.py build ascii_ply cpp pcl
python3 parsarium.py run ascii_ply cpp pcl controls/ascii_ply/triangle.ply
```
