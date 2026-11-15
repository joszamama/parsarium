# imlib2 — ASCII PNM / C++

- **Pinned release:** `1.12.7`
- **License:** Imlib2
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels
- **Underlying family:** Imlib2 PNM loader
- **Local input API:** `imlib_load_image_immediately(const char* file); imlib_image_get_data_for_reading_only()`
- **Documentation:** [API reference](<https://sourceforge.net/projects/enlightenment/files/imlib2-src/1.12.7/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
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

Imlib2 loader parsed P3; its primary upstream is not GitHub, so a comparable primary repository star count is unavailable.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
