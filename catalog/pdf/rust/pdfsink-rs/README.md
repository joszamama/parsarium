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

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/rust/pdfsink_rs/README.md)

```sh
python3 parsarium.py build pdf rust pdfsink_rs
python3 parsarium.py run pdf rust pdfsink_rs controls/pdf/one-page.pdf
```
