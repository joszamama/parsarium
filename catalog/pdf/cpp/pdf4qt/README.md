# pdf4qt — PDF / C++

- **Pinned release:** `1.6.0.0`
- **Upstream:** [source repository](<https://github.com/JakubMelka/PDF4QT>)
- **License:** MIT
- **Parsed scope:** PDF document page count
- **Underlying family:** PDF4QT PDF engine
- **Local input API:** `pdf::PDFDocumentReader::readFromFile(const QString& local filename); getReadingResult(); PDFDocument::getCatalog()->getPageCount()`
- **Documentation:** [API reference](<https://github.com/JakubMelka/PDF4QT/blob/v1.6.0.0/Pdf4QtLibCore/sources/pdfdocumentreader.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Native PDF4QT C++ document reader built from pinned v1.6.0.0 source. Its pinned Blend2D dependency uses NO_JIT. A recorded patch enables core-only building with Qt 6.12 on macOS and replaces parallel-policy calls with sequential algorithms for Apple libc++; the adapter uses C++20.

The pinned Docker build applies the SHA-recorded project-local core-library compatibility patch before compilation. It guards an editor-only translation target, uses sequential STL calls in two core headers, and links Fontconfig. The pinned PDF reader and parser source files are unchanged.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/cpp/pdf4qt/README.md)

```sh
python3 parsarium.py build pdf cpp pdf4qt
python3 parsarium.py run pdf cpp pdf4qt controls/pdf/one-page.pdf
```
