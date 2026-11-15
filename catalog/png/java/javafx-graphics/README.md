# javafx-graphics — PNG / Java

- **Pinned release:** `21.0.9`
- **License:** GPL-2.0-with-classpath-exception
- **Parsed scope:** RGBA pixels
- **Underlying family:** OpenJFX PNG image loader
- **Local input API:** `new javafx.scene.image.Image(InputStream); getPixelReader().getArgb(x,y)`
- **Documentation:** [API reference](<https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/image/Image.html>)
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
