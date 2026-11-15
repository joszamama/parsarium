# zpdf-document — PDF / Rust

- **Pinned release:** `0.18.0`
- **License:** MIT
- **Parsed scope:** PDF page tree
- **Underlying family:** zpdf
- **Local input API:** `PdfDocument::open(bytes).page_count()`
- **Documentation:** [API reference](<https://docs.rs/zpdf-document/0.18.0/zpdf_document/>)
- **Catalog evidence:** [parser record](../../../../data/rust/pdf/parsers.json) · [control verification](../../../../data/rust/pdf/verification.json) · [within-ecosystem ranking](../../../../data/rust/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
