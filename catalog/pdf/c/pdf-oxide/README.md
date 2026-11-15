# pdf_oxide — PDF / C

- **Pinned release:** `0.3.78`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** parsed PDF page count
- **Underlying family:** pdf_oxide Rust PDF parser via C ABI
- **Local input API:** `pdf_document_open(local file path, &error); pdf_document_get_page_count(handle, &error)`
- **Documentation:** [API reference](<https://github.com/yfedoseev/pdf_oxide/blob/v0.3.78/include/pdf_oxide_c/pdf_oxide.h>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

The C ABI calls the Rust pdf_oxide engine. The C++ adapter uses the same source release and engine through its RAII header; paths in different ecosystems are not independent syntax engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
