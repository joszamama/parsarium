# imtoolkit — ASCII PNM / C

- **Pinned release:** `3.15`
- **License:** MIT
- **Parsed scope:** P3 dimensions and two decoded RGB pixels
- **Underlying family:** IM Toolkit PNM driver
- **Local input API:** `imFileImageLoad(local path,0,&error); inspect imImage channel planes`
- **Documentation:** [API reference](<https://www.tecgraf.puc-rio.br/im/en/storage_guide.html>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_pnm/parsers.json) · [control verification](../../../../data/c/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

The public C API calls an IM Toolkit library implemented in C++; its own PNM driver handles ASCII P3. Build uses pinned source archive and pinned libpng dylib.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
