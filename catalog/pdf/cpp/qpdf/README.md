# qpdf — PDF / C++

- **Pinned release:** `12.4.2`
- **License:** Apache-2.0
- **Parsed scope:** PDF document page count
- **Underlying family:** qpdf C++ PDF parser
- **Local input API:** `QPDF::processFile(const char* local filename); QPDFPageDocumentHelper::getAllPages()`
- **Documentation:** [API reference](<https://github.com/qpdf/qpdf/blob/v12.4.2/examples/pdf-parse-content.cc>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Native qpdf C++ parser; distinct from Poppler and PoDoFo.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
