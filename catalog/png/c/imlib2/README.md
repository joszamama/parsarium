# imlib2 — PNG / C

- **Pinned release:** `1.12.7`
- **License:** Imlib2
- **Parsed scope:** pixels
- **Underlying family:** Imlib2 PNG loader (libpng-backed)
- **Local input API:** `imlib_load_image_immediately(const char* file); imlib_image_get_data_for_reading_only()`
- **Documentation:** [API reference](<https://sourceforge.net/projects/enlightenment/files/imlib2-src/1.12.7/>)
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

The pinned source release includes the documented Imlib2.h.in C API and a PNG loader module. Primary Enlightenment repository is not GitHub.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
