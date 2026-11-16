# fop-core — SVG / Java

- **Pinned release:** `2.12`
- **License:** Apache-2.0
- **Parsed scope:** PDF page dimensions and SVG-derived red/green drawing operations
- **Underlying family:** Apache FOP SVG-to-PDF transcoder using Apache Batik
- **Local input API:** `PDFTranscoder.transcode(TranscoderInput(InputStream), TranscoderOutput(OutputStream))`
- **Documentation:** [API reference](<https://xmlgraphics.apache.org/fop/dev/svg.html>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "red": true,
  "green": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/java/fop_core/README.md)

```sh
python3 parsarium.py build svg java fop_core
python3 parsarium.py run svg java fop_core controls/svg/red-green.svg
```
