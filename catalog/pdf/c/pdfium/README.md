# pdfium — PDF / C

- **Pinned release:** `159.0.8152.0`
- **License:** BSD-3-Clause
- **Parsed scope:** PDF document page count and first page object
- **Underlying family:** PDFium PDF parser
- **Local input API:** `FPDF_LoadDocument(local filename, NULL); FPDF_GetPageCount() and FPDF_LoadPage()`
- **Documentation:** [API reference](<https://pdfium.googlesource.com/pdfium/+/6688c576fd851f4159c6fae39396da50939de110/docs/getting-started.md>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Direct C API. SHA-256-pinned distributor binary release and original header matched to canonical source revision; binary provenance remains limited to distributor release claim and header match. Same release and engine as C++ PDF cell.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
