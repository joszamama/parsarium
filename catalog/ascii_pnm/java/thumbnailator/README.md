# thumbnailator — ASCII PNM / Java

- **Pinned release:** `0.4.21`
- **License:** MIT
- **Parsed scope:** ASCII PPM dimensions and red/green pixels
- **Underlying family:** Thumbnailator wrapper over ImageIO PNM provider (TwelveMonkeys or JAI)
- **Local input API:** `Thumbnails.of(File).scale(1.0).asBufferedImage() with installed PNM ImageIO provider`
- **Documentation:** [API reference](<https://github.com/coobird/thumbnailator/wiki/Examples>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/java/thumbnailator/README.md)

```sh
python3 parsarium.py build ascii_pnm java thumbnailator
python3 parsarium.py run ascii_pnm java thumbnailator controls/ascii_pnm/red-green.ppm
```
