# pdal_2.13 — ASCII PLY / Java

- **Pinned release:** `2.10.0`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PLY point-cloud subset: three parsed vertex coordinates through PDAL readers.ply; the face element is parsed past but PDAL exposes no mesh from readers.ply
- **Underlying family:** PDAL native PLY reader (readers.ply) via the PDAL JNI binding
- **Local input API:** `io.pdal.Pipeline(JSON with an explicit readers.ply stage on a local .ply path, LogLevel).execute(); getPointViews(); PointView.length() and getDouble(index, "X"/"Y")`
- **Documentation:** [API reference](<https://github.com/PDAL/java/blob/v2.10.0/README.md>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "points": 3,
  "second_x": 1.0,
  "last_y": 1.0
}
```

pdal_2.13 is the Scala/Java API of PDAL/java; pdal-native 2.10.0 is its JNI glue over libpdalcpp. The PLY text is parsed by PDAL io/PlyReader.cpp, the same engine as the C pdal-c lead (excluded there for adoption), not an independent JVM parser.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
