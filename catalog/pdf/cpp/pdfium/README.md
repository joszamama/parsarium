# pdfium — PDF / C++

- **Pinned release:** `159.0.8152.0`
- **License:** BSD-3-Clause
- **Parsed scope:** PDF document page count and first page object
- **Underlying family:** PDFium PDF parser
- **Local input API:** `FPDF_LoadDocument(const char* local filename, nullptr); FPDF_GetPageCount and FPDF_LoadPage, called from C++17`
- **Documentation:** [API reference](<https://pdfium.googlesource.com/pdfium/+/6688c576fd851f4159c6fae39396da50939de110/docs/getting-started.md>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Direct PDFium C API call from C++17. Prebuilt macOS arm64 artifact from bblanchon/pdfium-binaries chromium/8152 release is SHA-256 pinned; its original API header matches an independently pinned canonical PDFium source revision. Distribution is third-party; core engine is canonical PDFium. Binary provenance is limited to the distributor release claim and original header match.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
