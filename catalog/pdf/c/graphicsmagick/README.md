# graphicsmagick — PDF / C

- **Pinned release:** `1.3.49`
- **Upstream:** [source repository](<https://sourceforge.net/projects/graphicsmagick/>) · [Debian](<https://tracker.debian.org/pkg/graphicsmagick>)
- **License:** MIT
- **Parsed scope:** Rendered PDF page sequence and first page dimensions
- **Underlying family:** GraphicsMagick PDF coder + Ghostscript PDF interpreter
- **Local input API:** `MagickReadImage(local filename); MagickGetNumberImages(); MagickGetImageWidth()/MagickGetImageHeight()`
- **Documentation:** [API reference](<https://graphicsmagick.sourceforge.io/wand/magick_wand.html>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "width": 612,
  "height": 792
}
```

Distinct Magick package API; Ghostscript 10.08.0 performs underlying PDF interpretation in the recorded installation. The C and C++ APIs of this package share its core; its PDF syntax engine is shared with the separately counted Ghostscript path.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/c/graphicsmagick/README.md)

```sh
python3 parsarium.py build pdf c graphicsmagick
python3 parsarium.py run pdf c graphicsmagick controls/pdf/one-page.pdf
```
