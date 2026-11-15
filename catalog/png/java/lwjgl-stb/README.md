# lwjgl-stb — PNG / Java

- **Pinned release:** `3.4.3`
- **License:** BSD-3-Clause
- **Parsed scope:** RGBA pixels
- **Underlying family:** LWJGL binding to native stb_image PNG decoder
- **Local input API:** `STBImage.stbi_load_from_memory(ByteBuffer,...)`
- **Documentation:** [API reference](<https://javadoc.lwjgl.org/org/lwjgl/stb/STBImage.html>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
