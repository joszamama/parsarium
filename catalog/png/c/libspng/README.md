# libspng — PNG / C

- **Pinned release:** `0.7.4`
- **License:** BSD-2-Clause
- **Parsed scope:** pixels
- **Underlying family:** libspng
- **Local input API:** `spng_set_png_file(spng_ctx*, FILE*); spng_get_ihdr(...); spng_decode_image(...) to RGBA8`
- **Documentation:** [API reference](<https://github.com/randy408/libspng/blob/v0.7.4/spng/spng.h>)
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

Independent PNG parser using zlib for DEFLATE.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
