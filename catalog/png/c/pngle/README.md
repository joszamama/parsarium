# pngle — PNG / C

- **Pinned release:** `1.1.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** pngle with bundled miniz
- **Local input API:** `pngle_feed(pngle_t*, const void*, size_t) with draw callback and pngle_get_width/height`
- **Documentation:** [API reference](<https://github.com/kikuchan/pngle/blob/v1.1.0/src/pngle.h>)
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

Independent PNG parser with a bundled miniz DEFLATE implementation.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/c/pngle/README.md)

```sh
python3 parsarium.py build png c pngle
python3 parsarium.py run png c pngle controls/png/red-green.png
```
