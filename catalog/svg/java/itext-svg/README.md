# itext-svg — SVG / Java

- **Pinned release:** `9.8.0`
- **Upstream:** [source repository](<https://github.com/itext/itext-java>) · [Maven Central](<https://central.sonatype.com/artifact/com.itextpdf/svg>)
- **License:** AGPL-3.0-or-later
- **Parsed scope:** SVG XObject dimensions
- **Underlying family:** iText SVG parser and PDF renderer
- **Local input API:** `SvgConverter.convertToXObject(InputStream, PdfDocument).getWidth()/getHeight()`
- **Documentation:** [API reference](<https://api.itextpdf.com/iText/java/9.8.0/com/itextpdf/svg/converter/SvgConverter.html>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/java/itext_svg/README.md)

```sh
python3 parsarium.py build svg java itext_svg
python3 parsarium.py run svg java itext_svg controls/svg/red-green.svg
```
