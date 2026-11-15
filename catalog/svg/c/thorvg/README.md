# thorvg — SVG / C

- **Pinned release:** `1.1.3`
- **License:** MIT
- **Parsed scope:** parsed SVG document dimensions
- **Underlying family:** ThorVG SVG loader and native vector engine
- **Local input API:** `tvg_engine_init; tvg_picture_new; tvg_picture_load(local filename); tvg_picture_get_size`
- **Documentation:** [API reference](<https://github.com/thorvg/thorvg/blob/v1.1.3/README.md>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

ThorVG C binding and native C++ API are distinct ecosystem call paths over the same ThorVG SVG loader; they do not represent independent syntax engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
