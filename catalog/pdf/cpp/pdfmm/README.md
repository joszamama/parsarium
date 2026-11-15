# pdfmm — PDF / C++

- **Pinned release:** `0.10.0`
- **License:** LGPL-2.1-only
- **Parsed scope:** PDF document page count
- **Underlying family:** pdfmm, fork of PoDoFo
- **Local input API:** `mm::PdfMemDocument::Load(std::string_view local filename); GetPages().GetCount()`
- **Documentation:** [API reference](<https://github.com/pdfmm/pdfmm/blob/v0.10.0/src/pdfmm/base/PdfMemDocument.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Pdfmm 0.10.0 is a distinct C++17 library forked from PoDoFo and later moved back to the PoDoFo community. Its parser lineage is shared with PoDoFo, and its separate pinned source release is built as a shared library with direct dependency hashes recorded.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
