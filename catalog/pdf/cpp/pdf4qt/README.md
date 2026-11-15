# pdf4qt — PDF / C++

- **Pinned release:** `1.6.0.0`
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
