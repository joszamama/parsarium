# openpdf — PNG / Java

- **Pinned release:** `3.0.5`
- **License:** MPL-2.0 OR LGPL-2.1+
- **Parsed scope:** PNG dimensions
- **Underlying family:** OpenPDF fork of iText; current PNG path over Java ImageIO
- **Local input API:** `ImageLoader.getPngImage(byte[]).getWidth/getHeight`
- **Documentation:** [API reference](<https://javadoc.io/static/com.github.librepdf/openpdf/3.0.5/com.github.librepdf.openpdf/org/openpdf/text/ImageLoader.html>)
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

[Docker harness and verification receipt](../../../../projects/png/java/openpdf/README.md)

```sh
python3 parsarium.py build png java openpdf
python3 parsarium.py run png java openpdf controls/png/red-green.png
```
