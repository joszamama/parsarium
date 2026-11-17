# github.com/gographics/gmagick — ASCII PNM / Go

- **Pinned release:** `v1.0.0`
- **License:** BSD-3-Clause
- **Parsed scope:** P3 dimensions, format and color count
- **Underlying family:** GraphicsMagick
- **Local input API:** `NewMagickWand().ReadImageBlob([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gographics/gmagick@v1.0.0>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_pnm/parsers.json) · [control verification](../../../../data/go/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "format": "PPM",
  "colors": 2
}
```

Native GraphicsMagick 1.3.49 coders/pnm.c reader reached through the gmagick cgo MagickWand binding (built static from the pinned release tarball in the project image). GraphicsMagick forked from ImageMagick 5.5.2 in 2002, so it shares distant ancestry with the selected imagick.v3 path (ImageMagick 7); the two PNM coders have been maintained separately since.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_gographics_gmagick/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_gographics_gmagick
python3 parsarium.py run ascii_pnm go github_com_gographics_gmagick controls/ascii_pnm/red-green.ppm
```

**Coverage limit:** Only two valid ASCII controls (P3 PPM and P2 PGM, 2x1, maxval 255); GraphicsMagick 1.3.49 is built static from the pinned release tarball with delegates, modules and OpenMP disabled. No malformed input, fuzzing campaign, binary P4-P6 or PAM validation.
