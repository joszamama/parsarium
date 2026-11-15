# itext-io — PNG / Java

- **Pinned release:** `9.8.0`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** PNG dimensions
- **Underlying family:** iText 9 image I/O PNG codec
- **Local input API:** `ImageDataFactory.createPng(byte[]).getWidth/getHeight`
- **Documentation:** [API reference](<https://api.itextpdf.com/iText/java/9.8.0/com/itextpdf/io/image/ImageDataFactory.html>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
