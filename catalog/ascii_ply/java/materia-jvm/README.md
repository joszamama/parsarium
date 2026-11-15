# materia-jvm — ASCII PLY / Java

- **Pinned release:** `0.4.2.2`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY triangle position attribute count, one face and parsed indices
- **Underlying family:** Materia Kotlin ASCII PLY loader
- **Local input API:** `PLYLoader.load(String absolute local path) via Java coroutine runBlocking; JVM default AssetResolver reads local bytes`
- **Documentation:** [API reference](<https://github.com/codeyousef/Materia/blob/v0.4.2.2/src/commonMain/kotlin/io/materia/loader/PLYLoader.kt>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "indices": [
    0,
    1,
    2
  ]
}
```

Tagged JVM artifact exposes a Java-callable coroutine API over Materia’s Kotlin PLY parser. Project stars are auxiliary, not exact-release dependent counts or PLY-specific use.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
