# rustpdf — PDF / C

- **Pinned release:** `0.5.0`
- **License:** MIT
- **Parsed scope:** parsed two-page PDF page count from local bytes
- **Underlying family:** rustpdf Rust PDF parser via C ABI
- **Local input API:** `pdf_page_count(const uint8_t *local bytes, uintptr_t len, uintptr_t *out_count); pdf_last_error_message()`
- **Documentation:** [API reference](<https://github.com/rustpdf/rustpdf/blob/swift-v0.5.0/include/pdf.h>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/two-page.pdf`](../../../../controls/pdf/two-page.pdf)

## Observed control result

```json
{
  "pages": 2
}
```

MIT pdf-ffi 0.5.0 source-built cdylib exposes documented C byte input. Its pdf_page_count implementation calls pdf::render_page_count, which calls parser::PdfReader::parse. No other C PDF cell path uses this underlying Rust parser. The release tag is swift-v0.5.0 but the same tagged workspace includes the C ABI crate at version 0.5.0.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
