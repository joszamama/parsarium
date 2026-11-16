# imlib2 — SVG / C

- **Pinned release:** `1.12.7`
- **License:** Imlib2
- **Parsed scope:** SVG dimensions and red/green pixels through source-built Imlib2 SVG loader
- **Underlying family:** Imlib2 SVG loader over librsvg
- **Local input API:** `imlib_load_image_with_errno_return(local SVG filename, &error); imlib_image_get_width/height and imlib_image_get_data_for_reading_only`
- **Documentation:** [API reference](<https://git.enlightenment.org/old/legacy-imlib2/src/branch/master/src/lib/Imlib2.h>)
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

The official Imlib2 1.12.7 source contains an optional SVG plugin that delegates to librsvg. The installed Homebrew Imlib2 package lacks this plugin; the verifier enables and builds it from the pinned source. This is a distinct Imlib2 file-input API but shares the separately recorded librsvg syntax engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/imlib2/README.md)

```sh
python3 parsarium.py build svg c imlib2
python3 parsarium.py run svg c imlib2 controls/svg/red-green.svg
```
