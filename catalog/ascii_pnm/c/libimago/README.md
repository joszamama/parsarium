# libimago — ASCII PNM / C

- **Pinned release:** `2.4.2`
- **License:** LGPL-3.0-or-later
- **Parsed scope:** P3 dimensions and two decoded RGB pixels
- **Underlying family:** libimago PPM reader
- **Local input API:** `img_load_pixels(local path,&width,&height,IMG_FMT_RGBA32)`
- **Documentation:** [API reference](<https://github.com/jtsiomb/libimago/blob/v2.4.2/README.md>)
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

libimago has its own PPM reader; optional PNG and JPEG dependencies are disabled in this build.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
