# itextpdf — PNG / Java

- **Pinned release:** `5.5.13`
- **License:** AGPL-3.0
- **Parsed scope:** PNG dimensions
- **Underlying family:** iText 5 PNG codec
- **Local input API:** `PngImage.getImage(InputStream).getWidth/getHeight`
- **Documentation:** [API reference](<https://javadoc.io/static/com.itextpdf/itextpdf/5.5.13/com/itextpdf/text/pdf/codec/PngImage.html>)
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

[Docker harness and verification receipt](../../../../projects/png/java/itextpdf/README.md)

```sh
python3 parsarium.py build png java itextpdf
python3 parsarium.py run png java itextpdf controls/png/red-green.png
```
