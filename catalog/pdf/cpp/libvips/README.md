# libvips — PDF / C++

- **Pinned release:** `8.18.7`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** PDF page count and first page dimensions from PDF loader header
- **Underlying family:** libvips vips-poppler module over Poppler PDF parser
- **Local input API:** `vips::VImage::pdfload(local filename); get_int("n-pages"); width()/height()`
- **Documentation:** [API reference](<https://www.libvips.org/API/current/ctor.Image.pdfload.html>)
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

The installed vips-poppler module links Poppler GLib 26.11.0; C and C++ libvips APIs share the same package and Poppler syntax engine. The adapter reads format-aware PDF metadata; libvips renders pixels lazily.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
