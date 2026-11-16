# boofcv-io — PNG / Java

- **Pinned release:** `1.6.0`
- **License:** Apache-2.0
- **Parsed scope:** RGBA pixels
- **Underlying family:** BoofCV image I/O over Java ImageIO
- **Local input API:** `UtilImageIO.loadImage(path)`
- **Documentation:** [API reference](<https://boofcv.org/javadoc/boofcv/io/image/UtilImageIO.html>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/png/java/boofcv_io/README.md)

```sh
python3 parsarium.py build png java boofcv_io
python3 parsarium.py run png java boofcv_io controls/png/red-green.png
```
