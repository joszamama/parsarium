# imagemagick — PDF / C++

- **Pinned release:** `7.1.2-35`
- **Upstream:** [source repository](<https://github.com/ImageMagick/ImageMagick>) · [Debian](<https://tracker.debian.org/pkg/imagemagick>)
- **License:** ImageMagick
- **Parsed scope:** Rendered PDF page sequence and first page dimensions
- **Underlying family:** ImageMagick PDF coder + Ghostscript PDF interpreter
- **Local input API:** `Magick::readImages(vector<Magick::Image>*, local filename); vector size and first Image::columns()/rows()`
- **Documentation:** [API reference](<https://imagemagick.org/magick++/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
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

[Docker harness and verification receipt](../../../../projects/pdf/cpp/imagemagick/README.md)

```sh
python3 parsarium.py build pdf cpp imagemagick
python3 parsarium.py run pdf cpp imagemagick controls/pdf/one-page.pdf
```
