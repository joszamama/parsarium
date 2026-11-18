# resvg — SVG / C

- **Pinned release:** `0.50.0`
- **Upstream:** [source repository](<https://github.com/linebender/resvg>) · [Debian](<https://tracker.debian.org/pkg/resvg>)
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** resvg/usvg Rust SVG parser and tiny-skia renderer through C API
- **Local input API:** `resvg_parse_tree_from_file(local filename, options, &tree); resvg_get_image_size; resvg_render to RGBA pixmap`
- **Documentation:** [API reference](<https://github.com/linebender/resvg/blob/v0.50.0/crates/c-api/resvg.h>)
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

The C and C++ adapters use the same tagged resvg-capi source library. This is a distinct engine from librsvg, ImageMagick MSVG, and GraphicsMagick SVG-to-MVG; the two ecosystem paths are not independent from one another.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/resvg/README.md)

```sh
python3 parsarium.py build svg c resvg
python3 parsarium.py run svg c resvg controls/svg/red-green.svg
```

**Coverage limit:** The AFL++ target uses one-shot /work/replay @@ because the selected C API parses a local file; parser-source feedback comes from usvg Rust code.
