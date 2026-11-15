# pdf-syntax — PDF / Rust

- **Pinned release:** `0.6.2`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** PDF page tree
- **Underlying family:** hayro-syntax-derived parser
- **Local input API:** `Pdf::new(Arc::new(bytes)).pages()`
- **Documentation:** [API reference](<https://docs.rs/pdf-syntax/0.6.2/pdf_syntax/>)
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
