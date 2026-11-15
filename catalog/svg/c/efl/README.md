# efl — SVG / C

- **Pinned release:** `1.29.0`
- **License:** GPL-2.0-only AND LGPL-2.1-only AND BSD-2-Clause AND FTL AND zlib-acknowledgement
- **Parsed scope:** SVG dimensions and red/green pixels through Evas rsvg image loader
- **Underlying family:** EFL Evas image API over its rsvg loader and librsvg
- **Local input API:** `evas_object_image_file_set(Evas_Object*, local SVG filename, NULL); evas_object_image_size_get; evas_object_image_data_get`
- **Documentation:** [API reference](<https://download.enlightenment.org/rel/libs/efl/efl-1.29.0.tar.xz (src/lib/evas/Evas_Legacy.h)>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

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

The pinned Evas rsvg loader executable invokes librsvg. EFL is a distinct released C image API, but shares the separately recorded librsvg SVG syntax engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
