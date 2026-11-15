# oxidize-pdf — PDF / Rust

- **Pinned release:** `5.5.7`
- **License:** MIT
- **Parsed scope:** PDF page tree
- **Underlying family:** oxidize-pdf parser
- **Local input API:** `PdfDocument::open(path).page_count()`
- **Documentation:** [API reference](<https://docs.rs/oxidize-pdf/5.5.7/oxidize_pdf/>)
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
