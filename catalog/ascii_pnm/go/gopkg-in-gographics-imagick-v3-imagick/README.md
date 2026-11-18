# gopkg.in/gographics/imagick.v3/imagick — ASCII PNM / Go

- **Pinned release:** `v3.7.3`
- **Upstream:** [source repository](<https://github.com/gographics/imagick>) · [pkg.go.dev](<https://pkg.go.dev/gopkg.in/gographics/imagick.v3/imagick>)
- **License:** BSD-3-Clause
- **Parsed scope:** P3 dimensions
- **Underlying family:** ImageMagick
- **Local input API:** `MagickWand.ReadImageBlob([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/gopkg.in/gographics/imagick.v3/imagick@v3.7.3>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_pnm/parsers.json) · [control verification](../../../../data/go/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "height": 1,
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/gopkg_in_gographics_imagick_v3_imagick/README.md)

```sh
python3 parsarium.py build ascii_pnm go gopkg_in_gographics_imagick_v3_imagick
python3 parsarium.py run ascii_pnm go gopkg_in_gographics_imagick_v3_imagick controls/ascii_pnm/red-green.ppm
```
