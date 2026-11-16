# pngle — PNG / C++

- **Pinned release:** `1.1.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** pngle with bundled miniz
- **Local input API:** `pngle_feed(pngle_t*, const void*, size_t) with draw callback and pngle_get_width/height`
- **Documentation:** [API reference](<https://github.com/kikuchan/pngle/blob/v1.1.0/src/pngle.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/png/parsers.json) · [control verification](../../../../data/cpp/png/verification.json) · [within-ecosystem ranking](../../../../data/cpp/png/ranking.md)
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

Independent PNG parser with a bundled miniz DEFLATE implementation. Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/cpp/pngle/README.md)

```sh
python3 parsarium.py build png cpp pngle
python3 parsarium.py run png cpp pngle controls/png/red-green.png
```
