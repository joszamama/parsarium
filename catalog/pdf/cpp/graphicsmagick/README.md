# graphicsmagick — PDF / C++

- **Pinned release:** `1.3.49`
- **License:** MIT
- **Parsed scope:** Rendered PDF page sequence and first page dimensions
- **Underlying family:** GraphicsMagick PDF coder + Ghostscript PDF interpreter
- **Local input API:** `Magick::readImages(vector<Magick::Image>*, local filename); vector size and first Image::columns()/rows()`
- **Documentation:** [API reference](<https://graphicsmagick.sourceforge.io/>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
