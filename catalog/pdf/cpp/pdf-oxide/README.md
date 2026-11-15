# pdf_oxide — PDF / C++

- **Pinned release:** `0.3.78`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** parsed PDF page count
- **Underlying family:** pdf_oxide Rust PDF parser via C ABI
- **Local input API:** `pdf_oxide::Document::open(local file path); page_count()`
- **Documentation:** [API reference](<https://github.com/yfedoseev/pdf_oxide/blob/v0.3.78/cpp/include/pdf_oxide/pdf_oxide.hpp>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

The native C++17 RAII header wraps the same C ABI and Rust engine as the C adapter. C and C++ are separate ecosystem package paths, but not independent PDF parser engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
