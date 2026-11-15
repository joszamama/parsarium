# pdfsink-rs — PDF / Rust

- **Pinned release:** `0.2.20`
- **License:** MIT
- **Parsed scope:** PDF page model
- **Underlying family:** lopdf
- **Local input API:** `PdfDocument::open(path).len()`
- **Documentation:** [API reference](<https://docs.rs/pdfsink-rs/0.2.20/pdfsink_rs/>)
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
