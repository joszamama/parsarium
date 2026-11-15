# freeimage — PNG / C

- **Pinned release:** `3.18.0`
- **License:** FreeImage
- **Parsed scope:** pixels
- **Underlying family:** FreeImage PNG plugin (bundled libpng lineage)
- **Local input API:** `FreeImage_Load(FIF_PNG, const char*, PNG_DEFAULT); FreeImage_GetPixelColor(...)`
- **Documentation:** [API reference](<https://freeimage.sourceforge.io/faq.html>)
- **Catalog evidence:** [parser record](../../../../data/c/png/parsers.json) · [control verification](../../../../data/c/png/verification.json) · [within-ecosystem ranking](../../../../data/c/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0,
    255
  ],
  "second": [
    0,
    255,
    0,
    255
  ]
}
```

SourceForge package with bundled image codecs. Project adoption metric is unavailable from the uniform GitHub primary-repository star source; left unranked.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
