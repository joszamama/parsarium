# libigl — ASCII PLY / C++

- **Pinned release:** `2.6.4`
- **License:** MPL-2.0
- **Parsed scope:** three vertex positions and one triangle face matrix
- **Underlying family:** libigl readPLY over bundled tinyply 2.3.2
- **Local input API:** `igl::readPLY(local filename, Eigen vertex matrix, Eigen face matrix)`
- **Documentation:** [API reference](<https://libigl.github.io/dox/readPLY_8h.html>)
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

libigl has a distinct documented Eigen-matrix API but shares the tinyply parser family with the separately verified tinyply standalone package (which is pinned at 3.0).

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/cpp/libigl/README.md)

```sh
python3 parsarium.py build ascii_ply cpp libigl
python3 parsarium.py run ascii_ply cpp libigl controls/ascii_ply/triangle.ply
```
