# gopkg.in/gographics/imagick.v3/imagick — PNG / Go

- **Pinned release:** `v3.7.3`
- **Upstream:** [source repository](<https://github.com/gographics/imagick>) · [pkg.go.dev](<https://pkg.go.dev/gopkg.in/gographics/imagick.v3/imagick>)
- **License:** BSD-3-Clause
- **Parsed scope:** dimensions
- **Underlying family:** ImageMagick MagickWand
- **Local input API:** `MagickWand.ReadImageBlob([]byte); GetImageWidth(); GetImageHeight()`
- **Documentation:** [API reference](<https://pkg.go.dev/gopkg.in/gographics/imagick.v3/imagick@v3.7.3>)
- **Catalog evidence:** [parser record](../../../../data/go/png/parsers.json) · [control verification](../../../../data/go/png/verification.json) · [within-ecosystem ranking](../../../../data/go/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "height": 1,
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/go/gopkg_in_gographics_imagick_v3_imagick/README.md)

```sh
python3 parsarium.py build png go gopkg_in_gographics_imagick_v3_imagick
python3 parsarium.py run png go gopkg_in_gographics_imagick_v3_imagick controls/png/red-green.png
```
