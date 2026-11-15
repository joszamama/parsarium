# devil — PNG / C

- **Pinned release:** `1.8.0`
- **License:** LGPL-2.1-only
- **Parsed scope:** pixels
- **Underlying family:** DevIL PNG loader (libpng-backed)
- **Local input API:** `ilLoadImage(const ILstring path); ilGetInteger(IL_IMAGE_WIDTH/HEIGHT); ilGetData()`
- **Documentation:** [API reference](<https://openil.sourceforge.net/docs/DevIL%20Reference%20Guide.pdf>)
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

Recorded libIL links libpng; primary SourceForge project has no comparable GitHub repository star metric.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
