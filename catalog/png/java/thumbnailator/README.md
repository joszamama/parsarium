# thumbnailator — PNG / Java

- **Pinned release:** `0.4.21`
- **License:** MIT
- **Parsed scope:** RGBA pixels
- **Underlying family:** Thumbnailator image reader over Java ImageIO
- **Local input API:** `Thumbnails.of(File).scale(1.0).asBufferedImage()`
- **Documentation:** [API reference](<https://github.com/coobird/thumbnailator/wiki/Examples>)
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

[Docker harness and verification receipt](../../../../projects/png/java/thumbnailator/README.md)

```sh
python3 parsarium.py build png java thumbnailator
python3 parsarium.py run png java thumbnailator controls/png/red-green.png
```
