# qtpdf — PDF / C++

- **Pinned release:** `6.11.2`
- **License:** LGPL-3.0-only OR GPL-2.0-only
- **Parsed scope:** PDF document page count
- **Underlying family:** PDFium engine via Qt PDF
- **Local input API:** `QPdfDocument::load(const QString& local filename); error(); pageCount()`
- **Documentation:** [API reference](<https://doc.qt.io/qt-6/qpdfdocument.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Qt PDF module from the separate QtWebEngine distribution exposes the QPdfDocument C++17 API and bundles PDFium internally. It shares the PDFium engine with the direct PDFium path but is a distinct third-party package/API. The installed 6.11.2_1 framework and official v6.11.2 header are hash checked; Qt6Pdf.pc reports 6.12.0 despite the Homebrew formula version, so both values are recorded.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
