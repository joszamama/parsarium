# jzy3d-core — ASCII PLY / Java

- **Pinned release:** `2.2.1`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII triangle vertex positions (three vertices, second X and third Y); faces not exposed by this API
- **Underlying family:** Jzy3d public PLY vertex API over jPLY
- **Local input API:** `Ply.read(InputStream from local ASCII PLY file), returning List<Coord3d>`
- **Documentation:** [API reference](<https://doc.jzy3d.org/javadoc/2.2.1/org/jzy3d/io/ply/Ply.html>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "second_x": 1.0,
  "third_y": 1.0
}
```

Published Jzy3d Core library depends on its published org.smurn:jply:0.2.1; the jPLY 0.2.0 package path is already counted in this cell. This is a separate package API but not an independent PLY syntax engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/java/jzy3d_core/README.md)

```sh
python3 parsarium.py build ascii_ply java jzy3d_core
python3 parsarium.py run ascii_ply java jzy3d_core controls/ascii_ply/triangle.ply
```
