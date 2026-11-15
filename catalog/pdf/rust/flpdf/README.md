# flpdf — PDF / Rust

- **Pinned release:** `0.10.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** PDF page tree
- **Underlying family:** flpdf qpdf-style parser
- **Local input API:** `Pdf::open(File); PageDocumentHelper::get_all_pages()`
- **Documentation:** [API reference](<https://docs.rs/flpdf/0.10.0/flpdf/>)
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
