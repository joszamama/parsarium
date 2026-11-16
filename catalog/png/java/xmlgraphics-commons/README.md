# xmlgraphics-commons — PNG / Java

- **Pinned release:** `2.12`
- **License:** Apache-2.0
- **Parsed scope:** PNG dimensions and MIME
- **Underlying family:** XML Graphics image loader over Java ImageIO
- **Local input API:** `ImageManager.getImageInfo(file URI,DefaultImageSessionContext)`
- **Documentation:** [API reference](<https://xmlgraphics.apache.org/commons/image-loader.html>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/java/xmlgraphics_commons/README.md)

```sh
python3 parsarium.py build png java xmlgraphics_commons
python3 parsarium.py run png java xmlgraphics_commons controls/png/red-green.png
```
