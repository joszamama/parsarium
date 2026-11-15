# sail — ASCII PNM / C

- **Pinned release:** `1.3.1`
- **License:** MIT
- **Parsed scope:** P3 dimensions and two decoded RGB pixels
- **Underlying family:** SAIL native PNM codec
- **Local input API:** `sail_load_from_file(local path,&image)`
- **Documentation:** [API reference](<https://github.com/HappySeaFox/sail/blob/v1.3.1/src/sail/sail_junior.h>)
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

Built with only its native PNM codec and no external image codec.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
