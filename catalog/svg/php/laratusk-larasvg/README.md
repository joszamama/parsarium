# laratusk/larasvg — SVG / PHP

- **Pinned release:** `v2.5.1`
- **License:** MIT
- **Parsed scope:** Public converter class with isolated Illuminate Process facade factory; librsvg 2.63.4 renders the SVG.
- **Underlying family:** GNOME librsvg SVG renderer via rsvg-convert
- **Local input API:** `RsvgConvertConverter(local path, local binary)->toStdout('png') via public Laravel process facade`
- **Documentation:** [API reference](<https://github.com/laratusk/larasvg/blob/e37b0dd3dbc0035c5f66fb899fad242da7e10ced/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "left_rgb": [
    255,
    0,
    0
  ],
  "right_rgb": [
    0,
    255,
    0
  ]
}
```

Laravel wrapper shares the exact underlying rsvg-convert engine with atelier/rasterizer.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/php/laratusk_larasvg/README.md)

```sh
python3 parsarium.py build svg php laratusk_larasvg
python3 parsarium.py run svg php laratusk_larasvg controls/svg/red-green.svg
```
